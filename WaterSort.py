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
    
class Button():
    def __init__(self, x, y, width, height, buttonText = "Button", onclickFunction=None):
        self.onclickFunction = onclickFunction

        self.image = pygame.Surface([50, 190/4])
        self.image.fill("white")
        pygame.draw.rect(self.image, color, pygame.Rect(x, y, width, height))
        self.rect = self.image.get_rect(bottomleft = (x,y))

        self.buttonSurface = pygame.Surface((self.rect.width, self.rect.height))
        self.buttonRect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        self.buttonSurf = test_font.render(buttonText, True, (20, 20, 20))
    
    def update(self):
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)

    def onclick(self, puzzleSize):
        tempColors = COLOR_LIST.copy()
        colorList = []
        for i in range(puzzleSize):
            colorIndex = r.randint(0, len(tempColors) - 1)
            colorList.append(tempColors.pop(colorIndex))
        return self.onclickFunction(colorList)

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

# TEXT
text_surface = test_font.render("Water Sort Puzzle", False, "Black")
text_win = test_font.render("YOU WIN", False, "Green")


user_text = ''
input_rect = pygame.Rect(screenWidth / 2 - 50, 600, 100, 32)
color_active = pygame.Color("lightskyblue3")
color_passive = pygame.Color('chartreuse4')
color = color_passive

generatePuzzleButton = Button(screenWidth/2-25, 700, 25, 25, "Generate New Puzzle", generatePuzzle)
active = False

selectedTube = None

while True:
    newPuzzle = False

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
            if generatePuzzleButton.rect.collidepoint(event.pos):
                tubes = generatePuzzleButton.onclick(int(user_text))
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
        # MOUSEBUTTONDOWN Event to check player click input
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                active = True
            else:
                active = False
        # KEYDOWN Event for receiving input
        elif event.type == pygame.KEYDOWN:
  
            # Check for backspace
            if event.key == pygame.K_BACKSPACE:
  
                # get text input from 0 to -1 i.e. end.
                user_text = user_text[:-1]
  
            # Unicode standard is used for string
            # formation
            else:
                user_text += event.unicode       
    
    if active:
        color = color_active
    else:
        color = color_passive
    
    

    #DRAW
    screen.fill("grey")
    for tube in tubes:
        tube.drawColors()
    tubes.draw(screen)   
    screen.blit(text_surface, ((screenWidth/2) - text_surface.get_size()[0]/2 ,100))
    
    generatePuzzleButton.update()

    pygame.draw.rect(screen, color, input_rect)
    text_surface = test_font.render(user_text, True, (0, 0, 0))
    input_rect.w = max(100, text_surface.get_width()+10)
    
    # render at position stated in arguments
    screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))

    if checkWinState(tubes):
        screen.blit(text_win, ((screenWidth/2) - text_surface.get_size()[0]/2 ,200))

    pygame.display.update()
    clock.tick(60)