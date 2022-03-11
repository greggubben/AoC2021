#
# Adavent of Code Template
#
import sys
import copy

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


class Pair:
    leftVal = None
    leftIsPair = False
    leftIsEmpty = True
    leftChanged = False
    leftSplit = False

    rightVal = None
    rightIsPair = False
    rightIsEmpty = True
    rightChanged = False
    rightSplit = False

    parent = None
    explode = False


    def __init__(self, left=None, right=None):
        self.setLeft(left)
        self.setRight(right)

    def __copy__(self):
        return Pair(copy.copy(self.leftVal), copy.copy(self.rightVal))

    # Use this function to set left so important meta data is also set
    def setLeft(self, left):
        self.leftVal = left
        self.leftIsEmpty = (left is None)
        self.leftIsPair = isinstance(left, Pair)
        self.leftChanged = isinstance(left, int)
        if self.leftIsPair:
            left.setParent(self)

    # Use this function to set right so important meta data is also set
    def setRight(self, right):
        self.rightVal = right
        self.rightIsEmpty = (right is None)
        self.rightIsPair = isinstance(right, Pair)
        self.rightChanged = isinstance(right, int)
        if self.rightIsPair:
            right.setParent(self)

    def __str__(self):
        pairColor = ""

        leftPart = str(self.leftVal)
        if self.leftIsEmpty:
            leftPart = color.RED + leftPart + color.END
        elif self.leftChanged:
            leftPart = color.YELLOW + leftPart + color.END
        elif self.leftSplit:
            leftPart = color.CYAN + leftPart + color.END

        rightPart = str(self.rightVal)
        if self.rightIsEmpty:
            rightPart = color.RED + rightPart + color.END
        elif self.rightChanged:
            rightPart = color.YELLOW + rightPart + color.END
        elif self.rightSplit:
            rightPart = color.CYAN + rightPart + color.END

        if self.explode:
            pairColor = color.GREEN
        return "{}[{}{},{}{}]{}".format(pairColor,leftPart, pairColor,rightPart, pairColor, color.END)

    # Need to set reference to parent to make traversing the number easier
    def setParent(self, p):
        self.parent = p

    # Reset flags that help printing of number
    def reset(self):
        self.leftChanged = False
        self.rightChanged = False
        self.explode = False
        self.leftSplit = False
        self.rightSplit = False

        if self.leftIsPair:
            self.leftVal.reset()
        if self.rightIsPair:
            self.rightVal.reset()


    # Find the pair that needs exploding
    def findExplodePair(self, depth=0):
        depth+=1
        explodePair = None

        if depth > 4:
            if not self.leftIsPair and not self.rightIsPair:
                explodePair = self
                self.explode = True

        if explodePair is None and self.leftIsPair:
            explodePair = self.leftVal.findExplodePair(depth)

        if explodePair is None and self.rightIsPair:
            explodePair = self.rightVal.findExplodePair(depth)

        return explodePair

    # utility to add to number on left when drilling down
    # used by addLeft
    def addLeftLookDown(self, addVal):
        done = False

        # Work right to left because right is closest when going down
        if self.rightIsPair:
            # Right is a pair need to drill down
            done = self.rightVal.addLeftLookDown(addVal)
        else:
            # Right is a number
            self.setRight(self.rightVal + addVal)
            done = True

        if not done:
            if self.leftIsPair:
                # Left is a pair need to drill down
                done = self.leftVal.addLeftLookDown(addVal)
            else:
                # Left is a number
                self.setLeft(self.leftVal + addVal)
                done = True

        return done

    # utility to add to number on left when traversing number up
    # used by addLeft
    def addLeftLookUp(self, child, addVal):
        done = False

        if child == self.rightVal:
            # Came up right side - check for a number on left
            if self.leftIsPair:
                # Left is a pair need to drill down
                done = self.leftVal.addLeftLookDown(addVal)
            else:
                # Left is a number
                self.setLeft(self.leftVal + addVal)
                done = True

        if not done:
            # Check parent
            if self.parent is not None:
                done = self.parent.addLeftLookUp(self, addVal)

        return done

    # Add the number to the left
    def addLeft(self):
        done = False

        if self.parent is not None:
            done = self.parent.addLeftLookUp(self, self.leftVal)

        return done


    # utility to add to number on right when drilling down
    # used by addRight
    def addRightLookDown(self, addVal):
        done = False

        # Work left to right because left is closest when going down
        if self.leftIsPair:
            # Left is a pair need to drill down
            done = self.leftVal.addRightLookDown(addVal)
        else:
            # Left is a number
            self.setLeft(self.leftVal + addVal)
            done = True

        if not done:
            if self.rightIsPair:
                # Right is a pair need to drill down
                done = self.rightVal.addRightLookDown(addVal)
            else:
                # Right is a number
                self.setRight(self.rightVal + addVal)
                done = True

        return done

    # utility to add to number on right when traversing number up
    # used by addRight
    def addRightLookUp(self, child, addVal):
        done = False

        if child == self.leftVal:
            # Came up left side - check for a number on right
            if self.rightIsPair:
                # Right is a pair need to drill down
                done = self.rightVal.addRightLookDown(addVal)
            else:
                # Right is a number
                self.setRight(self.rightVal + addVal)
                done = True

        if not done:
            # Check parent
            if self.parent is not None:
                done = self.parent.addRightLookUp(self, addVal)

        return done

    # Add the number to the right
    def addRight(self):
        done = False

        if self.parent is not None:
            done = self.parent.addRightLookUp(self, self.rightVal)

        return done

    # replace the exploded pair with a 0
    def replace0(self):
        if self.parent is not None:
            if self.parent.leftIsPair and self.parent.leftVal == self:
                self.parent.setLeft(0)
            elif self.parent.rightIsPair and self.parent.rightVal == self:
                self.parent.setRight(0)


    # Find any split candidates
    def findSplitPair(self):
        splitPair = None

        if not self.leftIsPair and self.leftVal > 9:
                splitPair = self
                self.leftSplit = True

        if splitPair is None and self.leftIsPair:
            splitPair = self.leftVal.findSplitPair()

        if splitPair is None and not self.rightIsPair and self.rightVal > 9:
                splitPair = self
                self.rightSplit = True

        if splitPair is None and self.rightIsPair:
            splitPair = self.rightVal.findSplitPair()

        return splitPair

    # Do the split
    def split(self):

        if not self.leftIsPair and self.leftVal > 9:
            newLeft = int(self.leftVal / 2)
            newRight = round((self.leftVal / 2.0)+0.1)
            newPair = Pair(newLeft, newRight)
            self.setLeft(newPair)
        else:
            newLeft = int(self.rightVal / 2)
            newRight = round((self.rightVal / 2.0)+0.1)
            newPair = Pair(newLeft, newRight)
            self.setRight(newPair)

    # Calculate Magnitude
    def magnitude(self):
        leftNum = 0
        rightNum =0

        if self.leftIsPair:
            leftNum = self.leftVal.magnitude()
        else:
            leftNum = self.leftVal

        if self.rightIsPair:
            rightNum = self.rightVal.magnitude()
        else:
            rightNum = self.rightVal

        return 3*leftNum + 2*rightNum



