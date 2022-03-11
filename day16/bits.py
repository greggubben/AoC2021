#
# Adavent of Code Template
#
import sys
import numpy

fullBits = 0

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


typeNames = ["Sum", "Product", "Minimum", "Maximum", "Literal", "Greater than", "Less than", "Equal to"]
lengthNames = ["Bits", "Sub Packets"]

class Packet:
    version = 0
    typeID = 0
    number = 0
    lengthType = 0
    length = 0
    subPackets = []

    def __init__(self, v, t):
        self.version = v
        self.typeID = t
        self.subPackets = []

    def __str__(self):
        header = color.CYAN + "Packet: " + color.END
        info  = "|     Version: {}\n".format(self.version)
        info += "|     Type ID: {} - {}{}{}\n".format(self.typeID, color.GREEN, typeNames[self.typeID], color.END)
        if self.typeID == 4:
            header += "Literal Value"
            info += "|      Number: {}{}{}\n".format(color.YELLOW, self.number, color.END)
        else:
            header += "Operator"
            info += "|    Len Type: {}\n".format(self.lengthType)
            info += "|      Length: {} {}\n".format(self.length, lengthNames[self.lengthType])
            info += "| Sub Packets: {}{}{}\n".format(color.YELLOW, len(self.subPackets), color.END)
        boxLen = 30

        return "{}\n+{}+\n{}+{}+\n".format(header, "-"*boxLen, info,"-"*boxLen)

    #
    # Evaluate the commands and return the value
    #
    def evaluate(self):
        if self.typeID == 4:
            return self.number

        value = 0
        packetValues = []
        for sp in self.subPackets:
            packetValues.append(sp.evaluate())

        if self.typeID == 0:
            # Sum packets
            value = sum(packetValues)

        elif self.typeID == 1:
            # Product of packets
            value = numpy.prod(packetValues)

        elif self.typeID == 2:
            # Min packets
            value = min(packetValues)

        elif self.typeID == 3:
            # Max packets
            value = max(packetValues)

        elif self.typeID == 5:
            # Greater than
            if packetValues[0] > packetValues[1]:
                value = 1
            else:
                value = 0

        elif self.typeID == 6:
            # Less than
            if packetValues[0] < packetValues[1]:
                value = 1
            else:
                value = 0

        elif self.typeID == 7:
            # Equals
            if packetValues[0] == packetValues[1]:
                value = 1
            else:
                value = 0

        return value


    #
    # produce the formula
    #
    def formula(self):
        formulaString = ""

        if self.typeID == 4:
            formulaString += str(self.number)
        else:

            packetFormulas = []
            for sp in self.subPackets:
                packetFormulas.append(sp.formula())

            if self.typeID == 0:
                # Sum packets
                formulaString += "( " + " + ".join(packetFormulas) + " )"

            elif self.typeID == 1:
                # Product packets
                formulaString += "( " + " * ".join(packetFormulas) + " )"

            elif self.typeID == 2:
                # Minimum packets
                formulaString += "min( " + ", ".join(packetFormulas) + " )"

            elif self.typeID == 3:
                # Maximum packets
                formulaString += "max( " + ", ".join(packetFormulas) + " )"

            elif self.typeID == 5:
                # Greater than
                formulaString += "( " + packetFormulas[0] + " > " + packetFormulas[1] + " )"

            elif self.typeID == 6:
                # Less than
                formulaString += "( " + packetFormulas[0] + " < " + packetFormulas[1] + " )"

            elif self.typeID == 7:
                # Equals
                formulaString += "( " + packetFormulas[0] + " == " + packetFormulas[1] + " )"

        return formulaString


    #
    # Print the packets in nested format
    #
    def nestedPrint(self):

        printStr = str(self)

        if self.typeID != 4:
            for p in self.subPackets:
                spString = p.nestedPrint()
                for l in spString.splitlines():
                    printStr += "  " + l + "\n"

        return printStr








