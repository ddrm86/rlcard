from copy import deepcopy
from random import choice

from rlcard.core import Game
from rlcard.games.brisca.card import BriscaCard
from rlcard.games.brisca.dealer import BriscaDealer
from rlcard.games.brisca.player import BriscaPlayer


class BriscaGame(Game):

    def __init__(self, last_starting_player_id=None, allow_step_back=False):
        self.last_starting_player_id = last_starting_player_id
        self.allow_step_back = allow_step_back
        self.num_players = 2
        self.dealer = BriscaDealer()
        self.player1 = BriscaPlayer(0)
        self.player2 = BriscaPlayer(1)
        self.first_to_act = None
        self.second_to_act = None
        self.current_player = None
        self.history = []
        self.played_cards = []
        self.board = []
        self.round_number = 1

    def init_game(self):
        self.__init__(self.last_starting_player_id, self.allow_step_back)
        for _ in range(3):  # Three cards per player
            self.dealer.deal_cards(self.player1)
            self.dealer.deal_cards(self.player2)
        self.dealer.deal_trump_card()
        if self.last_starting_player_id is None:
            self.last_starting_player_id = choice([0, 1])
        if self.last_starting_player_id == 0:
            self.current_player = self.player2
            self.second_to_act = self.player1
        else:
            self.current_player = self.player1
            self.second_to_act = self.player2
        self.first_to_act = self.current_player
        state = self.get_state(self.get_player_id())
        return state, self.get_player_id()

    def save_current_state(self):
        d = deepcopy(self.dealer)
        p1 = deepcopy(self.player1)
        p2 = deepcopy(self.player2)
        b = deepcopy(self.board)
        pc = deepcopy(self.played_cards)
        rn = deepcopy(self.round_number)
        cp_id = self.current_player.player_id
        fta_id = self.first_to_act.player_id
        sta_id = self.second_to_act.player_id
        self.history.append((d, p1, p2, b, pc, rn, cp_id, fta_id, sta_id))

    def step(self, action):
        """ Perform one draw of the game and return next player number, and the state for next player
        """
        # TODO: player known cards: update when appropiate (substitution, use of substituted card, last rounds)
        if self.allow_step_back:
            self.save_current_state()

        if action == 'substitute':
            self.dealer.substitute_trump_card(self.current_player)
        else:
            card = BriscaCard.from_str_repr(action)
            self.current_player.hand.remove(card)
            self.board.append(card)
            self.played_cards.append(card)

        if self.is_round_over():
            round_winner = self.get_round_winner()
            round_loser = self.player1 if round_winner == self.player2 else self.player2
            round_winner.score += sum(card.value for card in self.board)
            if self.dealer.deck:
                self.dealer.deal_cards(round_winner)
                self.dealer.deal_cards(round_loser)
            self.first_to_act = round_winner
            self.current_player = round_winner
            self.second_to_act = round_loser
            self.board = []
            self.round_number += 1
        else:
            if action != 'substitute':
                self.current_player = self.second_to_act

        state = self.get_state(self.get_player_id())
        return state, self.get_player_id()

    def step_back(self):
        """ Return to the previous state of the game

        Returns:
            (bool): True if the game steps back successfully
        """
        if not self.history:
            return False
        self.dealer, self.player1, self.player2, self.board, self.played_cards, self.round_number,\
            cp_id, fta_id, sta_id = self.history.pop()
        self.current_player = self.player1 if cp_id == 0 else self.player2
        self.first_to_act = self.player1 if fta_id == 0 else self.player2
        self.second_to_act = self.player1 if sta_id == 0 else self.player2
        return True

    def get_player_num(self):
        """ Return the number of players in the game
        """
        return self.num_players

    def get_action_num(self):
        """ Return the number of possible actions in the game
        """
        return len(BriscaCard.valid_suit) * len(BriscaCard.valid_rank) + 1

    def get_player_id(self):
        return self.current_player.player_id

    def is_over(self):
        return not self.player1.hand and not self.player2.hand

    def get_state(self, player_id):
        player = self.player1 if player_id == 0 else self.player2
        state = {'id': player.player_id,
                 'act_first': self.first_to_act.player_id,
                 'score': player.score,
                 'hand': [str(card) for card in player.hand],
                 'trump_suit': self.dealer.trump_card.suit,
                 'trump_rank': self.dealer.trump_card.rank,
                 'played_cards': [str(card) for card in self.played_cards],
                 'board': [str(card) for card in self.board],
                 'round_number': self.round_number,
                 'actions': self.get_actions(player),
                 'known_cards': [str(card) for card in player.known_cards]}
        return state

    def get_actions(self, player):
        actions = [str(card) for card in player.hand]
        if self.player_can_substitute(player):
            actions.append('substitute')
        return actions

    def player_can_substitute(self, player):
        has_subs_card = self.dealer.get_substitute_trump_card() in player.hand
        won_last_round = player == self.first_to_act and self.round_number > 1
        not_last_round = bool(self.dealer.deck)
        return has_subs_card and won_last_round and not_last_round

    def is_round_over(self):
        return len(self.board) == self.num_players

    def get_round_winner(self):
        trump_suit = self.dealer.trump_card.suit
        card1, card2 = self.board
        if card1.suit == card2.suit:
            round_winner = self.first_to_act if card1 > card2 else self.second_to_act
        elif card1.suit == trump_suit:
            round_winner = self.first_to_act
        elif card2.suit == trump_suit:
            round_winner = self.second_to_act
        else:
            round_winner = self.first_to_act
        return round_winner
