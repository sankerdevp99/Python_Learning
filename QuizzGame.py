import random


question = ["What is HTTP","What is HTML"," Which is brain of computer","Smallest unit of a Program","ROM is a _______________ memory"]
answer = ["HYPER TEXT TRANSFER PROTOCOL","HYPER TEXT MARKUP LANGUAGE","CPU","TOKEN","PRIMARY"]
score= ["Take it Seriosly","Needs to take interest","Read more to score more","Good","Excellent","Outstanding"]
s=0
sequence= []


while (True):
    r = random.randint(0,4)
    if(r not in sequence):
        sequence.append(r)
        print(question[r])
        user_answer = input ("Enter your Answer ")
        Caps_User=user_answer.upper()
        if(answer[r]==Caps_User):
            print("Great Job")
            s+=1
        else:
            print("Answer got wrong")
    elif(len(sequence)==len(question)):
        break
    else:
        continue
print(f'Your Score is {s}')
print(f'{score[s]}')
    



