import pygame
import math
from pygame import gfxdraw
from typing import List
from variables import *
import sys

# Initialize Pygame
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Node:
    def __init__(self, x: int, y: int, name: str):
        self.x = x
        self.y = y
        self.name = name

        self.final = False
        self.action = False

        self.radius = NODE_RADIUS
        self.color = WHITE
        self.border_width = BORDER_WIDTH
        self.border_color = BLACK

        self.value = "MAXINT"
        
    def draw(self, mouse):
        """Draws the node"""

        if self.final == True:
            self.color = GREEN

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
            pygame.draw.line(screen, self.border_color, (self.x, self.y), (mouse.x, mouse.y), self.border_width)

    def mouse_over(self, coords: tuple):
        """Checks if the mouse is over the node"""
        x, y = coords
        if (self.x - x)**2 + (self.y - y)**2 <= self.radius**2:
            
            self.color = LIGHT_GRAY
            return True
        
        self.color = WHITE
        return False

    def clicked(self, coords: tuple):
        """Checks if the mouse clicked on the node amd changes the action to 'move'"""
        self.x, self.y = coords
        self.color = DARK_GRAY
        self.action = "Move"
        return True
    
        
        

class Edge:
    def __init__(self, start: Node, end: Node):
        self.start = start
        self.end = end
        self.action = False
        self.value = ""

        self.color = BLACK
        self.width = EDGE_THICKNESS
        
    def draw(self):
        """Draws the edge"""
        self.set_color()
        
        pygame.draw.line(screen, self.color, (self.start.x, self.start.y), (self.end.x, self.end.y), self.width) 
        text = FONT.render(self.value if self.value else "Add value", True, BLACK)
        screen.blit(text, ((self.start.x + self.end.x) // 2 - text.get_width() // 2 + 20 , (self.start.y + self.end.y) // 2 - text.get_height() // 2 - 20))

    def calculate_new_edge_points(self):
        """
        Calculate new start and end points for an edge that are closer by 2*radius on both ends.

        Parameters:
        start (tuple): (x1, y1) coordinates of the start point (P1)
        end (tuple): (x2, y2) coordinates of the end point (P2)
        radius (float): radius of the node

        Returns:
        tuple: (new_start, new_end) coordinates
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
        """Checks if the mouse is over the edge"""
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
        else:
            self.color = BLACK


class Graph:
    def __init__(self):
        self.nodes: List[Node] = []
        self.edges: List[Edge] = []
        
    def add_node(self, coord: tuple):
        node = Node(*coord, name=self.gen_name())
        self.nodes.append(node)
        
    def add_edge(self, edge: Edge):
        self.edges.append(edge)
    
    def gen_name(self):
        return chr(ord('A') + len(self.nodes))


class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text: str, function=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.text = text
        self.function = function

        self.color = WHITE
        self.border_color = BLACK
        self.border_width = BORDER_WIDTH
        
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, self.border_color, (self.x, self.y, self.width, self.height), self.border_width)

        text = FONT.render(self.text, True, BLACK)
        screen.blit(text, (self.x + self.width / 2 - text.get_width() / 2, self.y + self.height / 2 - text.get_height() / 2))

    
    def mouse_over(self, coords: tuple):
        x, y = coords
        if (self.x <= x <= self.x + self.width) and (self.y <= y <= self.y + self.height):
            self.color = LIGHT_GRAY
            return True
        
        self.color = WHITE
        return False
    
    def clicked(self):
        if self.function is not None:
            self.color = DARK_GRAY
            self.function(((self.x + self.width) * 2 , self.y + self.height))
            return True
    

class Mouse:
    def __init__(self):
        self.x = 0
        self.y = 0


def connect_nodes(graph, connected_nodes):
    """Connect two nodes with an edge"""
    connect = True
    for edge in graph.edges:
        if (edge.start == connected_nodes[0] and edge.end == connected_nodes[1]) or \
           (edge.start == connected_nodes[1] and edge.end == connected_nodes[0]):
            print("Nodes already connected!")
            connect = False
            break

    if connect:
        graph.add_edge(Edge(connected_nodes[0], connected_nodes[1]))
        print(f"Nodes connected: {connected_nodes[0].name}, {connected_nodes[1].name}")
        
    for node in connected_nodes:
        node.action = False


def reset_node_actions(graph):
    """Reset the action of all nodes to 'False'"""
    for node in graph.nodes:
        node.action = False


def handle_numeric_input(event , node: Node):
    # Check for standard numeric keys (0-9)
    """
    Handle numeric input from the user.

    Parameters
    ----------
    event : pygame.event
        The event object from Pygame.
    node : Node
        The node object that the user is currently interacting with.

    Returns
    -------
    str
        The current numeric input as a string. If the user pressed the return key,
        the input is returned and the function exits. Otherwise, the function returns
        the updated input string.
    """
    numeric_input = node.value

    if pygame.K_0 <= event.key <= pygame.K_9:
        numeric_input += chr(event.key) 

    # Check for numeric keypad keys (K_KP0 to K_KP9)
    elif event.key in keypad_mapping:
        numeric_input += keypad_mapping.get(event.key)

    elif event.key == pygame.K_BACKSPACE:
        numeric_input = numeric_input[:-1]

    elif event.key == pygame.K_RETURN:
        node.action = False
        return numeric_input 
    
    return numeric_input


def event_handler(mouse: Mouse, buttons: List[Button], graph: Graph):
    action_node = None
    connected_nodes = []
    final_nodes = []

    for event in pygame.event.get():
        # Quit event handling
        if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

        # Mouse update position
        if event.type == pygame.MOUSEMOTION:
            mouse.x, mouse.y = event.pos
            for button in buttons:
                button.mouse_over((mouse.x, mouse.y))

            for node in graph.nodes:
                node.mouse_over((mouse.x, mouse.y))

            for edge in graph.edges:
                edge.mouse_over((mouse.x, mouse.y))

         # Mouse button click event
        if event.type == pygame.MOUSEBUTTONUP:
            mouse.x, mouse.y = event.pos

            # Button click
            for button in buttons:
                if button.mouse_over((mouse.x, mouse.y)):
                    button.clicked()

            # Edge click
            for edge in graph.edges:
                if edge.mouse_over((mouse.x, mouse.y)):
                    # Reset the action of all edges marked as "Add"
                    for other_edge in graph.edges:
                        if other_edge.action == "Add":
                            other_edge.action = False
                    edge.clicked()
                    break

        # Node dragging with left mouse button
        if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
            for node in graph.nodes:
                if node.mouse_over((mouse.x, mouse.y)):
                    if node.action == "Move":
                        action_node = node
                        break
                    else:
                        action_node = node

            if action_node is not None:
                action_node.clicked((mouse.x, mouse.y))


        # Key event handling
        if event.type == pygame.KEYUP:
            # Create a new node when 'e' is pressed
            if event.key == pygame.K_e:
                graph.add_node((mouse.x, mouse.y))

            # Create a new edge when 'q' is pressed
            elif event.key == pygame.K_q:
                for node in graph.nodes:
                    if node.action == "Connect":
                        connected_nodes.append(node)

                    elif node.mouse_over((mouse.x, mouse.y)):
                        node.action = "Connect"
                        connected_nodes.append(node)
                
                if len(connected_nodes) == 2:
                    connect_nodes(graph, connected_nodes)
                    connected_nodes.clear()  # Reset for next connection

            # Cancel all node actions when 'r' is pressed
            elif event.key == pygame.K_r:
                reset_node_actions(graph)

            # Remove node when 'c' is pressed
            elif event.key == pygame.K_c:
                for node in graph.nodes:
                    if node.mouse_over((mouse.x, mouse.y)):
                        graph.nodes.remove(node)
            
                for edge in graph.edges:
                    if edge.mouse_over((mouse.x, mouse.y)):
                        graph.edges.remove(edge)

            # Mark node as final when 'f' is pressed
            elif event.key == pygame.K_f:
                for node in graph.nodes:
                    if node.final == True:
                        final_nodes.append(node)

                    if node.mouse_over((mouse.x, mouse.y)):
                        node.final = True
                    
                if len(final_nodes) >= 2:
                    for node in final_nodes:
                        node.final = False
                    final_nodes.clear()

            

            else:
                # Get the target edge
                target_edge = next((edge for edge in graph.edges if edge.action == "Add"), None)

                if target_edge is not None:
                    numeric_input = handle_numeric_input(event, target_edge)

                    # If input received, then update the value
                    if numeric_input is not None:
                        target_edge.value = numeric_input


def draw_graph(graph: Graph, mouse: Mouse):
    for edge in graph.edges:
        edge.draw()
    for node in graph.nodes:
        node.draw(mouse=mouse)


def draw_game(graph: Graph, buttons: List[Button], mouse: Mouse):
    screen.fill(WHITE)

    draw_graph(graph, mouse=mouse)
    for button in buttons:
        button.draw()
    pygame.display.update()


def main():
    graph = Graph()
    graph.add_node((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    buttons = []
    buttons.append(Button(10, 10, 100, 50, "Add Node", graph.add_node))
    mouse = Mouse()


    while True:
        event_handler(mouse=mouse, graph=graph, buttons=buttons)
        draw_game(graph, buttons, mouse)
        clock.tick(MAX_FPS)


if __name__ == "__main__":
    main()
