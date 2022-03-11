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


# list of successful paths
paths = []

# Holds all nodes
nodes = {}

class Node:
    name = ""
    multiVisit = False
    children = []

    # Constructor
    def __init__(self, name):
        self.name = name
        self.multiVisit = (name == name.upper())
        self.children = []

    # Add a child node to this node
    def addChild(self,child):
        self.children.append(child)



#
# Find a node and if it does not exist create it
#
def findNode(name):
    global nodes

    if name in nodes.keys():
        return nodes[name]
    else:
        node = Node(name)
        nodes[name] = node
        return node


#
# Print the contents of a node
#
def printNode(node):
    print("{}       Name: {}{}{}".format(color.CYAN, color.YELLOW,node.name,color.END))
    print("Multi Visit:", node.multiVisit)
    print("   Children:", len(node.children))
    for c in node.children:
        print("  -> ", c.name)


#
# Print all Nodes
#
def printAllNodes():
    global nodes

    for node in nodes.keys():
        print()
        printNode(nodes[node])


#
# Load the file into a data array
#
def loadData(filename):
    global nodes

    nodes = {}
    lines = 0

    f = open(filename)
    for line in f:
        line = line.strip()
        toNodeName, fromNodeName = line.split("-")
        toNode = findNode(toNodeName)
        fromNode = findNode(fromNodeName)
        toNode.addChild(fromNode)
        fromNode.addChild(toNode)
        #print(inputData[lines])
        lines += 1

    f.close()

    return lines


#
# Walk a nodes children
#
def walkNode(node, path):
    global paths

    path.append(node.name)
    if node.name == "end":
        # reached the end
        paths.append(path)
    else:
        for child in node.children:
            if child.multiVisit or child.name not in path:
                childPath = path.copy()
                walkNode(child, childPath)


#
# find all possble paths
#
def findPaths():
    global paths

    paths = []

    startNode = findNode("start")
    path = []
    walkNode(startNode, path)


#
#
# Walk a nodes children
#
def walkNode2(node, path, didSmallTwice):
    global paths

    path.append(node.name)
    if node.name == "end":
        # reached the end
        paths.append(path)
    else:
        for child in node.children:
            countLimit = 2
            if child.name == "start" or didSmallTwice: countLimit = 1
            childCount = path.count(child.name)
            if child.multiVisit or childCount < countLimit:
                thisSmallTwice = (didSmallTwice or (childCount == 1 and not child.multiVisit))
                childPath = path.copy()
                walkNode2(child, childPath, thisSmallTwice)


#
# find all possble paths
#
def findPaths2():
    global paths

    paths = []

    startNode = findNode("start")
    path = []
    walkNode2(startNode, path, False)

#
# Convert list of paths to list of strings
#
def path2Strings():
    global paths

    pathStrings = []

    for path in paths:
        pathStrings.append(",".join(path))

    return list(set(pathStrings))


#
# print the found paths
#
def printPaths():

    pathStrings = path2Strings()
    pathStrings.sort()
    for path in pathStrings:
        print(path)


#
# Main
#
def main():
    global nodes

    args = sys.argv[1:]
    if len(args) != 1:
        print("Usage: " + sys.argv[0] + " inputfile");
        return
    filename = args[0]
    print("Input File:", filename)

    # Load data
    lines = loadData(filename)
    print("  Lines Read: ", lines)
    print("Nodes Loaded: ", len(nodes))
    print()

    # Do Part 1 work
    #printAllNodes()
    findPaths()
    #printPaths()
    pathCount = len(paths)
    print()
    print("{}Path Count: {}{}{}".format(color.CYAN, color.YELLOW, pathCount, color.END))

    # Do Part 2 work
    print()
    findPaths2()
    #printPaths()
    pathCount = len(paths)
    print()
    print("{}Path Count 2: {}{}{}".format(color.CYAN, color.YELLOW, pathCount, color.END))


if __name__ == "__main__":
    main()
