import pygame
from sys import exit

SEARCHING_EVENT = pygame.event.custom_type()


class Tube(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("EmptyTube.png")
        self.rect = self.image.get_rect(topleft = (x,y))
        self.selected = False
        self.colors = []

    def select(self):
        self.image.set_alpha(100)
        self.selected = True

    def deselect(self):
        self.image.set_alpha(255)
        self.selected = False
    
    def setColors(self, colorList):
        self.colors = colorList

                    
                    
def checkCompatible(tube1, tube2):
    tube1FillHeight = len(tube1.colors)
    tube2FillHeight = len(tube2.colors)

    if tube1FillHeight == 0:
        return False
    elif tube2FillHeight == 0:
        return True
    elif tube2FillHeight == 4:
        return False
    elif tube1.colors[-1] == tube2.colors[-1]:
        return True
    elif tube1.colors[-1] != tube2.colors[-1]:
        return False

def pourColor(tube1, tube2):
    tube2.colors.append(tube1.colors.pop(-1))
    if checkCompatible(tube1, tube2):
        pourColor(tube1, tube2)



pygame.init()
screenWidth = 1280
screenHeight = 720
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Water Sort")
clock = pygame.time.Clock()
test_font = pygame.font.Font(None, 50)

tubes = pygame.sprite.Group()
# numTubes = 6
# for i in range(numTubes):
#     tubes.add(Tube( screenWidth / numTubes * i + (screenWidth/4/ numTubes), 300))
test_tube1 = Tube(300, 300)
test_tube1.setColors(["red", "green"])
test_tube2 = Tube(600, 300)
test_tube2.setColors(["red", "green"])
tubes.add(test_tube1)
tubes.add(test_tube2)

text_surface = test_font.render("Water Sort Puzzle", False, "Black")

selectedTube = None


while True:

    
    

    #Checks pygame event system to see if player has quit the game
    isSearching = pygame.event.get(SEARCHING_EVENT)
    events =  pygame.event.get()
    for event in events:
        # QUIT Event
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            print(selectedTube)
            for tube in tubes:
                if tube.rect.collidepoint(event.pos):
                    print(tube.colors)
                    if tube == selectedTube:
                        selectedTube = None
                        tube.deselect()
                    elif selectedTube == None:
                        selectedTube = tube
                        tube.select()
                        break
                    else:
                        if checkCompatible(selectedTube, tube):
                            pourColor(selectedTube, tube)
                        selectedTube.deselect()
                        selectedTube = None
                   
                    


    screen.fill("grey")

    tubes.draw(screen)
    screen.blit(text_surface, ((screenWidth/2) - text_surface.get_size()[0]/2 ,100))

    pygame.display.update()
    clock.tick(60)