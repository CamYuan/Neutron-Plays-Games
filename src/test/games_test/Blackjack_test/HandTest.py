import unittest
from games.Blackjack import Hand, Card, Player
from unittest.mock import MagicMock
from games.Blackjack.enums import Rank, Suits


class HandTest(unittest.TestCase):
  
  def setUp(self):
    self.jack = Card(Rank.JACK, Suits.SPADES)
    self.ace = Card(Rank.ACE, Suits.HEARTS)
    self.player = Player("Bob")
  
  def test_init(self):
    hand = Hand(self.player, bet=10)
    self.assertEqual(hand.player, self.player)
    self.assertEqual(hand.bet, 10)
    self.assertEqual(hand._cards, [])
    self.assertEqual(hand._Hand__softScore, 0)
    self.assertEqual(hand._Hand__hardScore, 0)
    self.assertFalse(hand._Hand__splitFromAces)
    
    hand = Hand(self.player, bet=10, splitAces=True)
    self.assertTrue(hand._Hand__splitFromAces)
  
  def test_repr(self):
    hand = Hand(self.player, bet=10)
    hand.addCard(self.ace)
    expected = self.player.name + ': ' + str(self.ace) 
    self.assertEqual(expected, str(hand))
  
  def test_addCard(self):
    hand = Hand(self.player, bet=10)
    hand._Hand__updateSoftScore = MagicMock()
    hand._Hand__updateHardScore = MagicMock()
    hand.addCard(self.ace)
    self.assertIn(self.ace, hand._cards)
    hand._Hand__updateSoftScore.assert_called_once_with(self.ace)
    hand._Hand__updateHardScore.assert_called_once_with(self.ace)    
    
    hand.addCard(self.ace)
    self.assertTrue(len(hand._cards) == 2)

  def test_updateSoftScore(self):
    hand = Hand(self.player, bet=10)
    hand._Hand__updateSoftScore(self.ace)
    self.assertEqual(hand._Hand__softScore, 11)
    hand._Hand__updateSoftScore(self.ace)
    self.assertEqual(hand._Hand__softScore, 12)

  def test_updateHardScore(self):
    hand = Hand(self.player, bet=10)
    hand._Hand__updateHardScore(self.ace)
    self.assertEqual(hand._Hand__hardScore, 1)
    
    hand._Hand__updateHardScore(self.ace)
    self.assertEqual(hand._Hand__hardScore, 2)
    
  def test_getSoftScore(self):
    hand = Hand(self.player, bet=10)
    hand._Hand__softScore = 21
    hand._Hand__hardScore = 10
    self.assertEqual(hand.getSoftScore(), 21)
    
    #soft bust returns hard score
    hand._Hand__softScore = 22
    self.assertEqual(hand.getSoftScore(), 10)
    
  def test_getHardScore(self):
    hand = Hand(self.player, bet=10)
    hand._Hand__hardScore = 10
    self.assertEqual(hand.getHardScore(), 10)
    
    
  def test_hasBlackjack(self):
    hand = Hand(self.player, bet=10)
    hand._Hand__softScore = 21
    self.assertTrue(hand.hasBlackjack())
    hand._Hand__softScore = 22
    self.assertFalse(hand.hasBlackjack())
  
  
  def test_canDoubleDown(self):
    hand = Hand(self.player, bet=10)
    self.assertFalse(hand.canDoubleDown())
    
    hand.addCard(self.ace)
    self.assertFalse(hand.canDoubleDown())
    
    hand.addCard(self.ace)
    self.assertTrue(hand.canDoubleDown())
    
    hand.addCard(self.ace)
    self.assertFalse(hand.canDoubleDown())
    
    hand = Hand(self.player, bet=10, splitAces=True)
    hand.addCard(self.ace)
    hand.addCard(self.ace)
    self.assertFalse(hand.canDoubleDown())
    
  def test_doubleDown(self):
    hand = Hand(self.player, bet=10)
    hand.doubleDown()
    self.assertEqual(hand.bet, 20)
  
  def test_canSplit(self):
    hand = Hand(self.player, bet=10)
    self.assertFalse(hand.canSplit())
    
    #One Card
    hand.addCard(self.ace)
    self.assertFalse(hand.canSplit())
    
    #Two Cards
    hand.addCard(self.ace)
    self.assertTrue(hand.canSplit())
    
    hand._cards.pop()
    hand.addCard(self.jack)
    self.assertFalse(hand.canSplit())
    
    #More than two Cards
    hand.addCard(self.ace)
    self.assertFalse(hand.canSplit())
    
    #Split from aces and two cards
    hand = Hand(self.player, bet=10, splitAces=True)
    hand.addCard(self.ace)
    hand.addCard(self.ace)
    self.assertFalse(hand.canSplit())
    
  def test_splitHand(self):
    hand = Hand(self.player, bet=10)
    hand.addCard(self.ace)
    hand.addCard(self.ace)
    newHand = hand.splitHand()
    self.assertEqual(len(hand._cards), 1)
    self.assertEqual(newHand._cards[0], self.ace)
    self.assertTrue(hand._Hand__splitFromAces)
    self.assertTrue(newHand._Hand__splitFromAces)
    self.assertEqual(newHand.bet, hand.bet)
    
    hand = Hand(self.player, bet=10)
    hand.addCard(self.jack)
    hand.addCard(self.jack)
    hand.splitHand()
    self.assertFalse(hand._Hand__splitFromAces)
    
    
  def test_isBust(self):
    hand = Hand(self.player, bet=10)
    hand._Hand__hardScore = 21
    self.assertFalse(hand.isBust())
    hand._Hand__hardScore = 22
    self.assertTrue(hand.isBust())
    
  def test_getPlayerAction(self):
    pass
  def test_getActionOptions(self):
    pass
    
  def test_processBlackjack(self):
    pass
    
  def test_processWin(self):
    pass
    
  def test_processLose(self):
    pass
  
  def test_processPush(self):
    pass
    
if __name__ == '__main__':
  unittest.main()
