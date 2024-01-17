import random
word_list = ['DUBAID', 'EXPENSE', 'STITLL', 'NOWENMEN', 'FIHFLIGHTS', 'ELHOTEL', 'VIVSSA', 'FOREREX', 'CDDRARD']
random_word = word_list[random.randint(0, len(word_list)-1)].lower()
print(random_word)
word = []
lives = 3
for i in random_word:
    word.append('-')
for i in word:
    print(i, end=' ')
while '-' in word and lives > 0:
    guess = input("\nGuess the letter")
    if guess in random_word:
        for i in range(len(word)):
            if guess == random_word[i]:
                word[i] = guess
    else:
        lives -= 1
        
        if lives == 1:
            print(f"You lose one life. You have {lives} life left")
        elif lives == 0:
            print(f"You have {lives} lives left. You are dead. ")
        else:
            print(f"You lose one life. You have {lives} lives left")
        

    for i in word:
        print(i, end= ' ')
    
    if '-' not in word:
        print("\nYou win")

print('testing')