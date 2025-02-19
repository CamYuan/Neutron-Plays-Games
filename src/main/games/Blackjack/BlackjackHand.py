from typing import List

from games.Blackjack import BlackjackCard, Player
from games.Blackjack.enums import Actions, Result
from .BlackjackCard import BlackjackCard

'''
A hand is each individual collection of cards. A player may split a hand which will create a seperate instance of a hand
'''
class BlackjackHand:

  def __init__(self, player, bet, splitAces=False):
    self.bet: int = bet
    self.player: Player = player
    self.softScore: int = 0 
    self.hardscore: int = 0
    self._cards: List[BlackjackCard] = []
    self._splitFromAces: bool = splitAces
    self._doubledDown: bool = False

  def __repr__(self):
    return ' '.join([str(card) for card in self._cards])

  def addCard(self, card: BlackjackCard):
    self._cards.append(card)
    self.updateSoftScore(card)
    self.updateHardScore(card)
      
  #TODO: This isn't going to work is A is first. Like A 9 9, Ace is treated like an 11 + 9 + 9 would be a "bust"
  def updateSoftScore(self, card: BlackjackCard):
    if(self.softScore + card.getSoftValue() <= 21):
      self.softScore += card.getSoftValue()
    else:
      self.softScore += card.getHardValue()
  
  def updateHardScore(self, card: BlackjackCard):
    self.hardscore += card.getHardValue()
    
  def getHandScore(self):
    if(self.softScore <= 21 and self.softScore > self.hardscore):
      return self.softScore
    else:
      return self.hardscore
    
  #Should only be called at beginning of a Round. 
  #There are other factors that rule out a Blackjack but I'm keeping it simple and expecting this only to be called once
  def hasBlackjack(self):
    return self.softScore == 21

  def canDoubleDown(self):
    if(len(self._cards) != 2 or self._splitFromAces):
      return False
    else:
      return True
  
  '''
  Can only split Aces once
  If both cards are the same rank, can split -> (A, 2, 3, 4, 5, 6, 7, 8, 9)
  If both cards have values > 9, can split -> (10, J, Q, K) all act as if they are the same
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
    self.player.bankroll -= self.bet
    self._doubledDown = True

  def splitHand(self) -> 'BlackjackHand':
    if self._cards[0].value() == 1:
        self._splitFromAces = True
    newHand = BlackjackHand(self.bet, self._splitFromAces)
    newHand.addCard(self._cards.pop())
    return newHand
  
  def getPlayerAction(self, playerSplitCount):
    if(self._splitFromAces or self._doubledDown or self.softScore == 21 or self.isBust()):
      return Actions.S
    optionsText, splitOptionAvailable, doubleDownOptionAvailable = self.getActionOptions(playerSplitCount)
    choice = self.player.askForDecision(optionsText, splitOptionAvailable, doubleDownOptionAvailable )
    return choice

  def getActionOptions(self, playerSplitCount):
    optionsText = "[H]it or [S]tand"
    splitOptionAvailable = False
    doubleDownOptionAvailable = False
    if(self.player.hasEnoughFunds(self.bet)):
      if self.canSplit() and playerSplitCount < 3:
        optionsText +=  " or Spli[T]"
        splitOptionAvailable = True
      if self.canDoubleDown():
        optionsText +=  " or [D]oubledown"
        doubleDownOptionAvailable = True
    optionsText += ": "
    return optionsText, splitOptionAvailable, doubleDownOptionAvailable
  
  def processBlackjack(self):
    self.player.recievePayout(self.bet * 2.5)
    self.player.finalizeHand(Result.BLACKJACK)

  def processWin(self):
    self.player.recievePayout(self.bet * 2)
    self.player.finalizeHand(Result.WIN)
  
  def processLose(self):
    self.player.finalizeHand(Result.LOSS)
  
  def processPush(self):
    self.player.recievePayout(self.bet)
    self.player.finalizeHand(Result.PUSH)
  
  
  
  
  

