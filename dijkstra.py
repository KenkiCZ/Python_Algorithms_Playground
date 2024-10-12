import pygame
import math
from pygame import gfxdraw
from typing import List, Dict
from queue import PriorityQueue
from variables import *
import sys

# Initialize Pygame
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
buttons = []

def get_mouse_coords():
    mouse = pygame.mouse.get_pos()
    return mouse


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
        if self.action == "Current":
            self.color = BLUE

        if self.root == True:
            self.color = GREEN

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

class Edge:
    def __init__(self, start: Node, end: Node):
        self.start = start
        self.end = end
        self.action = False
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
    
    def get_next_nodes(self, node: Node) -> Dict[Node, int]:
        """Get the next nodes for a given node
        Returns a dictionary with the next nodes and their weights
        """
        
        next_nodes = {}
        for edge in self.edges:
            if edge.start == node:
                next_nodes[edge.end] = edge.value
                edge.end.value = edge.value
            elif edge.end == node:
                next_nodes[edge.start] = edge.value
                edge.start.value = edge.value
                
        
        return next_nodes
    
    def dijkstra_algorithm(self, start: Node):
        # Initialize distances and previous node tracking
        distances = {node: float('infinity') for node in self.nodes}
        distances[start] = 0
        start.value = 0  # Set the starting node value to 0

        pq = PriorityQueue()
        pq.put((0, start))

        previous = {node: None for node in self.nodes}
        visited = set()

        while not pq.empty():
            current_distance, current_node = pq.get()

            if current_node in visited:
                continue

            visited.add(current_node)

            # Update node's value to the current distance from the start node
            current_node.value = current_distance

            # Check if current node is a root (but not the start node)
            if current_node.root and current_node != start:
                print(f"Found a root node (not the starting root): {current_node.name}")
                draw_game(self)
                break

            # Explore neighbors
            for neighbor, weight in self.get_next_nodes(current_node).items():
                if neighbor in visited:
                    continue
                new_distance = current_distance + weight

                # Update distance if a shorter path is found
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current_node
                    pq.put((new_distance, neighbor))

                    # Update neighbor node's value to the new distance
                    neighbor.value = new_distance

            current_node.action = "Current"
            draw_game(self)
            pygame.time.wait(2500)  # Slow down visualization for 2.5 seconds
        
        # Reset node actions after the algorithm finishes
        for node in self.nodes:
            node.action = None

        return previous, distances

    def get_shortest_path(self, start: Node, end: Node):
        """Returns the shortest path from start node to end node using the 'previous' dictionary."""
        previous, distances = self.dijkstra_algorithm(start)
        path = []
        current_node = end

        # Backtrack from the end node to the start node using the previous dictionary
        while current_node is not None:
            path.append(current_node)
            current_node = previous.get(current_node, None)

        path.reverse()

        if path and path[0] == start:
            print(f"Shortest path from {start.name} to {end.name}: {[node.name for node in path]}")
            print(f"Total distance: {distances[end]}")
            return distances[end]
        else:
            print(f"No path found from {start.name} to {end.name}")
            return None
    

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
    numeric_input = str(node.value)
    

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
    
    if not numeric_input:
        numeric_input = "0"
    return numeric_input


def event_handler(buttons: List[Button], graph: Graph):
    action_node = None
    connected_nodes = []
    root_nodes = []

    mouse_x, mouse_y = get_mouse_coords()

    for event in pygame.event.get():
        # Quit event handling
        if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

        # Mouse update position
        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            for button in buttons:
                button.mouse_over((mouse_x, mouse_y))

            for node in graph.nodes:
                node.mouse_over((mouse_x, mouse_y))

            for edge in graph.edges:
                edge.mouse_over((mouse_x, mouse_y))

         # Mouse button click event
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_x, mouse_y = event.pos

            # Button click
            for button in buttons:
                if button.mouse_over((mouse_x, mouse_y)):
                    button.clicked()

            # Edge click
            for edge in graph.edges:
                if edge.mouse_over((mouse_x, mouse_y)):
                    # Reset the action of all edges marked as "Add"
                    for other_edge in graph.edges:
                        if other_edge.action == "Add":
                            other_edge.action = False
                    edge.clicked()
                    break

        # Node dragging with left mouse button
        if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
            for node in graph.nodes:
                if node.mouse_over((mouse_x, mouse_y)):
                    if node.action == "Move":
                        action_node = node
                        break
                    else:
                        action_node = node

            if action_node is not None:
                action_node.clicked((mouse_x, mouse_y))


        # Key event handling
        if event.type == pygame.KEYUP:
            # Create a new node when 'e' is pressed
            if event.key == pygame.K_e:
                graph.add_node((mouse_x, mouse_y))

            # Create a new edge when 'q' is pressed
            elif event.key == pygame.K_q:
                for node in graph.nodes:
                    if node.action == "Connect":
                        connected_nodes.append(node)

                    elif node.mouse_over((mouse_x, mouse_y)):
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
                    if node.mouse_over((mouse_x, mouse_y)):

                        edges_to_delete = []
                        for edge in graph.edges:
                            if edge.start == node or edge.end == node:
                                edges_to_delete.append(edge)

                        for edge in edges_to_delete:
                            graph.edges.remove(edge)
                        graph.nodes.remove(node)
            
                for edge in graph.edges:
                    if edge.mouse_over((mouse_x, mouse_y)):
                        graph.edges.remove(edge)

            # Mark node as root when 'f' is pressed
            elif event.key == pygame.K_f:
                for node in graph.nodes:
                    if node.root == True:
                        root_nodes.append(node)

                    if node.mouse_over((mouse_x, mouse_y)):
                        node.root = True
                    
                if len(root_nodes) >= 2:
                    for node in root_nodes:
                        node.root = False
                    root_nodes.clear()

            # Dijkstra's algorithm when 'space' is pressed
            elif event.key == pygame.K_SPACE:
                root_nodes = [node for node in graph.nodes if node.root]
                if len(root_nodes) == 2:
                    
                        
                    start_node = next((node for node in graph.nodes if node.root), None)
                    if start_node:
                        distance = graph.get_shortest_path(start_node, root_nodes[1])
                        draw_game(graph, distance)
                        pygame.time.wait(5000)

            else:
                # Get the target edge
                target_edge = next((edge for edge in graph.edges if edge.action == "Add"), None)

                if target_edge is not None:
                    numeric_input = int(handle_numeric_input(event, target_edge))

                    # If input received, then update the value
                    if numeric_input is not None:
                        target_edge.value = numeric_input


def draw_game(graph: Graph, score: int = None):
    screen.fill(WHITE)

    if score is not None:
        score_text = SCORE_FONT.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT - score_text.get_height() - 10))

    for edge in graph.edges:
        edge.draw()
    for node in graph.nodes:
        node.draw()
    for button in buttons:
        button.draw()

    pygame.display.update()


def main():
    graph = Graph()
    graph.add_node((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    buttons.append(Button(10, 10, 100, 50, "Add Node", graph.add_node))


    while True:
        event_handler(graph=graph, buttons=buttons)
        draw_game(graph)
        clock.tick(MAX_FPS)


if __name__ == "__main__":
    main()
