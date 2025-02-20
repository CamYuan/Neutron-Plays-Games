from games.Blackjack.enums import Actions, Result

'''
Maybe this should be an agent instead? Especially now that the hands and splithand count are being moved to Round clss
'''
class Player:
  def __init__(self, name, bankroll=0):
    self.name = name 
    self.bankroll = bankroll
    self.wins = 0
    self.losses = 0
    self.pushes = 0

  def __repr__(self):
    return "{}: {}-{}-{} Remaining bankroll: {}".format(self.name, self.wins, self.losses, self.pushes, self.bankroll)
  
  def __hash__(self):
    return hash(self.name)
  
  def __eq__(self, other):
    return isinstance(other, Player) and self.name == other.name
  
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
    
  def hasEnoughFunds(self, amount):
    return amount <= self.bankroll    
    
  def askForBet(self):
    validBet = False
    betAmount = 0
    while(not validBet):
      try:
        betAmount = int(input("Your Funds: " + str(self.bankroll) + "\nHow much do you want to bet? "))
        validBet = self.hasEnoughFunds(betAmount) 
      except:
        print("Invalid Bet. Please enter a number")
        validBet = False
    self.bankroll -= betAmount
    return betAmount

  def askForDecision(self, optionsText, splitOptionAvailable, doubleDownOptionAvailable):
    choice = input(optionsText).upper()
    while not self.isValidUserAction(choice, splitOptionAvailable, doubleDownOptionAvailable):
      # Maybe we toggle user input or NN input here with a flag or something
      choice = input(optionsText).upper()
      # choice = getModelPrediction(dealer, hand)
    if choice == 'H':
      return Actions.H
    elif choice == 'S':
      return Actions.S
    elif choice == 'D': 
      return Actions.D
    elif choice == 'T':
      return Actions.T
    else:
      print("Invalid Input which shouldn't be possible")
  
  def isValidUserAction(self, choice, splitOptionAvailable, doubleDownOptionAvailable):
    valid =  choice == 'H' or choice == 'S' or (splitOptionAvailable and choice == 'T') or (doubleDownOptionAvailable and choice == 'D')
    if not valid: print('Invalid Input. Try again')
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