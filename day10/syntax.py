#
# Adavent of Code Template
#
import sys
from enum import Enum

# Global Variables
filename = ""
inputData = []

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


class Pair(Enum):
    PAREN = 0   # ()
    SQUARE = 1  # []
    BRACE = 2   # {}
    LTGT = 3    # <>


pair = {"(": ")",
        "[": "]",
        "{": "}",
        "<": ">"}


pairOpen = {"(": Pair.PAREN,
            "[": Pair.SQUARE,
            "{": Pair.BRACE,
            "<": Pair.LTGT}


pairClose = {")": Pair.PAREN,
             "]": Pair.SQUARE,
             "}": Pair.BRACE,
             ">": Pair.LTGT}


pairScore = {Pair.PAREN:      3,
             Pair.SQUARE:    57,
             Pair.BRACE:   1197,
             Pair.LTGT:   25137}


autoScore = {Pair.PAREN:  1,
             Pair.SQUARE: 2,
             Pair.BRACE:  3,
             Pair.LTGT:   4}


class Character:
    char = ""
    position = 0
    pair = 0
    def __init__(self, c, p, pairEnum):
        self.char = c
        self.position = p
        self.pair = pairEnum
    @classmethod
    def empty(self):
        return self("", 0, 0)


class IllegalCharacter:
    openChar = Character.empty()
    closeChar = Character.empty()
    def __init__(self, oc, cc):
        self.openChar = oc
        self.closeChar = cc


class State(Enum):
    OK = 0
    ILLEGAL = 1
    INCOMPLETE = 2


class Line:
    line = ""
    state = State.OK
    illegalChars = []
    autoCorrect = ""
    autoScore = 0
    def __init__(self):
        self.state = State.OK
        self.illegalChars = []
        self.autoCorrect = ""
        self.autoScore = 0


#
# Load the file into a data array
#
def loadData(filename):
    global inputData

    lines = 0

    f = open(filename)
    for line in f:
        l = Line()
        l.line = line.strip()
        inputData.append(l)
        #print(inputData[lines])
        lines += 1

    f.close()

    return lines


#
# Parse a Line
#
def parseLine(l):
    global pairOpen

    line = l.line
    l.state = State.OK
    stack = []


    #print(line)
    for cPos in range(len(line)):
        char = line[cPos]
        if char in pairOpen.keys():
            openChar = Character(char, cPos, pairOpen[char])
            stack.append(openChar)
            #print("Push", openChar.char)
        if char in pairClose.keys():
            closeChar = Character(char, cPos, pairClose[char])
            openChar = stack.pop()
            #print(" Pop", openChar.char, closeChar.char)
            if openChar.pair != closeChar.pair:
                # Illegal Character
                #print("Illegal", openChar.char, closeChar.char)
                i = IllegalCharacter(openChar, closeChar)
                l.illegalChars.append(i)
                l.state = State.ILLEGAL
                break

    if l.state == State.OK and len(stack) != 0:
        #print("Incomplete", len(stack))
        l.illegalChars = stack
        l.state = State.INCOMPLETE



#
# Parse the lines
#
def parseLines():
    global inputData

    for l in inputData:
      parseLine(l)


#
# Print the lines
#
def printLines():
    global inputData

    for d in inputData:
        #print(d.line)
        printStr = ""
        if d.state == State.OK:
            printStr += d.line

        elif d.state == State.ILLEGAL:
            illChar = d.illegalChars[0]
            printStr += d.line[:illChar.openChar.position]
            printStr += "{}{}{}".format(color.RED,d.line[illChar.openChar.position],color.END)
            printStr += d.line[illChar.openChar.position+1:illChar.closeChar.position]
            printStr += "{}{}{}".format(color.RED,d.line[illChar.closeChar.position],color.END)
            printStr += d.line[illChar.closeChar.position+1:]
            printStr += " - Expected {}, but found {} instead.".format(pair[illChar.openChar.char], illChar.closeChar.char)

        elif d.state == State.INCOMPLETE:
            pos = 0
            for i in d.illegalChars:
                #print(i.char, i.position)
                printStr += d.line[pos:i.position]
                printStr += "{}{}{}".format(color.RED,d.line[i.position],color.END)
                pos = i.position+1

            printStr += d.line[pos:]
            printStr += "{}{}{}".format(color.GREEN,d.autoCorrect,color.END)
            printStr += " - Incomplete {} points".format(d.autoScore)

        print(printStr)


#
# Calculate Score
#
def calculateScore():
    global inputData

    score = 0

    for d in inputData:
        if d.state == State.ILLEGAL:
            score += pairScore[d.illegalChars[0].closeChar.pair]

    return score


#
# Autocomplete missing closures
#
def autoComplete():
    global inputData

    incompleteScores = []
    for d in inputData:
        if d.state == State.INCOMPLETE:
            missingChars = ""
            for i in d.illegalChars:
                missingChars += pair[i.char]
            d.autoCorrect = missingChars

            d.autoScore = 0
            illChars = d.illegalChars.copy()
            illChars.reverse()
            for i in illChars:
                d.autoScore = (d.autoScore * 5) + autoScore[i.pair]
                #print(d.autoScore)
            incompleteScores.append(d.autoScore)

    incompleteScores.sort()
    scorePos = int((len(incompleteScores) - 1) / 2)
    return incompleteScores[scorePos]



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

    # Do Part 1 work
    print()
    parseLines()
    #printLines()
    score = calculateScore()
    print("{}Incorrect Score: {}{}{}".format(color.CYAN, color.YELLOW, score, color.END))

    # Do Part 2 work
    print()
    score = autoComplete()
    printLines()
    print("{}Auto Complete Score: {}{}{}".format(color.CYAN, color.YELLOW, score, color.END))


if __name__ == "__main__":
    main()
