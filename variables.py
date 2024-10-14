import pygame
from screeninfo import get_monitors
pygame.font.init()


def get_screen_size():
    monitor = get_monitors()[0]
    return monitor.width, monitor.height


# DEFINITIONS of time
NEXT_NODE_WAIT_TIME = 300
END_GAME_WAIT_TIME = 5000


# DEFINITIONS of paths
SAVE_PATH = "graph_3.json"
LOAD_PATH = "graph_2.json"

# DEFINIONS of colors

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# DEFINITIONS of sizes
NODE_RADIUS = 30
BORDER_WIDTH = 3

SCREEN_WIDTH, SCREEN_HEIGHT = get_screen_size()
SCREEN_HEIGHT -= 80
SCREEN_WIDTH -= 80
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# DEFINITIONS of edges
EDGE_THICKNESS = 5

RADIUS_INWARD = 1
TOLERANCE = 0.12

# DEFINITIONS of fonts
FONT_SIZE = 10
FONT = pygame.font.SysFont('Arial', FONT_SIZE, bold=True)
SCORE_FONT = pygame.font.SysFont('Arial', 30, bold=True)

# DEFINITIONS of FPS
MAX_FPS = 60

# Number mapping
keypad_mapping = {
    pygame.K_KP0: '0',
    pygame.K_KP1: '1',
    pygame.K_KP2: '2',
    pygame.K_KP3: '3',
    pygame.K_KP4: '4',
    pygame.K_KP5: '5',
    pygame.K_KP6: '6',
    pygame.K_KP7: '7',
    pygame.K_KP8: '8',
    pygame.K_KP9: '9'
}

