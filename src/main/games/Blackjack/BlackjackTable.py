import math
import random
from typing import List
from games.Blackjack import BlackjackCard, BlackjackHand, Player
from games.Blackjack.enums import Actions, Rank, Result, Suits


'''
TODO:
#Card Counting
RunningCount = 0
SuitCounts = [0,0,0,0]
'''
class BlackjackTable:
  def __init__(self, num_decks=6):
    self.minBet = 10
    self.maxBet = 1000
    self.numDecks = num_decks
    self.dealer = Player("Dealer", 10000000000)
    
    self.shoe = self.loadShoe(num_decks)
    self.isShuffleTime = False
    self.dealerHand: BlackjackHand  = None
    self.playerSplitCounts = {}
  
  def loadShoe(self, numberOfDecks) -> List[BlackjackCard]:
    shoe = []
    cutCard = BlackjackCard(None,None)
    for deck in range(0,numberOfDecks):
        for suit in Suits:
            for rank in Rank:
                shoe.append(BlackjackCard(rank,suit))
    random.shuffle(shoe) #shuffle
    #index between 70-90% of the BACK of the deck to insert the cutCard
    minIndex = math.floor(len(shoe)*.7)
    maxIndex = math.floor(len(shoe)*.9)
    shoe.insert(random.randint(minIndex,maxIndex), cutCard)
    return shoe


  def playRound(self, players):
    hands = self.initializeRound(players) #1
    self.deal(hands) #2
    self.checkBlackjacks(hands)
    self.playHands(hands)
    self.removeBustHands(hands)
    #Hands will get cleared when there is a blackjack or bust. 
    #If it's a dead hand, dealer doesn't take cards for no reason
    if(len(hands) > 0): 
      self.dealerHand.dealer = False
      self.playDealerHand()
      self.calculateScoresAndPayout(hands)
    self.reset()


    
  
  def initializeRound(self, players: List[Player]) -> List[BlackjackHand]:
    hands = []
    for player in players:
      bet = player.askForBet()
      hands.append(BlackjackHand(player, bet))
      self.playerSplitCounts[player] = 0
    hands.append(BlackjackHand(self.dealer, None, dealer=True)) #dealer hand goes last
    return hands
      
  def deal(self, hands: List[BlackjackHand]):
    for _ in range(2):
        for hand in hands:
            self.hit(hand)
    self.dealerHand = hands.pop()
    
  
  def hit(self, hand: BlackjackHand):
    card = self.shoe.pop()
    if(card.rank == None):
      # print("----------------------CUT CARD----------------------")
      self.isShuffleTime = True
      card = self.shoe.pop() #get the next card instead
    #TODO: card count here I think
    hand.addCard(card)
  
  def checkBlackjacks(self, hands: List[BlackjackHand]):
    dealerBlackjack = self.dealerHand.hasBlackjack()
    #Not offering insurance in this game
    #players will only have 1 hand each at this point
    if(dealerBlackjack):
      for hand in hands:
        if(hand.hasBlackjack()):
          hand.processPush()
        else:
          hand.processLose()
      self.reset() #round over
    else:
      for hand in hands[:]:
        if(hand.hasBlackjack()):
          hand.processBlackjack()
          hands.remove(hand) 
          
  def reset(self):
    self.dealerHand: BlackjackHand  = None
    self.playerSplitCounts = {}
    if(self.isShuffleTime):
      self.shoe = self.loadShoe(self.numDecks)
    
    
  def playHands(self, hands: List[BlackjackHand]):
    for index, hand in enumerate(hands):
      #After a split, the second hand won't get a card until the first hand is done
      if len(hand._cards) < 2: 
        self.hit(hand)
      print(self.dealerHand)
      print(hand)
      choice = hand.getPlayerAction(self.playerSplitCounts[hand.player]) 
      while(choice != Actions.S):
        print(choice)
        if(choice == Actions.H):
          self.hit(hand)
        elif(choice == Actions.T): 
          self.playerSplitCounts[hand.player] += 1
          newHand = hand.splitHand()
          hands.insert(index+1, newHand)
        elif(choice == Actions.D):
          hand.doubleDown()
          self.hit(hand)
        else: #Actions.S
          #Choice will automatically be stand if Aces were split or hand is bust
          'No op' #intentionally empty
        print(self.dealerHand)
        print(hand)
        choice = hand.getPlayerAction(self.playerSplitCounts[hand.player]) 
        
        
  #A hand should be removed right when they bust... but python lists and for loops can be funky so just do it here
  def removeBustHands(self, hands: List[BlackjackHand]):
    for hand in hands[:]:
      if(hand.isBust()):
        hand.processLose()
        hands.remove(hand)
        
  def playDealerHand(self):
    while(self.dealerHand.getHandScore() < 17):
      self.hit(self.dealerHand)
      
  def calculateScoresAndPayout(self, hands: List[BlackjackHand]):
    
    if(self.dealerHand.isBust()):
      for hand in hands:
        hand.processWin()
    else:
      for hand in hands:
        if(hand.getHandScore() > self.dealerHand.getHandScore()):
          hand.processWin()
        elif(hand.getHandScore() == self.dealerHand.getHandScore()):
          hand.processPush()
        else: #hand.getHandScore() < self.dealerHand.getHandScore()
          hand.processLose()
          
  def printHands(self, hands: List[BlackjackHand]):
    print(self.dealerHand)
    for hand in hands:
      print(hand)
      
      
if(__name__ == "__main__"):
  table = BlackjackTable()
  player1 = Player("player 1", 100000)
  player2 = Player("player 2", 100000)
  for i in range(10):
    table.playRound([player1, player2])
  print(player1.printStats())
  print(player2.printStats())


