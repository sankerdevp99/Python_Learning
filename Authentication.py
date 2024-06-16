#Simple Program used to authenticate user , User Name is ADMIN and Password is St0rE@1, and User only have 2 more attempts
#to correct the password


#Function to input UserName and Password
counter = 0
def logintry():
    username = input("Enter the User Name: ")
    password = input("Enter the Password: ")
    login(username,password)

#Function to Validate User Name and Passsword
def login(uid,pwd):
      global counter 
      if(uid=="ADMIN" and pwd =="St0rE@1"):
        print("Login Succesfully")
      else:
         if(counter<2):
            print(f'Try Again, {2-counter} attempts pending')
            counter+=1
            logintry()
            
         else:
            print("Attempts Over , Account Blocked")

#Calling Function         
logintry()


