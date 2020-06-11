import unittest

from rlcard.games.brisca.card import BriscaCard
from rlcard.games.brisca.game import BriscaGame


class TestBriscaGame(unittest.TestCase):
    def test_init_game(self):
        game = BriscaGame(last_starting_player_id=1)
        state, p_id = game.init_game()
        self.assertEqual(game.current_player.player_id, 0)
        self.assertEqual(game.first_to_act.player_id, 0)
        self.assertEqual(game.second_to_act.player_id, 1)
        self.assertEqual(game.num_players, 2)
        self.assertEqual(game.board, [])
        self.assertEqual(game.played_cards, [])
        self.assertEqual(len(game.player1.hand), 3)
        self.assertEqual(len(game.player2.hand), 3)
        self.assertFalse(set(game.player1.hand) & set(game.player2.hand))
        self.assertNotEqual(game.dealer.trump_card, None)
        self.assertEqual(game.round_number, 1)
        self.assertEqual(p_id, game.first_to_act.player_id)
        self.assertEqual(p_id, game.current_player.player_id)
        self.assertEqual(state['id'], p_id)

    def test_step_substitute(self):
        game = BriscaGame(last_starting_player_id=0)
        game.init_game()
        trump_card = BriscaCard('C', 'R')
        subs_card = BriscaCard('C', '7')
        game.player2.hand[0] = subs_card
        game.dealer.trump_card = trump_card
        game.round_number = 2
        state, p_id = game.step('substitute')
        self.assertEqual(p_id, 1)
        self.assertEqual(state['id'], p_id)
        self.assertTrue(trump_card in game.player2.hand)
        self.assertEqual(game.dealer.deck[-1], subs_card)
        self.assertEqual(game.first_to_act, game.player2)
        self.assertEqual(game.current_player, game.player2)
        self.assertEqual(game.second_to_act, game.player1)

    def test_step_first_card(self):
        game = BriscaGame(last_starting_player_id=1)
        game.init_game()
        p1_card = game.player1.hand[0]
        game.step(str(p1_card))
        self.assertEqual(game.board[0], p1_card)
        self.assertTrue(p1_card not in game.player1.hand)
        self.assertEqual(game.played_cards[-1], p1_card)
        self.assertEqual(game.player1, game.first_to_act)
        self.assertEqual(game.player2, game.second_to_act)
        self.assertEqual(game.player2, game.current_player)

    def test_step_second_card(self):
        game = BriscaGame(last_starting_player_id=1)
        game.init_game()
        p1_card = BriscaCard('B', '2')
        game.player1.hand[0] = p1_card
        p2_card = BriscaCard('B', '3')
        game.player2.hand[0] = p2_card
        p2_next_card = game.dealer.deck[0]
        p1_next_card = game.dealer.deck[1]
        game.step(str(p1_card))
        game.step(str(p2_card))
        self.assertEqual(game.player2, game.first_to_act)
        self.assertEqual(game.player1, game.second_to_act)
        self.assertEqual(game.player2, game.current_player)
        self.assertEqual(game.player2.score, 10)
        self.assertTrue(p1_next_card in game.player1.hand)
        self.assertTrue(p2_next_card in game.player2.hand)
        self.assertEqual(game.board, [])
        self.assertEqual(game.round_number, 2)

    def test_step_back(self):
        game = BriscaGame()
        game.init_game()
        self.assertRaises(NotImplementedError, game.step_back)

    def test_get_action_num(self):
        game = BriscaGame()
        self.assertEqual(game.get_action_num(), 41)

    def test_get_player_id(self):
        game = BriscaGame()
        game.init_game()
        self.assertEqual(game.get_player_id(), game.current_player.player_id)

    def test_get_is_game_over(self):
        game = BriscaGame()
        game.init_game()
        self.assertFalse(game.is_over())
        game.player1.hand = []
        game.player2.hand = []
        self.assertTrue(game.is_over())

    def test_get_actions(self):
        game = BriscaGame(last_starting_player_id=0)
        game.init_game()
        p1_cards_str = [str(card) for card in game.player1.hand]
        self.assertEqual(p1_cards_str, game.get_actions(game.player1))
        trump_card = BriscaCard('C', 'R')
        subs_card = BriscaCard('C', '7')
        game.player2.hand[0] = subs_card
        game.dealer.trump_card = trump_card
        game.round_number = 2
        p2_actions = game.get_actions(game.player2)
        self.assertEqual(len(p2_actions), 4)
        self.assertEqual(p2_actions[-1], 'substitute')

    def test_player_can_subs(self):
        game = BriscaGame(last_starting_player_id=0)
        game.init_game()
        trump_card = BriscaCard('C', 'R')
        subs_card = BriscaCard('C', '7')
        game.player2.hand[0] = subs_card
        game.dealer.trump_card = trump_card
        self.assertFalse(game.player_can_substitute(game.player1))
        self.assertFalse(game.player_can_substitute(game.player2))
        game.round_number = 2
        self.assertTrue(game.player_can_substitute(game.player2))
        game.first_to_act = game.player1
        self.assertFalse(game.player_can_substitute(game.player2))
        game.first_to_act = game.player2
        game.dealer.deck = []
        self.assertFalse(game.player_can_substitute(game.player2))

    def test_round_is_over(self):
        game = BriscaGame()
        game.init_game()
        self.assertFalse(game.is_round_over())
        game.board.append(BriscaCard('O', 'A'))
        self.assertFalse(game.is_round_over())
        game.board.append(BriscaCard('B', '2'))
        self.assertTrue(game.is_round_over())

    def test_round_winner(self):
        game = BriscaGame(last_starting_player_id=1)
        game.init_game()
        game.dealer.trump_card = BriscaCard('B', '2')
        p1 = game.player1
        p2 = game.player2
        b4, oa, b5, c3, ca, e2, os = \
            BriscaCard('B', '4'), BriscaCard('O', '5'), BriscaCard('B', '5'), BriscaCard('C', '3'), \
            BriscaCard('C', 'A'), BriscaCard('E', '2'), BriscaCard('O', 'S')
        game.board = [b4, oa]
        self.assertEqual(game.get_round_winner(), p1)
        game.board = [oa, b4]
        self.assertEqual(game.get_round_winner(), p2)
        game.board = [b4, b5]
        self.assertEqual(game.get_round_winner(), p2)
        game.board = [b5, b4]
        self.assertEqual(game.get_round_winner(), p1)
        game.board = [c3, ca]
        self.assertEqual(game.get_round_winner(), p2)
        game.board = [ca, c3]
        self.assertEqual(game.get_round_winner(), p1)
        game.board = [e2, os]
        self.assertEqual(game.get_round_winner(), p1)


if __name__ == '__main__':
    unittest.main()
