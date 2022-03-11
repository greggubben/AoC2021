#
# Adavent of Code Template
#
import sys

# Global Variables
dots = []
folds = []
grid = []
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


class Point:
    x = 0
    y = 0
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "({:>4},{:>4})".format(self.x, self.y)


class Fold:
    axis = ""
    line = 0
    def __init__(self, a, l):
        self.axis = a
        if self.axis == "x":
            self.line = l
        elif self.axis == "y":
            self.line = l
        else:
            raise ValueError("Bad Axis value" + a)

    def __str__(self):
        return "{}={}".format(self.axis, self.line)


#
# Load the file into a data array
#
def loadData(filename):
    global dots

    dots = []
    lines = 0

    loadPoints = True
    loadFolds = False

    f = open(filename)
    for line in f:
        line = line.strip()

        # Load the Fold section of the input file
        if loadFolds:
            parts = line.split(" ")
            foldParts = parts[2].split("=")
            folds.append(Fold(foldParts[0],int(foldParts[1])))

        # a blank line indicates change to fold section
        if len(line) == 0:
            loadPoints = False
            loadFolds = True

        # load dots section
        if loadPoints:
            x,y = line.split(",")
            dots.append(Point(int(x),int(y)))
        lines += 1

    f.close()

    return lines


#
# Create a grid based on Points
#
def createGrid():
    global dots, grid, maxX, maxY

    for p in dots:
        if p.x > maxX: maxX = p.x
        if p.y > maxY: maxY = p.y

    grid = [[False for x in range(maxX+1)] for y in range(maxY+1)]

    for p in dots:
        grid[p.y][p.x] = True

    maxX += 1
    maxY += 1


#
# perform a fold
#
def performFold(fold):
    global dots, grid, maxX, maxY

    #print("Fold:", str(fold))
    #print("MaxY:", maxY)
    #print("MaxX:", maxX)


    startY = 0
    endY = maxY
    startX = 0
    endX = maxX
    if fold.axis == "y":
        startY = fold.line
    elif fold.axis == "x":
        startX = fold.line
    else:
        print(color.RED,"Bad Axis:", fold.axis, color.END)
        return

    # Transfer dots
    for y in range(startY, endY):
        for x in range(startX, endX):
            #print(y,x)
            if grid[y][x]:
                newY = y
                newX = x
                if fold.axis == "y":
                    newY = (fold.line*2) - y
                else:
                    newX = (fold.line*2) - x
                #print("({},{}) -> ({},{})".format(y,x,newY,newX))
                grid[newY][newX] = True

    # Shrink Grid
    for y in range(maxY-1, startY-1, -1):
        if fold.axis == "y":
            grid.pop(y)
        else:
            for x in range(maxX-1, startX-1, -1):
                grid[y].pop(x)

    maxY = len(grid)
    maxX = len(grid[0])


#
# Do the folds
#
def doFolding(limit, printEachFold):
    global folds

    for f in range(limit):
        performFold(folds[f])
        if printEachFold:
            print()
            print("After fold:", str(folds[f]))
            printGrid()


#
# Count the number of Dots in the grid
#
def countDots():
    global grid

    dotCount = 0
    for y in range(maxY):
        for x in range(maxX):
            if grid[y][x]:
                dotCount += 1

    return dotCount


#
# Print Dots
#
def printDots():
    global dots

    for d in dots:
        print("{}".format(str(d)))


#
# Print Folds
#
def printFolds():
    global folds

    for f in folds:
        print("fold along {}".format(str(f)))


#
# Print Grid
#
def printGrid():
    global grid

    for row in grid:        # Y
        rowString = ""
        for dot in row:     # X
            if dot:
                rowString += "#"
            else:
                rowString += "."
        print(rowString)


#
# Main
#
def main():
    global dots, folds

    args = sys.argv[1:]
    if len(args) < 1:
        print("Usage: " + sys.argv[0] + " inputfile [print] [folds]");
        return
    filename = args[0]
    printEachFold = False
    if len(args) >= 2:
        printEachFold = bool(args[1])
    foldLimit = -1
    if len(args) >= 3:
        foldLimit = int(args[2])
    print("  Input File:", filename)
    print(" Print Folds:", printEachFold)
    print(" Limit Folds:", foldLimit)
    print()

    # Load data
    lines = loadData(filename)
    if foldLimit == -1:
        foldLimit = len(folds)
    print("  Lines Read: ", lines)
    print(" Dots Loaded: ", len(dots))
    print("Folds Loaded: ", len(folds))
    print(" Limit Folds:", foldLimit)
    print()

    # Do Part 1 work
    printDots()
    print()
    printFolds()
    print()
    createGrid()
    printGrid()
    doFolding(foldLimit, printEachFold)
    dotCount = countDots()

    print()
    print("{}Number of Dots: {}{}{}".format(color.CYAN, color.YELLOW, dotCount, color.END))


    # Do Part 2 work
    #print()
    #printArray()
    #print()
    #print("{}Answer: {}{}{}".format(color.CYAN, color.YELLOW, "X", color.END))


if __name__ == "__main__":
    main()
