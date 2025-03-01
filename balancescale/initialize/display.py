import pygame

#Initialize the module
pygame.init()

# Set up the display and window's title
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Balance Scale')

#Set up background
background = pygame.image.load('balancescale/assets/testbackground.jpg')
background = pygame.transform.scale(background, (width, height))
screen.blit(background, (0, 0))
pygame.display.update()

#Render the window
running_state = True
while running_state:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running_state = False

    #Update the display
    pygame.display.flip()