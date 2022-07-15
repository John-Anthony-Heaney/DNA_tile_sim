import pygame
import random
import copy
import time
from tileSetList import tileSetList

class Tile :
    def __init__(self, north, east,south,west):
        self.north = north
        self.east = east
        self.south = south
        self.west = west

    def setTilePos(self,x,y):
        self.x = x
        self.y = y

def showTable(size,screenDim):

    squareDim = screenDim/(size+2)
    tableDim = screenDim - squareDim
    for x in range(1,size + 2):
        pygame.draw.line(screen, (0,0,0), (x*squareDim,squareDim), (x*squareDim,tableDim),1)
        pygame.draw.line(screen, (0,0,0), (squareDim,x*squareDim), (tableDim,x*squareDim),1)

def showTile(tile,screenDim,tableSize):

        size = (screenDim/(tableSize+2))/2

        x = size*3 + size *2*tile.x
        y = screenDim-size*3 - size*2*tile.y

        tileColors = {0:(255,222,173),1:(0,255,0),2:(255,0,0)}

        brown = (255,222,173)
        green = (0,255,0)
        red = (255,0,0)
        black = (0,0,0)

        center = (x,y)
        topLeft = (x-size,y-size)
        topRight = (x+size,y-size)
        bottomLeft = (x-size,y+size)
        bottomRight = (x+size,y+size)

        pygame.draw.polygon(screen, tileColors[tile.north], (topLeft,topRight,center))
        pygame.draw.polygon(screen, tileColors[tile.east], (bottomRight,topRight,center))
        pygame.draw.polygon(screen, tileColors[tile.south] ,(bottomLeft,bottomRight,center))
        pygame.draw.polygon(screen, tileColors[tile.west], (topLeft,bottomLeft,center))

        pygame.draw.line(screen, black, topLeft, topRight,1)
        pygame.draw.line(screen, black, bottomLeft, bottomRight,1)
        pygame.draw.line(screen, black, topLeft, bottomLeft,1)
        pygame.draw.line(screen, black, topRight, bottomRight,1)
        pygame.draw.line(screen, black, topLeft, bottomRight,1)
        pygame.draw.line(screen, black, bottomLeft, topRight,1)

        font = pygame.font.Font('freesansbold.ttf', int(size/3))

        textNorth = font.render(str(tile.north), False, black, tileColors[tile.north])
        textEast = font.render(str(tile.east), False, black, tileColors[tile.east])
        textSouth = font.render(str(tile.south), False, black, tileColors[tile.south])
        textWest = font.render(str(tile.west), False, black, tileColors[tile.west])

        textRectNorth = textNorth.get_rect()
        textRectEast = textEast.get_rect()
        textRectSouth = textSouth.get_rect()
        textRectWest = textWest.get_rect()

        textRectNorth.center = (x, y-size/2)
        textRectEast.center =  (x+size/2, y)
        textRectSouth.center = (x, y+size/2)
        textRectWest.center = (x-size/2, y)


        screen.blit(textNorth, textRectNorth)
        screen.blit(textEast, textRectEast)
        screen.blit(textSouth, textRectSouth)
        screen.blit(textWest, textRectWest)

def checkTileND(pos):
        returnTile = None
        numPosTile = 0
        x = pos[0]
        y = pos[1]
        posList = [(x,y+1),(x+1,y),(x,y-1),(x-1,y)]
        for tile in tileSet:
            numTrue = 0
            numFalse = 0
            if(allTiles.get(posList[1]) != None):
                if(tile.east == allTiles.get(posList[1]).west):
                    numTrue +=1
                else:
                    numFalse +=1

            if(allTiles.get(posList[3]) != None):
                if(tile.west == allTiles.get(posList[3]).east):
                    numTrue +=1
                else:
                    numFalse +=1

            if(allTiles.get(posList[0]) != None):
                if(tile.north == allTiles.get(posList[0]).south):
                    numTrue +=1
                else:
                    numFalse +=1

            if(allTiles.get(posList[2]) != None):
                if(tile.south == allTiles.get(posList[2]).north):
                    numTrue +=1
                else:
                    numFalse +=1

            if(numTrue>1 and numFalse == 0):
                returnTile = tile
                numPosTile+=1

            if(numPosTile>1):
                break

        if(numPosTile>1):
            return "undetermined"
        elif(returnTile != None):
            return returnTile
        else:
            return "hole"

def cover(tile):

    x = tile.x
    y = tile.y
    posList = [(x,y+1),(x+1,y),(x,y-1),(x-1,y)]

    for pos in posList:

        if(allTiles.get(pos) == None):
            
            if(pos in possibles):

                tempTile = copy.deepcopy(checkTileD(pos))

                if(type(tempTile) == Tile):
                    tempTile.setTilePos(pos[0],pos[1])

                    newTiles[pos] = tempTile

                possibles.remove(pos)
              
            else:
                possibles.add(pos)

def genTileSetDict(tileSet):
    tileSetDict = {}
    
    for x in tileSetList:
        numPosTile = 0
        returnTile = None
        for tile in tileSet:
            
            tempList = [tile.north==x[0] or x[0]==None,
            tile.east==x[1] or x[1]==None,
            tile.south==x[2] or x[2]==None,
            tile.west==x[3] or x[3]==None]

            if(all(tempList)):
                numPosTile +=1
                if(returnTile == None):
                    returnTile = copy.deepcopy(tile)
                else:
                    break
        if(numPosTile>1):
            tileSetDict[x] = "undetermined"
        elif(returnTile != None):
            tileSetDict[x] = returnTile
        else:
            tileSetDict[x] = "hole"

    return tileSetDict 

def checkTileD(pos):
    lookUpList = [None,None,None,None]
    x = pos[0]
    y = pos[1]
    posList = [(x,y+1),(x+1,y),(x,y-1),(x-1,y)]

    if(allTiles.get(posList[0]) != None):
        lookUpList[0] = allTiles.get(posList[0]).south

    if(allTiles.get(posList[1]) != None):
        lookUpList[1] = allTiles.get(posList[1]).west

    if(allTiles.get(posList[2]) != None):
        lookUpList[2] = allTiles.get(posList[2]).north
          
    if(allTiles.get(posList[3]) != None):
        lookUpList[3] = allTiles.get(posList[3]).east

    
    return tileSetDict[tuple(lookUpList)]

start = time.process_time()

tableSize = 300

tileSet = [Tile(0,0,0,0),Tile(0,1,1,0),Tile(0,2,0,1),Tile(1,0,1,1),Tile(1,1,0,2),Tile(1,2,1,2)]

tileSetDict = genTileSetDict(tileSet)

allTiles = {}

newTiles = {}

prevTiles = {}

for x in range(tableSize):
        tile = copy.deepcopy(tileSet[random.randint(0, 5)])
        tile.setTilePos(x,x)

        allTiles[(x,x)] = tile


possibles = set()

for tile in allTiles.values():
    cover(tile)

prevTiles = copy.deepcopy(newTiles)

while(True):

    for tile in prevTiles.values():
        cover(tile)

    if newTiles == {}:
        break

    allTiles.update(newTiles)

    prevTiles = copy.deepcopy(newTiles)

    newTiles.clear()

print(time.process_time() - start)


pygame.init()

# Set up the drawing window
screenDim = 1000
screen = pygame.display.set_mode([screenDim, screenDim])


# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    showTable(tableSize,screenDim)

    for i in allTiles.values():
        showTile(i,screenDim,tableSize)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()

