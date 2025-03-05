import pygame

# Set up the display and window's title
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Balance Scale')

#Set up background
background = pygame.image.load('balancescale/assets/images/testbackground.jpg')
background = pygame.transform.scale(background, (width, height))
screen.blit(background, (0, 0))
pygame.display.update()