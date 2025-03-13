import pygame
import sys
import random
import datetime
from initialize.display import screen, background # Import the screen and background  

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Balance Scale Simulation")

# Load the background image
background = pygame.image.load("balancescale/assets/images/Rah.jpg.webp")
background = pygame.transform.scale(background, (screen_width, screen_height))

