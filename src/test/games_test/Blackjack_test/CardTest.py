import unittest
from games.Blackjack import Card
from games.Blackjack.enums import Suits, Rank


class CardTest(unittest.TestCase):
  
  def setUp(self):
    self.cards = []
    for rank in Rank:
      self.cards.append(Card(rank, None))

  def test_init(self):
    card = Card(Rank.ACE, Suits.HEARTS)
    self.assertEqual(card.rank, Rank.ACE)
    self.assertEqual(card.suit, Suits.HEARTS)
    
  def test_repr(self):
    card = Card(None, Suits.CLUBS)
    self.assertEqual(str(card), "Cut Card \u2612")
    
    card = Card(Rank.ACE, Suits.HEARTS)
    self.assertEqual(str(card), "A\u2665")

    card = Card(Rank.TEN, Suits.DIAMONDS)
    self.assertEqual(str(card), "10\u2666")

    card = Card(Rank.JACK, Suits.CLUBS)
    self.assertEqual(str(card), "J\u2663")

    card = Card(Rank.QUEEN, Suits.SPADES)
    self.assertEqual(str(card), "Q\u2660")

    card = Card(Rank.KING, Suits.SPADES)
    self.assertEqual(str(card), "K\u2660")

  def test_eq(self):
    c1 = Card(Rank.ACE, Suits.HEARTS)
    c2 = Card(Rank.ACE, Suits.HEARTS)
    self.assertEqual(c1, c2)
    
    c2 = Card(Rank.ACE, Suits.CLUBS)
    self.assertEqual(c1, c2)
    
    c1 = Card(Rank.TEN, Suits.CLUBS)
    c2 = Card(Rank.JACK, Suits.CLUBS)
    self.assertEqual(c1, c2)

    c2 = Card(Rank.EIGHT, Suits.HEARTS)
    self.assertNotEqual(c1, c2)
    
    c2 = "something"
    self.assertNotEqual(c1, c2)
    
  def test_value(self) -> None:
    for rank in Rank:
      card = Card(rank, None)
      self.assertEqual(card.value(), rank.value)
  
  def test_getSoftValue(self) -> None:
    for rank in Rank:
      card = Card(rank, None)
      if(rank == Rank.ACE):
        self.assertEqual(card.getSoftValue(), 11)
      elif(rank.value >= 10):  
        self.assertEqual(card.getSoftValue(), 10)
      else:
        self.assertEqual(card.getHardValue(), rank.value)
  
  def test_getHardValue(self) -> None:
    for rank in Rank:
      card = Card(rank, None)
      if(rank.value >= 10):
        self.assertEqual(card.getHardValue(), 10)
      else:
        self.assertEqual(card.getHardValue(), rank.value)



    
if __name__ == '__main__':
  unittest.main()
