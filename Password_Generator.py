#This Program is uesd to generate a password according to user defined length

import random 

#Function for generating password according to user defined length

def generate_password(len):  
    list_of_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()"  
    pass_str = ""  
    for i in range(len):  
        pass_str = pass_str + random.choice(list_of_chars)  
    return pass_str 

#Function asking for user to suggest the password length and user satisfaction about the password 
  
def selectPassword():
    length= int(input("Enter the Password Length:  "))
    password = generate_password(length)
    print(f'The Generated Password is {password}')
    response = input("Are you satisfied: ")
    if(response=='YES'):
        print("Thanks")
    else:
        selectPassword()

# Calling Function
selectPassword()    



