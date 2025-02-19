from typing import List
from games.Blackjack import BlackjackCard, BlackjackHand, Player
from HelperFunctions import *
from games.Blackjack.old_GameState import *
import numpy as np
import pickle
import sys, os, io

from games.Blackjack.enums import Actions, Result

class BlackjackTable:
  def __init__(self, num_decks=6):
    self.minBet = 10
    self.maxBet = 1000
    self.numDecks = num_decks
    self.dealer = Player("dealer", 10000000000)
    
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
      self.playDealerHand()
      self.calculateScoresAndPayout(hands)
    self.reset()


    
  
  def initializeRound(self, players: List[Player]) -> List[BlackjackHand]:
    hands = []
    for player in players:
      bet = player.askForBet()
      hands.append(BlackjackHand(player, bet))
      self.playerSplitCounts[player] = 0
    return hands
      
  def deal(self, hands: List[BlackjackHand]):
    hands.append(BlackjackHand(self.dealer, None)) #dealer hand goes last
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
      
      
if(__name__ == "__main__"):
  table = BlackjackTable()
  player1 = Player("p1", 100000)
  player2 = Player("2", 100000)
  table.playRound([player1, player2])
  print(player1.printStats())
  print(player2.printStats())


