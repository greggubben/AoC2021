#
# Adavent of Code Template
#
import sys

# Global Variables
filename = ""
inputData = []
slidingData = []


#
# Load the file into a data array
#
def loadData(filename):
    global inputData

    lines = 0

    f = open(filename)
    for line in f:
        inputData.append(int(line))
        #print(inputData[lines])
        lines += 1

    f.close()

    return lines


#
# Find how many times the current number is greater than previous
#
def findIncreases(sourceData):
    increases = 0
    decreases = 0
    for d in range(1,len(sourceData)):
        direction = ""
        if sourceData[d-1] < sourceData[d]:
            increases += 1
            direction = "(increased)"
        else:
            decreases += 1
            direction = "(decreased)"
        print(d, direction)

    return increases


#
# Find how many times the current number is greater than previous
#
def computeSlidingWindow():
    global inputData, slidingData

    for d in range(2,len(inputData)):
        slidingData.append(inputData[d-2]+inputData[d-1]+inputData[d])


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

    # Part 1
    increases = findIncreases(inputData)
    print("Increases: ", increases)

    # Part 2
    computeSlidingWindow()
    increases = findIncreases(slidingData)
    print("Sliding Increases: ", increases)


if __name__ == "__main__":
    main()
