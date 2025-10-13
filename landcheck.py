import pygame
import random
import pickle
from constants import *

pygame.init()

def create():
    image_path = "images/MapChart_Map.png"  # Change this to your image file
    image = pygame.image.load(image_path)

    pixel_array = pygame.surfarray.array3d(image)
    gamemap = pygame.surfarray.make_surface(pixel_array)

    land = []
    print(gamemap.get_size())
    for x in range(gamemap.get_size()[0]):
        land.append([])
        for y in range(gamemap.get_size()[1]):
            if gamemap.get_at((x, y)) == LAND_COLOR:
                land[x].append(True)
            else:
                land[x].append(False)

    file = 'data/landcheck.pkl'
    with open(file, 'wb') as file:
        pickle.dump(land, file)
    