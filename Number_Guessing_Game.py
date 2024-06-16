
#This Program is a number guessing name where user can guess a number between 1 to 50, if it matches with computer guessed
#number you win otherwise fail 
import random
#Function to generate a number in between 1 to 50
def guess():
    random_number = random.randint(1,50)
    guess = 0
    count = 0
    while count<10:
           count+=1
           guess = int(input("Guess the number between 1 and 50: " ))
           if guess < random_number:
            print("Sorry,guess again, Too Low")
           elif guess> random_number:
            print("Sorry, Guess Again, Too High")
           else:
              print("Congragulations Bro")
              break
    if(count==10): 
        print("You Failed")      
        print(f'The Guessed Number is {random_number}')


#Function calling
guess()
