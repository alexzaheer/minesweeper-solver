import random as rand
import re
#[['?' for i in range(width)]for i in range(height)]

dif = raw_input("Difficulty?(easy, nomral, hard) ").upper()
difD = {'EASY': 5,'NORMAL': 7,'HARD': 10}
numMines = 0
try: wh = difD[dif]*2
except:
    print "-.- the difficulty you chose was not found."
    exit(1)
usrMap = [['?' for i in range(wh)]for i in range(wh)]
alphaDict = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7,'i':8,'j':9,'k':10,'l':11,'m':12,'n':13,'o':14,'p':15,'q':16,'r':17,'s':18,'t':19}
alphaList = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t']
lives = 10
possGuess = re.compile('\\?.[1][0-9]|m.[1][0-9]|\\?..|m..')

def clrField(y,x):
    y = int(y)
    x = int(x)
    global usrMap,mineMap
    usrMap[y][x] = mineMap[y][x]
    try:
        if usrMap[y-1][x-1]=='?' and  y > 0 and x > 0:
            usrMap[y-1][x-1] = mineMap[y-1][x-1]
            if usrMap[y-1][x-1] == '0':
                clrField(y-1,x-1)
        if usrMap[y-1][x]=='?' and y > 0:
            usrMap[y-1][x] = mineMap[y-1][x]
            if usrMap[y-1][x] == '0':
                clrField(y-1,x)
        if usrMap[y-1][x+1]=='?' and y > 0 and x+1 < len(mineMap[0]):
            usrMap[y-1][x+1]= mineMap[y-1][x+1]
            if usrMap[y-1][x+1] == '0':
                clrField(y-1,x+1)
        if usrMap[y][x-1]=='?' and x > 0:
            usrMap[y][x-1]=mineMap[y][x-1]
            if usrMap[y][x-1] == '0':
                clrField(y,x-1)
        if usrMap[y][x+1]=='?' and x+1 < len(mineMap[0]):
            usrMap[y][x+1]=mineMap[y][x+1]
            if usrMap[y][x+1] == '0':
                clrField(y,x+1)
        if usrMap[y+1][x-1]=='?' and y+1<len(mineMap) and x>0:
            usrMap[y+1][x-1]=mineMap[y+1][x-1]
            if usrMap[y+1][x-1] == '0':
                clrField(y+1,x-1)
        if usrMap[y+1][x]=='?' and y+1<len(mineMap):
            usrMap[y+1][x]=mineMap[y+1][x]
            if usrMap[y+1][x] == '0':
                clrField(y+1,x)
        if usrMap[y+1][x+1]=='?' and y+1<len(mineMap) and x+1<len(mineMap[0]):
            usrMap[y+1][x+1]=mineMap[y+1][x+1]
            if usrMap[y+1][x+1] == '0':
                clrField(y+1,x+1)
    except:
        print 'clrField failed.'
def markMap(unMarked):
    for yi,y in enumerate(unMarked):

        for xi,x in enumerate(y):
            if x == 'x' and yi > 0 and xi > 0:
                if unMarked[yi-1][xi-1] != 'x':
                    unMarked[yi-1][xi-1] += 1
            if x == 'x' and yi > 0:
                if unMarked[yi-1][xi] != 'x':
                    unMarked[yi-1][xi] += 1
            if x == 'x' and yi > 0 and xi+1 < len(y):
                if unMarked[yi-1][xi+1] != 'x':
                    unMarked[yi-1][xi+1] += 1
            if x == 'x' and xi > 0:
                if unMarked[yi][xi-1] != 'x':
                    unMarked[yi][xi-1] += 1
            if x == 'x' and xi+1 < len(y):
                if unMarked[yi][xi+1] != 'x':
                    unMarked[yi][xi+1] += 1
            if x == 'x' and yi+1<len(unMarked) and x>0:
                if unMarked[yi+1][xi-1] != 'x':
                    unMarked[yi+1][xi-1] += 1
            if x == 'x' and yi+1<len(unMarked):
                if unMarked[yi+1][xi] != 'x':
                    unMarked[yi+1][xi] += 1
            if x == 'x' and yi+1<len(unMarked) and xi+1<len(y):
                if unMarked[yi+1][xi+1] != 'x':
                    unMarked[yi+1][xi+1] += 1
    for yi,y in enumerate(unMarked):
        for xi,x in enumerate(y):
            unMarked[yi][xi] = str(unMarked[yi][xi])
    return unMarked

def makeMap(w=20,h=20):
    """w = width, h = height

    generates a new map with random mines based on 1/75 chance"""
    global numMines,wh,dif,difD
    newMap = [[0 for i in range(wh)]for i in range(wh)]
    for valx,x in enumerate(newMap):
        for valy,y in enumerate(x):
            if rand.randint(0,difD[dif]) == 1:
                newMap[valy][valx] = 'x'    
                numMines += 1
    return markMap(newMap)
def printMines(xMap):
    global numMines
    global alphaList
    print '    ',alphaList
    for row,x in enumerate(xMap):
        if row < 10:
            print '',row,':',x
        else: print row,':',x
    print "Mines:",numMines


mineMap = makeMap()
printMines(usrMap)

print "If you want to quit, leave guess blank\n'mxx' to guess mine where xx is coords ex (ma0, ma1, mb3) three misses and you lose.\n'?xx' to show space, if it is a mine you lose"
while numMines >0:
    guess = raw_input("Guess: ")
    gMatch = possGuess.findall(guess)
    if not guess:
        break
    elif gMatch:
        for x in gMatch:
            if x[0] == 'm':
                try:
                    gx = mineMap[int(x[2])][alphaDict[x[1]]]
                    if gx == 'x':
                        print 'Hit.'
                        if usrMap[int(x[2])][alphaDict[x[1]]] != 'x':
                            usrMap[int(x[2])][alphaDict[x[1]]] = 'x'
                            numMines -= 1
                        else: print 'You already hit that one >.>'
                    else:
                        print 'Miss'
                        lives -= 0
                        print lives,'lives left'
                        if not lives:
                            print "Game over. Ran out of lives."
                            numMines=0
                            break
                except:
                    print "Guess failed."
            elif x[0] == '?':
               ## try:
                gx = mineMap[int(x[2])][alphaDict[x[1]]]
                if gx == 'x':
                    print 'GAME OVER: hit mine.'
                    numMines=0
                    break
                elif gx == '0':
                    clrField(x[2],alphaDict[x[1]])
                else:
                    print 'Whew.'
                    usrMap[int(x[2])][alphaDict[x[1]]] = mineMap[int(x[2])][alphaDict[x[1]]]
                ##except:
                  ##  print "Guess failed."
            
    else:
        print "o.O um... no."
    if numMines: printMines(usrMap)
print "Thank you for playing."
raw_input("Press enter to exit.")
