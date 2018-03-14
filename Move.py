#move class to organize the moves in chess.py
from utils import Vector, std_size

class Move(object):
    def __init__(self, figure, orig, dest):
        super(Move, self).__init__()
        self.figure = figure
        self.orig = orig
        self.dest = dest
    def to_str(self):
        return self.figure.name+" from "+self.orig.chess_notation()+" to "+self.dest.chess_notation()

def matrix_moves(figure, squares, Matrices):
    result = []
    pos = figure.pos
    try:    size = Vector(len(squares), len(squares[0]))
    except: size = Vector(8, 8)
    mag = int(size.dist()+1)
    for M in Matrices:
        for d in range(1, mag):
            added = pos.add(Vector(M[0]*d, M[1]*d))
            if(
                not added.in_ranges([0, size.x], [0, size.y])
                or squares[added.x][added.y] == figure.color
            ): #out of ranges or hit a fig. of the same color
                break
            if(added.in_ranges([0, size.x], [0, size.y])): #x and y in ranges of the gamespace
                result += [Move(figure, pos, pos.add(Vector(M[0]*d, M[1]*d)))]
            if(squares[added.x][added.y] != -1): #out of ranges or hit a fig. of a different color
                break
    return result

def equation_moves(figure, squares, X, equation):
    result = []
    try:    size = Vector(len(squares), len(squares[0]))
    except: size = Vector(8, 8)
    for x in X:
        for y in X:
            added = figure.pos.add(Vector(x,y))
            if(
                equation(x, y)
                and added.in_ranges([0,size.x],[0,size.y])
                and squares[added.x][added.y] != figure.color
            ):
                result += [Move(figure, figure.pos, added)]
    return result

def pawn_move(figure, squares):
    result = []
    try:    size = Vector(len(squares), len(squares[0]))
    except: size = Vector(8, 8)
    x, y = figure.pos.x, figure.pos.y
    if(figure.color == 0):  dx = 1 #white = 1 -> white moves down (+y) and black up (-y)
    else:                   dx = -1
    if(not x+dx in range(0, std_size.x)):
        figure.make_queen()
        return []
    if(squares[x+dx][y] == -1 and x+dx < size.x):
        result += [Move(figure, figure.pos, Vector(x+dx, y))]
        if(
            ((figure.color == 0 and x == 1)
            or (figure.color == 1 and x == 6))
            and squares[x+2*dx][y] == -1
        ):
            result += [Move(figure, figure.pos, Vector(x+2*dx, y))]
    if(y > 0 and squares[x+dx][y-1] == bool(not figure.color)):
        result += [Move(figure, figure.pos, Vector(x+dx, y-1))]
    if(y < size.y-1 and squares[x+dx][y+1] == bool(not figure.color)):
        result += [Move(figure, figure.pos, Vector(x+dx, y+1))]
    return result
