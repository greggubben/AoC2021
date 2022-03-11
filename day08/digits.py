#!/usr/bin/python3
#
# Adavent of Code Template
#
import sys

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


# Seven Segment Definition
#
#  000
# 1   2
# 1   2
#  333
# 4   5
# 4   5
#  666
#
class SevenSegment:
    seg0 = " "
    seg1 = " "
    seg2 = " "
    seg3 = " "
    seg4 = " "
    seg5 = " "
    seg6 = " "

    def getAsArray(self):
        return [self.seg0, self.seg1, self.seg2, self.seg3, self.seg4, self.seg5, self.seg6]

    def getDecode(self):
        return [self.seg0+self.seg1+self.seg2+self.seg4+self.seg5+self.seg6, \
                self.seg2+self.seg5, \
                self.seg0+self.seg2+self.seg3+self.seg4+self.seg6, \
                self.seg0+self.seg2+self.seg3+self.seg5+self.seg6, \
                self.seg1+self.seg2+self.seg3+self.seg5, \
                self.seg0+self.seg1+self.seg3+self.seg5+self.seg6, \
                self.seg0+self.seg1+self.seg3+self.seg4+self.seg5+self.seg6, \
                self.seg0+self.seg2+self.seg5, \
                self.seg0+self.seg1+self.seg2+self.seg3+self.seg4+self.seg5+self.seg6, \
                self.seg0+self.seg1+self.seg2+self.seg3+self.seg5+self.seg6]

    def getNumber(self, encodedString):
        num = 0
        #print("Encoded String", encodedString)
        segmentNumbers = self.getDecode()
        for n in range(len(segmentNumbers)):
            #print(" ",n,"Segment String", segmentNumbers[n])
            if len(encodedString) == len(segmentNumbers[n]):
                found = True
                for char in segmentNumbers[n]:
                    if encodedString.find(char) == -1:
                        #print("    False")
                        found = False
                        break
                if found:
                    #print("    True")
                    num = n
                    break
            #print(num)
        return num


class DigitStruct:
    line = ""
    part1 = ""
    part2 = ""
    part1Comp = []
    part2Comp = []
    sevenSegmentMap = SevenSegment()
    numberMap = []
    number = 0

#
# Array of number of segments by number
#            0 1 2 3 4 5 6 7 8 9
seven_seg = [6,2,5,5,4,5,6,3,7,6]
#            1 7 4 8
easy_seg  = [2,3,4,7]
easy_pos  = [1,7,4,8]


#
# Print Segment
#
def printSevenSegment(sevenSeg):
    print("  " + sevenSeg.seg0 + sevenSeg.seg0 + sevenSeg.seg0)
    print(sevenSeg.seg1 + "     " + sevenSeg.seg2)
    print(sevenSeg.seg1 + "     " + sevenSeg.seg2)
    print("  " + sevenSeg.seg3 + sevenSeg.seg3 + sevenSeg.seg3)
    print(sevenSeg.seg4 + "     " + sevenSeg.seg5)
    print(sevenSeg.seg4 + "     " + sevenSeg.seg5)
    print("  " + sevenSeg.seg6 + sevenSeg.seg6 + sevenSeg.seg6)


#
# Load the file into a data array
#
def loadData(filename):
    global inputData

    lines = 0

    f = open(filename)
    for line in f:
        digitInput = DigitStruct()
        digitInput.line = line
        parts = line.split("|")
        digitInput.part1 = parts[0]
        digitInput.part2 = parts[1]
        digitInput.part1Comp = digitInput.part1.split()
        digitInput.part2Comp = digitInput.part2.split()
        inputData.append(digitInput)
        #print(inputData[lines])
        lines += 1

    f.close()

    return lines


#
# find easy numbers
#
def findEasyNumbers():
    global inputData, easy_seg

    easyNumbers = 0
    for data in inputData:
        dataString = data.part1 + " | "
        for d in data.part2Comp:
            if len(d) in easy_seg:
                easyNumbers += 1
                dataString += color.YELLOW
            dataString += " " + d + color.END
        print(dataString)

    return easyNumbers

#
# Find Top Segment (Segment 0)
#
# subtract number 1 segments from number 7 segments
#
#  777     ...     SSS
# .   7   .   1   .   .
# .   7   .   1   .   .
#  ...  -  ...  =  ...
# .   7   .   1   .   .
# .   7   .   1   .   .
#  ...     ...     ...
#
def findSegment0(number1, number7):
    segement = ""
    for char in number7:
        if number1.find(char) == -1:
            segment = char
            break
    #print("Digit 1:", number1, "Digit 7:", number7, "Top Segment:", segment)
    return segment


