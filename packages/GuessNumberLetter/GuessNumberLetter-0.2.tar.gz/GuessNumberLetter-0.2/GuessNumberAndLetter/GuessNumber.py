from .GeneralGuess import GeneralGuess
from random import randint


class GuessNumber(GeneralGuess):
    def __init__(self):
        GeneralGuess.__init__(self)

    def guess(self, n):
        if n == self.number:
            print("You have the right number")
        elif n < self.number:
            print("Your number is below")
        elif n > self.number:
            print("Your number is high")

    def change_guess(self):
        self.number = randint(1, 1000)

    def get_answer(self):
        return self.number