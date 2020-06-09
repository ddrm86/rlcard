import numpy as np
from rlcard.envs import Env
from rlcard.games.brisca import Game
from rlcard.games.brisca.card import BriscaCard

class BriscaEnv(Env):
    """ Brisca Environment
    """

    raw_subs_action = 'substitute'
    enc_subs_action = 40

    def __init__(self, config):
        """ Initialize the Brisca environment
        """
        self.game = Game()
        super().__init__(config)
        self.state_shape = [2]

    def _get_legal_actions(self):
        raw_actions = self.game.get_actions(self.game.current_player)
        encoded_actions = []
        for action in raw_actions:
            if action == self.raw_subs_action:
                encoded_actions.append(self.enc_subs_action)
            else:
                card = BriscaCard.from_str_repr(action)
                encoded_actions.append(card.get_id())
        return encoded_actions

    def _extract_state(self, state):
        legal_actions = self._get_legal_actions()
        extracted_state = {'obs': [], 'legal_actions': legal_actions}
        return extracted_state

    def _decode_action(self, action_id):
        if action_id == self.enc_subs_action:
            return self.raw_subs_action
        else:
            return BriscaCard.get_repr_from_id(action_id)

    def get_payoffs(self):
        player1_score = self.game.player1.score
        player2_score = self.game.player2.score
        if player1_score > player2_score:
            return np.array([1, -1])
        elif player1_score == player2_score:
            return np.array([0, 0])
        else:
            return np.array([-1, 1])

    def get_perfect_information(self):
        raise NotImplementedError

    def _load_model(self):
        raise NotImplementedError
