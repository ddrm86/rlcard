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
        self.state_shape = [5, 40]

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
        hand = list(state['hand'])
        for i in range(3-len(hand)):
            hand.append(None)
        encoded_hand = [self._encode_card(BriscaCard.from_str_repr(card))
                        if card is not None else self._encode_card(None) for card in hand]
        board = state['board']
        if len(board) == 0:
            encoded_board = self._encode_card(None)
        else:
            encoded_board = self._encode_card(BriscaCard.from_str_repr(board[0]))
        encoded_trump_card = self._encode_card(BriscaCard(state['trump_suit'], state['trump_rank']))
        encoded_tuple = tuple(encoded_hand) + (encoded_board,) + (encoded_trump_card,)
        obs = np.vstack(encoded_tuple)
        legal_actions = self._get_legal_actions()
        extracted_state = {'obs': obs, 'legal_actions': legal_actions}
        return extracted_state

    def _encode_card(self, card: BriscaCard or None):
        num_cards = self.game.get_action_num() - 1  # discard substitute action
        one_hot = np.zeros(num_cards, dtype=int)
        if card is not None:
            card_id = card.get_id()
            one_hot[card_id] = 1
        return one_hot

    def _decode_action(self, action_id):
        if action_id == self.enc_subs_action:
            return self.raw_subs_action
        else:
            return BriscaCard.get_repr_from_id(action_id)

    def get_payoffs(self):
        player1_score = self.game.player1.score
        player2_score = self.game.player2.score
        return np.array([player1_score, player2_score])

    def get_perfect_information(self):
        raise NotImplementedError

    def _load_model(self):
        raise NotImplementedError
