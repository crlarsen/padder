# padder.py -- Python script to generate Prefix Adders in Verilog

## Description

Python script to generate a carry-in/carry-out Prefix Adder in Verilog. The user must specify how many
bits wide the adder will be. Also, there is an optional overflow flag which can be generated. Overflow
detection is useful during the addition of signed integers. The adders produced by this script
can also be used to perform subtraction by inverting the bits of the second operand before inputting
it to the adder and setting the carry-in bit to 1.

This script was used in writing the Verilog code for the video series [Building an FPU in Verilog](https://www.youtube.com/watch?v=rYkVdJnVJFQ&list=PLlO9sSrh8HrwcDHAtwec1ycV-m50nfUVs).
See the video *Building an FPU in Verilog: Building a Faster Integer Multiply Circuit, Part 2*.

You're welcome to use this code but please include a citation of my code authorship. A reference to my GitHub repository would be even better. Thanks!

**Usage**: `python padder.py [-o | --overflow] <number of bits>`

## Manifest

|   Filename   |                        Description                        |
|--------------|-----------------------------------------------------------|
| README.md | This file. |
| padder.py | Python script. |

## Copyright

:copyright: Chris Larsen, 2021
