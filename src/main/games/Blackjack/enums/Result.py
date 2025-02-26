from enum import Enum

class Result(Enum):
  BLACKJACK = 1
  WIN = 2
  LOSS = 3
  PUSH = 4
  BUST = 5  
  
  def __str__(self):
    return ["BLACKJACK", "WIN", "LOSS", "PUSH", "BUST"][self.value - 1]