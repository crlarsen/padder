import sys
from datetime import datetime

dt = datetime.today().strftime("%m/%d/%Y %I:%M:%S %p")

# TODO: Add support for bit counts which are a power of 2?
# TODO: Add command line flag to generate overflow bit.

def bitcnt(x):
  i = x
  count = 1 if i != 0 else 0
  while i & (i-1):
    count = count + 1
    i = i & (i-1)
  return count

if len(sys.argv) == 1:
  print("ERROR: No argument given\nUsage: %s <power of 2>" % (sys.argv[0]))
  sys.exit(1)
elif len(sys.argv) == 2:
  count = int(sys.argv[1])
  if bitcnt(count) != 1:
    print("ERROR: Argument must be a power of 2: %d" % (count))
    sys.exit(1)
else:
  print("ERROR: must give only one argument")
  sys.exit(1)

#Header info
print(
'''
`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Copyright: Chris Larsen, 2021
// Engineer: Chris Larsen
//
// Create Date: %s
// Design Name:
// Module Name: padder%d
// Project Name:
// Target Devices:
// Tool Versions:
// Description: %d-bit Integer Prefix Adder with Carry In/Carry Out
//
//       This adder was generated by a Python script written by Chris Larsen.
//       The adders generated by the Python script are all prefix adders.
//       Since this code was machine generated, in general you shouldn't be
//       editing this code by hand.
//
//       If bugs in the script are found I (Chris Larsen) would ask that you
//       send your bug fixes, and or other improvements, back so I can include
//       them in the git repository for the padder.py script.
//
//       Prefix adders are described in the book "Digital Design and Computer
//       Architecture, Second Edition" by David Money Harris & Sarah L. Harris.
//       To write this code I started by studying their diagram of a 16-bit
//       prefix adder, and extrapolated it to 32-bits, etc. I'm not an expert
//       in prefix adders. So if you have questions, please don't ask me;
//       please buy their fine book! :-)
//
// Dependencies: None
//
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
//
//////////////////////////////////////////////////////////////////////////////////

// This module exists to keep the Verilog compiler from complaining about
// outputs not being connected to inputs. Otherwise, I would have just used
// the module PijGij everywhere and been done with it. Also, it does use a few
// less gates than the PijGij module but I suspect a good Verilog compiler
// would make such optimizations for unused outputs automatically.
module Gij(\Pi:k , \Gi:k , \Gk-1:j , \Gi:j );
  input \Pi:k , \Gi:k , \Gk-1:j ;
  output \Gi:j ;

  assign \Gi:j = \Gi:k | (\Pi:k  & \Gk-1:j );
endmodule

module PijGij(\Pi:k , \Pk-1:j , \Gi:k , \Gk-1:j , \Pi:j , \Gi:j );
  input \Pi:k , \Pk-1:j , \Gi:k , \Gk-1:j ;
  output \Pi:j , \Gi:j ;

  assign \Pi:j = \Pi:k & \Pk-1:j ;
  assign \Gi:j = \Gi:k | (\Pi:k  & \Gk-1:j );
endmodule

module Sum(\Gi-1:-1 , Ai, Bi, Si);
  input \Gi-1:-1 , Ai, Bi;
  output Si;

  assign Si = \Gi-1:-1 ^ Ai ^ Bi;
endmodule

module padder%d(A, B, Cin, S, Cout);
  parameter N = %d;
  input [N-1:0] A, B;
  input Cin;
  output [N-1:0] S;
  output Cout;

  // P[i] is an alias for Pi:i, likewise G[i] is an alias for Gi:i
  wire [N-2:-1] P, G;
'''[1:] % (dt, count, count, count, count))

if count == 1:
  print(
'''
  assign P[-1] = 1'b0;
  assign G[-1] = Cin;
'''[1:])
else:
  print(
'''
  assign P = {A[N-2:0] | B[N-2:0], 1'b0};
  assign G = {A[N-2:0] & B[N-2:0], Cin};
'''[1:])
#Header info

# Compute the next node in the net.
def node(i, j, l, r):
  if i == j:
    p1Input = "P[%d]" % (i)
    g1Input = "G[%d]" % (i)
  else:
    p1Input = "\\P%d:%d " % (i, j)
    g1Input = "\\G%d:%d " % (i, j)

  if (l == r):
    p2Input = "P[%d]" % (l)
    g2Input = "G[%d]" % (l)
  else:
    p2Input = "\\P%d:%d " % (l, r)
    g2Input = "\\G%d:%d " % (l, r)

  pOutput = "\\P%d:%d " % (i, r)
  gOutput = "\\G%d:%d " % (i, r)

  if r == -1:
    # We don't need to compute \Pi:-1 because it will never be used.
    # This keeps the Verilog compiler from complaining that we have
    # outputs not connected to inputs.
    print("  wire %s;\n" % (gOutput))
    print("  Gij \\%d:%d (%s, %s, %s, %s);\n" % (i, r, p1Input, g1Input, g2Input, gOutput))
  else:
    print("  wire %s, %s;\n" % (pOutput, gOutput))
    print("  PijGij \\%d:%d (%s, %s, %s, %s, %s, %s);\n" % (i, r, p1Input, p2Input, g1Input, g2Input, pOutput, gOutput))

masks = []

for i in range(-1, count-1):
  masks.append([i, i]) # Push new node onto stack.

  # Merge and print top 2 stack items as long as the last N bits of i
  # are equal to 2**N - 2.
  m, v = 1, 0 # Start with N = 1
  while (i & m) == v:
    [i, j] = masks.pop()
    [l, r] = masks[-1]
    node(i, j, l, r)
    masks[-1][0] = i # Merge the 2 top nodes.
    m, v = ((m << 1) | 1), ((v << 1) | 2) # N = N + 1

  # Perform the rest of the work needed to compute Gi:-1
  [i, j] = masks[-1]
  for k in range(len(masks)-2, -1, -1):
    [l, r] = masks[k]
    node(i, j, l, r)
    j = r

  # Use Gi:-1 to propagate carry to compute bit i+1 of the sum.
  if i == -1:
    print("  Sum s%d(G[%d], A[%d], B[%d], S[%d]);\n" % (i+1, i, i+1, i+1, i+1));
  else:
    print("  Sum s%d(\\G%d:-1 , A[%d], B[%d], S[%d]);\n" % (i+1, i, i+1, i+1, i+1));

# Compute Cout and end the module.
if count == 1:
  print("  assign Cout = (G[%d] & A[%d]) | (\\G%d:-1 & B[%d]) | (A[%d] & B[%d]);\n" % (count-2, count-1, count-2, count-1, count-1, count-1))
else:
  print("  assign Cout = (\\G%d:-1 & A[%d]) | (\\G%d:-1 & B[%d]) | (A[%d] & B[%d]);\n" % (count-2, count-1, count-2, count-1, count-1, count-1))
print("endmodule");
