import pygame

pygame.init()
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
running = True

while running:

    #Checks pygame event system to see if player has quit the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("grey")

    pygame.display.flip()

    clock.tick(60)

pygame.quit()