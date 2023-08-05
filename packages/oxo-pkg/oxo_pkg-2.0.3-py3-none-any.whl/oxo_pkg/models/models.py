
# Models

line = "_______\n"

class Move:
    def __init__(self, position, value):
        self.position = position
        self.value = value
    def __str__(self):
        return self.value
    def __repr__(self):
        return "Move(%s, %s)" %(self.position, self.value)

class Grid:
    topRight = Move( "topRight", "-")
    topMid = Move( "topMid", "-")
    topLeft = Move( "topLeft", "-")
    midRight = Move( "midRight", "-")
    midMid = Move( "midMid", "-")
    midLeft = Move( "midLeft", "-")
    bottomRight = Move( "bottomRight", "-")
    bottomMid = Move( "bottomMid", "-")
    bottomLeft = Move( "bottomLeft", "-")
    def __str__(self):
        return "%s|%s|%s|%s|\n%s|%s|%s|%s|\n%s|%s|%s|%s|\n%s" %(line,
                                                                self.topLeft, self.topMid, self.topRight, line,
                                                                self.midLeft, self.midMid, self.midRight, line,
                                                                self.bottomLeft, self.bottomMid, self.bottomRight, line)

class Win:
    def __init__(self, win, value):
        self.win = win
        self.value = value