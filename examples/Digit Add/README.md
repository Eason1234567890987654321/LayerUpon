How to use
 Run it using the LayerUpon interpreter, enter two numbers separated by spaces, and end with =.
 examples:
  123+456=
  1+1=
  4+5=
  
How it works
 The program is divided into three stages:
  1.Read the first integer. Each time you read a digit, use current value × 10 + new digit to accumulate the integer.
  2.Read the second integer. After encountering the plus sign, start adding the second integer; when you see =, perform the addition.
  3.Output the result. Extract the decimal digits one by one using integer division and subtraction, and convert them to characters for output.
 
 The default generated version supports results of non-negative integers up to 20 digits. This isn't a limitation of Python integers, but rather the current generator's maximum number of decimal output digits.
 If you want to support longer results, you can run the generator:
  python generate_multi_digit_add.py --digits 100
 It will generate a LayerUpon program that supports up to 100 results.