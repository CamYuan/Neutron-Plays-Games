import math
import random
from typing import List
from games.Blackjack import Card, Hand, Player
from games.Blackjack.enums import Actions, Rank, Result, Suits

import logging
logger = logging.getLogger(__name__)

'''
TODO:
#Card Counting
RunningCount = 0
SuitCounts = [0,0,0,0]
'''
class Table:
  def __init__(self, num_decks=6):
    self.minBet = 10
    self.maxBet = 1000
    self.numDecks = num_decks
    self.dealer = Player("Dealer", 10000000000)
    
    self.shoe = self.loadShoe(num_decks)
    self.isShuffleTime = False
    self.dealerHand: Hand  = None
    self.playerSplitCounts = {}
    self.roundCounter = 0
  
  def loadShoe(self, numberOfDecks) -> List[Card]:
    shoe = []
    cutCard = Card(None,None)
    for deck in range(0,numberOfDecks):
        for suit in Suits:
            for rank in Rank:
                shoe.append(Card(rank,suit))
    random.shuffle(shoe) #shuffle
    #index between 70-90% of the BACK of the deck to insert the cutCard
    minIndex = math.floor(len(shoe)*.7)
    maxIndex = math.floor(len(shoe)*.9)
    shoe.insert(random.randint(minIndex,maxIndex), cutCard)
    return shoe


  def playRound(self, players):
    self.roundCounter += 1
    logger.info('\nRound ' + str(self.roundCounter))
    hands = self.initializeRound(players) #1
    self.deal(hands) #2
    self.checkBlackjacks(hands)
    self.playHands(hands)
    self.removeBustHands(hands)
    #Hands will get cleared when there is a blackjack or bust. 
    #If it's a dead hand, dealer doesn't take cards for no reason
    if(len(hands) > 0): 
      self.dealerHand.dealer = False #expose the dealer hand
      self.playDealerHand()
      self.calculateScoresAndPayout(hands)
    self.__reset()    
  
  def initializeRound(self, players: List[Player]) -> List[Hand]:
    hands = []
    for player in players:
      logger.info(player)
      bet = player.askForBet()
      hands.append(Hand(player, bet))
      self.playerSplitCounts[hash(player)] = 0
    hands.append(Hand(self.dealer, None, dealer=True)) #dealer hand goes last
    return hands
      
  def deal(self, hands: List[Hand]):
    for _ in range(2):
        for hand in hands:
            self.hit(hand)
    self.dealerHand = hands.pop()
  
  def hit(self, hand: Hand):
    card = self.shoe.pop()
    if(card.rank == None):
      logger.info("----------------------CUT CARD----------------------")
      self.isShuffleTime = True
      card = self.shoe.pop() #get the next card instead
    #TODO: card count here I think
    hand.addCard(card)
  
  def checkBlackjacks(self, hands: List[Hand]):
    dealerBlackjack = self.dealerHand.hasBlackjack()
    #Not offering insurance in this game
    #players will only have 1 hand each at this point
    if(dealerBlackjack):
      logger.info('Dealer Blackjack!')
      self.dealerHand.dealer = False
      logger.info(self.dealerHand)
      for hand in hands:
        if(hand.hasBlackjack()):
          hand.processPush()
        else:
          hand.processLose()
      hands.clear()
      self.__reset()   
    else:
      for hand in hands[:]:
        if(hand.hasBlackjack()):
          hand.processBlackjack()
          hands.remove(hand) 
          
  def __reset(self):
    self.dealerHand: Hand  = None
    self.playerSplitCounts = {}
    if(self.isShuffleTime):
      self.shoe = self.loadShoe(self.numDecks)
      self.isShuffleTime = False
    
    
  def playHands(self, hands: List[Hand]):
    for index, hand in enumerate(hands):
      logger.info('\n'+hand.player.name + '\'s turn')  
      #After a split, the second hand won't get a card until the first hand is done
      choice = ''
      while(choice != Actions.S):
        if len(hand._cards) < 2: 
          self.hit(hand)
        logger.info(self.dealerHand)
        logger.info(hand)
        actionOptions = hand.getActionOptions(self.playerSplitCounts[hash(hand.player)]) 
        if(len(actionOptions) == 1):
          choice = actionOptions[0] #forced stand
        else:
          choice = hand.player.getAction(actionOptions)
        logger.info(choice)
        if(choice == Actions.H):
          self.hit(hand)
        elif(choice == Actions.T): 
          self.playerSplitCounts[hash(hand.player)] += 1
          newHand = hand.splitHand()
          hands.insert(index+1, newHand)
        elif(choice == Actions.D):
          hand.doubleDown()
          self.hit(hand)
        else: #Actions.S
          #Choice will automatically be stand if Aces were split or hand is bust
          'No op' #intentionally empty
      logger.info(hand)

        
        
  #A hand should be removed right when they bust... but python lists and for loops can be funky so just do it here
  def removeBustHands(self, hands: List[Hand]):
    for hand in hands[:]:
      if(hand.isBust()):
        hands.remove(hand)
        hand.processBust()
        
  def playDealerHand(self):
    logger.info('\nDealer\'s turn')
    logger.info(self.dealerHand)
    while(self.dealerHand.getSoftScore() < 17):
      self.hit(self.dealerHand)
      logger.info(self.dealerHand)
      
      
  def calculateScoresAndPayout(self, hands: List[Hand]) -> Result:
    if(self.dealerHand.isBust()):
      logger.info('Dealer Bust!')
      for hand in hands:
        hand.processWin()
    else:
      for hand in hands:
        if(hand.getSoftScore() > self.dealerHand.getSoftScore()):
          hand.processWin()
        elif(hand.getSoftScore() == self.dealerHand.getSoftScore()):
          hand.processPush()
        else: #hand.getSoftScore() < self.dealerHand.getSoftScore()
          hand.processLose()
          
  def printHands(self, hands: List[Hand]):
    logger.info(self.dealerHand)
    for hand in hands:
      logger.info(hand)
  
  def getDealerUpCard(self):
    return self.dealerHand._cards[1]
      
      
if(__name__ == "__main__"):
  logging.basicConfig(level=logging.INFO,  format='%(message)s')
  logger = logging.getLogger(__name__)
  table = Table()
  player1 = Player("player 1", bankroll=100000, autobet=True)
  table.shoe.clear()
  table.shoe.append(Card(Rank.SIX, Suits.HEARTS))
  table.shoe.append(Card(Rank.SIX, Suits.HEARTS))
  table.shoe.append(Card(Rank.SIX, Suits.HEARTS))
  table.shoe.append(Card(Rank.SIX, Suits.HEARTS))
  table.shoe.append(Card(Rank.SIX, Suits.HEARTS))
  table.shoe.append(Card(Rank.SIX, Suits.HEARTS))
  table.shoe.append(Card(Rank.SIX, Suits.HEARTS))
  
  table.shoe.append(Card(Rank.TEN, Suits.HEARTS))
  table.shoe.append(Card(Rank.FIVE, Suits.HEARTS))
  
  table.shoe.append(Card(Rank.TEN, Suits.HEARTS))
  table.shoe.append(Card(Rank.FIVE, Suits.HEARTS))
  table.shoe.append(Card(Rank.EIGHT, Suits.HEARTS))
  table.shoe.append(Card(Rank.ACE, Suits.HEARTS))
  table.shoe.append(Card(Rank.EIGHT, Suits.HEARTS))
  table.shoe.append(Card(Rank.ACE, Suits.HEARTS))
  for i in range(5):
    table.playRound([player1])
  logger.info(player1.printStats())


