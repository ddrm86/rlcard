import unittest

from rlcard.games.brisca.card import BriscaCard
from rlcard.games.brisca.dealer import BriscaDealer
from rlcard.games.brisca.player import BriscaPlayer


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

    def test_deal_card(self):
        dealer = BriscaDealer()
        first_card = dealer.deck[0]
        player = BriscaPlayer(0)
        dealer.deal_cards(player)
        self.assertEqual(first_card, player.hand[0])
        self.assertEqual(len(dealer.deck), 39)

    def test_deal_trump(self):
        dealer = BriscaDealer()
        first_card = dealer.deck[0]
        dealer.deal_trump_card()
        self.assertEqual(len(dealer.deck), 40)
        self.assertEqual(first_card, dealer.trump_card)
        self.assertEqual(first_card, dealer.deck[-1])

    def test_deal_get_subs_trump(self):
        trump_card = BriscaCard('C', 'R')
        dealer = BriscaDealer()
        dealer.trump_card = trump_card
        subs_trump = dealer.get_substitute_trump_card()
        self.assertEqual(subs_trump, BriscaCard('C', '7'))

    def test_deal_get_subs_trump2(self):
        trump_card = BriscaCard('E', '7')
        dealer = BriscaDealer()
        dealer.trump_card = trump_card
        subs_trump = dealer.get_substitute_trump_card()
        self.assertEqual(subs_trump, BriscaCard('E', '2'))

    def test_deal_subs_trump(self):
        trump_card = BriscaCard('C', 'R')
        subs_card = BriscaCard('C', '7')
        dealer = BriscaDealer()
        dealer.deck[0] = trump_card
        dealer.deal_trump_card()
        player = BriscaPlayer(0)
        player.hand.append(subs_card)
        dealer.substitute_trump_card(player, subs_card)
        self.assertTrue(subs_card not in player.hand)
        self.assertTrue(trump_card in player.hand)
        self.assertEqual(len(dealer.deck), 40)
        self.assertEqual(subs_card, dealer.trump_card)
        self.assertEqual(subs_card, dealer.deck[-1])

    def test_deal_subs_trump2(self):
        trump_card = BriscaCard('C', 'R')
        subs_card = BriscaCard('B', '7')
        dealer = BriscaDealer()
        dealer.deck[0] = trump_card
        dealer.deal_trump_card()
        player = BriscaPlayer(0)
        player.hand.append(subs_card)
        self.assertRaises(ValueError, dealer.substitute_trump_card, player, subs_card)


if __name__ == '__main__':
    unittest.main()
