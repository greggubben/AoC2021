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


#
# Load the file into a data array
#
def loadData(filename):

    lines = []

    f = open(filename)
    for line in f:
        line = line.strip()
        l = list(line)
        lines.append(l)

    f.close()

    return lines


#
# Print Array
#
def printFloor(lines):

    for line in lines:
      print("".join(line))


#
# Find the east and south going sea cucumbers
#
def findSeaCucumbers(floor):
    east = []
    south = []

    for row, rowFloor in enumerate(floor):
        for col, colFloor in enumerate(rowFloor):
            if colFloor == ">":
                heappush(east,(row,col))
            elif colFloor == "v":
                heappush(south,(row,col))

    return east, south


#
# Move all sea cucumbers East
#
def moveEast(east, floor):
    newEast = []

    queuedChanges = []

    moved = False
    while len(east) > 0:
        row,col = heappop(east)
        nextCol = col + 1 if col + 1 < len(floor[0]) else 0
        if floor[row][nextCol] == ".":
            queuedChanges.append((row,col,"."))
            queuedChanges.append((row,nextCol,">"))
            heappush(newEast,(row,nextCol))
        else:
            heappush(newEast,(row,col))

    moved = len(queuedChanges) > 0

    for row,col,val in queuedChanges:
        floor[row][col] = val

    return newEast, moved


#
# Move all sea cucumbers South
#
def moveSouth(south, floor):
    newSouth = []

    queuedChanges = []

    moved = False
    while len(south) > 0:
        row,col = heappop(south)
        nextRow = row + 1 if row + 1 < len(floor) else 0
        if floor[nextRow][col] == ".":
            queuedChanges.append((row,col,"."))
            queuedChanges.append((nextRow,col,"v"))
            heappush(newSouth,(nextRow,col))
        else:
            heappush(newSouth,(row,col))

    moved = len(queuedChanges) > 0

    for row,col,val in queuedChanges:
        floor[row][col] = val

    return newSouth, moved


#
# Move unil all the sea cucumbers can't move anymore
#
def moveUntilStop(floor):

    east, south = findSeaCucumbers(floor)

    moves = 0

    moved = True

    while moved:
        moved = False
        east, eastMoved = moveEast(east,floor)
        south, southMoved = moveSouth(south,floor)
        moved = eastMoved or southMoved
        moves += 1
        #print("Move:",moves)
        #printFloor(floor)

    return moves


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
    floor = loadData(filename)
    print("      Lines Read: ", len(floor))
    print(" Floor (row,col): ({},{})".format(len(floor), len(floor[0])))
    print()

    # Do Part 1 work
    printFloor(floor)
    moves = moveUntilStop(floor.copy())
    #print("east:", len(east), "south:", len(south))
    print()
    print("{}Moves: {}{}{}".format(color.CYAN, color.YELLOW, moves, color.END))

    # Do Part 2 work
    #print()
    #printLines(lines)
    #print()
    #print("{}Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))


if __name__ == "__main__":
    main()
