import random

class Guess():
    """ Guess class for guessing a random number and telling the user if his/her own 
    guess is lower or higher than the actual number.
    
    Attributes:
        expected (number) representing the guess of the class      
    """
    def __init__(self):
        self.expected=random.randint(1, 1000)
      
        
    
    def my_guess(self,actual=None):
        """Function to determine if the guess is lower, higher or accurate
        
        Args: 
            actual(number)representing the guess of the user 
        
        Returns: 
            string: guess result
        """
        if(actual=None):
            return "Hey Buddy! You didn't enter a guess."
        elif(actual == self.expected):
            return "You're a genius mate!"
        elif(actual > self.expected):
            return "Sorry mate! Your guess is lower than the actual value"
        else:
            return "Sorry mate! Your guess is higher than the actual value"
        