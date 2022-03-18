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


class monad:
    LARGEST = 0
    SMALLEST = 1


#
# Load the file into a data array
#
def loadData(filename):

    lines = []

    f = open(filename)
    for line in f:
        line = line.strip()
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
# Print the instruction sets for comparison
#
def printInstructionSets(instructionSets):

    for i in range(len(instructionSets[0])):
        rowStr = ""
        for s, instructionSet in enumerate(instructionSets):
            colorStart, colorEnd = ("","") if s == 0 or instructionSet[i] == instructionSets[s-1][i] else (color.YELLOW, color.END)
            rowStr += "{}{:<9}{} ".format(colorStart,instructionSet[i],color.END)
        print(rowStr)


#
# initalize the ALU
#
def _initALU():
    alu = {"w":0, "x":0, "y":0, "z":0}
    return alu


#
# Perform a single instruction
#
def _performInstruction(inputValues, alu, instruction):
    command, *args = instruction.split()
    arg1 = args[0]
    arg = None if len(args) <= 1 else args[1]

    if command == "inp":
        arg2 = inputValues.pop(0)
        alu[arg1] = arg2
    elif command == "add":
        arg2Val = alu.get(arg2,-1) if arg2 in alu.keys() else int(arg2)
        alu[arg1] += arg2Val
    elif command == "mul":
        arg2Val = alu.get(arg2,-1) if arg2 in alu.keys() else int(arg2)
        alu[arg1] *= arg2Val
    elif command == "div":
        arg2Val = alu.get(arg2,-1) if arg2 in alu.keys() else int(arg2)
        alu[arg1] //= arg2Val
    elif command == "mod":
        arg2Val = alu.get(arg2,-1) if arg2 in alu.keys() else int(arg2)
        alu[arg1] %= arg2Val
    elif command == "eql":
        arg1Val = alu[arg1]
        arg2Val = alu.get(arg2,-1) if arg2 in alu.keys() else int(arg2)
        alu[arg1] = 1 if arg1Val == arg2Val else 0
    else:
        print(color.RED, "Command:", command, "not recognized!", color.END)


#
# Perform the set of instructions on the alu
#
def _runInstructions(inputValues, alu, instructions):

    for instruction in instructions:
        performInstruction(inputValues, alu, instruction)
        print("{}{:<15}{}".format(color.YELLOW if instruction.startswith("inp") else "", instruction, color.END), alu)
        #print(alu)


#
# Run a precompiled version of the instructions
#
def runCompiled(a1,a2,a3,w,x,y,z):
    x = 1 if (z%26 + a2) != w else 0
    #z = z//a1 * (25*x + 1)
    y = (w+a3)*x
    z = (z//a1 * (25*x + 1)) + y

    return (x,y,z)


#
# Create sets of instructions
#
def createSets(instructions):

    instructionSets = []

    instructionSet = []
    for instruction in instructions:
        if instruction.startswith("inp"):
            instructionSet = []
            instructionSets.append(instructionSet)
        instructionSet.append(instruction)

    return instructionSets


#
# Create sets of arguments for instructions
#
def createArgs(instructionSets):

    instructionArgs = []

    for instructionSet in instructionSets:
        for line, instruction in enumerate(instructionSet):
            if line == 4:
                command, arg1, arg2 = instruction.split()
                a1 = int(arg2)
            elif line == 5:
                command, arg1, arg2 = instruction.split()
                a2 = int(arg2)
            elif line == 15:
                command, arg1, arg2 = instruction.split()
                a3 = int(arg2)
        instructionArgs.append((a1, a2,a3))

    return instructionArgs


def __DecimalToAnyBaseArrayRecur__(array, decimal, base):
    array.append(decimal % base)
    div = decimal // base
    if(div == 0):
        return;
    __DecimalToAnyBaseArrayRecur__(array, div, base)

def DecimalToBase(decimal, base):
    array = []
    __DecimalToAnyBaseArrayRecur__(array, decimal, base)
    return array[::-1]


#
# Process each digit in the model number
#
def findModelDigit(direction, startZ, depth, instructionArgs):

    #print(depth)
    limit = len(instructionArgs)-1

    startZs = {}
    startDigit = 9 if direction == monad.LARGEST else 1
    endDigit = 0 if direction == monad.LARGEST else 10
    stepDigit = -1 if direction == monad.LARGEST else 1
    #for digit in range(9,0,-1):
    #for digit in range(1,10):
    for digit in range(startDigit, endDigit, stepDigit):
        newXYZ = runCompiled(*instructionArgs[depth], digit, 0,0,startZ)
        #print(" " * depth, digit, startZ, newXYZ, DecimalToBase(newXYZ[2],26))
        if instructionArgs[depth][0] == 1 or (instructionArgs[depth][0] == 26 and newXYZ[0] == 0):
            startZs[digit] = newXYZ[2]
        if depth == limit and newXYZ[2] == 0:
            # done
            return digit, True

    if depth < limit:
        for digit, nextStartZ in startZs.items():
            #previousALUs.append(childALU)
            model, foundModel = findModelDigit(direction, nextStartZ, depth+1, instructionArgs)
            if foundModel: 
                print(model)
                return digit * 10**(len(instructionArgs)-depth-1) + model, True

    return 0, False



#
# find the model number
#
def findModel(direction, instructions):
    instructionSets = createSets(instructions)
    printInstructionSets(instructionSets)
    instructionArgs = createArgs(instructionSets)
    print(instructionArgs)

    depth = 0
    model, found = findModelDigit(direction, 0, depth, instructionArgs)
    return model


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
    instructions = loadData(filename)
    print(" Instructions Read: ", len(instructions))
    print()
    #printLines(instructions)
    print()

    # Do Part 1 work
    print()
    answer = findModel(monad.LARGEST, instructions)
    print()
    print("{}Largest Model Number: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))

    # Do Part 2 work
    print()
    answer = findModel(monad.SMALLEST, instructions)
    print()
    print("{}Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))


if __name__ == "__main__":
    main()
