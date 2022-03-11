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

    def getCount(self):
        return (self.xMax-self.xMin+1) * (self.yMax-self.yMin+1) * (self.zMax-self.zMin+1)

    def toTuple(self):
        return (self.xMin, self.xMax, self.yMin, self.yMax, self.zMin, self.zMax)

    def xySets(self):
        sets = []
        for x in range(self.xMin, self.xMax+1):
            for y in range(self.yMin, self.yMax+1):
                s = (x,y)
                sets.append(s)
        return sets


class Step:
    action = 0
    cube = None

    actionString = ["off", "on"]

    def __init__(self, a, c):
        self.action = self.actionString.index(a)
        self.cube = c

    def __str__(self):
        return "{} {}".format(self.actionString[self.action], str(self.cube))


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
# Limit steps
#
def limitSteps(steps, limit):
    limitedSteps = []

    for step in steps:
        if limit.inside(step.cube):
            limitedSteps.append(step)

    return limitedSteps

#
# Calculate all the changes
#
def calculateChanges(steps):

    changes = []

    for step in steps:
        #print(str(step))
        toRemove = []
        for change in changes:
            cube = Cube(*change[0])
            if step.cube.overlap(cube):
                #print("overlap", str(cube), str(step.cube))
                s = (max(cube.xMin, step.cube.xMin), min(cube.xMax, step.cube.xMax), \
                     max(cube.yMin, step.cube.yMin), min(cube.yMax, step.cube.yMax), \
                     max(cube.zMin, step.cube.zMin), min(cube.zMax, step.cube.zMax))
                #print(s)
                toRemove.append([s, change[1] * -1])

        if step.action == 1:
            changes.append([step.cube.toTuple(),1])

        changes.extend(toRemove)

    return changes


#
# Count Lit
#
def countLit(changes):
    count = 0

    for change in changes:
        cube = Cube(*change[0])
        count += cube.getCount() * change[1]

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
    printSteps(steps)

    # Do Part 1 work
    print()
    limit = Cube(-50, 50, -50, 50, -50, 50)
    limitedSteps = limitSteps(steps, limit)
    changes = calculateChanges(limitedSteps)
    #print(changes)
    answer = countLit(changes)
    print()
    print("{}Initialization Cubes On: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))

    # Do Part 2 work
    print()
    changes = calculateChanges(steps)
    answer = countLit(changes)
    print("{}All Cubes On: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))


if __name__ == "__main__":
    main()
