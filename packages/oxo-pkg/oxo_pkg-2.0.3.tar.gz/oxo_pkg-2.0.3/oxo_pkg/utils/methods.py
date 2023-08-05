import sys
import random

from ..models.models import *
from ..resources.data import *


# Methods

def is_input_valid(input):
    if input in possible_input:
        return True
    else:
        return False

def input_to_move_key(input):
    return moves_map.get(input)

def get_available_move_keys(game):
    return_list = []
    for key in all_move_keys:
        move = getattr(game, key)
        if move.value == "-":
            return_list.append(key)
    return return_list

def is_move_valid(game, move_key):
    all_available_move_keys = get_available_move_keys(game)
    if move_key in all_available_move_keys:
        return True
    else:
        return False

def computer_move(game):
    all_available_move_keys = get_available_move_keys(game)
    random_index = random.randint(0, len(all_available_move_keys)-1)
    cpu_move_key = all_available_move_keys[random_index]
    return cpu_move_key

def check_for_win(game):
    for win_set in possible_wins:
        values = list(map(lambda position: getattr(game, position).value, win_set))
        if values.count("X") == 3 or values.count("O") == 3:
            return Win( True, values[0])
    return Win( False, "-")

def check_for_win_wrapper(game, string):
    win = check_for_win(game)
    if win.win == True:
        print (game)
        print (string %(win.value))
        return play_again()
    elif len(get_available_move_keys(game)) == 0:
        print (game)
        print ("oh ho, its a draw")
        return play_again()
    else:
        return False

def play_again():
    print ("would you like to play again?")
    replay = input(": ").lower()
    if replay in no_answers:
        print("bye bye!")
        sys.exit()
    elif replay in yes_answers:
        return True
    else:
        print ("not a valid input")
        print ("enter no or press Ctrl + C to exit")
        return play_again()



