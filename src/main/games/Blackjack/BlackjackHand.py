'''
{
    bet: int,
    _cards: list,
    bust: boolean,
    hasBlackjack: boolean,
    canDoubleDown: boolean,
    canSplit: boolean,
    alreadySplit: boolean,
    splitAces: boolean
}
'''
from typing import List
from .BlackjackCard import BlackjackCard


class BlackjackHand:

    def __init__(self, bet, splitAces=False):
        self.bet: int = bet
        self.softScore: int = 0 
        self.hardscore: int = 0
        self._cards: List[BlackjackCard] = []
        self._splitFromAces: bool = splitAces

    def __repr__(self):
        return ' '.join([str(card) for card in self._cards])

    def addCard(self, card: BlackjackCard):
        self._cards.append(card)
        self.updateSoftScore(card)
        self.updateHardScore(card)
        
    def updateSoftScore(self, card: BlackjackCard):
      if(self.softScore + card.getSoftValue() <= 21):
        self.softScore += card.getSoftValue()
      else:
        self.softScore += card.getHardValue()
    
    def updateHardScore(self, card: BlackjackCard):
      self.hardscore += card.getHardValue()

    def canDoubleDown(self):
      if(len(self._cards) != 2 or self._splitFromAces):
        return False
      else:
        return True
    
    '''
    Can only split Aces once
    If both _cards are the same rank, can split -> (A, 2, 3, 4, 5, 6, 7, 8, 9)
    If both _cards have values > 9, can split -> (10, J, Q, K) all act as if they are the same
    '''
    def canSplit(self):
      if(self._splitFromAces):
        return False
      if (len(self._cards) != 2):
        return False
      if(self._cards[0] == self._cards[1]) :
        return True
      else:
        return False
      
    def isBust(self):
      return self.hardscore > 21

    def doubleDown(self):
      self.bet *= 2

    def splitHand(self) -> 'BlackjackHand':
      if self._cards[0].value() == 1:
          self._splitFromAces = True
      newHand = BlackjackHand(self.bet, self._splitFromAces)
      newHand.addCard(self._cards.pop())
      return newHand

