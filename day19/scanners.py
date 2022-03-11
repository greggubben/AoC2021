#
# Adavent of Code Template
#
import sys
import math

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


class Coord:
    x = 0
    y = 0
    z = 0

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "{:>5},{:>5},{:>5}".format(self.x,self.y,self.z)


class Beacon:
    rawCoord = None
    realPosition = None

    def __init__(self, x, y, z, alsoReal = False):
        self.rawCoord = Coord(x,y,z)
        if alsoReal:
            self.realPosition = self.rawCoord

    def __str__(self):
        retString = ""
        if self.realPosition is None:
            retString = "Raw:  " + str(self.rawCoord)
        else:
            retString = color.GREEN + "Real: " + color.END + str(self.realPosition)

        return retString


    def hasRealPosition(self):
        return self.realPosition is not None

    def setRealPosition(self, p):
        self.realPosition = p


class Scanner:
    name = ""
    position = None
    orientation = 0
    beaconScans = []
    d2Between = {}      # Structure to hold a beacon's distance squared relative to another beacon
    d2s = []            # Simple structure to hold distance squared values to do overlap check

    def __init__(self, n):
        self.name = n
        self.position = None
        self.beaconScans = []
        self.d2Between = {}
        self.d2s = []

    def __str__(self):
        retString = "--- scanner " + self.name + " ---\n"
        if self.position is not None:
            retString += "Position: " + color.GREEN + str(self.position) + color.END + "\n"
        retString += " " + color.UNDERLINE + "Beacons" + color.END + ":\n"
        for b in self.beaconScans:
            retString += "    " + str(b) + "\n"
        return retString

    def setPosition(self, p):
        self.position = p

    def hasPosition(self):
        return self.position is not None

    def addBeacon(self, newb):
        for b in self.beaconScans:
            self.d2Between[b][newb] = (newb.rawCoord.x - b.rawCoord.x)**2 + (newb.rawCoord.y - b.rawCoord.y)**2 + (newb.rawCoord.z - b.rawCoord.z)**2
            self.d2s.append(self.d2Between[b][newb])
        self.beaconScans.append(newb)
        self.d2Between[newb] = {}

    def getBeaconsFromD2(self, d2):
        for b1 in self.d2Between.keys():
            for b2 in self.d2Between[b1].keys():
                if self.d2Between[b1][b2] == d2:
                    return b1, b2


#
# Class to manage the possible matches for a known beacon
#
class Possibilities:
    possibleMatches = {}

    def __init__(self):
        self.possibleMatches = {}

    def add(self, unknown, known):
        if unknown not in self.possibleMatches.keys():
            self.possibleMatches[unknown] = []
        if known not in self.possibleMatches[unknown]:
            self.possibleMatches[unknown].append(known)

    def find(self, unknown, known):
        if unknown not in self.possibleMatches.keys():
            return False
        return known in self.possibleMatches[unknown]

    def remove(self, value):
        for k in self.possibleMatches.keys():
            if value in self.possibleMatches[k]:
                self.possibleMatches[k].remove(value)
        if value in self.possibleMatches.keys():
            self.possibleMatches.pop(value)




#
# Load the file into a data array
#
def loadData(filename):

    lines = []
    scanners = []

    scanner = Scanner("")
    f = open(filename)
    for line in f:
        line = line.strip()
        if line.startswith("---"):
            parts = line.split(" ")
            scannerNum = parts[2]
            scanner = Scanner(scannerNum)
            scanners.append(scanner)
        elif len(line) != 0:
            parts = line.split(",")
            x = int(parts[0])
            y = int(parts[1])
            z = int(parts[2])
            newBeacon = Beacon(x,y,z)
            scanner.addBeacon(newBeacon)


        lines.append(line)

    f.close()

    return scanners, lines


#
# Print Scanners
#
def printScanners(scanners):

    for scanner in scanners:
      print(scanner)


#
# Return list of unknown Scanners
#
def getUnknownScanners(scanners):
    unknown = []

    for s in scanners:
        if not s.hasPosition():
            unknown.append(s)

    return unknown


