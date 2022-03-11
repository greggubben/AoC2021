#
# Adavent of Code Day 3
#
import sys

# Global Variables
filename = ""
bits=8
data =[]
gamma = 0
epsilon = 0
oxygen= 0
co2 = 0


#
# Load the file into a data array
#
def loadData(filename):
    global data

    lines = 0

    f = open(filename)
    for line in f:
        data.append(int(line,2))
        #print('{0:b}'.format(data[lines]).zfill(bits))
        lines += 1

    f.close()

    return lines


#
# Determine how many 0s and 1s in each bit
#
def calculateGammaEpsilon(bits):
    global gamma, epsilon

    zeros = [0] * bits
    ones  = [0] * bits

    # Count zeros and ones
    for d in data:
        mask = 1
        for b in range(bits):
            if (mask & d) == 0:
                zeros[b] += 1
            else:
                ones[b] += 1
            mask = mask << 1

    # build gamma and epsilon
    gamma = 0
    epsilon = 0
    mask = 1
    for b in range(bits):
        if ones[b] > zeros[b]:
            gamma += mask
        else:
            epsilon += mask
        mask = mask << 1


#
# Determine Oxygen Generator Rating
#
def calculateOxygen(bits):
    global oxygen

    sourceData = []
    filteredData = []

    sourceData = data

    # Loop through each bit
    for b in range(bits):
      mask = 1<<(bits - b - 1)
      #print(b, "Mask:", '{0:b}'.format(mask).zfill(bits))

      # Count zeros and ones
      zeros = 0
      ones = 0
      for d in sourceData:
        if (mask & d) == 0:
            zeros += 1
        else:
            ones += 1

      # Which to keep
      if (zeros > ones):
          keep = 0
          #print("  Keep 0")
      else:
          keep = mask
          #print("  Keep 1")
      
      # Filter for data to keep
      filteredData = []
      for d in sourceData:
          if ((d & mask) == keep):
              filteredData.append(d)

      # Are we down to only one reading left
      if (len(filteredData) == 1):
          oxygen = filteredData[0]
          #print("  Found Last Element")
          break

      # start over with next bit using the filtered data
      sourceData = filteredData


#
# Determine CO2 Generator Rating
#
def calculateCO2(bits):
    global co2

    sourceData = []
    filteredData = []

    sourceData = data

    # Loop through each bit
    for b in range(bits):
      mask = 1<<(bits - b - 1)
      #print(b, "Mask:", '{0:b}'.format(mask).zfill(bits))

      # Count zeros and ones
      zeros = 0
      ones = 0
      for d in sourceData:
        if (mask & d) == 0:
            zeros += 1
        else:
            ones += 1

      # Which to keep
      if (zeros <= ones):
          keep = 0
          #print("  Keep 0")
      else:
          keep = mask
          #print("  Keep 1")
      
      # Filter for data to keep
      filteredData = []
      for d in sourceData:
          if ((d & mask) == keep):
              filteredData.append(d)

      # Are we down to only one reading left
      if (len(filteredData) == 1):
          co2 = filteredData[0]
          #print("  Found Last Element")
          break

      # start over with next bit using the filtered data
      sourceData = filteredData



#
# Main
#
def main():
    global filename, bits

    args = sys.argv[1:]
    if len(args) != 2:
        print("Usage: " + sys.argv[0] + " inputfile bits");
        return
    filename = args[0]
    bits = int(args[1])
    print("Input File:", filename)
    print("Bits:", bits)

    # Load data
    lines = loadData(filename)
    print(" Lines Read: ", lines)
    print("Data Loaded: ", len(data))

    # Part 1: calculate Gamma, Epsilon, and power
    calculateGammaEpsilon(bits)
    power = gamma * epsilon
    print("  Gamma: ", '{0:b}'.format(gamma).zfill(bits), gamma)
    print("Epsilon: ", '{0:b}'.format(epsilon).zfill(bits), epsilon)
    print("  Power: ", power)

    # Part 2: calculate Oxygen and CO2 Generator Ratings
    calculateOxygen(bits)
    print("      Oxygen: ", '{0:b}'.format(oxygen).zfill(bits), oxygen)
    calculateCO2(bits)
    print("         CO2: ", '{0:b}'.format(co2).zfill(bits), co2)
    lifeSupport = oxygen * co2
    print("Life Support: ", lifeSupport)


if __name__ == "__main__":
    main()
