import pygame
import sys
import random
from queue import PriorityQueue

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
NODE_RADIUS = 20
FONT = pygame.font.Font(None, 36)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dijkstra's Algorithm Visualization")

class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def add_node(self, node):
        x = random.randint(NODE_RADIUS, WIDTH - NODE_RADIUS)
        y = random.randint(NODE_RADIUS, HEIGHT - NODE_RADIUS)
        self.nodes[node] = (x, y)
        self.edges[node] = {}

    def add_edge(self, start, end, weight):
        self.edges[start][end] = weight
        self.edges[end][start] = weight

def dijkstra(graph, start):
    distances = {node: float('infinity') for node in graph.nodes}
    distances[start] = 0
    pq = PriorityQueue()
    pq.put((0, start))
    previous = {node: None for node in graph.nodes}

    while not pq.empty():
        current_distance, current_node = pq.get()

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph.edges[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                pq.put((distance, neighbor))
                
        draw_graph(graph, distances, previous, current_node)
        pygame.time.wait(1500)  # Delay to slow down the visualization

    return distances, previous

def draw_graph(graph, distances, previous, current_node):
    screen.fill(WHITE)

    # Draw edges
    for start, ends in graph.edges.items():
        for end in ends:
            start_pos = graph.nodes[start]
            end_pos = graph.nodes[end]
            pygame.draw.line(screen, BLACK, start_pos, end_pos, 2)

    # Draw nodes
    for node, pos in graph.nodes.items():
        color = BLUE if node == current_node else RED
        pygame.draw.circle(screen, color, pos, NODE_RADIUS)
        node_text = FONT.render(str(node), True, WHITE)
        screen.blit(node_text, (pos[0] - 10, pos[1] - 10))

        # Draw distance
        if distances[node] < float('infinity'):
            distance_text = FONT.render(str(distances[node]), True, GREEN)
            screen.blit(distance_text, (pos[0] - 15, pos[1] + 30))

    pygame.display.flip()

def main():
    graph = Graph()
    
    # Add nodes
    for i in range(6):
        graph.add_node(i)

    # Add edges
    graph.add_edge(0, 1, 4)
    graph.add_edge(0, 2, 2)
    graph.add_edge(1, 2, 1)
    graph.add_edge(1, 3, 5)
    graph.add_edge(2, 3, 8)
    graph.add_edge(2, 4, 10)
    graph.add_edge(3, 4, 2)
    graph.add_edge(3, 5, 6)
    graph.add_edge(4, 5, 3)

    start_node = 0
    dijkstra(graph, start_node)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()