#
# Return list of known Scanners
#
def getKnownScanners(scanners):
    known = []

    for s in scanners:
        if s.hasPosition():
            known.append(s)

    return known


#
# See if scanners are seeing same beacons
# use distance squared between beacons to identify overlap
#
def beaconOverlap(knownScanner, unknownScanner):

    beacons = []
    match = 0
    for usd2 in unknownScanner.d2s:
        if usd2 in knownScanner.d2s:
            match += 1
            beacon1, beacon2 = unknownScanner.getBeaconsFromD2(usd2)
            if beacon1 not in beacons:
                beacons.append(beacon1)
            if beacon2 not in beacons:
                beacons.append(beacon2)

    return len(beacons) >= 12


#
# Map the unknown beacon positions to known beacon positions
#
def mapPositions (possibleMatches, unknownBeacon1, unknownBeacon2, knownBeacon1, knownBeacon2):

    if not unknownBeacon1.hasRealPosition() and unknownBeacon2.hasRealPosition():
        # beacon 1 is unknown, however beacon 2 is known
        # therefore beacon 1 must be the other point
        if unknownBeacon2.realPosition == knownBeacon1.realPosition:
            # unknown beacon 2 aligns with known beacon 1
            # therefore unknown beacon 1 must be aligned with known beacon 2
            print(color.YELLOW + "      found" + color.END, unknownBeacon1, "-->", knownBeacon2)
            unknownBeacon1.setRealPosition(knownBeacon2.realPosition)
            possibleMatches.remove(unknownBeacon1)
            possibleMatches.remove(knownBeacon2)

        elif unknownBeacon2.realPosition == knownBeacon2.realPosition:
            # unknown beacon 2 aligns with known beacon 2
            # therefore unknown beacon 1 must be aligned with known beacon 1
            print(color.YELLOW + "      found" + color.END, unknownBeacon1, "-->", knownBeacon1)
            unknownBeacon1.setRealPosition(knownBeacon1.realPosition)
            possibleMatches.remove(unknownBeacon1)
            possibleMatches.remove(knownBeacon1)

    elif unknownBeacon1.hasRealPosition() and not unknownBeacon2.hasRealPosition():
        # beacon 2 is unknown, however beacon 1 is known
        # therefore beacon 2 must be the other point
        if unknownBeacon1.realPosition == knownBeacon1.realPosition:
            # unknown beacon 1 aligns with known beacon 1
            # therefore unknown beacon 2 must be aligned with known beacon 2
            print(color.YELLOW + "      found" + color.END, unknownBeacon2, "-->", knownBeacon2)
            unknownBeacon2.setRealPosition(knownBeacon2.realPosition)
            possibleMatches.remove(unknownBeacon2)
            possibleMatches.remove(knownBeacon2)

        elif unknownBeacon1.realPosition == knownBeacon2.realPosition:
            # unknown beacon 1 aligns with known beacon 2
            # therefore unknown beacon 2 must be aligned with known beacon 1
            print(color.YELLOW + "      found" + color.END, unknownBeacon2, "-->", knownBeacon1)
            unknownBeacon2.setRealPosition(knownBeacon1.realPosition)
            possibleMatches.remove(unknownBeacon2)
            possibleMatches.remove(knownBeacon1)

    elif not unknownBeacon1.hasRealPosition() and not unknownBeacon2.hasRealPosition():
        # both beacons are unknown
        addBeacon1 = True
        addBeacon2 = True

        if possibleMatches.find(unknownBeacon1, knownBeacon1):
            # unknown Beacon 1 has been seen with knownBeacon1 before - must be match
            print(color.YELLOW + "      match " + color.END, unknownBeacon1, "-->", knownBeacon1)
            unknownBeacon1.setRealPosition(knownBeacon1.realPosition)
            possibleMatches.remove(unknownBeacon1)
            possibleMatches.remove(knownBeacon1)
            addBeacon1 = False
            # now that unknown Beacon 1 is known, unknown Beacon 2 must be known Beacon 2
            print(color.YELLOW + "      match " + color.END, unknownBeacon2, "-->", knownBeacon2)
            unknownBeacon2.setRealPosition(knownBeacon2.realPosition)
            possibleMatches.remove(unknownBeacon2)
            possibleMatches.remove(knownBeacon2)
            addBeacon2 = False

        elif possibleMatches.find(unknownBeacon1, knownBeacon2):
            # unknown Beacon 1 has been seen with knownBeacon2 before - must be match
            print(color.YELLOW + "      match " + color.END, unknownBeacon1, "-->", knownBeacon2)
            unknownBeacon1.setRealPosition(knownBeacon2.realPosition)
            possibleMatches.remove(unknownBeacon1)
            possibleMatches.remove(knownBeacon2)
            addBeacon1 = False
            # now that unknown Beacon 1 is known, unknown Beacon 2 must be known Beacon 1
            print(color.YELLOW + "      match " + color.END, unknownBeacon2, "-->", knownBeacon1)
            unknownBeacon2.setRealPosition(knownBeacon1.realPosition)
            possibleMatches.remove(unknownBeacon2)
            possibleMatches.remove(knownBeacon1)
            addBeacon2 = False

        elif possibleMatches.find(unknownBeacon2, knownBeacon1):
            # unknown Beacon 2 has been seen with knownBeacon1 before - must be match
            print(color.YELLOW + "      match " + color.END, unknownBeacon2, "-->", knownBeacon1)
            unknownBeacon2.setRealPosition(knownBeacon1.realPosition)
            possibleMatches.remove(unknownBeacon2)
            possibleMatches.remove(knownBeacon1)
            addBeacon2 = False
            # now that unknown Beacon 2 is known, unknown Beacon 1 must be known Beacon 2
            print(color.YELLOW + "      match " + color.END, unknownBeacon1, "-->", knownBeacon2)
            unknownBeacon1.setRealPosition(knownBeacon2.realPosition)
            possibleMatches.remove(unknownBeacon1)
            possibleMatches.remove(knownBeacon2)
            addBeacon1 = False

        elif possibleMatches.find(unknownBeacon2, knownBeacon2):
            # unknown Beacon 2 has been seen with knownBeacon2 before - must be match
            print(color.YELLOW + "      match " + color.END, unknownBeacon2, "-->", knownBeacon2)
            unknownBeacon2.setRealPosition(knownBeacon2.realPosition)
            possibleMatches.remove(unknownBeacon2)
            possibleMatches.remove(knownBeacon2)
            addBeacon2 = False
            # now that unknown Beacon 2 is known, unknown Beacon 1 must be known Beacon 1
            print(color.YELLOW + "      match " + color.END, unknownBeacon1, "-->", knownBeacon1)
            unknownBeacon1.setRealPosition(knownBeacon1.realPosition)
            possibleMatches.remove(unknownBeacon1)
            possibleMatches.remove(knownBeacon1)
            addBeacon1 = False

        # TODO: if a known beacon is already claimed do not add
        if addBeacon1:
            # Add to possible matches list for later
            print("      adding", unknownBeacon1, "-->", knownBeacon1)
            possibleMatches.add(unknownBeacon1, knownBeacon1)
            print("      adding", unknownBeacon1, "-->", knownBeacon2)
            possibleMatches.add(unknownBeacon1, knownBeacon2)

        if addBeacon2:
            # Add to possible matches list for later
            print("      adding", unknownBeacon2, "-->", knownBeacon1)
            possibleMatches.add(unknownBeacon2, knownBeacon1)
            print("      adding", unknownBeacon2, "-->", knownBeacon2)
            possibleMatches.add(unknownBeacon2, knownBeacon2)


