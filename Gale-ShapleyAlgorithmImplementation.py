import pygame
import sys
from typing import List, Tuple
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 800
BACKGROUND_COLOR = (255, 255, 255)
MAN_COLOR = (0, 0, 255)
WOMAN_COLOR = (255, 0, 0)
LINE_COLOR = (0, 255, 0)
TEXT_COLOR = (0, 0, 0)
FONT_SIZE = 20

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gale-Shapley Algorithm Visualization")
font = pygame.font.Font(None, FONT_SIZE)

def draw_people(men_positions, women_positions):
    for i, pos in enumerate(men_positions):
        pygame.draw.circle(screen, MAN_COLOR, pos, 20)
        draw_text(f"M{i}", (pos[0] - 10, pos[1] - 30))
    for i, pos in enumerate(women_positions):
        pygame.draw.circle(screen, WOMAN_COLOR, pos, 20)
        draw_text(f"W{i}", (pos[0] - 10, pos[1] - 30))

def draw_matches(matches, men_positions, women_positions):
    for man, woman in enumerate(matches):
        if woman is not None:
            pygame.draw.line(screen, LINE_COLOR, men_positions[man], women_positions[woman], 2)

def draw_text(text, position):
    text_surface = font.render(text, True, TEXT_COLOR)
    screen.blit(text_surface, position)

def gale_shapley(men_preferences: List[List[int]], women_preferences: List[List[int]]) -> List[Tuple[int, int]]:
    num_men = len(men_preferences)
    num_women = len(women_preferences)

    men_matched = [None] * num_men
    women_matched = [None] * num_women
    men_proposals = [0] * num_men

    # Calculate positions for visualization
    men_positions = [(100, 100 + i * (HEIGHT - 200) // (num_men - 1)) for i in range(num_men)]
    women_positions = [(WIDTH - 100, 100 + i * (HEIGHT - 200) // (num_women - 1)) for i in range(num_women)]

    while None in men_matched:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BACKGROUND_COLOR)
        draw_people(men_positions, women_positions)
        draw_matches(men_matched, men_positions, women_positions)

        man = men_matched.index(None)
        woman = men_preferences[man][men_proposals[man]]
        men_proposals[man] += 1

        draw_text(f"Man {man} proposes to Woman {woman}", (WIDTH // 2 - 100, 50))

        if women_matched[woman] is None:
            women_matched[woman] = man
            men_matched[man] = woman
            draw_text(f"Woman {woman} accepts", (WIDTH // 2 - 100, 80))
        else:
            current_match = women_matched[woman]
            if women_preferences[woman].index(man) < women_preferences[woman].index(current_match):
                men_matched[current_match] = None
                women_matched[woman] = man
                men_matched[man] = woman
                draw_text(f"Woman {woman} prefers Man {man} over Man {current_match}", (WIDTH // 2 - 150, 80))
            else:
                draw_text(f"Woman {woman} rejects Man {man}", (WIDTH // 2 - 100, 80))

        pygame.display.flip()
        pygame.time.wait(1000)  # Wait for 1 second between steps

    matches = list(enumerate(men_matched))
    return matches

# Generate random preferences for 5 men and 5 women
num_people = 10
men_preferences = [random.sample(range(num_people), num_people) for _ in range(num_people)]
women_preferences = [random.sample(range(num_people), num_people) for _ in range(num_people)]

# Print preferences
print("Men's preferences:")
for i, prefs in enumerate(men_preferences):
    print(f"Man {i}: {prefs}")

print("\nWomen's preferences:")
for i, prefs in enumerate(women_preferences):
    print(f"Woman {i}: {prefs}")

final_matches = gale_shapley(men_preferences, women_preferences)

# Display final matches
screen.fill(BACKGROUND_COLOR)
men_positions = [(100, 100 + i * (HEIGHT - 200) // (num_people - 1)) for i in range(num_people)]
women_positions = [(WIDTH - 100, 100 + i * (HEIGHT - 200) // (num_people - 1)) for i in range(num_people)]
draw_people(men_positions, women_positions)
draw_matches([woman for _, woman in final_matches], men_positions, women_positions)
draw_text("Final Matches", (WIDTH // 2 - 50, 50))

# Display final matches as text
for i, (man, woman) in enumerate(final_matches):
    draw_text(f"M{man} - W{woman}", (WIDTH // 2 - 30, 100 + i * 30))

pygame.display.flip()

# Wait for the user to close the window
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()