import math
import random
import time

#creates both players
def init():
    global humanPlayer, aiPlayer
    humanPlayer = Player(True)
    aiPlayer = Player(False)

class Victory(Exception):
    """Triggers victory screen and ends the game"""

class Player:
    def __init__(self, human, shipsHP = [0, 2, 3, 3, 4, 5]):
        """Creates a player object with the above ships. If the shipsHp argument is not provided, it will default"""
        self.human = human
        self.playerDefeatFlag = False
        self.shipsPlaced = 0
        self.ships = [[], [], [], [], [], [], [], [], [], []]
        self.tracking = [[], [], [], [], [], [], [], [], [], []]
        self.shipsHP = [0, 2, 3, 3, 4, 5]
        for y in range(0,10):
            for x in range(0,10):
                self.ships[y].append(0)
                self.tracking[y].append(0)
        self.gameIsAlive = True
        if not self.human:
            self.initialize()
    def turn(self):
        #checks if c is non-empty
        if self.human:
            self.userInput()
        else:
            #do ai turn
            print("AI turn")
            time.sleep(0.7)
            x = random.randint(0,9)
            y = random.randint(0,9)
            #repeat until a cell was found that was not shot at yet
            while self.tracking[x][y]:
                x = random.randint(0,9)
                y = random.randint(0,9)
            print("Ai fires")
            if humanPlayer.checkIfHit((x,y)):
                print("You were hit!")
                self.tracking[x][y] = 2
            else:
                print("The computer missed")
                self.tracking[x][y] = 1
    def printGrid(self):
        #move to ui
        num = "   "
        for n in range(1,11):
            s = " " + str(n) + " "
            num += s
        num += "    "
        for n in range(1,11):
            s = " " + str(n) + " "
            num += s
        print(num)
        for y in range(0,10):
            line = chr(y+65) + " ["
            for x in range(0,10):
                #water
                if (self.ships[x][y] == 0):
                    s = "~"
                elif (self.ships[x][y] == -1):
                    s = "#"
                #hit water
                elif (self.ships[x][y] == -2):
                    s = "*"
                #hit ship
                elif (self.ships[x][y] == -3):
                    s = "X"
                elif (self.ships[x][y] >= 1 and self.ships[x][y] <= 5):
                    s = "O"
                else:
                    raise Exception("That shouldn't have happened. Wrong number in the players grid at " + str((x,y)))
                line += " " + s + " "
            line += "] "+ chr(y+65) + " ["
            for x in range(0,10):
                #not yet hit
                if (self.tracking[x][y] == 0):
                    line += "   "
                #water
                elif (self.tracking[x][y] == 1):
                    line += " ~ "
                #enemy ship
                elif (self.tracking[x][y] == 2):
                    line += " X "
            line += "]"
            print(line)
            line = ""
        print("\n\n")
    def checkIfHit(self, c):
        """Checks if a shot was a hit or miss"""
        x = c[0]
        y = c[1]
        if (self.ships[x][y] > 0):
            self.ships[x][y] = -3
            self.shipsHP[self.ships[x][y]] -= 1
            self.checkForDefeat
            return True
        else:
            self.ships[x][y] = -2
            return False
    def checkForDefeat(self):
        """defeat condition"""
        if (sum(self.shipsHP) == 0):
            self.gameIsAlive = False
            self.playerDefeatFlag = True
            raise Victory()
            return True
        return False
    def initialize(self):
        """Initializes the ai player"""
        for n in range(1, len(self.shipsHP)+1):
            self.tryPlacement(6-n, self.shipsHP[6-n])
        for x in range(0,10):
            for y in range(0,10):
                if (self.ships[x][y] == -1):
                    self.ships[x][y] = 0
    def tryPlacement(self, index, length, coord=(0,0)):
        """Ai function to place ships"""
        horiz = random.randint(0,1)
        x = random.randint(0,9)
        y = random.randint(0,9)
        call = 0
        coord = (x,y)
        while not self.validatePlacement(coord, horiz, length):
            horiz = random.randint(0,1)
            coord = (random.randint(0,9),random.randint(0,9))
            call+=1
            if (call > 1000):
                printGrid(self.ships)
                raise Exception("Failed placement")
        self.surroundShip(coord, horiz, length)
        self.placeShip(coord, horiz, length, index)
    def validatePlacement(self, coord, horiz, length):
        #coord is a tuple of the starting point(x,y)
        #horiz is 1 if the ship is horizontal (y const)
        #length is the length of the ship    
        #ships is the 2d list for ship placement
        horiz = bool(horiz)
        if horiz:
            if (coord[0]+length > 9):
                return False
            for x in range(coord[0], coord[0]+length):
                #0 means empty water not neighboring an existing ship
                if (self.ships[x][coord[1]] != 0):
                    return False
        else:
            if (coord[1]+length > 9):
                return False
            for y in range(coord[1], coord[1]+length):
                #0 means empty water not neighboring an existing ship
                if (self.ships[coord[0]][y] != 0):
                    return False
        return True

    def surroundShip(self, coord, horiz, length):
        #is called before the ship is placed
        horiz = bool(horiz)
        x = coord[0]
        y = coord[1]
        call = 0
        if horiz:
            for a in range(x-1, x+length+1):
                for b in range(y-1, y+2):
                    if (a <= 9 and a >= 0 and b <= 9 and b >= 0):
                        call+=1
                        self.ships[a][b] = -1
        else:
            for b in range(y-1, y+length+1):
                for a in range(x-1, x+2):
                    if (a <= 9 and a >= 0 and b <= 9 and b >= 0):
                        call+=1
                        self.ships[a][b] = -1


    def placeShip(self, coord, horiz, length, index):
        """Is called after placement is validated, and surrounding area has been marked with -1"""
        if horiz:
            for x in range(coord[0], coord[0]+length):
                self.ships[x][coord[1]] = index #index = number of ship>=1
        else:
            for y in range(coord[1], coord[1]+length):
                self.ships[coord[0]][y] = index

    def userInput(self):
        self.printGrid()
        if (self.shipsPlaced < 5):
            try:
                print("You have to place your ships.")
                self.userPlaceShip()
            except:
                print("Please try again.")
                if (self.shipsPlaced < 5):
                    self.userInput()
        if (self.shipsPlaced >= 5):
            for x in range(0,10):
                for y in range(0,10):
                    if (self.ships[x][y] == -1):
                        self.ships[x][y] = 0
                self.shipsPlaced = 6
        s = input("Please enter target coordinates: ")
        c = convert(s)
        x = c[0]
        y = c[1]
        time.sleep(0.7)
        if aiPlayer.checkIfHit(c):
            self.tracking[x][y] = 2
            print("You hit!")
        else:
            self.tracking[x][y] = 1
            print("You missed!")
        return True


    def userPlaceShip(self):
        index = self.shipsPlaced+1
        length = self.shipsHP[-index]
        print("Please place a ship of length " + str(length))
        s = input("Enter the upper or left end of the ship and its direction (h=horizontal, v=vertical)")
        if not (len(s) == 3 or len(s) == 4):
            raise Exception("Please enter exactly three characters.")
        horiz = 0
        if (s.endswith("h")):
            horiz = 1
        elif (s.endswith("v")):
            horiz = 0
        else:
            raise Exception("Please enter either h or v.")
        s = s[:-1]
        coord = convert(s)
        if not self.validatePlacement(coord, horiz, length):
            raise Exception("Please adhere to the rules regarding the placement of ships.")
        else:
            self.surroundShip(coord, horiz, length)
            self.placeShip(coord, horiz, length, index)
            self.shipsPlaced += 1
            raise Exception #this will leab back to the except block

def convert(s):
    """Converts a two character string (eg. A7) to the corresponding coordinate tuple"""
    s.capitalize()
    x = 0
    y = 0
    if (s[0] >= "A" and s[0] <= "J"):
        y = ord(s[0]) - ord("A")
    else:
        raise Exception("Please enter a character from A to J.")
    s = s[1:]
    if not s.isdigit():
        raise Exception("Please enter a number from 1 to 10.")
    if (int(s) >= 1 and int(s) <= 10):
        x = int(s)-1
    else:
        raise Exception("Please enter a number from 1 to 10.")
    return (x,y)