#
# Try to match the unknown scanner's beacons with the known scanner's beacons
#
def matchEachBeacon(unknownScanner, knownScanner):

    possibleMatches = Possibilities()

    # Go through every beacon pair with matching distance squared
    for knownBeacon1 in knownScanner.d2Between:
      for knownBeacon2 in knownScanner.d2Between[knownBeacon1]:
        for unknownBeacon1 in unknownScanner.d2Between:
          for unknownBeacon2 in unknownScanner.d2Between[unknownBeacon1]:
            if knownScanner.d2Between[knownBeacon1][knownBeacon2] == \
                    unknownScanner.d2Between[unknownBeacon1][unknownBeacon2]:
              print()
              print("  D2: {}".format(knownScanner.d2Between[knownBeacon1][knownBeacon2]))
              print("      Known: {} - {}".format(str(knownBeacon1), str(knownBeacon2)))
              print("    Unknown: {} - {}".format(str(unknownBeacon1), str(unknownBeacon2)))
              # Figure out real positions for the 2 unknown beacons
              mapPositions(possibleMatches,unknownBeacon1,unknownBeacon2,knownBeacon1,knownBeacon2)

    # Handle any unmatched beacons
    if len(possibleMatches.possibleMatches) > 0:
        print(color.RED, "Leftover Possible Matches", len(possibleMatches.possibleMatches), color.END)
    #while unmatchedBeacons:
    #    determine match