#
# Load the file into a data array
#
def loadData(filename):

    lines = 0
    line = ""

    f = open(filename)
    for line in f:
        line = line.strip()
        #print(inputData[lines])
        lines += 1

    f.close()

    return line, lines


#
# get the specified number of bits from the bit list
#
def getBits(num, bits, bitPos):
    global fullBits

    print(format(bits,"0" + str(fullBits) + "b"), bitPos)
    print("{}{}".format(" "*(bits.bit_length()-bitPos),"^"*num), num)
    #print(num, bitPos)
    mask = 0
    for n in range(num):
        mask = mask<<1
        mask += 1
    remainingLen = bitPos - num
    mask = mask << remainingLen
    val = bits & mask
    val = val >> remainingLen
    bitPos -= num

    return val, bitPos


#
# process the next packet
#
def processNextPacket(bits, bitPos):

    version, bitPos = getBits(3, bits, bitPos)
    typeID, bitPos = getBits(3, bits, bitPos)
    packet = Packet(version, typeID)
    #print(str(packet))
    if typeID == 4:
        # Literal Value
        lastGroup = False
        number = 0
        while not lastGroup:
            more, bitPos = getBits(1, bits, bitPos)
            if more == 0: lastGroup = True
            numPart, bitPos = getBits(4, bits, bitPos)
            number = number << 4
            number += numPart
        packet.number = number

    else:
        # Operator
        lenType, bitPos = getBits(1, bits, bitPos)
        packet.lengthType = lenType
        if lenType == 0:
            # represent number of bits that contain sub-packets
            lenBits, bitPos = getBits(15, bits, bitPos)
            packet.length = lenBits
            startBits = bitPos
            while startBits - bitPos < lenBits:
                subPacket, bitPos = processNextPacket(bits, bitPos)
                packet.subPackets.append(subPacket)
        else:
            # represent the number of sub-packets
            subPacketCount, bitPos = getBits(11, bits, bitPos)
            packet.length = subPacketCount
            for sp in range(subPacketCount):
                subPacket, bitPos = processNextPacket(bits, bitPos)
                packet.subPackets.append(subPacket)

    #print()
    #print(str(packet))
    return packet, bitPos

#
# Process the Packets from the bits
#
def processPackets(bits, bitsLen):

    bitPos = bitsLen
    packets = []
    moreBits, p = getBits(bitPos, bits, bitPos)
    while moreBits != 0:
        packet, bitPos = processNextPacket(bits, bitPos)
        packets.append(packet)
        moreBits, p = getBits(bitPos, bits, bitPos)

    return packets


#
# Sum Versions
#
def sumVersions(packets):

    sumVer = 0
    for packet in packets:
        sumVer += packet.version
        if len(packet.subPackets) > 0:
            sumVer += sumVersions(packet.subPackets)

    return sumVer


#
# Main
#
def main():
    global fullBits

    args = sys.argv[1:]
    if len(args) != 1:
        print("Usage: " + sys.argv[0] + " inputfile");
        return
    filename = args[0]
    print("Input File:", filename)

    # Load data
    line, lines = loadData(filename)
    print(" Lines Read: ", lines)
    print("Data Loaded: ", len(line))
    print()
    print(line)
    print()

    # Do Part 1 work

    bits = int(line,16)
    fullBits = len(line) * 4
    #bitAlign = fullBits % 4
    #if bitAlign != 0: fullBits += (4-bitAlign)
    print()
    print(bits)
    print(format(bits, "0" + str(fullBits) + "b"))
    print("Bit Length:", bits.bit_length())
    print(" Full Bits:", fullBits)
    packets = processPackets(bits,fullBits)
    sumVer = sumVersions(packets)
    print()
    print(packets[0].nestedPrint())
    print()
    print("{}Sum of Versions: {}{}{}".format(color.CYAN, color.YELLOW, sumVer, color.END))

    # Do Part 2 work
    print()
    print(packets[0].formula())
    print()
    value = packets[0].evaluate()
    print("{}Evaluated Value: {}{}{}".format(color.CYAN, color.YELLOW, value, color.END))


if __name__ == "__main__":
    main()
