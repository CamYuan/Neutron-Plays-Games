from enum import Enum

class Actions(Enum):
  H = 1
  S = 2
  D = 3
  T = 4
  
  def __str__(self):
    return ["HIT", "STAND", "DOUBLE DOWN", "SPLIT"][self.value - 1]