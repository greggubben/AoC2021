#
# Adavent of Code Template
#
import sys

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


class Point:
    x = 0
    x = 0

    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __eq__(self,other):
        return (self.x == other.x and self.y == other.y)

    def copy (self):
        return Point(self.x, self.y)

    def __str__(self):
        return "({},{})".format(self.x,self.y)




class TargetArea:
    xMin = 0
    xMax = 0
    yMin = 0
    yMax = 0


#
# Load the file into a data array
#
def loadData(filename):
    targetArea = TargetArea()

    lines = 0

    f = open(filename)
    for line in f:
        line = line.strip()
        if line.startswith("target area: "):
            line = line[13:]
            xPart, yPart = line.split(",")
            # Get the X part
            xCoord = xPart.split("=")
            xTo,d,xFrom = xCoord[1].split(".")
            targetArea.xMin = int(xTo)
            targetArea.xMax = int(xFrom)

            # Get the Y part
            yCoord = yPart.split("=")
            yTo,d,yFrom = yCoord[1].split(".")
            targetArea.yMin = int(yTo)
            targetArea.yMax = int(yFrom)

        lines += 1

    f.close()

    return targetArea, lines


#
# Print Diagram
#
def printDiagram(sub, path, targetArea):
    # then find min and max for x and y from sub, path, and target
    minX = min(sub.x, targetArea.xMin)
    maxX = max(sub.x, targetArea.xMax)
    minY = min(sub.y, targetArea.yMin)
    maxY = max(sub.y, targetArea.yMax)

    for p in path:
        minX = min(minX, p.x)
        maxX = max(maxX, p.x)
        minY = min(minY, p.y)
        maxY = max(maxY, p.y)

    for y in range(maxY,minY-1,-1):
        rowString = ""
        for x in range(minX,maxX+1):
            diagramPoint = Point(x,y)
            if (sub == diagramPoint):
                rowString += color.GREEN + "S" + color.END
            elif (diagramPoint in path):
                rowString += color.RED + "#" + color.END
            elif (targetArea.xMin <= x and x <= targetArea.xMax) and \
                 (targetArea.yMin <= y and y <= targetArea.yMax):
                rowString += color.YELLOW + "T" + color.END
            else:
                rowString += "."
        print(rowString)


#
# Compute Trajectory
#
def computeTrajectory(sub, initialVelocity, targetArea):
    path = []
    hitTarget = False

    path.append(sub)
    nextVelocity = initialVelocity.copy()
    currentPos = sub.copy()
    while (currentPos.x <= targetArea.xMax and currentPos.y >= targetArea.yMin):
        currentPos.x += nextVelocity.x
        currentPos.y += nextVelocity.y
        path.append(currentPos.copy())
        if (targetArea.xMin <= currentPos.x and currentPos.x <= targetArea.xMax) and \
           (targetArea.yMin <= currentPos.y and currentPos.y <= targetArea.yMax):
               hitTarget = True
        if nextVelocity.x < 0:
            nextVelocity.x += 1
        elif nextVelocity.x > 0:
            nextVelocity.x -= 1
        nextVelocity.y -= 1

    return path, hitTarget


#
# Find the max Y position in a path
#
def findMaxY (path):
    maxY = path[0].y

    for p in path:
        if maxY < p.y: maxY = p.y

    return maxY


#
# Find the range of X velocities
#
def findXVelocityRange(startX, targetArea):

    posX = startX
    increment = 1
    while posX < targetArea.xMin:
        posX += increment
        increment += 1

    minX = increment - 1
    print("minX:",minX,"at",posX)

    while posX <= targetArea.xMax:
        posX += increment
        increment += 1

    maxX = increment - 1
    posX -= maxX
    print("maxX:",maxX,"at",posX)

    return minX, maxX


#
# find the range of Y velocities
#
def findYVelocityRange(startY, targetArea):

    minY = abs(startY - targetArea.yMin) - 1
    maxY = abs(startY - targetArea.yMax) - 1

    print("minY", minY, "maxY", maxY)

    return minY, maxY


#
# Find the highest Y for the probe
#
def computeHighestTrajectory(sub, targetArea):

    minX, maxX = findXVelocityRange(sub.x, targetArea)
    minY, maxY = findYVelocityRange(sub.y, targetArea)

    return minX, minY


#
# Find all Distinct Initial Velocities
# This code is biased to target area being below sub
#
def findAllVelocities(sub, targetArea):

    initialVelocities = []

    minX, maxX = findXVelocityRange(sub.x, targetArea)
    minY, maxY = findYVelocityRange(sub.y, targetArea)

    # Start with working from the target area
    for x in range(targetArea.xMin, targetArea.xMax+1):
        for y in range(targetArea.yMin, targetArea.yMax+1):
            # First shot into target always hits
            initialVelocities.append(Point(x,y))

            # Try to see if different steps will also hit the same point
            s = 1
            xVel = x
            yVel = y
            while xVel >= minX and yVel <= 0 and s < x:
                offset = (s * (s+1))/2
                xAdj = x+offset
                yAdj = y+offset

                xVel = int((xAdj)/(s+1))
                yVel = int((yAdj)/(s+1))

                if xAdj%(s+1) == 0 and yAdj%(s+1) == 0 and yVel <= 0:
                    vel = Point(xVel, yVel)
                    if vel not in initialVelocities:
                        initialVelocities.append(vel)

                s += 1

    # work along X Range because less falls short and more goes too far
    for x in range(minX,maxX+1):
        for y in range(minY+1):
            p = Point(x,y)
            path, hitTarget = computeTrajectory(sub,p,targetArea)
            if hitTarget:
                if p not in initialVelocities:
                    initialVelocities.append(p)

    return initialVelocities


#
# Print all the points in a array
#
def printPoints(pointArray):

    pointStrings = []

    for p in pointArray:
        pointStrings.append("{},{}".format(p.x, p.y))

    pointStrings.sort()
    print("\n".join(pointStrings))


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

    # Load data
    targetArea, lines = loadData(filename)
    print(" Lines Read: ", lines)
    print()
    print("Target Area")
    print(" X Min: ", targetArea.xMin)
    print(" X Max: ", targetArea.xMax)
    print(" Y Min: ", targetArea.yMin)
    print(" Y Max: ", targetArea.yMax)

    sub = Point(0,0)
    print()
    print("Sub")
    print(" X: ", sub.x)
    print(" Y: ", sub.y)
    # Do Part 1 work
    #sample = Point(7,9)
    #path = computeTrajectory(sub,sample,targetArea)
    #print()
    #printDiagram(sub,path,targetArea)
    #answer = findMaxY(path)

    print()
    x,y = computeHighestTrajectory(sub,targetArea)
    highestVelocity = Point(x,y)
    path, hitTarget = computeTrajectory(sub,highestVelocity,targetArea)
    print("Highest Velocity: ", str(highestVelocity))
    maxheight = findMaxY(path)
    #print()
    #printDiagram(sub,path,targetArea)

    print()
    print("{}Max Y: {}{}{}".format(color.CYAN, color.YELLOW, maxheight, color.END))

    # Do Part 2 work
    print()
    possibleVelocities = findAllVelocities(sub, targetArea)
    distinctInitialVelocities = len(possibleVelocities)

    #printPoints(possibleVelocities)

    print()
    print("{}Distinct Initial Velocities: {}{}{}".format(color.CYAN, color.YELLOW, distinctInitialVelocities, color.END))


if __name__ == "__main__":
    main()
