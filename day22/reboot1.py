#
# Adavent of Code Template
#
import sys
import numpy as np

# Global Variables

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


class Cube:
    xMin = 0
    xMax = 0
    yMin = 0
    yMax = 0
    zMin = 0
    zMax = 0

    def __init__(self, x1, x2, y1, y2, z1, z2):
        self.xMin = min(x1, x2)
        self.xMax = max(x1, x2)

        self.yMin = min(y1, y2)
        self.yMax = max(y1, y2)

        self.zMin = min(z1, z2)
        self.zMax = max(z1, z2)

    def __str__(self):
        return "x={}..{},y={}..{},z={}..{}".format(self.xMin, self.xMax, self.yMin, self.yMax, self.zMin, self.zMax)

    def inside(self, smaller):
        return self.xMin <= smaller.xMin and smaller.xMax <= self.xMax and \
               self.yMin <= smaller.yMin and smaller.yMax <= self.yMax and \
               self.zMin <= smaller.zMin and smaller.zMax <= self.zMax

    def overlap(self, other):
        return self.xMin <= other.xMax and self.xMax >= other.xMin and \
               self.yMin <= other.yMax and self.yMax >= other.yMin and \
               self.zMin <= other.zMax and self.zMax >= other.zMin

    def betweenX(self, value):
        return self.xMin <= value and value <= self.xMax

    def betweenY(self, value):
        return self.yMin <= value and value <= self.yMax

    def betweenZ(self, value):
        return self.zMin <= value and value <= self.zMax

    def size(self):
        return (self.xMax-self.xMin+1) * (self.yMax-self.yMin+1) * (self.zMax-self.zMin+1)

    def toTuple(self):
        return (self.xMin, self.xMax, self.yMin, self.yMax, self.zMin, self.zMax)


class Step:
    action = 0
    cube = None

    actionString = ["off", "on"]

    def __init__(self, a, c):
        self.action = self.actionString.index(a)
        self.cube = c

    def __str__(self):
        return "{} {}".format(self.actionString[self.action], str(self.cube))


class Section:
    state = 0
    count = 0

    def __init__(self, s, c):
        self.state = s
        self.count = c


#
# Load the file into a data array
#
def loadData(filename):

    lines = []
    steps = []

    f = open(filename)
    for line in f:
        x1 = x2 = y1 = y2 = z1 = z2 = 0
        line = line.strip()
        action, cube = line.split()
        dims = cube.split(",")
        for dim in dims:
            axis, range_ = dim.split("=")
            range1, _, range2 = range_.split(".")
            range1 = int(range1)
            range2 = int(range2)
            if axis == "x":
                x1 = range1
                x2 = range2
            elif axis == "y":
                y1 = range1
                y2 = range2
            elif axis == "z":
                z1 = range1
                z2 = range2

        steps.append(Step(action, Cube(x1, x2, y1, y2, z1, z2)))
        lines.append(line)

    f.close()

    return steps, lines


#
# Print Lines
#
def printLines(lines):

    for line in lines:
      print(line)


#
# Print Steps
#
def printSteps(steps):

    for step in steps:
      print(str(step))


#
# Limit boundary of number
def bound (low, high, value):
    return max(low, min(high, value))


#
# Turn on/off cubes within limit bounds by following the step
#
def setCubes(steps, limit):
    cubes = {}

    for step in steps:
        if step.cube.xMin > limit.xMax or step.cube.xMax < limit.xMin or \
           step.cube.yMin > limit.yMax or step.cube.yMax < limit.yMin or \
           step.cube.zMin > limit.zMax or step.cube.zMax < limit.zMin:
            continue

        xStart = bound(limit.xMin, limit.xMax, step.cube.xMin)
        xEnd = bound(limit.xMin, limit.xMax, step.cube.xMax)
        yStart = bound(limit.yMin, limit.yMax, step.cube.yMin)
        yEnd = bound(limit.yMin, limit.yMax, step.cube.yMax)
        zStart = bound(limit.zMin, limit.zMax, step.cube.zMin)
        zEnd = bound(limit.zMin, limit.zMax, step.cube.zMax)

        for x in range(xStart,xEnd+1):
            for y in range(yStart,yEnd+1):
                for z in range(zStart,zEnd+1):
                    s = (x,y,z)
                    cubes[s] = step.action

    return cubes



