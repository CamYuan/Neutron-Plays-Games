from games.Blackjack.BlackjackHand import BlackjackHand
from games.Blackjack.enums import Actions
class Player:
  def __init__(self, name, bankroll=0):
    self.name = name 
    self.bankroll = bankroll
    self.hands: list[BlackjackHand] = [] 
    self.splitHandCount = 0
    self.wins = 0
    self.losses = 0
    self.pushes = 0

  def __repr__(self):
    return "{}: {}-{}-{} Remaining bankroll: {}".format(self.name, self.wins, self.losses, self.pushes, self.bankroll)
  
  def printStats(self):
    totalHands = self.wins + self.losses + self.pushes
    winLossHands = totalHands - self.pushes
    output = ""
    output += "{}: {}-{}-{} / {} \n".format(self.name, self.wins, self.losses, self.pushes, totalHands )
    output += "{:.3%}-{:.3%}-{:.3%}\n".format(self.wins/totalHands, self.losses/totalHands, self.pushes/totalHands)
    if(winLossHands > 0):
      output += "Excluding ties\n"
      output +="{W:^9}-{L:^9}/{T:^9}\n".format(W="Wins", L="Loss",T="Total")
      output += "{W:^9}-{L:^9}/{T:^9}\n".format(W=self.wins, L=self.losses,T=winLossHands)
      output += "{Wins:.2%}-{Losses:.2%}\n".format(Wins=self.wins/winLossHands,Losses=self.losses/winLossHands)
    print(output)
    
  def printHands(self):
    for hand in self.hands:
      print(hand)

  def addHand(self, hand: BlackjackHand):
    self.hands.append(hand)

  def hasEnoughFunds(self, amount):
    return amount <= self.bankroll

  def clearHands(self):
    self.splitHandCount = 0
    self.hands.clear()

  def recievePayout(self, hand: BlackjackHand, multiplier):
    self.bankroll += hand.bet #Give the player the initial bet back first
    self.bankroll += hand.bet*multiplier

  def getPlayerAction(self, hand: BlackjackHand):
    if(hand._splitFromAces or hand.softScore == 21):
      return Actions.S
    options, splitOptionAvailable, doubleDownOptionAvailable = self.getActionOptions()
    choice = ''
    while not self.validUserChoice(choice, splitOptionAvailable, doubleDownOptionAvailable):
      # Maybe we toggle user input or bot input here witha  flag or something
      choice = input(options).upper()
      # choice = getModelPrediction(dealer, hand)
    if choice == 'H':
      return Actions.H
    elif choice == 'S':
      return Actions.S
    elif choice == 'D': 
      return Actions.D
    elif choice == 'T':
      self.splitHandCount += 1
      return Actions.T
    else:
      print("Invalid Input which shouldn't be possible")

  def getActionOptions(self, hand: BlackjackHand):
    options = "[H]it or [S]tand"
    splitOptionAvailable = False
    doubleDownOptionAvailable = False
    if(self.hasEnoughFunds(hand.bet)):
      if hand.canSplit() and self.splitHandCount < 3:
        options +=  " or Spli[T]"
        splitOptionAvailable = True
      if hand.canDoubleDown():
        options +=  " or [D]oubledown"
        doubleDownOptionAvailable = True
    options += ": "
    return options, splitOptionAvailable, doubleDownOptionAvailable
  
  def validUserChoice(self, choice, splitOptionAvailable, doubleDownOptionAvailable):
    return choice == 'H' or choice == 'S' or (splitOptionAvailable and choice == 'T') or (doubleDownOptionAvailable and choice != 'D')