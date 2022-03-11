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


'''
    Finished solution should look like this:

    #############
    #...........#
    ###A#B#C#D###
      #A#B#C#D#
      #########

'''

energy = {"A":1, "B":10, "C":100, "D":1000}

spaces = {(1,1):".", (1,2):".", (1,3):".", (1,4):".", (1,5):".", (1,6):".", (1,7):".", (1,8):".", (1,9):".", (1,10):".", (1,11):".", \
        (2,3):".",            (2,5):".",            (2,7):".",            (2,9):".", \
        (3,3):".",            (3,5):".",            (3,7):".",            (3,9):"."}

#
# Load the file into a data array
#
def loadData(filename):
    global spaces

    lines = []

    r = 0
    f = open(filename)
    for line in f:
        #line = line.strip()
        if r in [2,3]:
            for c in range(3,11,2):
                spaces[(r,c)] = line[c]
        r += 1

        lines.append(line)

    f.close()

    return lines


#
# Print Array
#
def printLines(lines):

    for line in lines:
      print(line)


#
# Print Burrow
#
def printBurrow():
    global spaces

    print("#############")

    rowStr = "#"
    for i in range(1,12):
        rowStr += color.CYAN + spaces[(1,i)] + color.END
    rowStr += "#"
    print(rowStr)

    rowStr = "###"
    for i in range(3,10,2):
        rowStr += color.CYAN + spaces[(2,i)] + color.END + "#"
    rowStr += "##"
    print(rowStr)

    rowStr = "  #"
    for i in range(3,10,2):
        rowStr += color.CYAN + spaces[(3,i)] + color.END + "#"
    print(rowStr)

    print("  #########  ")


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
    lines = loadData(filename)
    print(" Lines Read: ", len(lines))
    print()

    # Do Part 1 work
    printLines(lines)
    printBurrow()
    answer = "X"
    print()
    print("{}Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))

    # Do Part 2 work
    #print()
    #printLines(lines)
    #print()
    #print("{}Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))


if __name__ == "__main__":
    main()
