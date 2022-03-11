#
# Adavent of Code Template
#
import sys

# Global Variables
filename = ""
inputData = []
hpos = 0
depth = 0
aim = 0


#
# Load the file into a data array
#
def loadData(filename):
    global inputData

    lines = 0

    f = open(filename)
    for line in f:
        inputData.append(line.split())
        #print(inputData[lines])
        lines += 1

    f.close()

    return lines


#
# apply commands
#
def commands():
    global inputData, hpos, depth

    hpos = 0
    depth = 0

    for d in inputData:
        units = int(d[1])
        if d[0] == "forward":
                hpos += units
        elif d[0] == "down":
                depth += units
        elif d[0] == "up":
                depth -= units
        else:
                print("Unknown Command: ", d[0])


#
# apply commands
#
def aim():
    global inputData, hpos, depth, aim

    hpos = 0
    depth = 0
    aim = 0

    for d in inputData:
        units = int(d[1])
        if d[0] == "forward":
                hpos += units
                depth += aim * units
        elif d[0] == "down":
                aim += units
        elif d[0] == "up":
                aim -= units
        else:
                print("Unknown Command: ", d[0])



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
    commands()
    mult = hpos * depth
    print("Horizontal Position: ", hpos)
    print("              Depth: ", depth)
    print("         Multiplied: ", mult)

    # Part 2
    aim()
    mult = hpos * depth
    print("Horizontal Position: ", hpos)
    print("              Depth: ", depth)
    print("                Aim: ", aim)
    print("         Multiplied: ", mult)


if __name__ == "__main__":
    main()
