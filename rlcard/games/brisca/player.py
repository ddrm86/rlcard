from rlcard.core import Player


class BriscaPlayer(Player):
    def __init__(self, player_id):
        self.player_id = player_id
        self.hand = []
        self.score = 0
        self.known_cards = []

    def __eq__(self, other):
        if isinstance(other, BriscaPlayer):
            return self.player_id == other.player_id
        else:
            return NotImplemented

    def __hash__(self):
        return self.player_id * 43

    def available_order(self):
        raise NotImplementedError

    def play(self):
        raise NotImplementedError
