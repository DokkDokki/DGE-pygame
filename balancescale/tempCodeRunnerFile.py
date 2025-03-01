# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Draw the background
    display.screen.blit(display.background, (0, 0))

    # Draw the text on the screen
    display.screen.blit(title.text, title.text_rect)

    # Update the display
    pygame.display.flip()
    
    # Break the loop immediately
    running = False

# Quit pygame and exit program after the main loop ends
pygame.quit()
sys.exit()