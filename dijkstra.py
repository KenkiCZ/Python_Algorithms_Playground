from variables import *
from dijkstra_parts import *
from saving import save_graph, load_graph

import pygame
from pygame import gfxdraw
import math
import sys

from typing import List, Dict
from queue import PriorityQueue


# Initialize Pygame
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

graph = None
buttons = []


class Graph:
    def __init__(self):
        self.nodes: List[Node] = []
        self.edges: List[Edge] = []
        
    def add_node(self, node: Node, name: str = None):
        if name == None:
            node.name = self.gen_name()
        self.nodes.append(node)
        
    def add_edge(self, edge: Edge):
        self.edges.append(edge)
    
    def gen_name(self):
        return chr(ord('A') + len(self.nodes))
    
    def get_next_nodes(self, node: Node, visited: List[Node]) -> Dict[Node, int]:
        """
        Get the next nodes for a given node
        Returns a dictionary with the next nodes and their weights
        """
        
        next_nodes = {}
        for edge in self.edges:
            if edge.start == node:
                next_nodes[edge.end] = edge.value
                if edge.end not in visited:
                    edge.end.value = edge.value
            elif edge.end == node:
                next_nodes[edge.start] = edge.value
                if edge.start not in visited:
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
            for neighbor, weight in self.get_next_nodes(current_node, visited).items():
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
            pygame.time.wait(NEXT_NODE_WAIT_TIME)  # Slow down visualization for 2.5 seconds
        
        # Reset node actions after the algorithm finishes
        reset_node_actions(self)

        return previous, distances

    def get_shortest_path(self, start: Node, end: Node):
        """
        Returns the shortest path from start node to end node using the 'previous' dictionary.
        """
        for node in self.nodes:
            node.value = float("infinity")        
        previous, distances = self.dijkstra_algorithm(start)
        path = []
        current_node = end

        # Backtrack from the end node to the start node using the previous dictionary
        while current_node is not None:
            path.append(current_node)
            previous_node = previous.get(current_node, None)
            for edge in self.edges:
                if edge.start == previous_node and edge.end == current_node or edge.end == previous_node and edge.start == current_node:
                    edge.action = "Shortest"
            
            current_node = previous_node
                    

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
            self.function()
            return True
        
class MakeNodeButton(Button):
    def __init__(self, x: int, y: int, width: int, height: int, function=None):
        super().__init__(x, y, width, height, "Create Node", function)
    
    def clicked(self):
        if self.function is not None:
            self.color = DARK_GRAY
            self.function(Node((self.x + self.width) * 2 , self.y + self.height))
            return True
        
class SaveGraphButton(Button):
    def __init__(self, x: int, y: int, width: int, height: int, graph: Graph):
        super().__init__(x, y, width, height, "Save Graph", save_graph)
        self.graph = graph
    
    def clicked(self):
        if self.function is not None:
            self.color = DARK_GRAY
            self.function(self.graph)
            return True
    
class LoadGraphButton(Button):
    def __init__(self, x: int, y: int, width: int, height: int, graph: Graph):
        super().__init__(x, y, width, height, "Load Graph", load_graph)
        self.graph = graph
    
    def clicked(self):
        if self.function is not None:
            self.color = DARK_GRAY

            self.function(self.graph)
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
        node.action = None


def reset_node_actions(graph):
    """Reset the action of all nodes to 'None'"""
    for node in graph.nodes:
        node.action = None


def reset_edge_actions(graph):
    """Reset the action of all edges to 'None'"""
    for edge in graph.edges:
        edge.action = None


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
        node.action = None
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
                graph.add_node(Node(mouse_x, mouse_y))

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
                        pygame.time.wait(END_GAME_WAIT_TIME)

                        reset_node_actions(graph)
                        reset_edge_actions(graph)

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
    buttons.append(MakeNodeButton(10, 10, 100, 50, graph.add_node))
    buttons.append(SaveGraphButton(10, 70, 100, 50, graph))
    buttons.append(LoadGraphButton(10, 130, 100, 50, graph))

    while True:
        event_handler(graph=graph, buttons=buttons)
        draw_game(graph)
        clock.tick(MAX_FPS)


if __name__ == "__main__":
    main()