from .GeneralGuess import GeneralGuess
from random import randint
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
           'u', 'v', 'w', 'x', 'y', 'z']


class GuessLetter(GeneralGuess):
    def __init__(self):
        self.number = randint(1, 25)
        self.letter = letters[self.number]

    def guess(self, n):
        position = letters.index(n)
        if position == self.number:
            print("You have the right letter")
        elif position < self.number:
            print("Your letter is below")
        elif position > self.number:
            print("Your letter is high")

    def change_guess(self):
        self.number = randint(1, 25)

    def get_answer(self):
        return letters[self.number]
