import os
import random

TITLE = """
██╗  ██╗ █████╗ ███╗   ██╗ ██████╗ ███╗   ███╗ █████╗ ███╗   ██╗
██║  ██║██╔══██╗████╗  ██║██╔════╝ ████╗ ████║██╔══██╗████╗  ██║
███████║███████║██╔██╗ ██║██║  ███╗██╔████╔██║███████║██╔██╗ ██║
██╔══██║██╔══██║██║╚██╗██║██║   ██║██║╚██╔╝██║██╔══██║██║╚██╗██║
██║  ██║██║  ██║██║ ╚████║╚██████╔╝██║ ╚═╝ ██║██║  ██║██║ ╚████║
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝                                                                
by Leonel Olivares (ver. 1.0)

This is the hangman game, the objective is simple, DO NOT DIE!!!!!

Someone has kidnapped you and wants to play with you, you have to 
decipher the secret word, but if you don't decipher it you will end 
up hanged.

    RULES:
    - You have to enter a letter that you think belongs to the word (one
      per attempt). If the letter belongs to the word then the word will 
      be deciphered, otherwise you will lose a life and you will be closer 
      to being hanged.
    - You can only enter alphabet characters.
    - You only have 6 lives, if you run out of lives you lose.
    - If you discover the first word you are free, you won!, but you can 
      try infinite luck to know how skillful you are escaping from death.
    - Your lives do not reset, play until you die.

"""

WIN = """
 __   __  _______  __   __    _     _  ___   __    _  __  
|  | |  ||       ||  | |  |  | | _ | ||   | |  |  | ||  | 
|  |_|  ||   _   ||  | |  |  | || || ||   | |   |_| ||  | 
|       ||  | |  ||  |_|  |  |       ||   | |       ||  | 
|_     _||  |_|  ||       |  |       ||   | |  _    ||__| 
  |   |  |       ||       |  |   _   ||   | | | |   | __  
  |___|  |_______||_______|  |__| |__||___| |_|  |__||__| 
"""

LOSE = """
 _______  _______  __   __  _______    _______  __   __  _______  ______   
|       ||   _   ||  |_|  ||       |  |       ||  | |  ||       ||    _ |  
|    ___||  |_|  ||       ||    ___|  |   _   ||  |_|  ||    ___||   | ||  
|   | __ |       ||       ||   |___   |  | |  ||       ||   |___ |   |_||_ 
|   ||  ||       ||       ||    ___|  |  |_|  ||       ||    ___||    __  |
|   |_| ||   _   || ||_|| ||   |___   |       | |     | |   |___ |   |  | |
|_______||__| |__||_|   |_||_______|  |_______|  |___|  |_______||___|  |_|
"""

HANGMAN_PICS = ['''
  +---+
  |   |
      |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
========='''
]


def rules():
    os.system("clear")
    print(TITLE)
    input("Press ENTER to continue...")


def get_words():
    with open("./data.txt", "r", encoding="utf-8") as file:
        return [i.replace("\n","") for i in file]


def normalize(word):
    replacements = (
            ("á", "a"),
            ("é", "e"),
            ("í", "i"),
            ("ó", "o"),
            ("ú", "u"),
        )
    for a, b in replacements:
        word = word.replace(a, b).replace(a.upper(), b.upper())
    return word


def is_contained(word, letter):
    count = -1
    position = []
    while True:
        try:
            count = word.index(letter, count+1)
            position.append(count)
        except ValueError:
            break
    if len(position) > 0:
        return True, position
    else:
        return False, position


def validation_letter(letter):
    letter_without_spaces = letter.strip()
    try:
        assert not letter_without_spaces.isnumeric()
        assert len(letter_without_spaces) == 1
        letter_without_spaces = normalize(letter_without_spaces)
        letter_without_spaces = letter_without_spaces.lower()
        if letter_without_spaces != "ñ":
            assert ord(letter_without_spaces) > 96 and ord(letter_without_spaces) < 123
        return True, letter_without_spaces
    except AssertionError:
        return False, letter_without_spaces


def game(status_man, count_lives, score, word):
    size_word = len(word)
    hidden_word = ["_" for i in range(0, size_word)]
    word_normalize = normalize(word)
    err_mess = ""
    while count_lives > 0:
        os.system("clear")
        print("LIVES =", count_lives, "\t", "SCORE =", score)
        print(HANGMAN_PICS[status_man], "\t" + " ".join(hidden_word), "\n")
        if len(err_mess) > 0:
            print(err_mess)
        letter = input("Please enter a letter: ")
        valid_letter, letter = validation_letter(letter)
        if valid_letter:
            err_mess = ""
        else:
            err_mess = "You're stupid, you can only enter one character and it must be a letter of the alphabet."
            continue
        contained_letter, positions = is_contained(word_normalize, normalize(letter))
        if contained_letter:
            for i in positions:
                hidden_word[i] = word[i]
        else:
            status_man += 1
            count_lives -= 1
        if "".join(hidden_word) == word:
            return True, status_man, count_lives
    return False, status_man, count_lives


def main():
    status_game = True
    status_man = 0
    count_lives = 6
    score = 0
    infinity_game_question = True
    list_words = get_words()
    err_mess = ""
    rules()
    while status_game:
        word = random.choice(list_words).lower()
        status_game, status_man, count_lives = game(status_man, count_lives, score, word)
        if status_game:
            score += 1
            if infinity_game_question:
                while True:
                    try:
                        os.system("clear")
                        print(WIN, "\n")
                        print("You have succeeded, but will you have the same luck next time?")
                        print("1 - Continue")
                        print("2 - Finish and leave with a single point hahaha NOOB")
                        answer = int(input("Choose wisely: "))
                        assert answer == 1 or answer == 2
                        break
                    except AssertionError:
                        continue
                    except ValueError:
                        continue
                if answer == 1:
                    infinity_game_question = False
                else:
                    status_game = False
            os.system("clear")
            print("The word is:", word)
            print("Your score:", score)
            print("You have", count_lives, "lives left")
            input("Press ENTER to continue...")
        else:
            os.system("clear")
            print(LOSE, "\n")
            print("The word is:", word)
            print("Your score:", score)
            input("Press ENTER to exit...")
    os.system("clear")


if __name__ == "__main__":
    main()