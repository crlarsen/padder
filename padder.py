import sys

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
// Company:
// Engineer:
//
// Create Date: 06/05/2019 07:36:52 PM
// Design Name:
// Module Name: padder%d
// Project Name:
// Target Devices:
// Tool Versions:
// Description: Integer Prefix Adder with Carry In/Carry Out
//
// Dependencies:
//
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
//
//////////////////////////////////////////////////////////////////////////////////

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

  wire [N-2:0] P, G;

  assign P = A[N-2:0] | B[N-2:0];
  assign G = A[N-2:0] & B[N-2:0];

  wire \G-1:-1 , \P-1:-1 ;

  assign \G-1:-1 = Cin;
  assign \P-1:-1 = 1'b0;

  Sum s0(\G-1:-1 , A[0], B[0], S[0]); // Last line
''' % (count, count, count))
#Header info

def node(i, j, l, r):
  if i == j:
    p1Input = "P[%d]" % (i)
    g1Input = "G[%d]" % (i)
  else:
    p1Input = "\\P%d:%d " % (i, j)
    g1Input = "\\G%d:%d " % (i, j)

  if (l == r) and (l != -1):
    p2Input = "P[%d]" % (l)
    g2Input = "G[%d]" % (l)
  else:
    p2Input = "\\P%d:%d " % (l, r)
    g2Input = "\\G%d:%d " % (l, r)

  pOutput = "\\P%d:%d " % (i, r)
  gOutput = "\\G%d:%d " % (i, r)

  if r == -1:
    print("  wire %s;\n" % (gOutput))
    print("  Gij \\%d:%d (%s, %s, %s, %s);\n" % (i, r, p1Input, g1Input, g2Input, gOutput))
  else:
    print("  wire %s, %s;\n" % (pOutput, gOutput))
    print("  PijGij \\%d:%d (%s, %s, %s, %s, %s, %s);\n" % (i, r, p1Input, p2Input, g1Input, g2Input, pOutput, gOutput))


masks = []

for i in range(count-1):
  if (i & 1) == 0:
    j = i - 1
    node(i, i, j, j)
    masks.append([i, j])

    m, v = 3, 2
    while (i & m) == v:
      [i, j] = masks.pop()
      [l, r] = masks.pop()
      node(i, j, l, r)
      masks.append([i, r])
      m, v = ((m << 1) | 1), ((v << 1) | 2)

    top = len(masks) - 1
    [i, j] = masks[top]
    while j != -1:
      top = top - 1
      [l, r] = masks[top]
      node(i, j, l, r)
      j = r
  else:
    j = i
    for k in range(len(masks)-1, -1, -1):
      [l, r] = masks[k]
      node(i, j, l, r)
      j = r

  print("  Sum s%d(\\G%d:-1 , A[%d], B[%d], S[%d]);\n" % (i+1, i, i+1, i+1, i+1));

print("  assign Cout = (\\G%d:-1 & A[%d]) | (\\G%d:-1 & B[%d]) | (A[%d] & B[%d]);\n" % (count-2, count-1, count-2, count-1, count-1, count-1))
print("endmodule");
