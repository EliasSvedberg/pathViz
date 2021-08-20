import pygame as pygame, sys
from square import Square

class PathVisualizer:

    def __init__(self, pg, w, h, sqs, bgc, fc, fps):
        self.pygame = pg
        self.width = w
        self.height = h
        self.squareSize = sqs
        self.backgroundColor = bgc
        self.foregroundColor = fc
        self.numberOfRows = int(self.height / self.squareSize)
        self.numberOfColums = int(self.width / self.squareSize)
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.screen = self.pygame.display.set_mode((self.width, self.height))
        self.pygame.display.set_caption("PathViz")
        self.create_grid()

    def main_loop(self):
        #Game loop
        while (True):
            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT: #The user closed the window!
                    self.pygame.quit()
                    self.sys.exit() #Stop running

            self.draw_background()
            self.draw_grid()
            self.draw_grid()
            self.update()
            self.clock.tick(self.fps)#set frames/second

    def create_grid(self):
        self.squareGrid = [[Square(r, c, self.squareSize, False) for c in range(self.numberOfColums)] for r in range(self.numberOfRows)]

    def draw_grid(self):
        # for r in range(0, self.height, self.squareSize):
        #     for c in range(0, self.width, self.squareSize):
        #         rect = pygame.Rect(x, y, blockSize, blockSize)
        #         pygame.draw.rect(SCREEN, WHITE, rect, 1)
        for r in self.squareGrid:
            for c in r:
                rect = self.pygame.Rect(c.get_x_position(), c.get_y_position(), c.get_size(), c.get_size() )
                self.pygame.draw.rect(self.screen, self.foregroundColor, rect, 1)


    def draw_background(self):
        self.screen.fill(self.backgroundColor)

    def update(self):
        self.pygame.display.update()

w = 1600
h = 900
sqs = 10
bgc = (45, 45, 45)
fc = (171, 171, 171)
fps = 30
pathVisualiser = PathVisualizer(pygame, w, h, sqs, bgc, fc, fps)
pathVisualiser.main_loop()
