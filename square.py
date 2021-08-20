class Square:

    def __init__(self, row, col, size, pressed):
        self.row = row
        self.column = col
        self.size = size
        self.pressed = pressed

    def get_x_position(self):
        self.xPosition = self.column * self.size
        return self.xPosition

    def get_y_position(self):
        self.yPosition = self.row * self.size
        return self.yPosition

    def get_size(self):
        return self.size

