import unittest

from rlcard.games.brisca.card import BriscaCard
from rlcard.games.brisca.dealer import BriscaDealer
from rlcard.games.brisca.player import BriscaPlayer


class TestBriscaDealer(unittest.TestCase):

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
        dealer.substitute_trump_card(player)
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
        self.assertRaises(ValueError, dealer.substitute_trump_card, player)


if __name__ == '__main__':
    unittest.main()
