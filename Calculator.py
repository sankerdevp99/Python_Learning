# Python program for simple calculator having operations addition,subtraction,multiplication,division,exponents
from math import pow
# Function to add two numbers
def add(num1, num2):
	return num1 + num2
# Function to subtract two numbers
def subtract(num1, num2):
	return num1 - num2
# Function to multiply two numbers
def multiply(num1, num2):
	return num1 * num2
#Functuon to division two numbers
def divide(num1,num2):
  if (num2==0):
        print("Division by Zero is not Allowed")
  else:
	  return (num1/num2)
#Function to calculate exponent of number
def exponent(num1,num2):
	return pow(num1,num2)
# Take input from the user
print (f'Valid Operators are + , -,*,/,^')
operator = input("Select Valid Operator")

number_1 = float(input("Enter first number: "))
number_2 = float(input("Enter second number: "))

if operator == "+":
	print(number_1, "+", number_2, "=",
					round(add(number_1, number_2),2))

elif operator == "-":
	print(number_1, "-", number_2, "=",
					round(subtract(number_1, number_2),2))

elif operator== "*":
	print(number_1, "*", number_2, "=",
					round(multiply(number_1, number_2),2))

elif operator== "/":
	print(number_1, "/", number_2, "=",
					divide(number_1, number_2))
elif operator== "^":
	print(number_1, "^", number_2, "=",
				   round(exponent(number_1, number_2),2))	
else:
	print("Invalid Response")
