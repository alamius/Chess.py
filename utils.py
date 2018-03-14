#utils for chess.py

class Vector(object):
    def __init__(self, x=0, y=0, z=0):
        super(Vector, self).__init__()
        self.x=x
        self.y=y
        self.z=z
    def add(self, vec2):
        return Vector(
            self.x+vec2.x,
            self.y+vec2.y,
            self.z+vec2.z
        )
    def equals(self, vec2):
        return (
                self.x == vec2.x
            and self.y == vec2.y
            and self.z == vec2.z
        )
    def dist(self, vec2=None):
        if(vec2 == None):
            vec2 = Vector(0, 0, 0)
        return (
             (self.x-vec2.x)**2
            +(self.y-vec2.y)**2
            +(self.z-vec2.z)**2
        )**0.5
    def in_ranges(self, x_rng=[0, 1], y_rng=[0, 1], z_rng=[0, 1]):
        return (
                self.x in range(x_rng[0], x_rng[1])
            and self.y in range(y_rng[0], y_rng[1])
            and self.z in range(z_rng[0], z_rng[1])
        )
    def to_str(self, what=[True, True, False]):
        result = "("
        if(what[0]): result += str(self.x)
        if(what[0]*what[1]): result += ", "
        if(what[1]): result += str(self.y)
        if(what[1]*what[2]): result += ", "
        if(what[2]): result += str(self.z)
        result += ")"
        return result
    def chess_notation(self):
        if(not self.in_ranges([0, std_size.x], [0, std_size.y])):
            raise IndexError(
                "The values of "+self.to_str()+" are out of the bounds of the rectangular range from "
                +Vector(0, 0).to_str()+" to "+std_size.to_str()+"."
            )
        else:
            return "ABCDEFGH"[self.y]+str(self.x+1)

std_size = Vector(8, 8)

def color_to_str(color):
    return "black"*(color==0)+"white"*(color==1)

def sort(Values):
    if(len(Values) <= 1):
        return Values
    # if(len(Values) == 2):
    #     return [min(Values), max(Values)]
    t = Values[len(Values)//2]
    smaller = []
    bigger = []
    i = 0
    while i < len(Values):
        v = Values[i]
        if(v < t):   smaller += [v]
        elif(v > t): bigger += [v]
        if(v != t):  del Values[i]
        else:        i += 1
    return sort(smaller)+Values+sort(bigger)

def diagram_to_str(Values, class_num=10): #Values = list of results, like [3, 5, 3, 7] not counted like {3:2, 5:1, 7:1}
    Values = sort(Values)
    class_width = (Values[-1]-Values[0])/class_num
    classed_values = []
    i = 0
    v = Values[0]
    while i < len(Values)-1:
        classed_values += [[]]
        for j in range(i, len(Values)):
            if(v < Values[j] <= v+class_width):
                classed_values[-1] += [Values[j]]
        i += len(classed_values[-1])
        v += class_width
    class_heights = [len(classed) for classed in classed_values]
    scale = 160/max(class_heights)
    return "".join(["#"*int(scale*height)+"\n" for height in class_heights])
