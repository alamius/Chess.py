#Programming an object-oriented Chess Game in Python 3!
#Basic structure:
# - Game has:
#  - Players (2) #random, NN, inputbased
#  - Field:
#   - 2D-index-arr for pointing to the figures in the figure array
#  - Figure array:
#   - Name, Position, Basic Movement, Killedness

from random import random
from utils import Vector
from Game import Game
from Figure import Figure
# from std import std_movements, std_names, std_figures

T = []
for c in range(1000):
    game = Game()
    game.no_log=True
    while(game.won == -1):
        game.move_figure()
        # game.to_str_game_board()
        # game.log_output()
        # input("[ENTER] to continue...")
    T += [game.turns]
# T = [t/5 for t in range(1, 10)] #testing the diagram
from utils import diagram_to_str
print(diagram_to_str(T[:]))
file = open("output["+str(random())+"].T", 'x')
output = "\n".join([str(t) for t in T])
file.write(output)
file.close()
