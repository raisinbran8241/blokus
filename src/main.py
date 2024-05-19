import pygame
from game import Game

# Game setup
pygame.init()
game = Game(4)
clock = pygame.time.Clock()
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            game.handle_keyboard(event)
        pos = pygame.mouse.get_pos()
        game.handle_mouse(event, pos)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
