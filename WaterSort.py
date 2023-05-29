import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption("Water Sort")
clock = pygame.time.Clock()
running = True

test_surface = pygame.Surface((100,200))
test_surface.fill("red")

while running:

    #Checks pygame event system to see if player has quit the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill("grey")

    screen.blit(test_surface, (200,100))

    pygame.display.update()
    clock.tick(60)

pygame.quit()