#the figures for chess.py
from utils import Vector, color_to_str, std_size
from std import *

class Figure(object):
    def __init__(self, name, pos,  movements, color, squares, image): #image is a single or rectangle characterarray (=string)
        super(Figure, self).__init__()
        self.name = name
        self.pos = pos
        #movements(figure, squares) -> Move array that contains all currently possible moves
        self.movements = movements #a function that returns all possible places for that figure
        self.color = color #1 = white, 0 = black
        self.squares = squares
        self.image = image
    def to_str(self):
        return self.name+" ['"+self.image+"', "+color_to_str(self.color)+", "+self.pos.chess_notation()+"]"
    def get_moves(self):
        # print(self.to_str()+" is being checked for possible moves.")
        return self.movements(self, self.squares)
    def make_queen(self):
        self.name = "Queen"
        self.movements = (lambda figure, squares : matrix_moves(figure, squares, Matrices["straight"]+Matrices["diagonal"]))
        self.image = std_images["Queen"][self.color]

def std_figures(): #will just be referenced if saved as an array
    return [
        Figure(
            std_names[k],
            std_pos[k][0],
            std_movements[std_names[k]],
            0, None,
            std_images[std_names[k]][0]
        )
        for k in range(8)
    ]+[
        Figure("Pawn",      Vector(1, y),  pawn_move,                0, None, "°") for y in range(8)
    ]+[
        Figure(
            std_names[k],
            std_pos[k][1],
            std_movements[std_names[k]],
            1, None,
            std_images[std_names[k]][1]
        )
        for k in range(8)
    ]+[
        Figure("Pawn",      Vector(6, y),  std_movements["Pawn"],    1, None, "^") for y in range(8)
    ]
