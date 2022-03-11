#
# Adavent of Code Template
#
import sys
import math

# Global Variables
filename = ""
inputData = []
maxX = 0
maxY = 0
lowestPoints = []

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


class Height:
    value = 0
    lowestLinear = False
    basin = False
    basinSize = 0
    def __init__(self, v):
        self.value = v

class Point:
    value = 0
    x = 0
    y = 0
    basinSize = 0
    def __init__(self, x, y, v):
        self.x = x
        self.y = y
        self.value = v


#
# Load the file into a data array
#
def loadData(filename):
    global inputData, maxX, maxY

    lines = 0

    f = open(filename)
    for line in f:
        row = []
        for char in line:
            if ord(char) != 10:
                val = ord(char) - 48
                point = Height(val)
                row.append(point)
        inputData.append(row)
        #print(inputData[lines])
        lines += 1

    f.close()
    maxY = len(inputData)
    maxX = len(inputData[0])

    return lines


#
# Print the grid
#
def printGrid():
    global inputData

    for d in inputData:
        rowString = ""
        for p in d:
            if p.lowestLinear:
                rowString += color.YELLOW
            elif p.basin:
                rowString += color.CYAN
            rowString += str(p.value)
            if p.lowestLinear or p.basin:
                rowString += color.END
        print(rowString)


#
# Find lowest point using linear checks
#
def findLowestLinear():
    global inputData, maxX, maxY, lowestPoints

    for y in range(maxY):
        for x in range(maxX):
            p = inputData[y][x]
            if     ((y == 0) or (inputData[y-1][x].value > p.value)) \
               and ((x == 0) or (inputData[y][x-1].value > p.value)) \
               and ((y == maxY-1) or (inputData[y+1][x].value > p.value)) \
               and ((x == maxX-1) or (inputData[y][x+1].value > p.value)):
                p.lowestLinear = True
                lowestPoints.append(Point(x,y,p.value))


#
# Compute the Risk score
#
def computeRisk():
    global lowestPoints
    risk = 0

    #for d in inputData:
    #    rowString = ""
    #    for p in d:
    #        if p.lowestLinear:
    #            risk += p.value + 1

    for p in lowestPoints:
        risk += p.value + 1

    return risk


#
# Find the size of a basin
#
def findBasin(x, y):
    global inputData, maxX, maxY

    size = 1    # Always include current point

    p = inputData[y][x]

    if p.basin:
        # already been here - nothing to add
        return 0

    p.basin = True

    if (y != 0):
        p_next = inputData[y-1][x]
        if (not p_next.basin) and ((p_next.value != 9) and (p.value < p_next.value)):
            size += findBasin(x, y-1)

    if (x != 0):
        p_next = inputData[y][x-1]
        if (not p_next.basin) and ((p_next.value != 9) and (p.value < p_next.value)):
            size += findBasin(x-1, y)

    if (y < maxY-1):
        p_next = inputData[y+1][x]
        if (not p_next.basin) and ((p_next.value != 9) and (p.value < p_next.value)):
            size += findBasin(x, y+1)

    if (x < maxX-1):
        p_next = inputData[y][x+1]
        if (not p_next.basin) and ((p_next.value != 9) and (p.value < p_next.value)):
            size += findBasin(x+1, y)

    return size


#
# find the Basins
#
def findBasins():
    global lowestPoints

    for p in lowestPoints:
        p.basinSize = findBasin(p.x, p.y)



def sortFunc(e):
    return e.basinSize

#
# Find the largest Basins
#
def findLargestBasins(numBasins):
    basins = []

    lowestPoints.sort(reverse=True, key=sortFunc)

    for x in range(numBasins):
        basins.append(lowestPoints[x].basinSize)

    return basins

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
    print("Grid (X,Y): ({:>4},{:>4})".format(maxX, maxY))

    # Do the work
    print()
    print("Lowest Point")
    print()
    findLowestLinear()
    #printGrid()
    risk = computeRisk()
    print("{}Risk: {}{}{}".format(color.CYAN, color.YELLOW, risk, color.END))

    print()
    print("3 Largest Basins")
    print()
    findBasins()
    printGrid()
    largestBasins = findLargestBasins(3)
    answer = math.prod(largestBasins)
    print("{}Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))


if __name__ == "__main__":
    main()
