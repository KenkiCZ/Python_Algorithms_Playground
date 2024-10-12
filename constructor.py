from variables import *

class Node:
    def __init__(self, x: int, y: int, name: str):
        self.x = x
        self.y = y
        self.name = name

        self.root = False
        self.action = False

        self.radius = NODE_RADIUS
        self.color = WHITE
        self.border_width = BORDER_WIDTH
        self.border_color = BLACK

        self.value = 0
        self.parent = None  # Add parent attribute for path reconstruction
        


class Edge:
    def __init__(self, start: Node, end: Node):
        self.start = start
        self.end = end
        self.action = False
        self.value = 1

        self.color = BLACK
        self.width = EDGE_THICKNESS
        

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


class Graph: