import pygame
from variables import *
import sys

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Node:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.radius = NODE_RADIUS
        self.color = WHITE
        self.border_width = BORDER_WIDTH
        self.border_color = BLACK
        
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        pygame.draw.circle(screen, self.border_color, (self.x, self.y), self.radius, self.border_width)
        
class Edge:
    def __init__(self, start: Node, end: Node):
        self.start = start
        self.end = end
        self.color = BLACK
        self.width = EDGE_THICKNESS
        
    def draw(self):
        pygame.draw.line(screen, self.color, (self.start.x, self.start.y), (self.end.x, self.end.y), self.width)

class Graph:

def main():

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    main()