#
# Determine the position of the scanner
#
def determineScannerPosition(unknownScanner):

    #for adjust in [-1, 1]
    firstX = None
    firstY = None
    firstZ = None
    for beacon in unknownScanner.beaconScans:
        xColor = ""
        yColor = ""
        zColor = ""
        if beacon.hasRealPosition():
            x = beacon.rawCoord.x + beacon.realPosition.x
            y = beacon.rawCoord.y + beacon.realPosition.y
            z = beacon.rawCoord.z + beacon.realPosition.z
            if firstX is None:
                firstX = x
                firstY = y
                firstZ = z
            else:
                if firstX == x:
                    xColor = color.GREEN
                if firstY == y:
                    yColor = color.GREEN
                if firstZ == z:
                    zColor = color.GREEN

            print("   Raw: ",str(beacon.rawCoord))
            print(" + Real:",str(beacon.realPosition))
            print(" =      ","{}{:>5}{},{}{:>5}{},{}{:>5}{}".format(xColor,x,color.END,yColor,y,color.END,zColor,z,color.END))
            print()


    for angle in range(0,360,90):
        print("cos", angle, math.cos(math.radians(angle)))


#
# Do the alignment math
#
def alignScanner(unknownScanner, knownScanner):

    # First match up each beacon
    matchEachBeacon(unknownScanner, knownScanner)

    # Find Scanner Position
    determineScannerPosition(unknownScanner)

    # Update beacons with real positions
    #updateBeaconRealPosition(unknownScanner)


#
# find beacon locations
#
def findBeaconPositions(scanners):

    beacons = []

    # Set up scanner 0 at coordinates 0, 0, 0
    scanner0 = scanners[0]
    scanner0.setPosition(Coord(0,0,0))
    for b in scanner0.beaconScans:
        b.setRealPosition(b.rawCoord)
        beacons.append(b)

    unknownScanners = getUnknownScanners(scanners)
    while len(unknownScanners) > 0:
        knownScanners = getKnownScanners(scanners)
        for knownScanner in knownScanners:
            print("Known Scanner: ", color.GREEN, knownScanner.name, color.END)
            for unknownScanner in unknownScanners:
                if beaconOverlap(knownScanner,unknownScanner):
                    print("  {}   Match: {}{}".format(color.YELLOW, unknownScanner.name, color.END))
                    alignScanner(unknownScanner, knownScanner)
                else:
                    print("  No Match: {}".format(unknownScanner.name))
        unknownScanners = getUnknownScanners(scanners)
        unknownScanners = []

    return beacons





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
    scanners, lines = loadData(filename)
    print(" Lines Read: ", len(lines))
    print()

    # Do Part 1 work
    printScanners(scanners)
    beacons = findBeaconPositions(scanners)
    printScanners(scanners)
    answer = len(beacons)
    print()
    print("{}Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer, color.END))

    # Do Part 2 work
    #print()
    #printLines(lines)
    #print()
    #print("{}Answer: {}{}{}".format(color.CYAN, color.YELLOW, answer color.END))


if __name__ == "__main__":
    main()
