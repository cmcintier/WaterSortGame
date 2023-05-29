import pygame
from sys import exit

SEARCHING_EVENT = pygame.event.custom_type()


class Tube(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("EmptyTube.png")
        self.rect = self.image.get_rect(topleft = (x,y))
        self.selected = False
        self.isSearching = False
        self.colors = []

    def select(self):
        self.image.set_alpha(100)
        self.selected = True
        print(isSearching)

    def deselect(self):
        self.image.set_alpha(255)
        self.selected = False
    
    def update(self, events, searchEvents):

        if self.isSearching:
            pygame.event.post(pygame.event.Event(SEARCHING_EVENT, color=self.colors))

        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(event.pos):
                    if self.selected:
                        self.deselect()
                        self.isSearching = False
                    else:
                        self.select()
                        if len(searchEvents) == 1:
                            print("Two Selected")
                            self.ifSearching = False
                        else:
                            print("One Selected")
                            self.isSearching = True                   
                    
                    
    
    




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
    isSearching = pygame.event.get(SEARCHING_EVENT)
    events =  pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill("grey")

    tubes.update(events, isSearching)
    tubes.draw(screen)
    screen.blit(text_surface, ((screenWidth/2) - text_surface.get_size()[0]/2 ,100))

    pygame.display.update()
    clock.tick(60)