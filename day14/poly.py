#
# Adavent of Code Template
#
import sys

# Global Variables
insertionRules = {}
polymer = ""

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
    global insertionRules, polymer

    insertionRules = {}
    lines = 0

    loadPolymer = True
    loadRules = False

    f = open(filename)
    for line in f:
        line = line.strip()

        # Load the Rules section of the input file
        if loadRules:
            parts = line.split(" ")
            pair = str(parts[0])
            insert = str(parts[2])
            insertionRules[pair] = insert

        # a blank line indicates change in loading
        if len(line) == 0:
            loadPolymer = False
            loadRules = True

        # load the polymer string
        if loadPolymer:
            polymer = line

        lines += 1

    f.close()

    return lines


#
# Perform Insertion
#
def performStepsString(steps):
    global polymer, insertionRules

    modPoly = polymer
    print("Template:", modPoly)
    for s in range(steps):
        newPoly = ""
        for cPos in range(len(modPoly)-1):
            chars = modPoly[cPos] + modPoly[cPos+1]
            #print("chars", chars)
            if chars in insertionRules.keys():
                newPoly += modPoly[cPos] + insertionRules[chars]
        newPoly += modPoly[len(modPoly)-1]
        modPoly = newPoly
        print("After step {}:".format(s),modPoly)

    return modPoly


#
# Count the occurances of each character
#
def countOccurancesString(poly):
    
    minCount = len(poly)
    maxCount = 0

    chars = {}
    for c in poly:
        if c in chars.keys():
            chars[c] += 1
        else:
            chars[c] = 1

    for c in chars.keys():
        if chars[c] > maxCount: maxCount = chars[c]
        if chars[c] < minCount: minCount = chars[c]

    return minCount,maxCount


#
# Perform Insertion
#
def performStepsBucket(steps):
    global polymer, insertionRules

    polyBuckets = {}
    # Initialize the buckets
    for cPos in range(len(polymer)-1):
        chars = polymer[cPos] + polymer[cPos+1]
        if chars in polyBuckets.keys():
            polyBuckets[chars] += 1
        else:
            polyBuckets[chars] = 1

    print(polyBuckets)

    for s in range(steps):
        newPoly = {}
        for bucket in polyBuckets.keys():
            if bucket in insertionRules.keys():
                middleChar = insertionRules[bucket]
                firstBucket = bucket[0] + middleChar
                lastBucket = middleChar + bucket[1]

                if firstBucket in newPoly.keys():
                    newPoly[firstBucket] += polyBuckets[bucket]
                else:
                    newPoly[firstBucket] = polyBuckets[bucket]

                if lastBucket in newPoly.keys():
                    newPoly[lastBucket] += polyBuckets[bucket]
                else:
                    newPoly[lastBucket] = polyBuckets[bucket]

        polyBuckets = newPoly
        print("After step {}:".format(s),polyBuckets)

    return polyBuckets


#
# Count the occurances of each character
#
def countOccurancesBucket(poly):
    
    minCount = sum(poly.values())
    maxCount = 0

    chars = {}
    for k in poly.keys():
        count = poly[k]
        c = k[0]
        if c in chars.keys():
            chars[c] += count
        else:
            chars[c] = count

    c = polymer[len(polymer)-1]
    if c in chars.keys():
        chars[c] += 1
    else:
        chars[c] = 1


    print(chars)

    for c in chars.keys():
        if chars[c] > maxCount: maxCount = chars[c]
        if chars[c] < minCount: minCount = chars[c]

    return minCount,maxCount


#
# Print Insertion Rules
#
def printInsertionRules():
    global insertionRules

    for k in insertionRules.keys():
      print("{} -> {}".format(k, insertionRules[k]))


#
# Main
#
def main():
    global insertionRules, polymer

    args = sys.argv[1:]
    if len(args) != 2:
        print("Usage: " + sys.argv[0] + " inputfile steps");
        return
    filename = args[0]
    steps = int(args[1])
    print("Input File:", filename)
    print("     Steps:", steps)
    print()

    # Load data
    lines = loadData(filename)
    print("  Lines Read: ", lines)
    print("Rules Loaded: ", len(insertionRules))
    print()

    # Do Part 1 work
    print("Polymer:", polymer)
    print()
    print("Insertion Rules:")
    printInsertionRules()
    print()
    poly = performStepsBucket(steps)
    minCount, maxCount = countOccurancesBucket(poly)
    answer = maxCount - minCount
    print("{}Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))

    # Do Part 2 work
    #print()
    #printArray()
    #print()
    #print("{}Answer: {}{}{}".format(color.CYAN, color.YELLOW, "X", color.END))


if __name__ == "__main__":
    main()
