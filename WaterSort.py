import pygame
from sys import exit

class Tube(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("EmptyTube.png")
        self.rect = self.image.get_rect(topleft = (x,y))



pygame.init()
screenWidth = 1280
screenHeight = 720
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Water Sort")
clock = pygame.time.Clock()
test_font = pygame.font.Font(None, 50)

tubes = pygame.sprite.Group()
numTubes = 6
for i in range(numTubes):
    tubes.add(Tube( screenWidth / numTubes * i + (screenWidth/4/ numTubes), 300))


text_surface = test_font.render("Water Sort Puzzle", False, "Black")

while True:

    #Checks pygame event system to see if player has quit the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill("grey")

    # screen.blit(empty_tube, (200,100))
    tubes.draw(screen)
    screen.blit(text_surface, ((screenWidth/2) - text_surface.get_size()[0]/2 ,100))
    

    pygame.display.update()
    clock.tick(60)

pygame.quit()