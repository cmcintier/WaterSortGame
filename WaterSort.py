import pygame
import random as r
from sys import exit

COLOR_LIST = ["red", "orange", "yellow", "green", "blue", "purple"," pink", "navy"]

class Color(pygame.sprite.Sprite):
    def __init__(self, color, parentTube, fillLevel):
        
        super().__init__()
        self.image = pygame.Surface([50, 190/4])
        self.image.fill(color)
        pygame.draw.rect(self.image, color, pygame.Rect(parentTube.rect.x+25, parentTube.rect.y + (190/4*fillLevel), 50, 190/4))
        self.rect = self.image.get_rect(bottomleft = (parentTube.rect.x+25, parentTube.rect.y + (190/4*fillLevel)))
    

class Tube(pygame.sprite.Sprite):
    def __init__(self, x, y, colorList = []):
        super().__init__()
        self.image = pygame.image.load("EmptyTube.png")
        self.rect = self.image.get_rect(topleft = (x,y))
        self.selected = False
        self.colors = colorList
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

    if tube1FillHeight == 0:   # tube1 is empty (nothing to pour)
        return False
    elif tube2FillHeight == 0: # tube2 is empty
        return True
    elif tube2FillHeight == 4: # tube2 is full
        return False
    elif tube1.colors[-1] == tube2.colors[-1]: # colors are compatible
        return True
    elif tube1.colors[-1] != tube2.colors[-1]: # colors are incompatible
        return False

def pourColor(tube1, tube2):
    tube2.colors.append(tube1.removeColor())
    # recursivly calls itself if colors are the same to continuously pour multiple of the same color
    if checkCompatible(tube1, tube2):
        pourColor(tube1, tube2)

def generatePuzzle(colorList):
    numTubes = len(colorList) + 2
    tubes = pygame.sprite.Group()
    allColors = colorList + colorList + colorList + colorList
    for x in range(numTubes):
        if x < numTubes - 2:
            tubeColors = []
            for i in range(4):
                l = len(allColors)
                if l == 1:
                    color = allColors.pop(0)
                else:
                    randChoice = r.randint(0, l-1)
                    color = allColors.pop(randChoice)
                tubeColors.append(color)     
            
            tube = Tube(screenWidth / numTubes * x + (screenWidth/4/ numTubes), 300, tubeColors)
            tubes.add(tube)
        else:
            print("balls")
            tube = Tube(screenWidth / numTubes * x + (screenWidth/4/ numTubes), 300, [])
            tubes.add(tube)
    
    return tubes

def checkWinState(tubes):
    totalColors = len(tubes) - 2
    fullCount = 0
    for tube in tubes:
        colors = tube.colors
        if len(tube.colors) == 4 and colors[0] == colors [1] and colors[0] == colors[2] and colors[0] == colors[3]:
            fullCount += 1
    return totalColors == fullCount


pygame.init()
screenWidth = 1280
screenHeight = 720
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Water Sort")
clock = pygame.time.Clock()
test_font = pygame.font.Font(None, 50)

tubes = generatePuzzle(COLOR_LIST[0:6])
text_surface = test_font.render("Water Sort Puzzle", False, "Black")
text_win = test_font.render("YOU WIN", False, "Green")

selectedTube = None

while True:

    tubes.update()

    #Handling pygame's event system
    events =  pygame.event.get()
    for event in events:
        # QUIT Event
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # MOUSEBUTTONUP Event to check collisions
        elif event.type == pygame.MOUSEBUTTONUP:
            print(selectedTube)
            for tube in tubes:
                if tube.rect.collidepoint(event.pos):
                    print(tube.colors)
                    #deselecting tube
                    if tube == selectedTube:
                        selectedTube = None
                        tube.deselect()
                    #No tube selected
                    elif selectedTube == None:
                        selectedTube = tube
                        tube.select()
                        break
                    #first tube is already selected
                    else:
                        if checkCompatible(selectedTube, tube):
                            pourColor(selectedTube, tube)
                        selectedTube.deselect()
                        selectedTube = None
                   
    #DRAW
    screen.fill("grey")
    for tube in tubes:
        tube.drawColors()
    tubes.draw(screen)   
    screen.blit(text_surface, ((screenWidth/2) - text_surface.get_size()[0]/2 ,100))
    if checkWinState(tubes):
        screen.blit(text_win, ((screenWidth/2) - text_surface.get_size()[0]/2 ,200))

    pygame.display.update()
    clock.tick(60)