import unittest

from rlcard.games.brisca.card import BriscaCard

class TestBriscaCard(unittest.TestCase):

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

    def test_equal(self):
        self.assertEqual(BriscaCard('C', '7'), BriscaCard('C', '7'))

    def test_not_equal_rank(self):
        self.assertNotEqual(BriscaCard('C', '7'), BriscaCard('C', '2'))

    def test_not_equal_suit(self):
        self.assertNotEqual(BriscaCard('C', '7'), BriscaCard('E', '7'))

    def test_greater(self):
        self.assertGreater(BriscaCard('C', 'A'), BriscaCard('E', '3'))
        self.assertGreater(BriscaCard('C', 'A'), BriscaCard('C', 'R'))
        self.assertGreater(BriscaCard('C', '4'), BriscaCard('O', '2'))
        self.assertGreater(BriscaCard('C', 'C'), BriscaCard('C', 'S'))

    def test_not_greater(self):
        self.assertLessEqual(BriscaCard('C', 'R'), BriscaCard('E', '3'))
        self.assertLessEqual(BriscaCard('O', 'A'), BriscaCard('C', 'A'))
        self.assertLessEqual(BriscaCard('C', '4'), BriscaCard('O', '6'))
        self.assertLessEqual(BriscaCard('C', 'C'), BriscaCard('C', 'R'))

    def test_equal_hash(self):
        self.assertEqual(BriscaCard('C', 'R').__hash__(), BriscaCard('C', 'R').__hash__())

    def test_not_equal_hash(self):
        self.assertNotEqual(BriscaCard('C', 'R').__hash__(), BriscaCard('O', 'R').__hash__())
        self.assertNotEqual(BriscaCard('C', 'R').__hash__(), BriscaCard('C', 'A').__hash__())

    def test_deck(self):
        deck = BriscaCard.init_brisca_deck()
        self.assertEqual(len(deck), 40)

    def test_str_repr(self):
        card = BriscaCard('O', '3')
        str_repr = '3O'
        self.assertEqual(str(card), str_repr)
        self.assertEqual(card.__repr__(), str_repr)
        self.assertEqual(card, BriscaCard.from_str_repr(str_repr))

    def test_id(self):
        card = BriscaCard('O', '2')
        self.assertEqual(card.get_id(), 10)
        card = BriscaCard('B', 'A')
        self.assertEqual(card.get_id(), 9)
        card = BriscaCard('E', 'A')
        self.assertEqual(card.get_id(), 39)

    def test_repr_from_id(self):
        self.assertEqual(BriscaCard.get_repr_from_id(10), '2O')
        self.assertEqual(BriscaCard.get_repr_from_id(9), 'AB')
        self.assertEqual(BriscaCard.get_repr_from_id(39), 'AE')


if __name__ == '__main__':
    unittest.main()
