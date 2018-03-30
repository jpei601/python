"""Week 3, Exercise 3.

Steps on the way to making your own guessing game.
"""



import random

import os
import sys
"""
the following is important, it add the current workspace into the sys.path, so python can search th module by the path and got it
"""
print(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# because the week3 is sub-fold of current workspace, the search order is the starting from workspace, so there need add week3
# another way it to put the path of week3 into the sys.path, and can use exercise directly..
from week3.exercise1 import not_number_rejector

def advancedGuessingGame():
    """Play a guessing game with a user.

    The exercise here is to rewrite the exampleGuessingGame() function
    from exercise 3, but to allow for:
    * a lower bound to be entered, e.g. guess numbers between 10 and 20
    * ask for a better input if the user gives a non integer value anywhere.
      I.e. throw away inputs like "ten" or "8!" but instead of crashing
      ask for another value.
    * chastise them if they pick a number outside the bounds.
    * see if you can find the other failure modes.
      There are three that I can think of. (They are tested for.)

    NOTE: whilst you CAN write this from scratch, and it'd be good for you to
    be able to eventually, it'd be better to take the code from exercise 2 and
    marge it with code from excercise 1.
    Remember to think modular. Try to keep your functions small and single
    purpose if you can!
    """
    print("\nwelcome to the guessing game!")
    print("A number between _? and _ ?")
    lowerBound = not_number_rejector("Enter an lower bound: ")

    flag = False
    while not flag:
        upperBound = not_number_rejector("Enter an upper bound: ")
        if (upperBound>=lowerBound):
          flag = True
        else:
          print("the upperBound is less than lowerBound")

    print("OK then, a number between {} and {} ?".format(lowerBound,upperBound))

    actualNumber = random.randint(lowerBound, upperBound)

    guessed = False

    xstr = ""
    while not guessed:
      try:
        xstr = input("guess a number: ")
        guessedNumber = int(xstr)
        print("you guessed {},".format(guessedNumber),)
        if (guessedNumber == actualNumber):
            print("you got it!! It was {}".format(actualNumber))
            guessed = True
        elif guessedNumber < actualNumber:
            print("too small, try again ")
        else:
            print("too big, try again   ")
      except Exception:
        print("you entered {} is not a number".format(xstr))

    return "You got it!"


if __name__ == "__main__":
    advancedGuessingGame()