#
# Find Middle Segment (Segment 3)
#
# The only common segment between the number 4 and all 3 numbers with 5 segements
# is the middle segement.
# Need to evaluate all 3 numbers with 5 segements because we do not yet know which
# number they represent. We already know only numbers 2, 3, and 5 use 5 segements.
#
#  ...     222     333     555     ...
# 4   4   .   2   .   3   5   .   .   .
# 4   4   .   2   .   3   5   .   .   .
#  444  &  222  &  333  &  555  =  SSS
# .   4   2   .   .   3   .   5   .   .
# .   4   2   .   .   3   .   5   .   .
#  ...     222     333     555     ...
#
def findSegment3(number4, fiveSegs):
    segement = ""

    five0 = fiveSegs[0]
    five1 = fiveSegs[1]
    five2 = fiveSegs[2]

    for char in number4:
        if ((five0.find(char) != -1) & (five1.find(char) != -1) & (five2.find(char) != -1)):
            segment = char
            break
    #print("Digit 4:", number4, "Five 0:", five0, "Five 1:", five1, "Five 2:", five2, "Middle Segment:", segment)
    return segment


#
# Find Bottom Segment (Segment 6)
#
# After removing known segments 0 and 3 from all the 5 segment numbers, the onlyi
# common segment between the 3 numbers with 5 segements is the middle segement.
# Need to evaluate all 3 numbers with 5 segements because we do not yet know which
# number they represent. We already know only numbers 2, 3, and 5 use 5 segements.
#
#  xxx      222     333     555      ...
# .   .    .^^^2   .^^^3   5^^^.    .   .
# .   .    .   2   .   3   5   .    .   .
#  xxx  ^(  222  &  333  &  555  )=  ...
# .   .    2^^^.   .^^^3   .^^^5    .   .
# .   .    2   .   .   3   .   5    .   .
#  ...      222     333     555      SSS
#
def findSegment6(segment0, segment3, fiveSegs):
    segement = ""

    five0 = fiveSegs[0].replace(segment0,'').replace(segment3,'')
    five1 = fiveSegs[1].replace(segment0,'').replace(segment3,'')
    five2 = fiveSegs[2].replace(segment0,'').replace(segment3,'')

    for char in five0:
        if ((five0.find(char) != -1) & (five1.find(char) != -1) & (five2.find(char) != -1)):
            segment = char
            break
    #print("Segment 0:", segment0, "Segment 3:", segment3, "Five 0:", five0, "Five 1:", five1, "Five 2:", five2, "Middle Segment:", segment)
    return segment


#
# Find Left Top Segment (Segment 1)
#
# After removing known segments 3 and all segments in number 1 from the segments
# in number 4, only segment 1 is left.
#
#  ...     ...     ...     ... 
# 4   4   .   .   .   1   S   .
# 4   4   .   .   .   1   S   .
#  444  -  xxx  -  ...  =  ... 
# .   4   .   .   .   1   .   .
# .   4   .   .   .   1   .   .
#  ...     ...     ...     ... 
#
def findSegment1(segment3, number4, number1):
    segement = ""

    four = number4.replace(segment3,'')
    for char in number1:
        four = four.replace(char, '')
    segment = four
    #print("Segment 3:", segment3, "Number 4", number4, "Number 1", number1, "Left Top Segment", segment)
    return segment


#
# Find Left Bottom Segment (Segment 4)
#
# After removing known segments 0 & 6 and all segments in number 4 from the segments
# in number 8, only segment 4 is left.
#
#  888     xxx     ...     ... 
# 8   8   .   .   4   4   .   .
# 8   8   .   .   4   4   .   .
#  888  -  ...  -  444  =  ... 
# 8   8   .   .   .   4   S   .
# 8   8   .   .   .   4   S   .
#  888     xxx     ...     ... 
#
def findSegment4(segment0, segment6, number8, number4):
    segement = ""

    eight = number8.replace(segment0,'').replace(segment6,'')
    for char in number4:
        eight = eight.replace(char, '')
    segment = eight
    #print("Segment 0", segment0, "Segment 6", segment6, "Number 8", number8, "Number 4:", number4, "Left Bottom Segment", segment)
    return segment


#
# Find Right Bottom Segment (Segment 5)
#
# After removing known segments 0, 1, 3, 6 from all the 5 segment numbers.
# The 5 segment number with only 1 segment remaining will be the 5 which identifies
# Segment 5.
#
#   222     333     555      xxx      ...     ...     ...       ...
#  .   2   .   3   5   .    x   .    .   2   .   3   .   .     .   .
#  .   2   .   3   5   .    x   .    .   2   .   3   .   .     .   .
# [ 222  ,  333  ,  555  ]-  xxx  =[  ...  ,  ...  ,  ...  ].:  ...
#  2   .   .   3   .   5    .   .    2   .   .   3   .   5     .   S
#  2   .   .   3   .   5    .   .    2   .   .   3   .   5     .   S
#   222     333     555      xxx      ...     ...     ...       ...
#
def findSegment5(segment0, segment1, segment3, segment6, fiveSegs):
    segement = ""

    five0 = fiveSegs[0].replace(segment0, '') \
                       .replace(segment3, '') \
                       .replace(segment6, '') \
                       .replace(segment1, '')
    five1 = fiveSegs[1].replace(segment0, '') \
                       .replace(segment3, '') \
                       .replace(segment6, '') \
                       .replace(segment1, '')
    five2 = fiveSegs[2].replace(segment0, '') \
                       .replace(segment3, '') \
                       .replace(segment6, '') \
                       .replace(segment1, '')

    #print("five0", five0, "five1", five1, "five2", five2)

    if len(five0) == 1:
        segment = five0
    elif len(five1) == 1:
        segment = five1
    elif len(five2) == 1:
        segment = five2
    #print("Right Bottom Segment", segmentMap.seg5)
    return segment


