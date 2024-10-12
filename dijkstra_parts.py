from variables import *
import pygame
from pygame import gfxdraw
import math

def get_mouse_coords():
    return pygame.mouse.get_pos()

class Node:
    def __init__(self, x: int, y: int, name: str = None):
        self.x = x
        self.y = y
        self.name = name

        self.root = None
        self.action = None

        self.radius = NODE_RADIUS
        self.color = WHITE
        self.border_width = BORDER_WIDTH
        self.border_color = BLACK

        self.value = 0
        self.parent = None
        
    def draw(self):
        """Draws the node"""

        self.check_actions()

        # Draw circle
        gfxdraw.filled_circle(screen, self.x, self.y, self.radius, self.color)
        gfxdraw.aacircle(screen, self.x, self.y, self.radius-1, self.color)

        # Draw value in right corner
        text = FONT.render(str(self.value), True, BLACK)
        screen.blit(text, (self.x + self.radius, self.y - self.radius))

        # Draw name in center
        text = FONT.render(self.name, True, BLACK)
        screen.blit(text, (self.x - text.get_width() // 2, self.y - text.get_height() // 2))

        # Create border
        gfxdraw.aacircle(screen, self.x, self.y, self.radius, self.border_color)
        gfxdraw.aacircle(screen, self.x, self.y, self.radius+1, self.border_color)

        if self.action == "Connect":
            mouse_x, mouse_y = get_mouse_coords()
            pygame.draw.line(screen, self.border_color, (self.x, self.y), (mouse_x, mouse_y), self.border_width)

    def check_actions(self):
        if self.root == True:
            self.color = GREEN
        
        elif self.action == "Current":
            self.color = BLUE
    

    def mouse_over(self, coords: tuple):
        """Checks if the mouse is over the node

        Args:
            coords (tuple): (x, y) coordinates of the mouse
        """
        x, y = coords
        if (self.x - x)**2 + (self.y - y)**2 <= self.radius**2:
            
            self.color = LIGHT_GRAY
            return True
        
        self.color = WHITE
        return False

    def clicked(self, coords: tuple):
        """Checks if the node was clicked"""
        self.x, self.y = coords
        self.color = DARK_GRAY
        self.action = "Move"
        return True
            
    def __lt__(self, other):
        return self.value < other.value

    def __name__(self):
        return self.name

    def to_dict(self):
        """Convert Node to a dictionary."""
        return {
            'x': self.x,
            'y': self.y,
            'name': self.name,
            'root': self.root,
            'radius': self.radius,
            'value': self.value,
        }
    
class Edge:
    def __init__(self, start: Node, end: Node):
        self.start = start
        self.end = end
        self.action = None
        self.value = 1

        self.color = BLACK
        self.width = EDGE_THICKNESS
        
    def draw(self):
        """Draws the edge"""
        self.set_color()
        
        pygame.draw.line(screen, self.color, (self.start.x, self.start.y), (self.end.x, self.end.y), self.width) 
        text = FONT.render(str(self.value), True, BLACK)
        screen.blit(text, ((self.start.x + self.end.x) // 2 - text.get_width() // 2 + 20 , (self.start.y + self.end.y) // 2 - text.get_height() // 2 - 20))

    def calculate_new_edge_points(self):
        """
        Calculate new start and end points for an edge that are closer by 2*radius on both ends.
        """
        x1, y1 = self.start.x, self.start.y
        x2, y2 = self.end.x, self.end.y
        
        edge_length = math.dist((x1, y1), (x2, y2))
        
        if edge_length == 0:
            raise ValueError("The start and end points are the same!")
        
        # Calculate the normalized direction vector
        direction_x = (x2 - x1) / edge_length
        direction_y = (y2 - y1) / edge_length
        
        # Move start and end points inward by 2*radius
        new_start = (x1 + RADIUS_INWARD * NODE_RADIUS * direction_x, y1 + RADIUS_INWARD * NODE_RADIUS * direction_y)
        new_end = (x2 - RADIUS_INWARD * NODE_RADIUS * direction_x, y2 - RADIUS_INWARD * NODE_RADIUS * direction_y)
        
        return new_start, new_end

    def mouse_over(self, coords: tuple):
        """
        Checks if the mouse is over the edge
        """
        x, y = coords

        new_start, new_end = self.calculate_new_edge_points()

        # Unpack the coordinates of start and end points
        x1, y1 = new_start[0], new_start[1]
        x2, y2 = new_end[0], new_end[1]

        # Calculate the distance from the point to both ends of the edge
        dist_to_start = math.dist((x, y), (x1, y1))

        dist_to_end = math.dist((x, y), (x2, y2))
        edge_length = math.dist((x1, y1), (x2, y2))

        # Check if the sum of distances to the start and end equals the length of the edge (with some tolerance)
        if abs((dist_to_start + dist_to_end) - edge_length) < TOLERANCE:
            return True
        
        return False
    
    def clicked(self):
        self.action = "Add"
        return True
    
    def set_color(self):
        if self.action == "Add":
            self.color = RED
        elif self.action == "Hover":
            self.color = DARK_GRAY
        elif self.action == "Shortest":
            self.color = GREEN
        else:
            self.color = BLACK

    def to_dict(self):
        """Convert Edge to a dictionary."""
        return {
            'start': self.start.name,
            'end': self.end.name,
            'value': self.value
        }
