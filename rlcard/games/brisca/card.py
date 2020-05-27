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


class BriscaCard(SpanishCard):
    """
    Single card for the game of Brisca ( https://www.nhfournier.es/en/como-jugar/brisca/ )

    """
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
    def init_brisca_deck():
        """ Initialize a deck for the game of Brisca

        Returns:
            (list): A list of BriscaCard object
        """
        deck = [BriscaCard(suit, rank) for suit in SpanishCard.valid_suit for rank in SpanishCard.valid_rank]
        return deck
