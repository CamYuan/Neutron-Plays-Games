import unittest
from games.Blackjack import BlackjackHand, BlackjackCard, Player
from unittest.mock import MagicMock
from games.Blackjack.enums import Rank, Suits


class BlackjackHandTest(unittest.TestCase):
  
  def setUp(self):
    self.jack = BlackjackCard(Rank.JACK, Suits.SPADES)
    self.ace = BlackjackCard(Rank.ACE, Suits.HEARTS)
    self.player = Player("Bob")
  
  def test_init(self):
    hand = BlackjackHand(self.player, bet=10)
    self.assertEqual(hand.player, self.player)
    self.assertEqual(hand.bet, 10)
    self.assertEqual(hand._cards, [])
    self.assertEqual(hand._BlackjackHand__softScore, 0)
    self.assertEqual(hand._BlackjackHand__hardScore, 0)
    self.assertFalse(hand._BlackjackHand__splitFromAces)
    
    hand = BlackjackHand(self.player, bet=10, splitAces=True)
    self.assertTrue(hand._BlackjackHand__splitFromAces)
  
  def test_repr(self):
    hand = BlackjackHand(self.player, bet=10)
    hand.addCard(self.ace)
    expected = self.player.name + ': ' + str(self.ace) 
    self.assertEqual(expected, str(hand))
  
  def test_addCard(self):
    hand = BlackjackHand(self.player, bet=10)
    hand._BlackjackHand__updateSoftScore = MagicMock()
    hand._BlackjackHand__updateHardScore = MagicMock()
    hand.addCard(self.ace)
    self.assertIn(self.ace, hand._cards)
    hand._BlackjackHand__updateSoftScore.assert_called_once_with(self.ace)
    hand._BlackjackHand__updateHardScore.assert_called_once_with(self.ace)    
    
    hand.addCard(self.ace)
    self.assertTrue(len(hand._cards) == 2)

  def test_updateSoftScore(self):
    hand = BlackjackHand(self.player, bet=10)
    hand._BlackjackHand__updateSoftScore(self.ace)
    self.assertEqual(hand._BlackjackHand__softScore, 11)
    hand._BlackjackHand__updateSoftScore(self.ace)
    self.assertEqual(hand._BlackjackHand__softScore, 12)

  def test_updateHardScore(self):
    hand = BlackjackHand(self.player, bet=10)
    hand._BlackjackHand__updateHardScore(self.ace)
    self.assertEqual(hand._BlackjackHand__hardScore, 1)
    
    hand._BlackjackHand__updateHardScore(self.ace)
    self.assertEqual(hand._BlackjackHand__hardScore, 2)
    
  def test_getHandScore(self):
    pass
  
  def test_hasBlackjack(self):
    pass
  
  
  def test_canDoubleDown(self):
    hand = BlackjackHand(self.player, bet=10)
    self.assertFalse(hand.canDoubleDown())
    
    hand.addCard(self.ace)
    self.assertFalse(hand.canDoubleDown())
    
    hand.addCard(self.ace)
    self.assertTrue(hand.canDoubleDown())
    
    hand.addCard(self.ace)
    self.assertFalse(hand.canDoubleDown())
    
    hand = BlackjackHand(self.player, bet=10, splitAces=True)
    hand.addCard(self.ace)
    hand.addCard(self.ace)
    self.assertFalse(hand.canDoubleDown())
    
  def test_doubleDown(self):
    hand = BlackjackHand(self.player, bet=10)
    hand.doubleDown()
    self.assertEqual(hand.bet, 20)
  
  def test_canSplit(self):
    hand = BlackjackHand(self.player, bet=10)
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
    hand = BlackjackHand(self.player, bet=10, splitAces=True)
    hand.addCard(self.ace)
    hand.addCard(self.ace)
    self.assertFalse(hand.canSplit())
    
  def test_splitHand(self):
    hand = BlackjackHand(self.player, bet=10)
    hand.addCard(self.ace)
    hand.addCard(self.ace)
    newHand = hand.splitHand()
    self.assertEqual(len(hand._cards), 1)
    self.assertEqual(newHand._cards[0], self.ace)
    self.assertTrue(hand._BlackjackHand__splitFromAces)
    self.assertTrue(newHand._BlackjackHand__splitFromAces)
    self.assertEqual(newHand.bet, hand.bet)
    
    hand = BlackjackHand(self.player, bet=10)
    hand.addCard(self.jack)
    hand.addCard(self.jack)
    hand.splitHand()
    self.assertFalse(hand._BlackjackHand__splitFromAces)
    
    
  def test_isBust(self):
    hand = BlackjackHand(self.player, bet=10)
    hand._BlackjackHand__hardScore = 21
    self.assertFalse(hand.isBust())
    hand._BlackjackHand__hardScore = 22
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
