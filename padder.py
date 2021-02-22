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

masks = []

for i in range(count-1):
  if i == 0:
    print("  wire \\G%d:-1 ;\n" % (i))
    print("  Gij \\%d:%d (P[%d], G[%d], \\G-1:-1 , \\G%d:-1 );\n" % (i, i-1, i, i, i))
    masks.append([0, -1])
  elif (i & 1) == 0:
    j = i - 1
    print("  wire \\P%d:%d , \\G%d:%d ;\n" % (i, j, i, j))
    print("  PijGij \\%d:%d (P[%d], P[%d], G[%d], G[%d], \\P%d:%d , \\G%d:%d );\n" % (i, j, i, j, i, j, i, j, i, j))
    masks.append([i, j])
    r = j
    if (i & 3) == 2:
      [i, j] = masks.pop()
      [l, r] = masks.pop()
      if r == -1:
        print("  wire \\G%d:%d ;\n" % (i, r))
        print("  Gij \\%d:%d (\\P%d:%d , \\G%d:%d , \\G%d:%d , \\G%d:%d );\n" % (i, r, i, j, i, j, l, r, i, r))
      else:
        print("  wire \\P%d:%d , \\G%d:%d ;\n" % (i, r, i, r))
        print("  PijGij \\%d:%d (\\P%d:%d , \\P%d:%d , \\G%d:%d , \\G%d:%d , \\P%d:%d , \\G%d:%d );\n" % (i, r, i, j, l, r, i, j, l, r, i, r, i, r))
      masks.append([i, r])
      if (i & 7) == 6:
        [i, j] = masks.pop()
        [l, r] = masks.pop()
        if r == -1:
          print("  wire \\G%d:%d ;\n" % (i, r))
          print("  Gij \\%d:%d (\\P%d:%d , \\G%d:%d , \\G%d:%d , \\G%d:%d );\n" % (i, r, i, j, i, j, l, r, i, r))
        else:
          print("  wire \\P%d:%d , \\G%d:%d ;\n" % (i, r, i, r))
          print("  PijGij \\%d:%d (\\P%d:%d , \\P%d:%d , \\G%d:%d , \\G%d:%d , \\P%d:%d , \\G%d:%d );\n" % (i, r, i, j, l, r, i, j, l, r, i, r, i, r))
        masks.append([i, r])
        if (i & 15) == 14:
          [i, j] = masks.pop()
          [l, r] = masks.pop()
          if r == -1:
            print("  wire \\G%d:%d ;\n" % (i, r))
            print("  Gij \\%d:%d (\\P%d:%d , \\G%d:%d , \\G%d:%d , \\G%d:%d );\n" % (i, r, i, j, i, j, l, r, i, r))
          else:
            print("  wire \\P%d:%d , \\G%d:%d ;\n" % (i, r, i, r))
            print("  PijGij \\%d:%d (\\P%d:%d , \\P%d:%d , \\G%d:%d , \\G%d:%d , \\P%d:%d , \\G%d:%d );\n" % (i, r, i, j, l, r, i, j, l, r, i, r, i, r))
          masks.append([i, r])
          if (i & 31) == 30:
            [i, j] = masks.pop()
            [l, r] = masks.pop()
            if r == -1:
              print("  wire \\G%d:%d ;\n" % (i, r))
              print("  Gij \\%d:%d (\\P%d:%d , \\G%d:%d , \\G%d:%d , \\G%d:%d );\n" % (i, r, i, j, i, j, l, r, i, r))
            else:
              print("  wire \\P%d:%d , \\G%d:%d ;\n" % (i, r, i, r))
              print("  PijGij \\%d:%d (\\P%d:%d , \\P%d:%d , \\G%d:%d , \\G%d:%d , \\P%d:%d , \\G%d:%d );\n" % (i, r, i, j, l, r, i, j, l, r, i, r, i, r))
            masks.append([i, r])
            if (i & 63) == 62:
              [i, j] = masks.pop()
              [l, r] = masks.pop()
              if r == -1:
                print("  wire \\G%d:%d ;\n" % (i, r))
                print("  Gij \\%d:%d (\\P%d:%d , \\G%d:%d , \\G%d:%d , \\G%d:%d );\n" % (i, r, i, j, i, j, l, r, i, r))
              else:
                print("  wire \\P%d:%d , \\G%d:%d ;\n" % (i, r, i, r))
                print("  PijGij \\%d:%d (\\P%d:%d , \\P%d:%d , \\G%d:%d , \\G%d:%d , \\P%d:%d , \\G%d:%d );\n" % (i, r, i, j, l, r, i, j, l, r, i, r, i, r))
              masks.append([i, r])
              if (i & 127) == 126:
                [i, j] = masks.pop()
                [l, r] = masks.pop()
                if r == -1:
                  print("  wire \\G%d:%d ;\n" % (i, r))
                  print("  Gij \\%d:%d (\\P%d:%d , \\G%d:%d , \\G%d:%d , \\G%d:%d );\n" % (i, r, i, j, i, j, l, r, i, r))
                else:
                  print("  wire \\P%d:%d , \\G%d:%d ;\n" % (i, r, i, r))
                  print("  PijGij \\%d:%d (\\P%d:%d , \\P%d:%d , \\G%d:%d , \\G%d:%d , \\P%d:%d , \\G%d:%d );\n" % (i, r, i, j, l, r, i, j, l, r, i, r, i, r))
                masks.append([i, r])
    # End nested if's
    top = len(masks) - 1
    [i, j] = masks[top]
    while j != -1:
      top = top - 1
      [l, r] = masks[top]
      if r == -1:
        print("  wire \\G%d:%d ;\n" % (i, r))
        print("  Gij \\%d:%d (\\P%d:%d , \\G%d:%d , \\G%d:%d , \\G%d:%d );\n" % (i, r, i, j, i, j, l, r, i, r))
      else:
        print("  wire \\P%d:%d , \\G%d:%d ;\n" % (i, r, i, r))
        print("  PijGij \\%d:%d (\\P%d:%d , \\P%d:%d , \\G%d:%d , \\G%d:%d , \\P%d:%d , \\G%d:%d );\n" % (i, r, i, j, l, r, i, j, l, r, i, r, i, r))
      j = r
  else:
    j = i
    for k in range(len(masks)-1, -1, -1):
      [l, r] = masks[k]
      if i == j:
        if r == -1:
          print("  wire \\G%d:%d ;\n" % (i, r))
          print("  Gij \\%d:%d (P[%d], G[%d], \\G%d:%d , \\G%d:%d );\n" % (i, r, i, i, l, r, i, r))
        else:
          print("  wire \\P%d:%d , \\G%d:%d ;\n" % (i, r, i, r))
          print("  PijGij \\%d:%d (P[%d], \\P%d:%d , G[%d], \\G%d:%d , \\P%d:%d , \\G%d:%d );\n" % (i, r, i, l, r, i, l, r, i, r, i, r))
      elif r == -1:
        print("  wire \\G%d:%d ;\n" % (i, r))
        print("  Gij \\%d:%d (\\P%d:%d , \\G%d:%d , \\G%d:%d , \\G%d:%d );\n" % (i, r, i, j, i, j, l, r, i, r))
      else:
        print("  wire \\P%d:%d , \\G%d:%d ;\n" % (i, r, i, r))
        print("  PijGij \\%d:%d (\\P%d:%d , \\P%d:%d , \\G%d:%d , \\G%d:%d , \\P%d:%d , \\G%d:%d );\n" % (i, r, i, j, l, r, i, j, l, r, i, r, i, r))
      j = r
  print("  Sum s%d(\\G%d:-1 , A[%d], B[%d], S[%d]);\n" % (i+1, i, i+1, i+1, i+1));

print("  assign Cout = (\\G%d:-1 & A[%d]) | (\\G%d:-1 & B[%d]) | (A[%d] & B[%d]);\n" % (count-2, count-1, count-2, count-1, count-1, count-1))
print("endmodule");