#
# Convert a string to a snail number
#
def line2number(line):

    parseStack = []

    indent = 0

    for c in line:
        #print("char",c)
        if c == "[":
            value = Pair()
            #print(" " * indent, "push",value)
            indent += 1
            parseStack.append(value)
        elif c == "]":
            #print(" " * indent, "right",value)
            parseStack[-1].setRight(value)
            value = parseStack.pop()
            #print(" " * indent, "pop",value)
            indent -= 1
        elif c == ",":
            #print(" " * indent, "left",value)
            parseStack[-1].setLeft(value)
            pass
        else:
            value = int(c)      # All regular numbers are single digits
            #print(" " * indent, "num",value)

    return value



#
# Load the file into a data array
#
def loadData(filename):

    lines = []
    numbers = []

    f = open(filename)
    for line in f:
        line = line.strip()
        lines.append(line)
        numbers.append(line2number(line))

    f.close()

    return lines, numbers


#
# Print Array
#
def printLines(lines, numbers):

    for l in range(len(lines)):
        print()
        print(lines[l])
        print(numbers[l])



#
# Reduce the number
#
def reduceNumber(number):

    number.reset()

    print("{:<16}{}".format("after addition:",number))
    changed = True  # need to be optimistic to enter loop
    while changed:
        changed = False
        explodePair = number.findExplodePair()
        if explodePair is not None:
            print("{:<16}{}".format("found explode:",number))
            done = explodePair.addLeft()
            done = explodePair.addRight()
            explodePair.replace0()
            print("{:<16}{}".format("after explode:",number))
            changed = True
        else:
            splitPair = number.findSplitPair()
            if splitPair is not None:
                print("{:<16}{}".format("found split:",number))
                splitPair.split()
                print("{:<16}{}".format("after split:",number))
                changed = True

        number.reset()


    return number


#
# Add all the numbers
#
def addNumbers(numbers):

    sumNumber = None
    lastNumber = None
    print()
    
    for n in numbers:
        nCopy = copy.copy(n)
        if sumNumber is None:
            sumNumber = nCopy
            lastNumber = n
        else:
            sumNumber = Pair(sumNumber,nCopy)
            sumNumber = reduceNumber(sumNumber)
            print()
            print(" ",lastNumber)
            print("+",n)
            print("=",sumNumber)
            print()

    return sumNumber

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
    lines, numbers = loadData(filename)
    print()
    print("    Lines Read: ", len(lines))
    print("Numbers Loaded: ", len(numbers))
    print()

    # Do Part 1 work
    printLines(lines, numbers)
    sumNumber = addNumbers(numbers)
    magnitude = sumNumber.magnitude()
    print()
    print("{}Magnitude: {}{}{}".format(color.CYAN, color.YELLOW, magnitude, color.END))

    # Do Part 2 work
    #print()
    #printLines(lines)
    #print()
    #print("{}Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer color.END))


if __name__ == "__main__":
    main()
