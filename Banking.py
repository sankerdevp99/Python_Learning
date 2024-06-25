import random

# Minumum Account Balance need to be maintained 2000
Account_Balance = 2000

#Function to Generate Account Number
def BankAccount_Number():
    account_number = ''
    for i in range(10):
        num = random.randint(0,9)
        strnum=str(num)
        account_number+=strnum
    if(account_number[0]=="0"):
        BankAccount_Number()
    else:
        return(account_number)

#Function to generate AGE Eligibility
def Minority_Check(age):
    if (age>=18):
        number = BankAccount_Number()
        print(f'Pay 2000 for starting an account. Your Account Number is  {number}')
    else:
        print("You are not eligible to start an Account")
        

#Function for deositing the amount
def Deposit(num):
    global Account_Balance
    Account_Balance+=num
    return(Account_Balance)

#Function for withdrawl the Amount
def WithDraw(num):
    global Account_Balance
    Account_Balance-=num
    return(Account_Balance)

#Function to calculate the fixed deposit amount after the tenure
def Simple_Interset(Principal_Amount,Rate_of_interset,Number_of_Years):
    SI = (Principal_Amount * Rate_of_interset * Number_of_Years)/100
    return (Principal_Amount+SI)


###################################################################################################


 ##    Banking Service ##

while(True):
    print("Welcome to Sanker Banking Services please select the options below for your services")
    print (" 1.Open a savings bank account\n 2.Deposit Money\n 3.With Draw Money \n 4.Fixed Deposit \n 5.Account Closing")
    user_input = int(input(" Type Response "))
    if ( user_input == 1):
        user_age = int(input("Enter Your Age: "))
        Minority_Check(user_age)
    elif(user_input==2):
        user_account_number = int(input("Enter Account Number"))
        user_deposit_money = int(input("Enter the Ammount planned to deposit"))
        Account_Balance=Deposit(user_deposit_money)
        print(f'Your current Account Balance is {Account_Balance}')
    elif(user_input==3):
        user_account_number = int(input("Enter Account Number"))
        user_withdraw_money = int(input("Enter the Amount to be withdrawed"))
        print(Account_Balance)
        if (Account_Balance-2000<user_withdraw_money):
            print("Your Minimum balance need to be retained, Withdrwal not possible")
        else:
            Account_Balance=WithDraw(user_withdraw_money)
            print(f'Your current Account Balance is {Account_Balance}')
    elif(user_input==4):
        print("For Fixed Deposit , Rate of interest is 8.5 % , for an year ")
        user_account_number = int(input("Enter Account Number"))
        user_choice = float(input("Enter the Amount planning to Deposit: "))
        time_span = int (input("Enter the number of year plan to deposit"))
        FD_Amount = Simple_Interset(user_choice,8.5,time_span)
        print(f'The final Amount after tenure is {FD_Amount}')
    elif(user_input==5):
        print(f'You can close the account, your  withdrawl amount is {Account_Balance}')
        break
    else:
        print("Invalid Response")

    




