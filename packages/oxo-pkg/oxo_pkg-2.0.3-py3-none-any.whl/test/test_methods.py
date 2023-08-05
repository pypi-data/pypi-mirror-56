# to run unit tests run 'python -m unittest test.test_methods' from project home directory

import unittest, os, sys
import StringIO
sys.path.append(os.path.abspath('./src'))
# this had to be added to the path to pick up methods file
# to print path
# print(sys.path)

# !!!!!! this needs mock installed (pip install --user mock) - without it will fail with a really obscure error!!!
from mock import patch
# for python 2.7.12 but this is part of unittest from python 3.3
# to be removed if test becomes flakey

from src.oxo.utils.methods import *
from src.oxo.models.models import *
from src.oxo.resources.data import *


def fill_grid(grid, move_keys, value):
    for key in move_keys:
        setattr(grid, key, Move( key, value))

def remove_move_keys(move_keys):
    # list constructor should be replaced with .copy() in python 3.3+
    some_move_keys = list(all_move_keys)
    for key in move_keys:
        some_move_keys.remove(key)
    return some_move_keys

def redirect_output():
    redirected_output = StringIO.StringIO()
    sys.stdout = redirected_output
    return redirected_output

def return_output_to_normal():
    sys.stdout = sys.__stdout__


class TestMethods(unittest.TestCase):

    def test_health_check(self):
        self.assertEqual(1, 1)

    def test_is_input_valid_false(self):
        self.assertEqual(is_input_valid("x"), False)

    def test_is_input_valid_true(self):
        for input in possible_input:
            self.assertEqual(is_input_valid(input), True)

    def test_input_to_move_key(self):
        self.assertEqual(input_to_move_key("tl"), "topLeft")
        self.assertEqual(input_to_move_key("mm"), "midMid")
        self.assertEqual(input_to_move_key("br"), "bottomRight")

    def test_get_available_move_keys_all(self):
        game = Grid()
        self.assertEqual(get_available_move_keys(game), all_move_keys)

    def test_get_available_move_keys_some(self):
        game = Grid()
        made_moves = ["topLeft", "midMid", "bottomRight"]
        fill_grid(game, made_moves, "O")
        expected = remove_move_keys(made_moves)

        self.assertEqual(get_available_move_keys(game), expected)

    def test_get_available_move_keys_none(self):
        game = Grid()
        fill_grid(game, all_move_keys, "O")
        self.assertEqual(get_available_move_keys(game), [])

    def test_get_available_move_keys_one(self):
        game = Grid()
        almost_all_move_keys = remove_move_keys(["bottomRight"])
        fill_grid(game, almost_all_move_keys, "O")
        self.assertEqual(get_available_move_keys(game), ["bottomRight"])

    def test_is_move_valid_true(self):
        game = Grid()
        self.assertEqual(is_move_valid(game, "midMid"), True)

    def test_is_move_valid_false(self):
        game = Grid()
        setattr(game, "midMid", Move( "midMid", "O"))
        self.assertEqual(is_move_valid(game, "midMid"), False)

    def test_computer_move(self):
        game = Grid()
        almost_all_move_keys = remove_move_keys(["bottomLeft"])
        fill_grid(game, almost_all_move_keys, "X")
        self.assertEqual(computer_move(game), "bottomLeft")

    def test_computer_move_some(self):
        game = Grid()
        made_moves = ["topLeft", "midMid", "bottomRight"]
        fill_grid(game, made_moves, "X")
        remaining_moves = remove_move_keys(made_moves)
        self.assertEqual(computer_move(game) in remaining_moves, True)

    def test_check_for_win_true_x(self):
        game = Grid()
        made_moves = possible_wins[0]
        fill_grid(game, made_moves, "X")
        expected_win = check_for_win(game)
        self.assertEqual(expected_win.win, True)
        self.assertEqual(expected_win.value, "X")

    def test_check_for_win_true_o(self):
        game = Grid()
        made_moves = possible_wins[1]
        fill_grid(game, made_moves, "O")
        expected_win = check_for_win(game)
        self.assertEqual(expected_win.win, True)
        self.assertEqual(expected_win.value, "O")

    def test_check_for_win_false(self):
        game = Grid()
        made_moves_x = ["topMid", "bottomMid"]
        fill_grid(game, made_moves_x, "X")
        setattr(game, "midMid", Move( "midMid", "O"))
        expected_lose = check_for_win(game)
        self.assertEqual(expected_lose.win, False)
        self.assertEqual(expected_lose.value, "-")

    def test_check_for_win_true_all(self):
        for win_set in possible_wins:
            game = Grid()
            fill_grid(game, win_set, "X")
            expected_win = check_for_win(game)
            self.assertEqual(expected_win.win, True)
            self.assertEqual(expected_win.value, "X")

    # @patch('src.oxo.utils.methods.play_again')
    # def test_check_for_win_wrapper_x(self, mock_play_again):
    #     redirected_output = redirect_output()
    #
    #     game = Grid()
    #     made_moves = possible_wins[0]
    #     fill_grid(game, made_moves, "X")
    #
    #     check_for_win_wrapper(game, "congratulations! %s's win")
    #
    #     return_output_to_normal()
    #
    #     output = redirected_output.getvalue()
    #
    #     self.assertIn("congratulations! X's win", output)
    #     mock_play_again.assert_called()
    #
    # @patch('src.oxo.utils.methods.play_again')
    # def test_check_for_win_wrapper_o(self, mock_play_again):
    #     redirected_output = redirect_output()
    #
    #     game = Grid()
    #     made_moves = possible_wins[1]
    #     fill_grid(game, made_moves, "O")
    #
    #     check_for_win_wrapper(game, "you lose! %s's win")
    #
    #     return_output_to_normal()
    #
    #     output = redirected_output.getvalue()
    #     self.assertIn("you lose! O's win", output)
    #     mock_play_again.assert_called()
    #
    # @patch('src.oxo.utils.methods.play_again')
    # def test_check_for_draw(self, mock_play_again):
    #     redirected_output = redirect_output()
    #
    #     game = Grid()
    #     x_moves = ["topRight", "topLeft", "midRight", "bottomLeft", "bottomMid"]
    #     o_moves = ["topMid", "midLeft", "midMid", "bottomRight"]
    #
    #     fill_grid(game, x_moves, "X")
    #     fill_grid(game, o_moves, "O")
    #
    #     check_for_win_wrapper(game, "any string %s")
    #
    #     return_output_to_normal()
    #
    #     output = redirected_output.getvalue()
    #     self.assertIn("oh ho, its a draw", output)
    #     mock_play_again.assert_called()

    def test_check_for_draw_false(self):
        redirected_output = redirect_output()

        game = Grid()
        setattr(game, "topLeft", Move( "topRight", "X"))
        setattr(game, "bottomRight", Move( "topRight", "O"))

        check_for_win_wrapper(game, "any string %s")

        return_output_to_normal()

        output = redirected_output.getvalue()
        self.assertEquals("", output)



if __name__ == '__main__':
    unittest.main()
