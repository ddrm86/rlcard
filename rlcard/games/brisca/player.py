from rlcard.core import Player


class BriscaPlayer(Player):
    def __init__(self, player_id):
        super().__init__(player_id)
        self.score = 0

    def available_order(self):
        raise NotImplementedError

    def play(self):
        raise NotImplementedError