#
# Find all the sets in range
#
def getSets(xMin,xMax,yMin,yMax,zMin,zMax):
    sets = []

    xMinIn = xMin + 1
    xMaxIn = xMax - 1
    yMinIn = yMin + 1
    yMaxIn = yMax - 1
    zMinIn = zMin + 1
    zMaxIn = zMax - 1

    # Points
    sets.append((xMin,xMin, yMin,yMin, zMin,zMin))
    sets.append((xMax,xMax, yMin,yMin, zMin,zMin))
    sets.append((xMin,xMin, yMax,yMax, zMin,zMin))
    sets.append((xMin,xMin, yMin,yMin, zMax,zMax))
    sets.append((xMax,xMax, yMax,yMax, zMin,zMin))
    sets.append((xMax,xMax, yMin,yMin, zMax,zMax))
    sets.append((xMin,xMin, yMax,yMax, zMax,zMax))
    sets.append((xMax,xMax, yMax,yMax, zMax,zMax))

    # Lines
    if xMinIn <= xMaxIn:
        sets.append((xMinIn,xMaxIn, yMin,yMin, zMin,zMin))
        sets.append((xMinIn,xMaxIn, yMax,yMax, zMin,zMin))
        sets.append((xMinIn,xMaxIn, yMin,yMin, zMax,zMax))
        sets.append((xMinIn,xMaxIn, yMax,yMax, zMax,zMax))
    if yMinIn <= yMaxIn:
        sets.append((xMin,xMin, yMinIn,yMaxIn, zMin,zMin))
        sets.append((xMax,xMax, yMinIn,yMaxIn, zMin,zMin))
        sets.append((xMin,xMin, yMinIn,yMaxIn, zMax,zMax))
        sets.append((xMax,xMax, yMinIn,yMaxIn, zMax,zMax))
    if zMinIn <= zMaxIn:
        sets.append((xMin,xMin, yMin,yMin, zMinIn,zMaxIn))
        sets.append((xMax,xMax, yMin,yMin, zMinIn,zMaxIn))
        sets.append((xMin,xMin, yMax,yMax, zMinIn,zMaxIn))
        sets.append((xMax,xMax, yMax,yMax, zMinIn,zMaxIn))

    # Planes
    if xMinIn <= xMaxIn and yMinIn <= yMaxIn:
        sets.append((xMinIn,xMaxIn, yMinIn,yMaxIn, zMin, zMin))
        sets.append((xMinIn,xMaxIn, yMinIn,yMaxIn, zMax, zMax))
    if yMinIn <= yMaxIn and zMinIn <= zMaxIn:
        sets.append((xMin,xMin, yMinIn,yMaxIn, zMinIn, zMaxIn))
        sets.append((xMax,xMax, yMinIn,yMaxIn, zMinIn, zMaxIn))
    if xMinIn <= xMaxIn and zMinIn <= zMaxIn:
        sets.append((xMinIn,xMaxIn, yMin,yMin, zMinIn, zMaxIn))
        sets.append((xMinIn,xMaxIn, yMax,yMax, zMinIn, zMaxIn))

    # Grid
    if xMinIn <= xMaxIn and yMinIn <= yMaxIn and zMinIn <= zMaxIn:
        sets.append((xMinIn,xMaxIn,yMinIn,yMaxIn,zMinIn,zMaxIn))


    # Dedup
    sets = list(dict.fromkeys(sets))

    return sets


#
# Check if a Cube is contained in a Step's Cube
#
def inSteps(cube, steps):
    found = False

    for step in steps:
        found = step.cube.inside(cube)
        if found:
            break

    return found


