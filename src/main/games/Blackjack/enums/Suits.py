from enum import Enum

class Suits(Enum):
  HEARTS = 1
  DIAMONDS = 2
  CLUBS = 3
  SPADES = 4
  
  def __str__(self):
    return ["\u2665", "\u2666", "\u2663", "\u2660"][self.value - 1]
      
