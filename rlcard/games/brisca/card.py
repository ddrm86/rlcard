from functools import total_ordering

from rlcard.core import Card


class SpanishCard(Card):
    """
    Single card of a standard Spanish deck of 40 cards ( https://en.wikipedia.org/wiki/Spanish_playing_cards )

    """
    valid_suit = ['B', 'O', 'C', 'E']
    valid_rank = ['A', '2', '3', '4', '5', '6', '7', 'S', 'C', 'R']

    def __init__(self, suit, rank):
        """ Initialize the suit and rank of a card

        Args:
            suit: string, suit of the card, should be one of valid_suit
            rank: string, rank of the card, should be one of valid_rank
        """
        if suit not in SpanishCard.valid_suit:
            raise ValueError('Invalid suit')
        if rank not in SpanishCard.valid_rank:
            raise ValueError('Invalid rank')
        super().__init__(suit, rank)

    def __repr__(self):
        return self.__str__()


@total_ordering
class BriscaCard(SpanishCard):
    """
    Single card for the game of Brisca ( https://www.nhfournier.es/en/como-jugar/brisca/ )

    """
    # Ordered from lesser to greater for convenience
    valid_rank = ['2', '4', '5', '6', '7', 'S', 'C', 'R', '3', 'A']
    value = None

    def __init__(self, suit, rank):
        """ Initialize the suit, rank and value of a card

        Args:
            suit: string, suit of the card, should be one of valid_suit
            rank: string, rank of the card, should be one of valid_rank
        """
        super().__init__(suit, rank)
        if rank == 'A':
            self.value = 11
        elif rank == '3':
            self.value = 10
        elif rank == 'R':
            self.value = 4
        elif rank == 'C':
            self.value = 3
        elif rank == 'S':
            self.value = 2
        else:
            self.value = 0

    @staticmethod
    def from_str_repr(str_repr):
        """ Initialize the suit and rank of a card

        Args:
            str_repr: string representation of a card (two characters: rank + suit)
        """
        rank, suit = str_repr
        return BriscaCard(suit, rank)

    def __eq__(self, other):
        if not isinstance(other, BriscaCard):
            return False
        return self.rank == other.rank and self.suit == other.suit

    def __gt__(self, other):
        if not isinstance(other, BriscaCard):
            return False
        return BriscaCard.valid_rank.index(self.rank) > BriscaCard.valid_rank.index(other.rank)

    def __hash__(self):
        suit_index = BriscaCard.valid_suit.index(self.suit)
        rank_index = BriscaCard.valid_rank.index(self.rank)
        return rank_index + 43 * suit_index

    def get_id(self):
        num_cards_in_suit = len(self.valid_rank)
        suit_id = self.valid_suit.index(self.suit)
        rank_id = self.valid_rank.index(self.rank)
        card_id = suit_id * num_cards_in_suit + rank_id
        return card_id

    @staticmethod
    def get_repr_from_id(card_id):
        num_cards_in_suit = len(BriscaCard.valid_rank)
        suit_index = card_id // num_cards_in_suit
        rank_index = card_id % num_cards_in_suit
        card_repr = BriscaCard.valid_rank[rank_index] + BriscaCard.valid_suit[suit_index]
        return card_repr

    @staticmethod
    def init_brisca_deck():
        """ Initialize a deck for the game of Brisca

        Returns:
            (list): A list of BriscaCard object
        """
        deck = [BriscaCard(suit, rank) for suit in SpanishCard.valid_suit for rank in SpanishCard.valid_rank]
        return deck
