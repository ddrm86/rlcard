import unittest

from rlcard.games.brisca.player import BriscaPlayer


class TestBriscaPlayer(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(BriscaPlayer(0), BriscaPlayer(0))

    def test_not_eq(self):
        self.assertNotEqual(BriscaPlayer(0), BriscaPlayer(1))

    def test_same_hash(self):
        self.assertEqual(BriscaPlayer(0).__hash__(), BriscaPlayer(0).__hash__())

    def test_dif_hash(self):
        self.assertNotEqual(BriscaPlayer(0).__hash__(), BriscaPlayer(1).__hash__())

    def test_no_data_sharing(self):
        p1 = BriscaPlayer(0)
        p2 = BriscaPlayer(1)
        self.assertNotEqual(p1.player_id, p2.player_id)
        p1.hand.append('whatever')
        self.assertNotEqual(p1.hand, p2.hand)
        p1.known_cards.append('whatever')
        self.assertNotEqual(p1.known_cards, p2.known_cards)
        p1.score = 42
        self.assertNotEqual(p1.score, p2.score)


if __name__ == '__main__':
    unittest.main()
