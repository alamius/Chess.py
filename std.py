from Move import matrix_moves, equation_moves, pawn_move
from utils import Vector, std_size


Matrices = {
    "straight":[[1, 0], [0, 1], [-1, 0], [0, -1]],
    "diagonal":[[1, 1], [-1, 1], [-1, -1], [1, -1]]
}

std_movements = {
    "Tower": (lambda figure, squares : matrix_moves(figure, squares, Matrices["straight"])),
    "Knight":(lambda figure, squares : equation_moves(figure, squares, [-2, -1, 1, 2], (lambda x, y: abs(x)+abs(y) == 3))),
    "Bishop":(lambda figure, squares : matrix_moves(figure, squares, Matrices["diagonal"])),
    "Queen": (lambda figure, squares : matrix_moves(figure, squares, Matrices["straight"]+Matrices["diagonal"])),
    "King":  (lambda figure, squares : equation_moves(figure, squares, [-1, 0, 1], (lambda x, y: abs(x)+abs(y) > 0))),
    "Pawn":  pawn_move
}

std_images = {
    "Tower":("Ħ", "ħ"),
    "Knight":("?", "ß"),
    "Bishop":("Ð", "ð"),
    "Queen":("Þ", "þ"),
    "King":("Ŧ", "ŧ"),
    "Pawn":("°", "^"),
}

std_names = [
    "Tower",
    "Tower",
    "Knight",
    "Knight",
    "Bishop",
    "Bishop",
    "Queen",
    "King",
    "Pawn",
    "Pawn",
    "Pawn",
    "Pawn",
    "Pawn",
    "Pawn",
    "Pawn",
    "Pawn",
]
std_pos = [
    [Vector(0, 0), Vector(7, 0)],
    [Vector(0, 7), Vector(7, 7)],
    [Vector(0, 1), Vector(7, 1)],
    [Vector(0, 6), Vector(7, 6)],
    [Vector(0, 2), Vector(7, 2)],
    [Vector(0, 5), Vector(7, 5)],
    [Vector(0, 3), Vector(7, 3)],
    [Vector(0, 4), Vector(7, 4)]
]
