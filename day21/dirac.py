#
# Adavent of Code Day 21
# Dirac Dice
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


class DeterministicDice:
    lastResult = 0
    rolls = 0

    def __init__(self):
        self.lastResult = 0
        self.rolls = 0

    def roll(self):
        self.rolls += 1
        self.lastResult += 1
        if self.lastResult > 100: self.lastResult = 1
        return self.lastResult


class Player:
    name = ""
    startingPos = 0
    pos = 0
    score = 0
    universe = 0

    def __init__(self, n, p):
        self.name = n
        self.startingPos = p
        self.pos = p
        self.score = 0
        self.universe = 0

    def __str__(self):
        return "Player {} at position {}{}{} with score {}{}{}".format(self.name, color.YELLOW, self.pos, color.END, color.GREEN, self.score, color.END)

    def reset(self):
        self.pos = self.startingPos
        self.score = 0
        self.universe = 0



#
# Load the file into a data array
#
def loadData(filename):
    global inputData

    lines = []
    players = []

    f = open(filename)
    for line in f:
        line = line.strip()
        parts = line.split()
        name = parts[1]
        position = int(parts[4])
        player = Player(name, position)
        players.append(player)

        lines.append(line)

    f.close()

    return players[0], players[1], lines


#
# Print Array
#
def printLines(lines):

    for line in lines:
      print(line)


#
# play deterministic dirac dice
#
def playDeterministic(player1, player2):

    turns = 0
    winner = None
    loser = None
    dice = DeterministicDice()
    players = [player1, player2]

    won = False
    while not won:
        player = players[turns%2]
        move = dice.roll() + dice.roll() + dice.roll()
        newPos = (player.pos + move)%10
        if newPos == 0: newPos = 10
        player.pos = newPos
        player.score += newPos
        won = player.score >= 1000
        print(str(player))
        if won:
            winner = player
            loser = players[(turns+1)%2]
            break

        turns += 1

    return winner, loser, dice.rolls


#
# Compute the universes for each move in 1 turn
#
def getMoves2Universes():
    moves = {}
    totalUniverses = 0

    for d1 in range(1,4):
        for d2 in range(1,4):
            for d3 in range(1,4):
                move = d1+d2+d3
                totalUniverses += 1
                if move in moves.keys():
                    moves[move] += 1     # universes
                else:
                    moves[move] = 1      # universes

    return moves, totalUniverses


#
# Sum the winning universes
#
def sumWinningUniverses(score):
    universes = 0

    for s in range(21,32):
        for p in score[s]:
            universes += p

    return universes


#
# play quantum dirac dice
#
def playQuantum_old(player1, player2):

    moves, universesByTurn = getMoves2Universes()
    print("Moves {Move:Universes}", moves)
    print("    Universes By Turn:", universesByTurn)

    player1.reset()
    player2.reset()

    score1 = [[0 for p in range(11)] for _ in range(32)]
    score2 = [[0 for p in range(11)] for _ in range(32)]

    score1[0][player1.pos] = 1
    score2[0][player2.pos] = 1

    turns = 0
    players = [player1, player2]
    scores = [score1, score2]

    done = False
    while not done:
        player = players[turns%2]
        score = scores[turns%2]
        done = True                 # be optimistic there is no more moves left
        #print()
        #print("Turn", turns)
        #print(player)
        #print(score)

        # Move the player and multiply the universes
        for s in range(20,-1,-1):
            #print("score:", s, "universes",score[s])
            for p in range(11):
                if score[s][p] != 0:
                    done = False        # need to move - not done
                    for move in moves.keys():
                        newPos = (p + move)%10
                        if newPos == 0: newPos = 10
                        newScore = s + newPos
                        score[newScore][newPos] += score[s][p] * moves[move]

                    score[s][p] = 0
            #print(score)

        # If player moved then the other player also advanced through universes
        if not done:
            otherScore = scores[(turns+1)%2]

            for s in range(len(otherScore)):
                for p in range(len(otherScore[s])):
                    otherScore[s][p] *= universesByTurn

        turns += 1

    universes1 = sumWinningUniverses(score1)
    universes2 = sumWinningUniverses(score2)

    return universes1, universes2


#
# play quantum dirac dice
#
def playQuantum(player1, player2):

    moves, universesByTurn = getMoves2Universes()
    print("Moves {Move:Universes}", moves)
    print("    Universes By Turn:", universesByTurn)

    player1.reset()
    player2.reset()
    players = [player1, player2]

    #   [ score1, score2, pos1, pos2, universe1, universe2 ]
    score = 0
    pos = 2
    universe = 4
    lastTurn = {}
    lastTurn[(0, 0, player1.pos, player2.pos)] = 1

    turns = 0
    done = False
    while not done:
        offset = turns%2
        otherOffset = (turns+1)%2
        #print()
        #print(lastTurn)

        newTurn = {}
        for t in lastTurn.keys():
            curScore = t[score+offset]
            curPos = t[pos+offset]
            otherScore = t[score+otherOffset]
            otherPos = t[pos+otherOffset]
            for move in moves.keys():
                newPos = (curPos + move)%10
                if newPos == 0: newPos = 10
                newScore = curScore + newPos
                newUniverse = lastTurn[t] * moves[move]
                if newScore >= 21:
                    players[offset].universe += newUniverse
                else:
                    newT = set(t)
                    if offset == 0:
                        #player1
                        newT = (newScore, otherScore, newPos, otherPos)
                    else:
                        #player2
                        newT = (otherScore, newScore, otherPos, newPos)
                    if newT in newTurn.keys():
                        newTurn[newT] += newUniverse
                    else:
                        newTurn[newT] = newUniverse

        #print(newTurn.keys())
        lastTurn = newTurn
        turns += 1
        done = len(lastTurn) == 0




    return player1.universe, player2.universe


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
    player1, player2, lines = loadData(filename)
    print(" Lines Read: ", len(lines))
    print()

    # Do Part 1 work
    print("Starting Positions:")
    print(player1)
    print(player2)
    print()
    winner, loser, rolls = playDeterministic(player1, player2)
    print()
    print("Loser score:", loser.score)
    print("      Rolls:", rolls)
    answer = loser.score * rolls
    print()
    print("{}Deterministic Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))

    # Do Part 2 work
    print()
    #universes1, universes2 = playQuantum_old(player1, player2)
    universes1, universes2 = playQuantum(player1, player2)
    print("Player 1 Universes:", universes1)
    print("Player 2 Universes:", universes2)
    if universes1 > universes2:
        answer = universes1
        winningPlayer = "Player 1"
    else:
        answer = universes2
        winningPlayer = "Player 2"

    print()
    print("{}Winner {}: {}{}{}".format(color.CYAN, winningPlayer, color.YELLOW, answer, color.END))


if __name__ == "__main__":
    main()
