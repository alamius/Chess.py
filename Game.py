#Game object for chess.py
from utils import Vector, color_to_str, std_size
#from Figure import std_figures
from random import randint

class Game(object):
    def __init__(self, size=std_size, figures=None):
        from Figure import std_figures
        super(Game, self).__init__()
        self.size = size
        if(figures == None):
            self.figures = std_figures()
        else:
            self.figures = figures
        self.squares = []
        for x in range(self.size.x):
            self.squares += [[]]
            for y in range(self.size.y):
                self.squares[x] += [-1]
        for fig_index in range(len(self.figures)):
            fig = self.figures[fig_index]
            if(self.squares[fig.pos.x][fig.pos.y] == -1): #if there is no figure there
                self.squares[fig.pos.x][fig.pos.y] = fig_index #noting the index of the figure on it's position in the squares
            else:
                raise ValueError(
                    "Figure #"+str(fig_index)
                    +" ("+fig.to_str()
                    +") has a Position, that is used by Figure #"
                    +str(self.squares[fig.pos.x][fig.pos.y])
                    +" ("+self.get_figure_by_pos(fig.pos.x, fig.pos.y).to_str()+")"
                )
        got_sq = self.get_squares()
        for fig_index in range(len(self.figures)):
            self.figures[fig_index].squares = got_sq
        self.turns = 1 #white begins
        self.log = []
        self.no_log = False
        self.won = -1
    def get_figure_by_pos(self, x, y):
        sq = self.squares[x][y]
        if(sq == -1):
            raise ValueError("There is no figure on this square ("+Vector(x, y).chess_notation()+").")
        else:
            return self.figures[sq]
    def to_str_square(self, x, y, size=Vector(3, 3)):
        col = "#"*bool(0 == (x+y-1)%2)+" "*bool(1 == (x+y-1)%2)
        result = [col]*size.y*size.x
        fig_index = self.squares[x][y]
        if(fig_index != -1):
            fig = self.figures[fig_index]
            fig_pos = Vector(size.x//2, size.y//2)
            result[fig_pos.x*size.y+fig_pos.y] = fig.image
        return ["".join(result[k:k+size.y]) for k in range(0, len(result), size.y)]
    def to_str_fancy(self, size=Vector(3, 3), auto_print=True):
        result = ""
        result_arr = [[self.to_str_square(x, y, size) for y in range(self.size.y)] for x in range(self.size.x)]
        result += "  "+"".join([
            " "*(size.y//2+1)+"ABCDEFGH"[i]+" "*(size.y//2)
            for i in range(8)
        ])+" \n"
        x_sep = "  +"+("–"*size.y+"+")*self.size.y
        for big_x in range(self.size.x):
            result += x_sep+"\n"
            for x in range(size.x):
                if(x == size.x//2):
                    result += str(big_x+1)+" "
                else:
                    result += "  "
                for big_y in range(self.size.y):
                    result += "|"
                    for y in range(size.y):
                        result += result_arr[big_x][big_y][x][y]
                result += "|\n"
        result += x_sep+"\n"
        if(auto_print):
            print(result)
        return result
    def to_str(self, auto_print=True):
        x_sep = "+"+"–+"*self.size.y
        result = x_sep + "\n"
        for x in range(self.size.x):
            result += "|"
            for y in range(self.size.y):
                try:
                    result += self.get_figure_by_pos(x, y).image
                except ValueError:
                    if((x+y)%2):
                        result += "#"
                    else:
                        result += " "
                result += "|"
            result += "\n" + x_sep + "\n"
        if(auto_print):
            print(result)
        return result
    def get_squares(self):
        result = []
        for x in range(self.size.x):
            result += [[]]
            for y in range(self.size.y):
                try:
                    result[x] += [self.get_figure_by_pos(x, y).color]
                except ValueError:
                    result[x] += [-1]
        return result
    def get_all_moves(self, color=-1):
        result = []
        for figure in self.figures:
            if(color == figure.color or color == -1):
                result += figure.get_moves()
        return result
    def move_figure(self):
        moves = self.get_all_moves(color=self.turns%2)
        try:
            chosen = moves[randint(0, 20000)%len(moves)]
        except ZeroDivisionError:
            self.to_str_game_board()
            exit("Exit: There seems to be no possible move on the current board!")
        self.execute_move(chosen)
        self.turns += 1
    def execute_move(self, move):
        squares = self.get_squares()
        figure = move.figure
        pos = figure.pos
        dest = move.dest
        if(figure.color != self.turns%2):
            raise ValueError(
                "The color of the Figure "+figure.to_str()+" ("+color_to_str(figure.color)
                +") that is to move to "+dest.chess_notation()
                +" is not the color of the current turn ("+color_to_str(self.turns%2)+")"
            )
        if(squares[dest.x][dest.y] == figure.color):
            raise ValueError(
                "The color of the square "+pos.to_str()+" ("+color_to_str(squares[dest.x][dest.y])+
                ") that is to move to is of the same color as the moving Figure ("+str(figure.color)+")"
            )
        if(squares[dest.x][dest.y] == bool(not figure.color)):
            killed = self.get_figure_by_pos(dest.x, dest.y)
            if not self.no_log:
                self.log += [
                    "Player "+color_to_str(self.turns%2)+" kills "
                    +killed.to_str()+" of his opponent with "+figure.to_str()+"."
                ]
            if(killed.name == "King"):
                if not self.no_log:
                    self.log += [
                        "The "+color_to_str(killed.color)+" king has been killed. "+color_to_str(figure.color)+" has won. "]
                self.won = figure.color
            sq = self.squares[dest.x][dest.y]
            del self.figures[sq]
            for x in range(self.size.x):
                for y in range(self.size.y):
                    if(self.squares[x][y] >= sq):
                        self.squares[x][y] -= 1
        else:
            if not self.no_log:
                self.log += [
                    "Player "+color_to_str(self.turns%2)+" moves "+figure.to_str()
                    +" to "+dest.chess_notation()+"."
                ]
        self.squares[dest.x][dest.y] = self.squares[pos.x][pos.y]
        self.squares[pos.x][pos.y] = -1
        figure.pos = dest
        #re-sending all the correct squares to the figures
        got_sq = self.get_squares()
        for fig_index in range(len(self.figures)):
            self.figures[fig_index].squares = got_sq
    def to_str_game_board(self):
        board = self.to_str_fancy(size=Vector(1, 2), auto_print=False).split("\n")[:-1]
        Pos = [
            figure.pos for figure in self.figures
        ]
        moves = self.get_all_moves(color=self.turns%2)
        moves = [move.to_str() for move in moves]
        moves_rest = []
        if(len(moves)/(len(board)-2) > 5):
            moves_rest = moves[(len(board)-2)*5:]
            moves = moves[:(len(board)-2)*5]
        for row in range(len(moves)):
            board[row%(len(board)-2)+1] += "\t"+moves[row]
        for row in range(len(board)):
            print(board[row])
        while(len(moves_rest) > 0):
            print(end="\t")
            for t in range(6):
                if(len(moves_rest) == 0):
                    break
                print(moves_rest[0], end="\t")
                del moves_rest[0]
            print()
        self.log_output()
    def log_output(self):
        print("\n".join(self.log))
        self.log = []
