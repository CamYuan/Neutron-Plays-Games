import unittest
from games.Blackjack import BlackjackHand, BlackjackCard
from unittest.mock import MagicMock
from games.Blackjack.enums import Rank, Suits


class BlackjackHandTest(unittest.TestCase):
  
  def setUp(self):
    self.ace = BlackjackCard(Rank.ACE, Suits.HEARTS)
    self.jack = BlackjackCard(Rank.JACK, Suits.SPADES)
  
  def test_init(self):
    hand = BlackjackHand(10)
    self.assertEqual(hand.bet, 10)
    self.assertEqual(hand.softScore, 0)
    self.assertEqual(hand.hardscore, 0)
    self.assertEqual(hand._cards, [])
    self.assertFalse(hand._splitFromAces)
    
    hand = BlackjackHand(10, True)
    self.assertTrue(hand._splitFromAces)
  
  def test_repr(self):
    hand = BlackjackHand(10)
    hand.addCard(self.ace)
    self.assertEqual(str(hand), str(self.ace))
  
  def test_addCard(self):
    hand = BlackjackHand(10)
    hand.updateSoftScore = MagicMock()
    hand.updateHardScore = MagicMock()
    hand.addCard(self.ace)
    self.assertIn(self.ace, hand._cards)
    hand.updateSoftScore.assert_called_once_with(self.ace)
    hand.updateHardScore.assert_called_once_with(self.ace)    
    
    hand.addCard(self.ace)
    self.assertTrue(len(hand._cards) == 2)

  def test_updateSoftScore(self):
    hand = BlackjackHand(10)
    hand.updateSoftScore(self.ace)
    self.assertEqual(hand.softScore, 11)
    hand.updateSoftScore(self.ace)
    self.assertEqual(hand.softScore, 12)

  def test_updateHardScore(self):
    hand = BlackjackHand(10)
    hand.updateHardScore(self.ace)
    self.assertEqual(hand.hardscore, 1)
    
    hand.updateHardScore(self.ace)
    self.assertEqual(hand.hardscore, 2)
    
  def test_canDoubleDown(self):
    hand = BlackjackHand(10)
    self.assertFalse(hand.canDoubleDown())
    
    hand.addCard(self.ace)
    self.assertFalse(hand.canDoubleDown())
    
    hand.addCard(self.ace)
    self.assertTrue(hand.canDoubleDown())
    
    hand.addCard(self.ace)
    self.assertFalse(hand.canDoubleDown())
    
    hand = BlackjackHand(10, True)
    hand.addCard(self.ace)
    hand.addCard(self.ace)
    self.assertFalse(hand.canDoubleDown())
    
  def test_canSplit(self):
    hand = BlackjackHand(10)
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
    hand = BlackjackHand(10, True)
    hand.addCard(self.ace)
    hand.addCard(self.ace)
    self.assertFalse(hand.canSplit())
  def test_isBust(self):
    hand = BlackjackHand(10)
    hand.hardscore = 21
    self.assertFalse(hand.isBust())
    hand.hardscore = 22
    self.assertTrue(hand.isBust())
    
  def test_doubleDown(self):
    hand = BlackjackHand(10)
    hand.doubleDown()
    self.assertEqual(hand.bet, 20)
    
  def test_splitHand(self):
    hand = BlackjackHand(10)
    hand.addCard(self.ace)
    hand.addCard(self.ace)
    newHand = hand.splitHand()
    self.assertEqual(len(hand._cards), 1)
    self.assertEqual(newHand._cards[0], self.ace)
    self.assertTrue(hand._splitFromAces)
    self.assertTrue(newHand._splitFromAces)
    self.assertEqual(newHand.bet, hand.bet)
    
    hand = BlackjackHand(10)
    hand.addCard(self.jack)
    hand.addCard(self.jack)
    hand.splitHand()
    self.assertFalse(hand._splitFromAces)
    
    