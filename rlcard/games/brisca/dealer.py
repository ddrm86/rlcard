from rlcard.core import Dealer
import random

from rlcard.games.brisca.card import BriscaCard


class BriscaDealer(Dealer):
    """ The trump card defines the trump suit. It is dealt after all players, shown publicly, and goes to the end
    of the deck. It is dealt to the player that plays last in the last trick of the game. Can be substituted by the
    player that won the previous trick for the seven of the trump suit or the deuce if the trump card is <= 7.
    """
    trump_card: BriscaCard = None

    def __init__(self):
        """ Initialize a Brisca dealer class
        """
        self.deck = BriscaCard.init_brisca_deck()
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_cards(self, player):
        card = self.deck.pop(0)
        player.hand.append(card)

    def deal_trump_card(self):
        self.trump_card = self.deck.pop(0)
        self.deck.append(self.trump_card)

    def get_substitute_trump_card(self):
        tcard_suit = self.trump_card.suit
        trump_card_seven = BriscaCard(tcard_suit, '7')
        trump_card_deuce = BriscaCard(tcard_suit, '2')
        correct_trump_card = trump_card_seven if self.trump_card > trump_card_seven else trump_card_deuce
        return correct_trump_card

    def substitute_trump_card(self, player, new_trump_card):
        correct_trump_card = self.get_substitute_trump_card()
        if new_trump_card != correct_trump_card:
            raise ValueError('Incorrect trump card')
        player.hand.remove(new_trump_card)
        player.hand.append(self.trump_card)
        self.trump_card = new_trump_card
        self.deck.pop()
        self.deck.append(new_trump_card)
