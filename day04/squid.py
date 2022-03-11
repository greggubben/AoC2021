#
# Adavent of Code Template
#
import sys
import copy

# Global Variables
filename = ""
inputData = []
bingoBoards = []

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
    global inputData, bingoBoards

    loadBoards = False
    bingoBoard = [[0 for r in range(5)] for c in range(5)]
    row = 0
    col = 0

    lines = 0

    f = open(filename)
    for line in f:
        if loadBoards:
            if not line.strip():
                # Blank line starts new board
                bingoBoard = [[0 for r in range(5)] for c in range(5)]
                row = 0
                col = 0
                bingoBoards.append(bingoBoard)
                #print("New Board")
            else:
                squares = line.split()
                col = 0
                for s in squares:
                    square = {}
                    square["value"] = int(s)
                    square["selected"] = False
                    #print(row, col, square)
                    bingoBoard[row][col] = square
                    col += 1
                row += 1

        else:
            # First line is drawn numbers
            lineData = line.split(",")
            for d in lineData:
                inputData.append(int(d))
            loadBoards = True
            #print("First Line")
        lines += 1

    f.close()

    return lines


#
# Reset all boards to unmarked
#
def resetBoards():
    for bingoCard in bingoBoards:
        for r in range(5):
            for c in range(5):
                bingoCard[r][c]["selected"] = False


#
# Mark the drawn number on the card
#
def markCard(card, drawnNumber):
    found = False
    for r in range(5):
        for c in range(5):
            if card[r][c]["value"] == drawnNumber:
                card[r][c]["selected"] = True
                found = True
                break
        if found:
            break
    return found


#
# Check if the card won
#
def checkCard(card):
    won = False

    # Check rows
    for r in range(5):
        rowFilled = True
        for c in range(5):
            rowFilled &= card[r][c]["selected"]
            if not rowFilled:
                break
        if rowFilled:
            won = True
            break

    # if a row is fully selected then we have a winner
    if won:
        return won

    # Check colums
    for c in range(5):
        columnFilled = True
        for r in range(5):
            columnFilled &= card[r][c]["selected"]
            if not columnFilled:
                columnFilled = False
                break
        if columnFilled:
            won = True
            break

    return won


#
# Loop through Array
# draw a number and check each board for the number
#
def findFirstWinningBoard():
    global inputData, bingoBoards

    markedCards = 0
    weHaveAWinner = False
    winningCard = []
    winningDraw = 0

    for drawn in inputData:
        markedCards = 0
        for bingoCard in bingoBoards:
            if markCard(bingoCard, drawn):
                markedCards += 1
                if checkCard(bingoCard):
                    winningCard = bingoCard
                    weHaveAWinner = True
                    break

        #print("Drawn: {:>4} Marked: {:>4} Winners: {}".format(drawn, markedCards, weHaveAWinner))
        if weHaveAWinner:
            winningDraw = drawn
            break
    return winningCard, winningDraw


#
# Loop through Array
# draw a number and check each board for the number
#
def findLastWinningBoard():
    global inputData, bingoBoards

    #
    unwonBoards = copy.deepcopy(bingoBoards)
    wonBoards = []

    markedCards = 0
    winningCards = 0
    weHaveAWinner = False
    winningCard = []
    winningDraw = 0

    for drawn in inputData:
        markedCards = 0
        winningCards = 0
        wonBoards = []
        for bingoCard in unwonBoards:
            if markCard(bingoCard, drawn):
                markedCards += 1
                if checkCard(bingoCard):
                    winningCards += 1
                    winningCard = bingoCard
                    weHaveAWinner = True
                    wonBoards.append(winningCard)

        # Remove all the won boards from the game
        for w in wonBoards:
            unwonBoards.remove(w)

        print("Drawn: {:>4} Marked: {:>4} Winners: {}".format(drawn, markedCards, winningCards))
        if len(unwonBoards) == 0:
            winningDraw = drawn
            break
    return winningCard, winningDraw


#
# Print a bingo boards
#
def printCard(bingoCard):
    for r in range(5):
        rowText = ""
        for c in range(5):
            postText = ""
            if bingoCard[r][c]["selected"]:
                rowText += color.BOLD + color.YELLOW
                postText = color.END
            rowText += "{:>4}".format(bingoCard[r][c]["value"]) + postText
        print(rowText)


#
# Print a bingo boards
#
def sumUnmarked(bingoCard):
    unmarkedSum = 0
    for r in range(5):
        for c in range(5):
            if not bingoCard[r][c]["selected"]:
                unmarkedSum += bingoCard[r][c]["value"]

    return unmarkedSum
            

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
    print("   Lines Read: ", lines)
    print(" Bingo Boards: ", len(bingoBoards))
    print("Drawn Numbers: ", len(inputData))
    #print(bingoBoards)

    # Do the work
    print()
    print("Win First")
    winningBoard, winningDraw = findFirstWinningBoard()
    printCard(winningBoard)
    unmarkedSum = sumUnmarked(winningBoard)
    score = unmarkedSum * winningDraw
    print("Winning Draw: ", winningDraw)
    print("Unmarked Sum: ", unmarkedSum)
    print(" Final Score: ", score)

    resetBoards()

    print()
    print("Win Last")
    winningBoard, winningDraw = findLastWinningBoard()
    printCard(winningBoard)
    unmarkedSum = sumUnmarked(winningBoard)
    score = unmarkedSum * winningDraw
    print("Winning Draw: ", winningDraw)
    print("Unmarked Sum: ", unmarkedSum)
    print(" Final Score: ", score)


if __name__ == "__main__":
    main()
