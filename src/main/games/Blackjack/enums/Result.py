from enum import Enum

class Result(Enum):
  BLACKJACK = 1
  WIN = 2
  LOSS = 3
  PUSH = 4
  
  def __str__(self):
    return ["BLACKJACK", "WIN", "LOSS", "PUSH"][self.value - 1]