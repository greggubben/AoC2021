#
# Adavent of Code Template
#
import sys
from heapq import heappush, heappop

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


'''
    Finished solution should look like this:

    #############
    #...........#
    ###A#B#C#D###
      #A#B#C#D#
      #########

'''

ENERGY = {"A":1, "B":10, "C":100, "D":1000}
HALLSTOPS = [0,1,3,5,7,9,10]
HALLLENGTH = 11
ENTRANCES = {"A":2, "B":4, "C":6, "D":8}
ROOMS = 4
roomDepth = 2
amphipodTypes = ["A", "B", "C", "D"]


#
# Load the file into a data array
#
def loadData(filename):

    lines = []
    burrow = ""

    f = open(filename,"r")
    for c in f.read():
        if c in "ABCD.":
            burrow += c

    f.close()

    return burrow


#
# Print Array
#
def printLines(lines):

    for line in lines:
      print(line)


#
# Print Burrow
#
def printBurrow(burrow):

    burrowString = "#############\n#"

    for p in range(len(burrow)):
        occupant = burrow[p]
        burrowString += (color.CYAN if occupant == "." else color.YELLOW) + occupant + color.END
        if p >= HALLLENGTH:
            burrowString += "#"
        if p == HALLLENGTH-1:
            burrowString += "#\n###"
        elif p == HALLLENGTH+ROOMS-1:
            burrowString += "##\n  #"
        elif p>=HALLLENGTH and (p-HALLLENGTH+1)%ROOMS == 0:
            burrowString += "  \n  #"

    burrowString += "########"

    print(burrowString)


#
# Print the changes in the burrow (paths) to the solution
#
def printPath(path):
    for burrow in path:
        print()
        printBurrow(burrow)


#
# See if the path is clear
#
def pathClear(startPos, endPos, burrow):
    step = 1 if startPos < endPos else -1
    for pos in range(startPos+step, endPos+step, step):
        if burrow[pos] != ".":
            return False
    return True


#
# Get hallway possibilities
#
def getHallPositions(entrancePos, burrow):
    for hallPos in [pos for pos in HALLSTOPS if burrow[pos] == "."]:
        if pathClear(entrancePos, hallPos, burrow):
            yield hallPos


#
# See if the Amphipod can leave its room
#
def canLeaveRoom(burrow, roomPoses):
    for roomPos in roomPoses:
        if burrow[roomPos] == ".":
            continue
        return roomPos, True

    return -1, False


#
# See if the Amphipod can enter its room
#
def canEnterRoom(startPos, amphipod, burrow, roomPos):
    entrancePos = ENTRANCES[amphipod]
    bestPos = -1
    for pos in roomPos:
        if burrow[pos] == ".":
            bestPos = pos
        elif burrow[pos] != amphipod:
            return -1, False
    if pathClear(startPos, entrancePos, burrow):
        return bestPos, True
    else:
        return -1, False


#
# move the amphipod
#
def move(pos1, pos2, burrow):
    b = list(burrow)
    b[pos1], b[pos2] = b[pos2], b[pos1]
    return "".join(b)


#
# Get the possible moves
#
def getPossibleMoves(burrow, target):
    # handle Hallway to Room first - can only go into a room
    for startPos in [pos for pos in HALLSTOPS if burrow[pos] != "."]:
        a = burrow[startPos]
        endPos, canEnter = canEnterRoom(startPos, a, burrow, target[a])
        if canEnter:
            yield startPos, endPos

    # handle Room to Hallway
    for room in "ABCD":
        startPos, canLeave = canLeaveRoom(burrow,target[room])
        if canLeave:
            for endPos in getHallPositions(ENTRANCES[room], burrow):
                yield startPos, endPos


#
# Find the least amount of energy to get amphipods into their rooms
#
def findLeastEnergy(burrow):
    target = {r: [p for p in range(HALLLENGTH+n,len(burrow),ROOMS)] for n,r in enumerate('ABCD')}
    print("target\n", target)
    targetI = {v:key for key,val in target.items() for v in val}
    print("targetI\n", targetI)
    solution = "."*HALLLENGTH + "ABCD"*((len(burrow)-HALLLENGTH)//ROOMS)
    print("solution\n", solution)
    print("burrow\n", burrow)

    stuffToEvaluate = [(0,burrow,[burrow])]
    evaluated = {burrow:0}

    while stuffToEvaluate:
        evalCost, evalState, evalPath = heappop(stuffToEvaluate)
        if evalState == solution: return evalCost, evalPath   # Least expensive found
        for startPos, endPos in getPossibleMoves(evalState, target):
            hallPos, roomPos = (startPos, endPos) if startPos < endPos else (endPos, startPos)
            entrancePos = ENTRANCES[targetI[roomPos]]
            hallDistance = abs(entrancePos - hallPos)
            roomDistance = (roomPos - HALLLENGTH)//4 + 1
            distance = hallDistance + roomDistance
            newCost = evalCost + distance * ENERGY[evalState[startPos]]
            newState = move(startPos, endPos, evalState)
            newPath = evalPath.copy()
            newPath.append(newState)
            if evaluated.get(newState, 999999) > newCost:
                evaluated[newState] = newCost
                heappush(stuffToEvaluate,(newCost, newState, newPath))


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
    burrow = loadData(filename)
    print(" Characters Read: ", len(burrow))
    print()

    # Do Part 1 work
    #printLines(lines)
    printBurrow(burrow)
    answer, path = findLeastEnergy(burrow)
    printPath(path)
    print()
    print("{}Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))

    # Do Part 2 work
    #print()
    #printLines(lines)
    #print()
    #print("{}Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))


if __name__ == "__main__":
    main()
