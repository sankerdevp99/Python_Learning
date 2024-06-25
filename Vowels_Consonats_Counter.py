#Function used to count number of vowels and consonants in a string

def Vowels_Consonats_Counter(st):
    vowel_letters = ["A","E","I","O","U"]
    consonats_letters = ["B","C","D","F","G","H","J","K","L","M","N","P","Q","R","S","T","V","W","X","Y","Z"]

    (vowels,consonants)=(0,0)
    GT = st.upper()
    for ch in GT:
        if (ch in vowel_letters):
            vowels+=1
        elif(ch in consonats_letters):
            consonants+=1
    return (vowels,consonants)


user_input = input("Enter the Sentence: ")
count_vowels,count_consonants = Vowels_Consonats_Counter(user_input)
print(f'Total Number of Vowels {count_vowels} \n Total Number of Consonants {count_consonants}')