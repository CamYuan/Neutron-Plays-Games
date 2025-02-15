from .enums import Rank, Suits
class BlackjackCard:

  #None is used for a special card, the Cut Card, which is inserted in the shoe and indicates a shuffle
  def __init__(self, rank: Rank | None, suit: Suits | None):
      self.rank = rank  
      self.suit = suit 

  def __repr__(self):
    if(self.rank == None):
      return "Cut Card \u2612"
    else:
      return self.rank.value[1] + self.suit.value
    
  def __eq__(self, other):
    if isinstance(other, BlackjackCard):
      return self.rank == other.rank 
    return False
  
  def value(self):
    return self.rank.value[0]
    
  def getSoftValue(self):
    if(self.rank == Rank.ACE):
      return 11
    else:
      return self.getHardValue()

  def getHardValue(self):
    if(self.value() >= 10):
      return 10
    else:
      return self.rank


#TODO: add card counting values from https://www.blackjackapprenticeship.com/card-counting-systems/
