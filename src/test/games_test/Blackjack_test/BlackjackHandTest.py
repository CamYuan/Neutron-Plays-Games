import unittest
from games.Blackjack import BlackjackHand, BlackjackCard
from unittest.mock import MagicMock


class BlackjackHandTest(unittest.TestCase):
  
  def setUp(self):
    test: BlackjackCard = MagicMock(spec=BlackjackCard)
    self.mockBlackjackCard = MagicMock(spec=BlackjackCard)
    self.mockBlackjackCard.getSoftValue.return_value = 11
    self.mockBlackjackCard.getHardValue.return_value = 1
    self.mockBlackjackCard.value.return_value = 1
  
  def test_init(self):
    hand = BlackjackHand(10)
    self.assertEqual(hand.bet, 10)
    self.assertEqual(hand.softScore, 0)
    self.assertEqual(hand.hardscore, 0)
    self.assertEqual(hand._cards, [])
    self.assertFalse(hand._splitFromAces)
    
    hand = BlackjackHand(10, True)
    self.assertTrue(hand._splitFromAces)
  
  def test_addCard(self):
    hand = BlackjackHand(10)
    hand.updateSoftScore = MagicMock()
    hand.updateHardScore = MagicMock()
    hand.addCard(self.mockBlackjackCard)
    self.assertIn(self.mockBlackjackCard, hand._cards)
    hand.updateSoftScore.assert_called_once_with(self.mockBlackjackCard)
    hand.updateHardScore.assert_called_once_with(self.mockBlackjackCard)    
    
    hand.addCard(self.mockBlackjackCard)
    self.assertTrue(len(hand._cards) == 2)

  def test_updateSoftScore(self):
    hand = BlackjackHand(10)
    hand.updateSoftScore(self.mockBlackjackCard)
    self.assertEqual(hand.softScore, 11)
    hand.updateSoftScore(self.mockBlackjackCard)
    self.assertEqual(hand.softScore, 12)

  def test_updateHardScore(self):
    hand = BlackjackHand(10)
    hand.updateHardScore(self.mockBlackjackCard)
    self.assertEqual(hand.hardscore, 1)
    
    hand.updateHardScore(self.mockBlackjackCard)
    self.assertEqual(hand.hardscore, 2)
    
  def test_canDoubleDown(self):
    hand = BlackjackHand(10)
    self.assertFalse(hand.canDoubleDown())
    
    hand.addCard(self.mockBlackjackCard)
    self.assertFalse(hand.canDoubleDown())
    
    hand.addCard(self.mockBlackjackCard)
    self.assertTrue(hand.canDoubleDown())
    
    hand.addCard(self.mockBlackjackCard)
    self.assertFalse(hand.canDoubleDown())
    
    hand = BlackjackHand(10, True)
    hand.addCard(self.mockBlackjackCard)
    hand.addCard(self.mockBlackjackCard)
    self.assertFalse(hand.canDoubleDown())
    
  def test_canSplit(self):
    hand = BlackjackHand(10)
    self.assertFalse(hand.canSplit())
    
    #One Card
    hand.addCard(self.mockBlackjackCard)
    self.assertFalse(hand.canSplit())
    
    #Two Cards
    self.mockBlackjackCard.__eq__.return_value = True
    hand.addCard(self.mockBlackjackCard)
    self.assertTrue(hand.canSplit())
    
    self.mockBlackjackCard.__eq__.return_value = False
    self.assertFalse(hand.canSplit())
    
    #More than two Cards
    hand.addCard(self.mockBlackjackCard)
    self.assertFalse(hand.canSplit())
    
    #Split from aces and two cards
    hand = BlackjackHand(10, True)
    hand.addCard(self.mockBlackjackCard)
    hand.addCard(self.mockBlackjackCard)
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
    secondCard = MagicMock(spec=BlackjackCard)
    secondCard.getSoftValue.return_value = 11
    secondCard.getHardValue.return_value = 1
    hand = BlackjackHand(10)
    hand.addCard(self.mockBlackjackCard)
    hand.addCard(secondCard)
    card = hand.splitHand()
    self.assertEqual(card, secondCard)
    self.assertEqual(len(hand._cards), 1)
    self.assertTrue(hand._splitFromAces)
    
    hand = BlackjackHand(10)
    hand.addCard(secondCard)
    hand.addCard(secondCard)
    hand.splitHand()
    self.assertFalse(hand._splitFromAces)
    
    