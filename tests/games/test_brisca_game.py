import unittest

from rlcard.games.brisca.card import BriscaCard


class TestBlackjackGame(unittest.TestCase):

    def test_card_value(self):
        bc = BriscaCard('O', 'A')
        self.assertEqual(bc.value, 11)
        bc = BriscaCard('E', '3')
        self.assertEqual(bc.value, 10)
        bc = BriscaCard('B', 'R')
        self.assertEqual(bc.value, 4)
        bc = BriscaCard('C', 'C')
        self.assertEqual(bc.value, 3)
        bc = BriscaCard('O', 'S')
        self.assertEqual(bc.value, 2)
        bc = BriscaCard('O', '6')
        self.assertEqual(bc.value, 0)

    def test_suit(self):
        bc = BriscaCard('O', 'A')
        self.assertEqual(bc.suit, 'O')

    def test_rank(self):
        bc = BriscaCard('O', 'A')
        self.assertEqual(bc.rank, 'A')

    def test_invalid_suit(self):
        self.assertRaises(ValueError, BriscaCard, 'S', '6')

    def test_invalid_rank(self):
        self.assertRaises(ValueError, BriscaCard, 'E', '9')

    def test_deck(self):
        deck = BriscaCard.init_brisca_deck()
        self.assertEqual(len(deck), 40)


if __name__ == '__main__':
    unittest.main()
