#
# Adavent of Code Template
#
import sys
from collections import deque

# Global Variables
filename = ""
fish = []
fishByAge = deque([0 for f in range(9)])
days = 0

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
    global fish

    lines = 0

    f = open(filename)
    for line in f:
        fishesString = line.split(",")
        lines += 1
        for fishString in fishesString:
            inFish = int(fishString)
            fish.append(inFish)
            fishByAge[inFish] += 1

    f.close()

    return lines


#
# Replace with real work
#
def printFish():
    global fish

    fishString = ""
    sep = ""
    for f in fish:
        if f == 0:
            fishString += sep + color.RED + str(f) + color.END
        elif f == 8:
            fishString += sep + color.GREEN + str(f) + color.END
        else:
            fishString += sep + str(f)
        sep = ","
    return fishString


#
# Simulate each day passing by using an array representing each fish
#
def simulateDaysSlow(days):
    global fish

    dayString = "day "
    newFish = 0
    for d in range(1,days+1):
        newFish = 0
        for f in range(len(fish)):
            fish[f] -= 1
            if fish[f] < 0:
                fish[f] = 6
                newFish += 1

        for f in range(newFish):
            fish.append(8)

        #print("After {:>2} {}: {}".format(d, dayString, printFish()))
        dayString = "days"

    return len(fish)


#
# Simulate each day passing by using an array of how many fish at that age
#
def simulateDaysFast(days):
    global fishByAge

    #dayString = "day "
    newFish = 0
    for d in range(1,days+1):
        newFish = fishByAge.popleft()
        fishByAge[6] += newFish
        fishByAge.append(newFish)

        #print("After {:>2} {}: {}".format(d, dayString, printFish()))
        #dayString = "days"

    return sum(fishByAge)


#
# Count the fish by age
#

#
# Main
#
def main():
    global filename, fish, days

    args = sys.argv[1:]
    if len(args) != 2:
        print("Usage: " + sys.argv[0] + " inputfile days");
        return
    filename = args[0]
    days = int(args[1])
    print("Input File:", filename)
    print("      Days:", days)
    print()

    # Load data
    lines = loadData(filename)
    print(" Lines Read: ", lines)
    print("Data Loaded: ", len(fish))
    print()

    # Do the work
    print("Initial State:", printFish())
    #numFish = simulateDaysSlow(days)
    numFish = simulateDaysFast(days)
    print("{}Total Fish: {}{}{}".format(color.CYAN, color.YELLOW, numFish, color.END))


if __name__ == "__main__":
    main()