#
# Find Right Top Segment (Segment 2)
#
# subtract segment 5 from number 1 segments
#
#  ...     ...     ...
# .   1   .   .   .   .
# .   1   .   .   .   .
#  ...  -  ...  =  ...
# .   1   .   x   .   S
# .   1   .   x   .   S
#  ...     ...     ...
#
def findSegment2(segment5, number1):
    segment = number1.replace(segment5,'')
    #print("Number 1:", number1, "Segment 5:", number5, "Right Top Segment:", segment)
    return segment




#
# Decode Segments
#
def decodeSegments(decodedNums, fiveSegs):
    segmentMap = SevenSegment()
    # Find top segment
    segmentMap.seg0 = findSegment0(decodedNums[1], decodedNums[7])
    #printSevenSegment(segmentMap)

    # Find middle segment
    segmentMap.seg3 = findSegment3(decodedNums[4], fiveSegs)
    #printSevenSegment(segmentMap)

    # Find bottom segment
    segmentMap.seg6 = findSegment6(segmentMap.seg0, segmentMap.seg3, fiveSegs)
    #printSevenSegment(segmentMap)

    # find left top segment
    segmentMap.seg1 = findSegment1(segmentMap.seg3, decodedNums[4], decodedNums[1])
    #printSevenSegment(segmentMap)

    # find left bottom segment
    segmentMap.seg4 = findSegment4(segmentMap.seg0, segmentMap.seg6, decodedNums[8], decodedNums[4])
    #printSevenSegment(segmentMap)

    # find right bottom segment
    segmentMap.seg5 = findSegment5(segmentMap.seg0, segmentMap.seg1, segmentMap.seg3, segmentMap.seg6, fiveSegs)
    #printSevenSegment(segmentMap)

    # find right top segment
    segmentMap.seg2 = findSegment2(segmentMap.seg5, decodedNums[1])
    #printSevenSegment(segmentMap)

    return segmentMap



#
# Find the Segement Patterns
#
def findPatterns():
    global inputData

    for d in inputData:
        decodedNums = ["" for s in range(10)]
        fiveSegs = []
        for p1Comp in d.part1Comp:
            if len(p1Comp) in easy_seg:
                pos = easy_seg.index(len(p1Comp))
                decodedNums[easy_pos[pos]] = p1Comp
            elif len(p1Comp) == 5:
                fiveSegs.append(p1Comp)

        d.sevenSegmentMap = decodeSegments(decodedNums, fiveSegs)
        #printSevenSegment(d.segmentMap)

        # map to part 1
        segmentNumbers = d.sevenSegmentMap.getDecode()
        for p1Comp in d.part1Comp:
            if p1Comp not in decodedNums:
                n = d.sevenSegmentMap.getNumber(p1Comp)
                decodedNums[n] = p1Comp

        d.numberMap = decodedNums
        dataString = d.part1 + " | "
        for nm in d.numberMap:
            dataString += " " + nm
        #print(dataString)
        #for n in range(len(d.numberMap)):
            #print(n,d.numberMap[n])


#
# Calculate numbers
#
def calculateNumbers():
    global inputData

    for d in inputData:
        d.number = 0
        for p2Comp in d.part2Comp:
            n = d.sevenSegmentMap.getNumber(p2Comp)
            d.number = d.number*10 + n
        #print(d.number)


#
# Sum up the decoded numbers
#
def sumNumbers():
    global inputData

    sumNum = 0
    for d in inputData:
        sumNum += d.number

    return sumNum


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


    # Do the work
    print()
    print("Easy Numbers")
    print()
    easyNumbers = findEasyNumbers()
    print("{}Easy Numbers: {}{}{}".format(color.CYAN, color.YELLOW, easyNumbers, color.END))

    print()
    print("Sum Numbers")
    print()
    findPatterns()
    calculateNumbers()
    sums = sumNumbers()
    print("{}Sum Numbers: {}{}{}".format(color.CYAN, color.YELLOW, sums, color.END))


if __name__ == "__main__":
    main()
