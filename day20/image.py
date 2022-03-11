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


#
# Load the file into a data array
#
def loadData(filename):
    global inputData

    lines = []

    enhancementString = ""
    image = []

    f = open(filename)
    for line in f:
        line = line.strip()
        if line == "":
            pass
        elif enhancementString == "":
            enhancementString = line
        else:
            image.append(line)
        lines.append(line)

    f.close()

    return enhancementString, image, lines


#
# Print Image
#
def printImage(image):

    for line in image:
      print(line)


#
# Cound lit pixels
#
def countLitPixels(image):
    count = 0

    for i in image:
        count += i.count('#')
    return count


#
# Get subgrid
#
def getSubImage(x1, y1, x2, y2, image):
    return [row[x1:x2] for row in image[y1:y2]]


#
# Expand Image
#
def expandImage(image, expand):
    expandedImage = []
    for _ in range(expand):
        expandedImage.append("." * (len(image[0])+(expand*2)))
    for row in image:
        expandedImage.append(("."*expand) + row + ("."*expand))
    for _ in range(expand):
        expandedImage.append("." * (len(image[0])+(expand*2)))
    return expandedImage


#
# Perform the enhancement
#
def performEnhancement(image):
    global enhancementString

    sourceImage = image

    enhancedImage = []
    enhancedImageY = len(image) - 2
    enhancedImageX = len(image[0]) - 2
    for y in range(enhancedImageY):
        enhancedRow = ""
        for x in range(enhancedImageX):
            enhPart = getSubImage(x,y,x+3,y+3,sourceImage)
            indexString = "".join(enhPart)
            indexString = indexString.translate(str.maketrans({'.':'0','#':'1'}))
            index = int(indexString,2)
            enhancedRow += enhancementString[index]
        enhancedImage.append(enhancedRow)

    return enhancedImage



#
# Enhance the image
#
def enhanceImage(image, enhancements):

    enhancedImage = expandImage(image, 4 + (enhancements*2))
    for _ in range(enhancements):
        enhancedImage = performEnhancement(enhancedImage)

    return enhancedImage


#
# Main
#
def main():
    global enhancementString

    args = sys.argv[1:]
    if len(args) != 2:
        print("Usage: " + sys.argv[0] + " inputfile enhancements");
        return
    filename = args[0]
    enhancements = int(args[1])
    print("  Input File:", filename)
    print("Enhancements:", enhancements)

    # Load data
    enhancementString, image, lines = loadData(filename)
    print("  Lines Read: ", len(lines))
    print(" Enhancement: ", len(enhancementString))
    print("   Image y,x: ", len(image), ",", len(image[0]))
    print()

    # Do Part 1 work
    printImage(image)
    enhancedImage = enhanceImage(image, enhancements)
    printImage(enhancedImage)
    answer = countLitPixels(enhancedImage)
    print()
    print("{}Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))

    # Do Part 2 work
    #print()
    #printLines(lines)
    #print()
    #print("{}Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer color.END))


if __name__ == "__main__":
    main()
