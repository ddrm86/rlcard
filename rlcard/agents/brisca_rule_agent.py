from rlcard.games.brisca.card import BriscaCard


class BriscaRuleAgent(object):
    """ A brisca ruled based agent.

    A set of heuristic rules that define a basic somewhat greedy strategy:
    - First to act:
        + Substitute if possible.
        + Draw card of the lowest rank. In a tie: avoid drawing card of the trump suit.
    - Second to act:
        + Draw card that earns the most points. In a tie: avoid drawing card of the trump suit.
    """

    def __init__(self, action_num):
        """ Initilize the agent

        Args:
            action_num (int): The size of the ouput action space
        """
        self.use_raw = True
        self.action_num = action_num

    @staticmethod
    def step(state):
        """ Predict the action given the curent state in gerenerating training data.

        Args:
            state (dict): An dictionary that represents the current state

        Returns:
            action (int): The action predicted (randomly chosen) by the random agent
        """
        raw_obs = state['raw_obs']
        raw_actions = state['raw_legal_actions']
        if raw_obs['id'] == raw_obs['act_first']:
            action = BriscaRuleAgent.act_first(raw_obs, raw_actions)
        else:
            action = BriscaRuleAgent.act_second(raw_obs, raw_actions)
        return action

    @staticmethod
    def act_first(obs, actions):
        if 'substitute' in actions:
            return 'substitute'
        trump_suit = obs['trump_suit']
        hand = sorted([BriscaCard.from_str_repr(card) for card in obs['hand']])
        min_card = hand[0]
        if min_card.suit == trump_suit:
            for card in hand[1:]:
                if card.value == min_card.value and card.suit != trump_suit:
                    min_card = card
        return str(min_card)

    @staticmethod
    def get_score(board_card, player_card, trump_suit):
        total_value = board_card.value + player_card.value
        if board_card.suit == player_card.suit:
            if board_card > player_card:
                score = -total_value
            else:
                score = total_value
        elif player_card.suit == trump_suit:
            score = total_value
        else:
            score = -total_value
        return score

    @staticmethod
    def act_second(obs, actions):
        trump_suit = obs['trump_suit']
        board_card = BriscaCard.from_str_repr(obs['board'][0])
        best_card = BriscaCard.from_str_repr(actions[0])
        best_value = BriscaRuleAgent.get_score(board_card, best_card, trump_suit)
        for card_str in actions[1:]:
            card = BriscaCard.from_str_repr(card_str)
            value = BriscaRuleAgent.get_score(board_card, card, trump_suit)
            if value > best_value:
                best_card = card
                best_value = value
        return str(best_card)

    def eval_step(self, state):
        """ Predict the action given the current state for evaluation.
            Since rule based agents are not trained. This function is equivalent to step function

        Args:
            state (dict): An dictionary that represents the current state

        Returns:
            action (int): The action predicted (randomly chosen) by the random agent
            probs (list): The list of action probabilities
        """
        return self.step(state), []
