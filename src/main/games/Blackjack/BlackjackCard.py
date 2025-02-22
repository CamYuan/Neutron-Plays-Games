from .enums import Rank, Suits
class BlackjackCard:

  #None is used for a special card, the Cut Card, which is inserted in the shoe and indicates a shuffle
  def __init__(self, rank: Rank | None, suit: Suits | None):
      self.rank: Rank = rank  
      self.suit: Suits = suit 

  def __repr__(self):
    if(self.rank == None):
      return "Cut Card \u2612"
    else:
      return str(self.rank) + str(self.suit)
    
  '''
  in the context of blackjack, 10, J, Q, and K are considered equal
  '''
  def __eq__(self, other):
    if isinstance(other, BlackjackCard):
      return self.rank == other.rank or (self.rank.value >= 10 and other.rank.value >= 10)
    return False
  
  def value(self):
    return self.rank.value
    
  def getSoftValue(self):
    if(self.rank == Rank.ACE):
      return 11
    else:
      return self.getHardValue()

  def getHardValue(self):
    if(self.value() >= 10):
      return 10
    else:
      return self.value()


#TODO: add card counting values from https://www.blackjackapprenticeship.com/card-counting-systems/
