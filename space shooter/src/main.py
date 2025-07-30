import pygame
from os.path import join

pygame.init()
WINDOW_WIDTH, WIDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WIDOW_HEIGHT))
pygame.display.set_caption("Space shooter")
running = True

# sruface
surface = pygame.Surface((100, 200))
surface.fill("orange")
x = 100
y = 150

player_surface = pygame.image.load(join("images", "player.png")).convert_alpha()
start_surface = pygame.image.load(join("images", "star.png")).convert_alpha()

while running:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # draw the game
    # fill the window with red color
    display_surface.fill("darkgray")
    x += 0.1
    display_surface.blit(player_surface, (x, y))
    display_surface.blit(start_surface, (x+100, y))
    pygame.display.update()

pygame.quit()
