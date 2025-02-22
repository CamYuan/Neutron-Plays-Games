import unittest
from games.Blackjack import BlackjackCard
from games.Blackjack.enums import Suits, Rank


class BlackjackCardTest(unittest.TestCase):
  
  def setUp(self):
    self.cards = []
    for rank in Rank:
      self.cards.append(BlackjackCard(rank, None))

  def test_init(self):
    card = BlackjackCard(Rank.ACE, Suits.HEARTS)
    self.assertEqual(card.rank, Rank.ACE)
    self.assertEqual(card.suit, Suits.HEARTS)

  def test_value(self) -> None:
    for rank in Rank:
      card = BlackjackCard(rank, None)
      self.assertEqual(card.value(), rank.value)
  
  def test_getHardValue(self) -> None:
    for rank in Rank:
      card = BlackjackCard(rank, None)
      if(rank.value >= 10):
        self.assertEqual(card.getHardValue(), 10)
      else:
        self.assertEqual(card.getHardValue(), rank.value)
  
  def test_getSoftValue(self) -> None:
    for rank in Rank:
      card = BlackjackCard(rank, None)
      if(rank == Rank.ACE):
        self.assertEqual(card.getSoftValue(), 11)
      elif(rank.value >= 10):  
        self.assertEqual(card.getSoftValue(), 10)
      else:
        self.assertEqual(card.getHardValue(), rank.value)


  def test_str(self):
    card = BlackjackCard(None, Suits.CLUBS)
    self.assertEqual(str(card), "Cut Card \u2612")
    
    card = BlackjackCard(Rank.ACE, Suits.HEARTS)
    self.assertEqual(str(card), "A\u2665")

    card = BlackjackCard(Rank.TEN, Suits.DIAMONDS)
    self.assertEqual(str(card), "10\u2666")

    card = BlackjackCard(Rank.JACK, Suits.CLUBS)
    self.assertEqual(str(card), "J\u2663")

    card = BlackjackCard(Rank.QUEEN, Suits.SPADES)
    self.assertEqual(str(card), "Q\u2660")

    card = BlackjackCard(Rank.KING, Suits.SPADES)
    self.assertEqual(str(card), "K\u2660")

  def test_eq(self):
    c1 = BlackjackCard(Rank.ACE, Suits.HEARTS)
    c2 = BlackjackCard(Rank.ACE, Suits.HEARTS)
    self.assertEqual(c1, c2)
    
    c2 = BlackjackCard(Rank.ACE, Suits.CLUBS)
    self.assertEqual(c1, c2)
    
    c1 = BlackjackCard(Rank.TEN, Suits.CLUBS)
    c2 = BlackjackCard(Rank.JACK, Suits.CLUBS)
    self.assertEqual(c1, c2)

    c2 = BlackjackCard(Rank.EIGHT, Suits.HEARTS)
    self.assertNotEqual(c1, c2)
    
    c2 = "something"
    self.assertNotEqual(c1, c2)
    
    
    
if __name__ == '__main__':
  unittest.main()
