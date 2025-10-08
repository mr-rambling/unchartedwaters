import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Random Tile Map")

# Tile dimensions
TILE_SIZE = 32
GRID_WIDTH = SCREEN_WIDTH // TILE_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // TILE_SIZE

# Tile colors (example)
GRASS_COLOR = (0, 150, 0)
WATER_COLOR = (0, 0, 150)
MOUNTAIN_COLOR = (100, 100, 100)

# Generate a random map
game_map = []
for y in range(GRID_HEIGHT):
    row = []
    for x in range(GRID_WIDTH):
        tile_type = random.choice(["grass", "water", "mountain"])
        row.append(tile_type)
    game_map.append(row)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the map
    screen.fill((0, 0, 0)) # Clear screen
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            tile_type = game_map[y][x]
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if tile_type == "grass":
                pygame.draw.rect(screen, GRASS_COLOR, rect)
            elif tile_type == "water":
                pygame.draw.rect(screen, WATER_COLOR, rect)
            elif tile_type == "mountain":
                pygame.draw.rect(screen, MOUNTAIN_COLOR, rect)

    pygame.display.flip()

pygame.quit()