import pygame
from sys import exit

class Color(pygame.sprite.Sprite):
    def __init__(self, color, parentTube, fillLevel):
        
        super().__init__()
        self.image = pygame.Surface([50, 50])
        self.image.fill(color)
        pygame.draw.rect(self.image, color, pygame.Rect(parentTube.rect.x+25, parentTube.rect.y + (50*fillLevel), 50, 50))
        self.rect = self.image.get_rect(bottomleft = (parentTube.rect.x+25, parentTube.rect.y + (50*fillLevel)))
        print(self.rect.x)
    

class Tube(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("EmptyTube.png")
        self.rect = self.image.get_rect(topleft = (x,y))
        self.selected = False
        self.colors = []
        self.colorGroup = pygame.sprite.Group()

    def select(self):
        self.image.set_alpha(100)
        self.selected = True

    def deselect(self):
        self.image.set_alpha(255)
        self.selected = False
    
    def setColors(self, colorList):
        self.colors = colorList

    def drawColors(self):
        for fillLevel in range(len(self.colors)):
            self.colorGroup.add(Color(self.colors[fillLevel], self, 4-fillLevel))
        self.colorGroup.update()
        self.colorGroup.draw(screen)

    def removeColor(self):
        self.colorGroup.empty()
        return self.colors.pop(-1)

                    
                    
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
    tube2.colors.append(tube1.removeColor())
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
test_tube1.setColors(["red", "blue"])
test_tube2 = Tube(600, 300)
test_tube2.setColors(["red", "blue"])
tubes.add(test_tube1)
tubes.add(test_tube2)

text_surface = test_font.render("Water Sort Puzzle", False, "Black")

selectedTube = None

while True:

    tubes.update()

    #Checks pygame event system to see if player has quit the game
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

    
    for tube in tubes:
        tube.drawColors()
    tubes.draw(screen)   
    screen.blit(text_surface, ((screenWidth/2) - text_surface.get_size()[0]/2 ,100))

    pygame.display.update()
    clock.tick(60)