#
# Adavent of Code Template
#
import sys
from statistics import mean, median, mode, stdev

# Global Variables
filename = ""
inputData = []
minPos = 0
maxPos = 0
crabs = []

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


class CrabMetrics:
    mean = 0
    mode = 0
    median = 0
    stddev = 0


#
# Load the file into a data array
#
def loadData(filename):
    global inputData, maxPos

    lines = 0

    f = open(filename)
    for line in f:
        crabs = line.split(",")
        for c in crabs:
            crabPos = int(c)
            inputData.append(crabPos)
            if crabPos > maxPos:
                maxPos = crabPos
        #print(inputData[lines])
        lines += 1

    f.close()

    return lines


#
# Load the crabs
#
def loadCrabs():
    global inputData, crabs

    inputData.sort()

    crabs = [0 for c in range(maxPos+1)]

    crabCount = 0
    for i in inputData:
        crabs[i] += 1
        crabCount += 1

    return crabCount


#
# Calculate Stats about the crabs
#
def calculateStats():
    global inputData

    crabStats = CrabMetrics()

    inputData.sort()
    crabStats.mean   = round(mean(inputData))
    crabStats.median = round(median(inputData))
    crabStats.mode   = mode(inputData)
    crabStats.stddev = stdev(inputData)

    return crabStats


#
# Calculate Energy needed
#
def calculateLinearEnergy(centerPos):
    global inputData

    energyNeeded = 0
    for c in inputData:
        energyNeeded += abs(centerPos - c)

    return energyNeeded


#
# Calculate Energy needed
#
def calculateGrowthEnergy(centerPos):
    global inputData

    energyNeeded = 0
    for c in inputData:
        gap = abs(centerPos - c)
        e = (gap * (gap + 1)) / 2
        energyNeeded += e

    return energyNeeded


#
# Print trend around number provided
# 1 down, number, 1 up
#
def printTrend(label, value, calcEnergyFunc):
    foundLeast = False

    energyDown = calcEnergyFunc(value-1)
    energy = calcEnergyFunc(value)
    energyUp = calcEnergyFunc(value+1)

    downStatus = color.GREEN
    status = color.GREEN
    upStatus = color.GREEN

    if (energyDown < energy):
        downStatus = color.RED
    if (energyUp < energy):
        upStatus = color.RED
    if ((energyDown > energy) & (energyUp > energy)):
        foundLeast = True
    else:
        status = color.RED

    print("{}Down {}: {:>4} - Energy: {}{}".format(downStatus, label, str(value-1), str(energyDown), color.END))
    print("{}     {}: {:>4} - Energy: {}{}".format(status, label, str(value), str(energy), color.END))
    print("{}  Up {}: {:>4} - Energy: {}{}".format(upStatus, label, str(value+1), str(energyUp), color.END))

    return foundLeast


#
# Brute Force Walk through crab positions
#
def walk(crabStats, calcEnergyFunc):
    global inputData

    keyPositions = [inputData[0], inputData[len(inputData)-1], crabStats.mean, crabStats.median, crabStats.mode]
    keyPositions.sort()
    leastEnergy = keyPositions[0]

    # figure out start, end for walk
    startPos = keyPositions[0]
    endPos = keyPositions[4]
    minEnergy = calcEnergyFunc(keyPositions[0])
    maxEnergy = calcEnergyFunc(keyPositions[4])

    for k in keyPositions:
        kEnergy = calcEnergyFunc(k)
        kPlusEnergy = calcEnergyFunc(k+1)
        #print (k, kEnergy, kPlusEnergy)
        if kPlusEnergy > kEnergy:
            #print("UP")
            # Tending up - set max
            if kEnergy < maxEnergy:
                endPos = k
                maxEnergy = kEnergy
        else:
            #print("DOWN")
            # Tending down - set min
            if kEnergy < minEnergy:
                startPos = k
                minEnergy = kEnergy

    print()
    print("Start:", startPos, " Energy:", minEnergy)
    print("  End:", endPos, " Energy:", maxEnergy)
    print()

    # do the walk
    lastEnergy = minEnergy
    for p in range(startPos, endPos+1):
        energy = calcEnergyFunc(p)
        direction = ""
        if energy <=lastEnergy:
            # trending down
            lastEnergy = energy
            direction = "Down"
        else:
            # trending back up
            # done
            leastEnergy = p-1
            direction = "Up"
            break
        #print(p, energy, direction)



    return leastEnergy




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
    crabCount = loadCrabs()
    print("    Lines Read: ", lines)
    print("   Data Loaded: ", len(inputData))
    print("  Crabs Loaded: ", crabCount)
    print("Crab Positions: ", len(crabs))
    print("  Min Position: ", minPos)
    print("  Max Position: ", maxPos)


    # Do the work
    print()
    print("Linear")
    print()
    crabStats = calculateStats()

    print("Std Dev: {}".format(str(crabStats.stddev)))
    print()

    position = 0
    label = ""
    if printTrend("Mean", crabStats.mean, calculateLinearEnergy):
        position = crabStats.mean
        label = "Mean"
    print()
    if printTrend("Median", crabStats.median, calculateLinearEnergy):
        position = crabStats.median
        label = "Median"
    print()
    if printTrend("Mode", crabStats.mode, calculateLinearEnergy):
        position = crabStats.mode
        label = "Mode"
    print()

    if label == "":
        print(color.RED, color.BOLD, "ANSWER NOT FOUND", color.END)
    else:
        energy = calculateLinearEnergy(position)
        print("{}{}: {}{:>4}{} - Energy: {}{}{}".format(color.CYAN, label, color.YELLOW, str(position), color.CYAN, color.YELLOW, str(energy), color.END))

    print()
    print("Growth")
    print()
    position = 0
    label = ""
    if printTrend("Mean", crabStats.mean, calculateGrowthEnergy):
        position = crabStats.mean
        label = "Mean"
    print()
    if printTrend("Median", crabStats.median, calculateGrowthEnergy):
        position = crabStats.median
        label = "Median"
    print()
    if printTrend("Mode", crabStats.mode, calculateGrowthEnergy):
        position = crabStats.mode
        label = "Mode"
    print()

    if label == "":
        walkPos = walk(crabStats, calculateGrowthEnergy)
        if printTrend("Walk", walkPos, calculateGrowthEnergy):
            position = walkPos
            label = "Walk"

    if label == "":
        print(color.RED, color.BOLD, "ANSWER NOT FOUND", color.END)
    else:
        energy = calculateGrowthEnergy(position)
        print("{}{}: {}{:>4}{} - Energy: {}{}{}".format(color.CYAN, label, color.YELLOW, str(position), color.CYAN, color.YELLOW, str(energy), color.END))


if __name__ == "__main__":
    main()
