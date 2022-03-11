#
# Adavent of Code Template
#
import sys

# Global Variables
inputData = []
maxX = 0
maxY = 0

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


class Octopus:
    energy = 0
    flashed = False
    def __init__(self, e):
        self.energy = e
        self.flashed = False


#
# Load the file into a data array
#
def loadData(filename):
    global inputData, maxX, maxY

    lines = 0
    inputData = []

    f = open(filename)
    for line in f:
        line = line.strip()
        rowData = []
        for c in line:
            rowData.append(Octopus(int(c)))
        inputData.append(rowData)
        #print(inputData[lines])
        lines += 1

    f.close()
    maxY = len(inputData)
    maxX = len(inputData[0])

    return lines


#
# Print Grid
#
def printGrid(flashes = -1):
    global inputData

    for y in range(maxY):
        rowString = ""
        for x in range(maxX):
            o = inputData[y][x]
            if o.flashed:
                rowString += color.YELLOW
            rowString += str(o.energy)
            if o.flashed:
                rowString += color.END
        print(rowString)
    if flashes != -1:
        print("Flashes:", flashes)


#
# Reset any Flashes
#
def resetFlashes():
    global inputData

    for r in inputData:
        for c in r:
            c.flashed = False


#
# See if all octopi flashed
#
def allFlashed():
    global inputData

    allFlashed = True

    for r in inputData:
        for c in r:
            if not c.flashed:
                allFlashed = False
                break
        if not allFlashed:
            break

    return allFlashed


#
# Perform a flash on this octopus
#
def addEnergy(y,x, level=0):
    global inputData, maxX, maxY

    level += 1
    indent = "  " * level
    #print(indent, "Add ({:>2},{:>2})".format(y,x))

    flashes = 0
    o = inputData[y][x]
    if not o.flashed:
        o.energy += 1
        if o.energy > 9:
            o.flashed = True
            o.energy = 0
            flashes += 1

            flashMinY = y-1
            if flashMinY < 0: flashMinY = 0
            flashMaxY = y+1
            if flashMaxY == maxY: flashMaxY = maxY-1
            flashMinX = x-1
            if flashMinX < 0: flashMinX = 0
            flashMaxX = x+1
            if flashMaxX == maxX: flashMaxX = maxX-1
            #print(indent, "FLASH @({:>2},{:>2}): ({:>2},{:>2}) -> ({:>2},{:>2})".format(y,x,flashMinY, flashMinX, flashMaxY, flashMaxX))

            for flashY in range(flashMinY, flashMaxY+1):
                for flashX in range(flashMinX, flashMaxX+1):
                    #print(indent,"Adding ({:>2},{:>2})".format(flashY,flashX))
                    flashes += addEnergy(flashY, flashX, level)

    return flashes



#
# Increase energy by 1
#
def increaseEnergy():
    global maxX, maxY

    flashes = 0
    for y in range(maxY):
        for x in range(maxX):
            flashes += addEnergy(y,x)

    return flashes


#
# Advance through the number of steps
#
def advanceSteps(steps, printInterval):
    global inputData

    flashes = 0
    for s in range(steps):
        
        resetFlashes()
        flashes += increaseEnergy()

        if ((s+1) % printInterval) == 0:
            print()
            print("After step {}:".format(s+1))
            printGrid(flashes)

    return flashes


#
# Advance through the number of steps
#
def advanceUntilAllFlash(printInterval):
    global inputData

    flashes = 0
    steps = 0


    while (not allFlashed()):
        
        resetFlashes()
        steps += 1
        flashes += increaseEnergy()

        #if ((steps) % printInterval) == 0:
        #    print()
        #    print("After step {}:".format(steps))
        #    printGrid(flashes)

    return steps, flashes


#
# Main
#
def main():
    global inputData

    args = sys.argv[1:]
    if len(args) != 3:
        print("Usage: " + sys.argv[0] + " inputfile steps print_interval");
        return
    filename = args[0]
    steps = int(args[1])
    printInterval = int(args[2])
    print("    Input File:", filename)
    print("         Steps:", steps)
    print("Print Interval:", printInterval)

    # Load data
    lines = loadData(filename)
    print(" Lines Read: ", lines)
    print("Data Loaded: ", len(inputData))

    # Do Part 1 work
    print()
    print("Before any Steps:")
    printGrid()
    flashes = advanceSteps(steps, printInterval)
    print()
    print("{}Flashes after {} Steps: {}{}{}".format(color.CYAN, steps, color.YELLOW, flashes, color.END))

    # Do Part 2 work
    print()
    lines = loadData(filename)
    print(" Lines Read: ", lines)
    print("Data Loaded: ", len(inputData))
    allFlashStep,flashes = advanceUntilAllFlash(printInterval)
    print()
    print("{}First Step when all Flash: {}{}{}".format(color.CYAN, color.YELLOW, allFlashStep, color.END))


if __name__ == "__main__":
    main()
