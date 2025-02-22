from typing import List

from games.Blackjack import BlackjackCard, Player
from games.Blackjack.enums import Actions, Result
from .BlackjackCard import BlackjackCard

'''
A hand is each individual collection of cards. A player may split a hand which will create a seperate instance of a hand
'''
class BlackjackHand:

  def __init__(self, player, bet=0, splitAces=False, dealer=False):
    self.bet: int = bet
    self.player: Player = player
    self.dealer = dealer
    self._cards: List[BlackjackCard] = []
    
    self.__softScore: int = 0 
    self.__hardScore: int = 0
    self.__splitFromAces: bool = splitAces
    self.__doubledDown: bool = False

  def __repr__(self):
    if(self.dealer):
      return self.player.name + ': '+ str(self._cards[1])
    else:
      return self.player.name + ': ' +' '.join([str(card) for card in self._cards])

  def addCard(self, card: BlackjackCard):
    self._cards.append(card)
    self.__updateSoftScore(card)
    self.__updateHardScore(card)
      
  #Softscore can 'bust' in which case the class will default to the hard score
  def __updateSoftScore(self, card: BlackjackCard):
    if(self.__softScore + card.getSoftValue() <= 21):
      self.__softScore += card.getSoftValue()
    else:
      self.__softScore += card.getHardValue()
  
  def __updateHardScore(self, card: BlackjackCard):
    self.__hardScore += card.getHardValue()
    
  def getHandScore(self):
    if(self.__softScore <= 21 and self.__softScore > self.__hardScore):
      return self.__softScore
    else:
      return self.__hardScore
    
  #Should only be called at beginning of a Round. 
  #There are other factors that rule out a Blackjack but I'm keeping it simple and expecting this only to be called once
  def hasBlackjack(self):
    return self.__softScore == 21

  def canDoubleDown(self):
    if(len(self._cards) != 2 or self.__splitFromAces):
      return False
    else:
      return True
  
  def doubleDown(self):
    self.bet *= 2
    self.player.bankroll -= self.bet
    self.__doubledDown = True
  
  '''
  Can only split Aces once
  If both cards are the same rank, can split -> (A, 2, 3, 4, 5, 6, 7, 8, 9)
  If both cards have values > 9, can split -> (10, J, Q, K) all act as if they are the same
  '''
  def canSplit(self):
    if(self.__splitFromAces):
      return False
    if (len(self._cards) != 2):
      return False
    if(self._cards[0] == self._cards[1]) :
      return True
    else:
      return False
    
  def splitHand(self) -> 'BlackjackHand':
    if self._cards[0].value() == 1:
        self.__splitFromAces = True
    newHand = BlackjackHand(player=self.player, bet=self.bet, splitAces=self.__splitFromAces)
    newHand.addCard(self._cards.pop())
    return newHand
  
  def isBust(self):
    return self.__hardScore > 21
  
  def getPlayerAction(self, playerSplitCount):
    if(self.__splitFromAces or self.__doubledDown or self.__softScore == 21 or self.isBust()):
      return Actions.S
    optionsText, splitOptionAvailable, doubleDownOptionAvailable = self.getActionOptions(playerSplitCount)
    choice: str = self.player.askForDecision(optionsText, splitOptionAvailable, doubleDownOptionAvailable )
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
    print(str(self), "Blackjack!")

  def processWin(self):
    self.player.recievePayout(self.bet * 2)
    self.player.finalizeHand(Result.WIN)
    print(str(self), "Win!")
  
  def processLose(self):
    self.player.finalizeHand(Result.LOSS)
    print(str(self), "Loss!")
  
  def processPush(self):
    self.player.recievePayout(self.bet)
    self.player.finalizeHand(Result.PUSH)
    print(str(self), "Push!")

  
  
  
  
  