#
# Turn on/off cubes by following the step
#
def setCubesNoLimit(steps):
    cubes = {}

    # determin all breaks in cubes
    xs = []
    ys = []
    zs = []

    for step in steps:
        if step.cube.xMin not in xs: xs.append(step.cube.xMin)
        if step.cube.xMax not in xs: xs.append(step.cube.xMax)
        if step.cube.yMin not in ys: ys.append(step.cube.yMin)
        if step.cube.yMax not in ys: ys.append(step.cube.yMax)
        if step.cube.zMin not in zs: zs.append(step.cube.zMin)
        if step.cube.zMax not in zs: zs.append(step.cube.zMax)

    xs.sort()
    ys.sort()
    zs.sort()

    #print("x", xs)
    #print("y", ys)
    #print("z", zs)

    # Build structure to hold cubes initialized to off
    for xPos in range(len(xs)-1):
        for yPos in range(len(ys)-1):
            for zPos in range(len(zs)-1):
                if inSteps(Cube(xs[xPos],xs[xPos+1],ys[yPos],ys[yPos+1],zs[zPos],zs[zPos+1]),steps):
                    sets = getSets(xs[xPos], xs[xPos+1], ys[yPos], ys[yPos+1], zs[zPos], zs[zPos+1])
                    #print(xs[xPos], xs[xPos+1], ys[yPos], ys[yPos+1], zs[zPos], zs[zPos+1])
                    #print(sets)
                    for s in sets:
                        (xMin,xMax, yMin,yMax, zMin,zMax) = s
                        count = (xMax-xMin+1) * (yMax-yMin+1) * (zMax-zMin+1)
                        cubes[s] = Section(0, count)

    # Perform the Steps
    for step in steps:
        print(str(step))
        xSteps = []
        xPos = xs.index(step.cube.xMin)
        while xPos < len(xs) and xs[xPos] <= step.cube.xMax:
            xSteps.append(xs[xPos])
            xPos += 1
        if len(xSteps) == 1:
            xSteps.append(xSteps[0])
        ySteps = []
        yPos = ys.index(step.cube.yMin)
        while yPos < len(ys) and ys[yPos] <= step.cube.yMax:
            ySteps.append(ys[yPos])
            yPos += 1
        if len(ySteps) == 1:
            ySteps.append(ySteps[0])
        zSteps = []
        zPos = zs.index(step.cube.zMin)
        while zPos < len(zs) and zs[zPos] <= step.cube.zMax:
            zSteps.append(zs[zPos])
            zPos += 1
        if len(zSteps) == 1:
            zSteps.append(zSteps[0])

        for xPos in range(len(xSteps)-1):
            for yPos in range(len(ySteps)-1):
                for zPos in range(len(zSteps)-1):
                    sets = getSets(xSteps[xPos], xSteps[xPos+1], ySteps[yPos], ySteps[yPos+1], zSteps[zPos], zSteps[zPos+1])
                    for s in sets:
                        #print(s, step.action, cubes[s].count)
                        cubes[s].state = step.action

    return cubes


#
# sum the amount on
#
def sumCubesOn(cubes):
    count = 0

    for c in cubes.values():
        if c.state == 1:
            count += c.count

    return count


#
# Main
#
def main():

    args = sys.argv[1:]
    if len(args) != 1:
        print("Usage: " + sys.argv[0] + " inputfile");
        return
    filename = args[0]
    print("Input File:", filename)
    print()

    # Load data
    steps, lines = loadData(filename)
    print("  Lines Read: ", len(lines))
    print("Steps Loaded: ", len(steps))
    print()

    # Do Part 1 work
    print()
    #printLines(lines)
    printSteps(steps)
    limit = Cube(-50, 50, -50, 50, -50, 50)
    cubes = setCubes(steps, limit)
    answer = sum(cubes.values())
    print()
    print("{}Initialization Cubes On: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))

    # Do Part 2 work
    print()
    cubes = setCubesNoLimit(steps)
    #print(cubes)
    answer = sumCubesOn(cubes)
    print("{}All Cubes On: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))


if __name__ == "__main__":
    main()
