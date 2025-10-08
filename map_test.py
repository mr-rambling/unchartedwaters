import pygame
from pygame.locals import *
import sys
import numpy as np

width, height = 1080, 720

# Load your 2D world map image
image_path = "MapChart_Map.png"  # Change this to your image file
image = pygame.image.load(image_path)

# Convert image to a pixel array (Surface to array)
pixel_array = pygame.surfarray.array3d(image)

def centre_viewport(x, y, viewport_x, viewport_y):
    '''
    returns a viewport Rect of size (viewport_x, viewport_y) centered on coords (x, y)
    '''
    centre_x = x - viewport_x / 2
    centre_y = y - viewport_y / 2
    return pygame.Rect(centre_x, centre_y, viewport_x, viewport_y)    

def map_display():
    # Initialize pygame
    pygame.init()

    # Display the image using pygame window (optional)
    screen = pygame.display.set_mode((width, height))
    surface = pygame.surfarray.make_surface(pixel_array)
    pygame.display.set_caption("2D World Map")

    # Set up font for displaying text
    font = pygame.font.Font(None, 36)

    seville = (4804, 2187)

    left = seville[0]
    top = seville[1]
    subset_rect = centre_viewport(*seville, width, height)

    pygame.key.set_repeat(1, 10)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    left += 5
                if event.key == pygame.K_LEFT:
                    left -= 5
                if event.key == pygame.K_DOWN:
                    top += 5
                if event.key == pygame.K_UP:
                    top -= 5
                    

        subset_rect = centre_viewport(left, top, width, height)
        # Get the current mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Render the coordinates as text
        coord_text = font.render(f"Mouse X: {mouse_x + subset_rect.left}, Mouse Y: {mouse_y + subset_rect.top}", True, (0, 0, 0)) # Black text
        
        screen.fill((0, 0, 0))  # Clear the screen
        screen.blit(surface, (0, 0), subset_rect) # Blit the subset to the top-left of the screen
        screen.blit(coord_text, (mouse_x,mouse_y))
        pygame.display.flip()

    pygame.quit()

# Now, pixel_array contains the RGB values of the image pixels
# pixel_array[x, y] gives the [R, G, B] value at (x, y)

def main():
    map_display()

if __name__ == '__main__':
    main()