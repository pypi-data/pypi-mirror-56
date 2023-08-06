from random import randint


class GeneralGuess:
    def __init__(self):
            self.number = randint(1, 1000)

    def guess(self, n):
        pass

    def change_guess(self):
        pass

    def get_answer(self):
        if not self.is_letter:
            return self.number
        else:
            return self.is_letter
