import pygame as pygame, sys
from collections import deque
import math
from square import Square

class PathVisualizer:

    def __init__(self, pg, sys, w, h, cw, sqs, bgc, fc, fps):
        self.pygame = pg
        self.pygame.init()
        self.sys = sys
        self.width = w
        self.height = h
        self.help = False
        self.commandWidth = w
        self.commandHeight = cw
        self.squareSize = sqs
        self.backgroundColor = bgc
        self.foregroundColor = fc
        self.fontSize = 40
        self.bigFontSize = 60
        self.font = self.pygame.font.SysFont(None, self.fontSize)
        self.bigFont = self.pygame.font.SysFont(None, self.bigFontSize)
        self.numberOfRows = int(self.height / self.squareSize)
        self.numberOfColums = int(self.width / self.squareSize)
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.screen = self.pygame.display.set_mode((self.width, self.height + self.commandHeight))
        self.pygame.display.set_caption("PathViz")
        self.start_new_pathvisualizer()

    def main_loop(self):
        while (True):
            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT:
                    self.pygame.quit()
                    self.sys.exit()
                elif event.type == self.pygame.KEYDOWN:
                    self.command_handler(event)
                elif self.pygame.mouse.get_pressed()[0]:
                    self.mouse_left()
                elif self.pygame.mouse.get_pressed()[2]:
                    self.mouse_right()

            self.draw_background()
            self.draw_command()
            self.draw_grid()
            self.draw_help()
            self.update()
            self.clock.tick(self.fps)

    def a_star(self):
        openSet = []
        visitedNodes = []
        cameFrom = {}
        gScore = {}
        fScore = {}

        for r in self.squareGrid:
            for c in r:
                if not c.get_startnode():
                    gScore[c] = math.inf
                    fScore[c] = math.inf
                else:
                    gScore[c] = 0
                    fScore[c] = self.heuristic_function(c, self.squareGrid[self.endNodeRow][self.endNodeColumn])
                    openSet.append(c)

        while openSet:
            fScore_subset = {key: value for key, value in fScore.items() if key in openSet}
            for key, value in fScore_subset.items():
                if value == min(fScore_subset.values()):
                    current = key
            visitedNodes.append((current.get_row(), current.get_col()))
            if current.get_endnode():
                return self.reconstruct_path(cameFrom, current, visitedNodes)
            openSet.remove(current)
            for neigbor in self.get_neighbors(current):
                tentativeGscore = gScore[current] + 1
                if tentativeGscore < gScore[neigbor]:
                    cameFrom[neigbor] = current
                    gScore[neigbor] = tentativeGscore
                    fScore[neigbor] = gScore[neigbor] + self.heuristic_function(neigbor, self.squareGrid[self.endNodeRow][self.endNodeColumn])
                    neigbor.set_open()
                    if neigbor not in openSet:
                        openSet.append(neigbor)
            current.set_visited()
            current.set_closed()
            self.draw_grid()
            self.update()

    def reconstruct_path(self, cameFrom, current, visitedNodes):
        optimalPath = deque()
        optimalPath.append((current.get_row(), current.get_col()))
        current.set_optimal()
        while current in cameFrom.keys():
            current = cameFrom[current]
            current.set_optimal()
            optimalPath.appendleft((current.get_row(), current.get_col()))
        return optimalPath, visitedNodes

    def get_neighbors(self, node):
        currentNodeRow = node.get_row()
        currentNodeColumn = node.get_col()
        neighbors = []
        if currentNodeRow - 1 >= 0:
            northNeighbor = self.squareGrid[currentNodeRow-1][currentNodeColumn]
            neighbors.append(northNeighbor)
        if currentNodeColumn + 1 < self.numberOfColums:
            eastNeighbor = self.squareGrid[currentNodeRow][currentNodeColumn+1]
            neighbors.append(eastNeighbor)
        if currentNodeRow + 1 < self.numberOfRows:
            southNeighbor = self.squareGrid[currentNodeRow+1][currentNodeColumn]
            neighbors.append(southNeighbor)
        if currentNodeColumn - 1 >= 0:
            westNeighbor = self.squareGrid[currentNodeRow][currentNodeColumn-1]
            neighbors.append(westNeighbor)

        return [neigbor for neigbor in neighbors if not neigbor.get_wall()]

    def heuristic_function(self, currentNode, endNode):
        return abs(endNode.get_col() - currentNode.get_col()) + abs(endNode.get_row() - currentNode.get_row())


    def bfs(self):
        q = deque()
        for r in self.squareGrid:
            for c in r:
                if c.get_startnode():
                    q.append([c])

        while q:
            path = q.popleft()
            node = path[-1]
            if node.get_endnode():
                for n in path:
                    n.set_optimal()
                return path
            for neigbor in self.get_neighbors(node):
                if not neigbor.get_visited():
                    new_path = list(path)
                    new_path.append(neigbor)
                    q.append(new_path)
                    neigbor.set_visited()

            # if not node.get_visited():
            #     for neigbor in self.get_neighbors(node):
            #         new_path = list(path)
            #         new_path.append(neigbor)
            #         q.append(new_path)
            #         neigbor.set_open()
            #         if neigbor.get_endnode():
            #             for n in new_path:
            #                 n.set_optimal()
            #             return new_path
            # node.set_visited()
            # node.set_closed()
            self.draw_grid()
            self.update()

    def start_new_pathvisualizer(self):
        self.commandText = ""
        self.create_grid()
        self.create_start_node()
        self.create_end_node()

    def create_grid(self):
        self.squareGrid = [[Square(r, c, self.squareSize, False) for c in range(self.numberOfColums)] for r in range(self.numberOfRows)]

    def create_start_node(self):
        self.startNodeRow, self.startNodeColumn = (22, 5)
        self.squareGrid[self.startNodeRow][self.startNodeColumn].set_startnode()

    def create_end_node(self):
        self.endNodeRow, self.endNodeColumn = (22, 75)
        self.squareGrid[self.endNodeRow][self.endNodeColumn].set_endnode()

    def mouse_left(self):
        mouseXpos, mouseYpos = self.pygame.mouse.get_pos()
        mouseRow = mouseYpos // self.squareSize
        mouseColumn = mouseXpos // self.squareSize
        if 0 <= mouseRow < self.numberOfRows and 0 <= mouseColumn < self.numberOfColums:
            self.squareGrid[mouseRow][mouseColumn].set_wall()

    def mouse_right(self):
        mouseXpos, mouseYpos = self.pygame.mouse.get_pos()
        mouseRow = mouseYpos // self.squareSize
        mouseColumn = mouseXpos // self.squareSize
        if 0 <= mouseRow < self.numberOfRows and 0 <= mouseColumn < self.numberOfColums:
            self.squareGrid[mouseRow][mouseColumn].set_normal()

    def command_handler(self, event):
        if event.key == self.pygame.K_RETURN:
            self.submit_command()
        elif event.key == self.pygame.K_BACKSPACE:
            self.pop_command_text()
        else:
            self.insert_command_text(event)

    def submit_command(self):
        if self.commandText.lower() == "restart":
            self.start_new_pathvisualizer()
        elif self.commandText.lower() == "search astar":
            optimalPath, visitedNodes = self.a_star() #gör nåt med optimalpath
        elif self.commandText.lower() == "search bfs":
            self.bfs() #gör nåt med resultatet
        elif self.commandText.lower() == "help":
            self.help = True
        elif self.commandText.lower() == "exit":
            self.help = False
        self.clear_command_text()

    def clear_command_text(self):
        self.commandText = ""

    def pop_command_text(self):
        self.commandText = self.commandText[:-1]

    def insert_command_text(self, event):
        self.commandText += event.unicode

    def draw_command(self):
        commandHeader = "Enter command --> "
        yPadding = 10
        commandTextSurf = self.font.render(commandHeader + self.commandText, True, self.foregroundColor)
        self.screen.blit(commandTextSurf, commandTextSurf.get_rect(topleft = (self.width // 8, self.height + yPadding)))

    def draw_help(self):
        if self.help:
            helpTextList = ["Usage",
                            "Command-->Description",
                            "help --> Brings up help menu",
                            "search -a --> searches using algorithm '-a' ",
                            "restart --> restart the application",
                            "quit --> quits the application",
                            "Algorithms",
                            "Astar --> 'search Astar' to run"
                            ]
            stringVertLoc = 0
            padding = 15
            for index, line in enumerate(helpTextList):
                if line in ("Usage", "Algorithms"):
                    helpSurface = self.bigFont.render(line, True, self.foregroundColor)
                    self.screen.blit(helpSurface, helpSurface.get_rect(midtop = (self.width // 2, self.height // 8 + stringVertLoc)))
                    stringVertLoc += self.bigFont.get_height() + padding
                else:
                    helpSurface = self.font.render(line, True, self.foregroundColor)
                    self.screen.blit(helpSurface, helpSurface.get_rect(topleft = (self.width // 4, self.height // 8 + stringVertLoc)))
                    stringVertLoc += self.font.get_height() + padding

    def draw_grid(self):
        if not self.help:
            for r in self.squareGrid:
                for c in r:
                    rect = self.pygame.Rect(c.get_x_position(), c.get_y_position(), c.get_size(), c.get_size())
                    if c.get_wall():
                        border = 0
                        color = self.foregroundColor
                    elif c.get_startnode() or c.get_endnode():
                        border = 0
                        color = (126, 173, 105)
                    elif c.get_optimal():
                        border = 0
                        color = (223, 192, 10)
                    elif c.get_open():
                        border = 0
                        color = (199, 17, 80)
                    elif c.get_visited():
                        border = 0
                        color = (66, 116, 253)
                    else:
                        border = 1
                        color = self.foregroundColor

                    self.pygame.draw.rect(self.screen, color, rect, border)

    def draw_background(self):
        self.screen.fill(self.backgroundColor)

    def update(self):
        self.pygame.display.update()

w = 1600
h = 900
cw = 50
sqs = 20
bgc = (45, 45, 45)
fc = (171, 171, 171)
fps = 30
pathVisualiser = PathVisualizer(pygame, sys, w, h, cw, sqs, bgc, fc, fps)
pathVisualiser.main_loop()
