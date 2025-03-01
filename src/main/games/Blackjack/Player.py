from typing import List
from games.Blackjack.enums import Actions, Result

import logging
logger = logging.getLogger(__name__)

'''
I think an Agent/NN could just inherit from this class and overload the askForBet and getAction methods
'''
class Player:
  def __init__(self, name, bankroll=0, autobet=False):
    self.name: str = name 
    self.bankroll: int = bankroll
    self.autobet = autobet
    self.wins: int = 0
    self.losses: int = 0
    self.pushes: int = 0
    self.busts: int = 0

  def __repr__(self):
    return "{}: {}-{}-{} Remaining bankroll: {}".format(self.name, self.wins, self.losses, self.pushes, self.bankroll)
  
  def __hash__(self):
    return hash(self.name)
  
  def __eq__(self, other):
    return isinstance(other, Player) and self.name == other.name
  
  def printStats(self):
    logger.info(self)
    totalHands = self.wins + self.losses + self.pushes
    winLossHands = totalHands - self.pushes
    logger.info('\n' +self.name + " Stats:\n")
    output = ""
    output +="{W:^9}-{L:^9}-{P:^9}/{T:^9}\n".format(W="Wins", L="Loss",P="Push",T="Total")
    output +="{W:^9}-{L:^9}-{P:^9}/{T:^9}\n".format(W=self.wins, L=self.losses, P=self.pushes, T=totalHands) 
    output += "{:^9.2%}-{:^9.2%}-{:^9.2%}\n".format(self.wins/totalHands, self.losses/totalHands, self.pushes/totalHands)
    if(winLossHands > 0):
      output += "\nExcluding ties\n"
      output +="{W:^9}-{L:^9}/{T:^9}\n".format(W="Wins", L="Loss",T="Total")
      output += "{W:^9}-{L:^9}/{T:^9}\n".format(W=self.wins, L=self.losses,T=winLossHands)
      output += "{Wins:^9.2%}-{Losses:^9.2%}\n".format(Wins=self.wins/winLossHands, Losses=self.losses/winLossHands)
    logger.info(output)
    
  def hasEnoughFunds(self, amount):
    return amount <= self.bankroll    
    
  def askForBet(self):
    if(self.autobet):
      self.bankroll -= 10
      return 10
    logger.info('\n')
    validBet = False
    betAmount = 0
    while(not validBet):
      try:
        betAmount = int(input("Your Funds: " + str(self.bankroll) + "\nHow much do you want to bet? "))
        validBet = self.hasEnoughFunds(betAmount) 
      except:
        logger.info("Invalid Bet. Please enter a number")
        validBet = False
    self.bankroll -= betAmount
    return betAmount

  '''
  Override this method if you want to utilize a NN model.
  Something like 
  def askForDecision(self, availableOptions: List[Actions]):
    return model.predict(availableOptions)
  Hmm might need to ensure that the model is choosing valid actions
  also it might want more information
  '''
  def getAction(self, availableOptions: List[Actions]):
    optionsText = "[S]tand"
    if(availableOptions.__contains__(Actions.H)):
      optionsText += " or [H]it"
    if(availableOptions.__contains__(Actions.D)):
      optionsText += " or [D]oubledown"
    if(availableOptions.__contains__(Actions.T)):
      optionsText += " or Spli[T]"
    optionsText += ": "
    choice = input('\n' + optionsText).upper()
    while not self.isValidUserAction(choice, availableOptions):
      choice = input(optionsText).upper()
    if choice == 'H':
      return Actions.H
    elif choice == 'S':
      return Actions.S
    elif choice == 'D': 
      return Actions.D
    elif choice == 'T':
      return Actions.T
    else:
      logger.info("Invalid Input which shouldn't be possible")
  
  def isValidUserAction(self, choice: str, availableOptoins: List[Actions]):
    valid =  choice == 'H' or choice == 'S' or (choice == 'T' and availableOptoins.__contains__(Actions.T)) or (choice == 'D' and availableOptoins.__contains__(Actions.D))
    if not valid: logger.info('Invalid Input. Try again')
    return valid
  
  def recievePayout(self, amount):
    self.bankroll += amount
  
  def finalizeHand(self, result: Result):
    if(result == Result.WIN):
      self.wins += 1
    elif(result == Result.BLACKJACK):
      self.wins += 1
    elif(result == Result.LOSS):
      self.losses += 1
    elif(result == Result.PUSH):
      self.pushes += 1
    elif(result == Result.BUST):
      self.busts += 1
      self.losses += 1
   
  #used for calculating reward   
  def resetScore(self):
    self.wins = 0
    self.losses = 0
    self.pushes = 0
    self.busts = 0