#
# Adavent of Code Template
#
import sys

# Global Variables
filename = ""
inputData = []
maxX = 0
maxY = 0
grid = []

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

# Defines an X,Y cartesian point
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Defines a line with start point and end point
class Line:
    def __init__(self, start, end):
        self.start = start
        self.end   = end


#
# Create a point from text
#
def getPoint(text):
    global maxX, maxY
    xText, yText = text.split(",")
    x = int(xText)
    y = int(yText)
    p = Point(x, y)

    # find max values incase it is important later
    if x > maxX:
        maxX = x
    if y > maxY:
        maxY = y

    # return the point
    return p


#
# Create a line from text
#
def getLine(startText, endText):
    startPoint = getPoint(startText)
    endPoint = getPoint(endText)
    l = Line(startPoint, endPoint)
    return l


#
# Load the file into a data array
#
def loadData(filename):
    global inputData

    lines = 0

    f = open(filename)
    for line in f:
        startText, command, endText = line.split()
        l = getLine(startText, endText)
        inputData.append(l)
        #print(inputData[lines])
        lines += 1

    f.close()

    return lines


#
# Initialize the Grid
#
def initGrid():
    global grid, maxX, maxY

    grid = [[0 for y in range(maxY+1)] for x in range(maxX+1)]


#
# Draw Horizontal and Vertical lines only
#
def drawHorizVertLines():
    global inputData
    verticalLines = 0
    horizontalLines = 0
    direction = ""

    for line in inputData:
        direction = "Skip"
        if line.start.x == line.end.x:
            drawVerticalLine(line)
            verticalLines += 1
            direction = "Vertical"
        elif line.start.y == line.end.y:
            drawHorizontalLine(line)
            horizontalLines += 1
            direction = "Horizontal"
        #print("{},{} -> {},{} {}".format(line.start.x, line.start.y, line.end.x, line.end.y, direction))

    return horizontalLines, verticalLines


#
# Draw Diagonal lines only
#
def drawDiagonalLines():
    global inputData
    diagonalLines = 0
    direction = ""

    for line in inputData:
        direction = "Skip"
        if line.start.x == line.end.x:
            direction = "Done"
        elif line.start.y == line.end.y:
            direction = "Done"
        else:
            drawDiagonalLine(line)
            diagonalLines += 1
            direction = "Diagonal"
        #print("{},{} -> {},{} {}".format(line.start.x, line.start.y, line.end.x, line.end.y, direction))

    return diagonalLines


#
# Draw a horizontal line
#
def drawHorizontalLine(line):
    global grid

    y = line.start.y
    lowX = line.start.x
    highX = line.end.x

    if line.start.x > line.end.x:
        lowX = line.end.x
        highX = line.start.x

    for x in range(lowX, highX+1):
        grid[x][y] += 1


#
# Draw a verical line
#
def drawVerticalLine(line):
    global grid

    x = line.start.x
    lowY = line.start.y
    highY = line.end.y

    if line.start.y > line.end.y:
        lowY = line.end.y
        highY = line.start.y

    for y in range(lowY, highY+1):
        grid[x][y] += 1


#
# Draw a diagonal line
# only 45 degree
#
def drawDiagonalLine(line):
    global grid

    low = line.start.x
    high = line.end.x
    dirY = 1
    dirX = 1

    if line.start.y > line.end.y:
        dirY = -1

    if line.start.x > line.end.x:
        dirX = -1
        low = line.end.x
        high = line.start.x

    distance = high - low
    for p in range(distance+1):
        grid[line.start.x+(p*dirX)][line.start.y+(p*dirY)] += 1


#
# Count how many lines are at each point
#
def countPoints():
    global grid
    zeroPoints = 0
    onePoints = 0
    multPoints = 0

    for x in range(maxX+1):
        for y in range(maxY+1):
            p = grid[x][y]
            if p == 0:
                zeroPoints += 1
            elif p == 1:
                onePoints += 1
            else:
                multPoints += 1
    return zeroPoints, onePoints, multPoints
    

#
# Print the grid
#
def printGrid():
    global grid

    for y in range(maxY+1):
        rowString = ""
        for x in range(maxX+1):
            p = grid[x][y]
            if p == 0:
                rowString += "."
            elif p == 1:
                rowString += "1"
            else:
                rowString += color.YELLOW + str(p) + color.END
        print(rowString)


#
# Main
#
def main():
    global filename, inputData

    args = sys.argv[1:]
    if len(args) != 1:
        print("Usage: " + sys.argv[0] + " inputfile");
        return
    filename = args[0]
    print("Input File:", filename)

    # Load data
    lines = loadData(filename)
    print(" Lines Read: ", lines)
    print("Data Loaded: ", len(inputData))
    print()
    print("Max X: ", maxX)
    print("Max Y: ", maxY)
    print()

    # Do the work
    print("Horizontal and Vertical")
    initGrid()
    horizontalLines, verticalLines = drawHorizVertLines()
    zeroPoints, onePoints, multPoints = countPoints()
    print("H Lines: {:>3}".format(horizontalLines))
    print("V Lines: {:>3}".format(verticalLines))
    print("Zero Points: {:>5}".format(zeroPoints))
    print(" One Points: {:>5}".format(onePoints))
    print("{}Mult Points: {}{:>5}{}".format(color.CYAN, color.YELLOW, multPoints, color.END))
    #printGrid()

    print()
    print("Horizontal, Vertical, and Diagonal")
    diagonalLines = drawDiagonalLines()
    zeroPoints, onePoints, multPoints = countPoints()
    print("D Lines: {:>3}".format(diagonalLines))
    print("Zero Points: {:>5}".format(zeroPoints))
    print(" One Points: {:>5}".format(onePoints))
    print("{}Mult Points: {}{:>5}{}".format(color.CYAN, color.YELLOW, multPoints, color.END))
    #printGrid()



if __name__ == "__main__":
    main()
