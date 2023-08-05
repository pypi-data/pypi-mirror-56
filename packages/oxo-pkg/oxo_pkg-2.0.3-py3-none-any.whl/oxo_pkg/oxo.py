#!/usr/bin/python

import sys, getopt

from .utils.methods import *
from .models.models import *

def run():
    # for eachArg in sys.argv[1:]:
    #     print(eachArg)
    # print("something")

    game = Grid()

    def turn():
        try:
            print(game)
            your_move = input("your move: ").lower()

            if is_input_valid(your_move):
                # print "input is valid"
                move_key = input_to_move_key(your_move)
                if is_move_valid(game, move_key):
                    # print "move is valid"
                    setattr(game, move_key, Move( move_key, "X"))
                    # print "grid updated"

                    if check_for_win_wrapper(game, "congratulations! %s's win") == True:
                        run()

                    cpu_move_key = computer_move(game)
                    setattr(game, cpu_move_key, Move( cpu_move_key, "O"))
                    print("computer makes a move: " + cpu_move_key)

                    if check_for_win_wrapper(game, "you lose! %s's win") == True:
                        run()

                    turn()
                else:
                    print("move is NOT valid - move %s is already taken" %(your_move))
                    turn()
            else:
                print("invalid input")
                turn()
        except KeyboardInterrupt:
            print(" - program exited")
            print("bye bye!")
            sys.exit()

    turn()

if __name__ == "__main__":
    run()