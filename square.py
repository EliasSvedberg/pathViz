class Square:

    def __init__(self, row, col, size, wall):
        self.row = row
        self.column = col
        self.size = size
        self.wall = wall
        self.startnode = False
        self.endnode = False
        self.visited = False
        self.open = False
        self.optimalNode = False

    def get_row(self):
        return self.row

    def get_col(self):
        return self.column

    def set_wall(self):
        self.wall = True

    def set_closed(self):
        self.open = False

    def set_open(self):
        self.open = True

    def get_open(self):
        return self.open

    def set_normal(self):
        self.wall = False

    def get_wall(self):
        return self.wall

    def get_x_position(self):
        self.xPosition = self.column * self.size
        return self.xPosition

    def get_y_position(self):
        self.yPosition = self.row * self.size
        return self.yPosition

    def get_size(self):
        return self.size

    def set_visited(self):
        self.visited = True

    def unset_visited(self):
        self.visited = False

    def get_visited(self):
        return self.visited

    def set_optimal(self):
        self.optimalNode = True

    def unset_optimal(self):
        self.optimalNode = False

    def get_optimal(self):
        return self.optimalNode

    def set_endnode(self):
        self.endnode = True

    def get_endnode(self):
        return self.endnode

    def set_startnode(self):
        self.startnode = True

    def get_startnode(self):
        return self.startnode

