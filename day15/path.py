#
# Adavent of Code Template
#
import sys
import numpy as np
from scipy.sparse import dok_array
from scipy.sparse.csgraph import shortest_path

# Global Variables
inputGrid = []
maxY = 0
maxX = 0

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
# Class to hold the Graph and provide utilities
#
class Graph(object):
    def __init__(self, nodes, init_graph):
        self.nodes = nodes
        self.graph = self.construct_graph(nodes, init_graph)

    def construct_graph(self, nodes, init_graph):
        '''
        This method makes sure that the graph is symmetrical. In other words, if there's a path from node A to B with a value V, there needs to be a path from node B to node A with a value V.
        '''
        graph = {}
        for node in nodes:
            graph[node] = {}

        graph.update(init_graph)

        for node, edges in graph.items():
            for adjacent_node, value in edges.items():
                if graph[adjacent_node].get(node, False) == False:
                    graph[adjacent_node][node] = value

        return graph

    def get_nodes(self):
        "Returns the nodes of the graph."
        return self.nodes

    def get_outgoing_edges(self, node):
        "Returns the neighbors of a node."
        connections = []
        for out_node in self.nodes:
            if self.graph[node].get(out_node, False) != False:
                connections.append(out_node)
        return connections

    def value(self, node1, node2):
        "Returns the value of an edge between two nodes."
        return self.graph[node1][node2]


#
# Dijkstra shortest path algorithm
#
def dijkstra_algorithm(graph, start_node):
    unvisited_nodes = list(graph.get_nodes())
 
    # We'll use this dict to save the cost of visiting each node and update it as we move along the graph   
    shortest_path = {}
 
    # We'll use this dict to save the shortest known path to a node found so far
    previous_nodes = {}
 
    # We'll use max_value to initialize the "infinity" value of the unvisited nodes   
    max_value = sys.maxsize
    for node in unvisited_nodes:
        shortest_path[node] = max_value
    # However, we initialize the starting node's value with 0   
    shortest_path[start_node] = 0
    
    # The algorithm executes until we visit all nodes
    while unvisited_nodes:
        print("Unvisited Node Count:", len(unvisited_nodes))
        # The code block below finds the node with the lowest score
        current_min_node = None
        for node in unvisited_nodes: # Iterate over the nodes
            if current_min_node == None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node

        print("  Current Min Node:", current_min_node, "with path", shortest_path[current_min_node])
                
        # The code block below retrieves the current node's neighbors and updates their distances
        neighbors = graph.get_outgoing_edges(current_min_node)
        print("    Neighbor Count:", len(neighbors))
        for neighbor in neighbors:
            print("    Neighbor:", neighbor, "with path:", shortest_path[neighbor], "and value", graph.value(current_min_node, neighbor))

            tentative_value = shortest_path[current_min_node] + graph.value(current_min_node, neighbor)
            if tentative_value < shortest_path[neighbor]:
                print("              updating path:", tentative_value)
                shortest_path[neighbor] = tentative_value
                # We also update the best path to the current node
                previous_nodes[neighbor] = current_min_node
 
        # After visiting its neighbors, we mark the node as "visited"
        unvisited_nodes.remove(current_min_node)
    
    return previous_nodes, shortest_path


#
# Create a string representing the node name
#
def getNodeName(y,x):
    return "{},{}".format(y,x)


#
# Add Graph Edge
#
def addEdge(node,y,x):
    global inputGrid

    nextNodeName = getNodeName(y,x)
    nextNodeWeight = inputGrid[y][x]
    node[nextNodeName] = nextNodeWeight


#
# Build the Graph
#
def buildNodeList(grid):

    maxy = len(grid)
    maxx = len(grid[0])

    nodes = []

    for y in range(maxy):
        for x in range(maxx):
            nodeName = getNodeName(y,x)
            nodes.append(nodeName)
    return nodes


#
# Build the Graph
#
def buildGraph():

    nodes = []
    init_graph = {}

    for y in range(maxY):
        for x in range(maxX):
            nodeName = getNodeName(y,x)
            nodes.append(nodeName)
            init_graph[nodeName] = {}
            if y > 0:
                addEdge(init_graph[nodeName],y-1,x)
            if y < maxY-1:
                addEdge(init_graph[nodeName],y+1,x)
            if x > 0:
                addEdge(init_graph[nodeName],y,x-1)
            if x < maxX-1:
                addEdge(init_graph[nodeName],y,x+1)

    return nodes, init_graph


#
# compute the linear position of a coordinates
#
def getPos(y,x,maxx):
    return y*maxx + x


#
# compute the cordinates from a linear position
#
def getCoord(p,maxx):
    y = int(p/maxx)
    x = p%maxx
    return y,x


#
# Build a dictionary of keys array
#
def buildDokArray(sourceGrid):

    maxy = len(sourceGrid)
    maxx = len(sourceGrid[0])
    dimensions = maxy*maxx
    sparse_array = dok_array((dimensions, dimensions), dtype=np.int32)

    for y in range(maxy):
        for x in range(maxx):
            fromPos = getPos(y,x,maxx)
            if y > 0:
                toPos = getPos(y-1,x,maxx)
                sparse_array[fromPos,toPos] = sourceGrid[y-1][x]
            if y < maxy-1:
                toPos = getPos(y+1,x,maxx)
                sparse_array[fromPos,toPos] = sourceGrid[y+1][x]
            if x > 0:
                toPos = getPos(y,x-1,maxx)
                sparse_array[fromPos,toPos] = sourceGrid[y][x-1]
            if x < maxx-1:
                toPos = getPos(y,x+1,maxx)
                sparse_array[fromPos,toPos] = sourceGrid[y][x+1]

    return sparse_array


#
# Load the file into a data array
#
def loadData(filename):
    global inputGrid, maxY, maxX

    inputGrid = []
    lines = 0

    f = open(filename)
    for line in f:
        line = line.strip()

        row = []
        for c in line:
            row.append(int(c))

        inputGrid.append(row)
        #print(inputData[lines])
        lines += 1

    f.close()

    maxY = len(inputGrid)
    maxX = len(inputGrid[0])

    return lines


#
# Print the result path
#
def print_result(previous_nodes, shortest_path, start_node, target_node):
    path = []
    node = target_node
    
    while node != start_node:
        path.append(node)
        node = previous_nodes[node]
 
    # Add the start node manually
    path.append(start_node)
    
    print("We found the following best path with a value of {}.".format(shortest_path[target_node]))
    print(" -> ".join(reversed(path)))

    return path


#
# Print Grid
#
def printGrid(grid, path = []):

    maxy = len(grid)
    maxx = len(grid[0])

    for y in range(maxy):
        rowStr = ""
        for x in range(maxx):
            c = grid[y][x]
            nodeName = getNodeName(y,x)
            if nodeName in path:
                rowStr += color.YELLOW + str(c) + color.END
            else:
                if c == None or c == 0:
                    rowStr += color.RED + "X" + color.RED
                else:
                    rowStr += str(c)

        print(rowStr)


#
# Sum up the risk score
#
def sumRisk(path, shortest_path):
    global inputGrid

    riskScore = 0

    print("{:>4} {:>4} {:>4} {:>4}".format("node","val","risk","path"))
    path.reverse()
    for p in path:
        y,x = p.split(",")
        y = int(y)
        x = int(x)
        if p != "0,0":
            riskScore += inputGrid[y][x]
        print("{:>4} {:>4} {:>4} {:>4}".format(p,inputGrid[y][x],riskScore,shortest_path[p]))

    return riskScore


#
# Expand the grid
#
def expandGrid(sourceGrid, dim):

    sourceY = len(sourceGrid)
    sourceX = len(sourceGrid[0])
    newY = sourceY * dim
    newX = sourceX * dim

    newGrid = [[0 for x in range(newX)] for y in range(newY)]
        
    # prime new grid with source
    for y in range(sourceY):
        for x in range(sourceX):
            newGrid[y][x] = sourceGrid[y][x]

    # replicate across
    for bigX in range(1,dim):
        for y in range(sourceY):
            for x in range(sourceX):
                newVal = newGrid[y][x+((bigX-1)*sourceX)] + 1
                if newVal > 9: newVal = 1
                newGrid[y][x+bigX*sourceX] = newVal

    # replicate down
    for bigY in range(1,dim):
        for bigX in range(dim):
            for y in range(sourceY):
                for x in range(sourceX):
                    newVal = newGrid[y+((bigY-1)*sourceY)][x+(bigX*sourceX)] + 1
                    if newVal > 9: newVal = 1
                    newGrid[y+bigY*sourceY][x+bigX*sourceX] = newVal

    return newGrid


#
# Build the path based on predecessors
#
def buildPath(predecessors, maxx):

    path = []

    y = maxx-1    # safe because square
    x = maxx-1

    pos = getPos(y,x,maxx)
    path.append(getNodeName(y,x))

    while pos != 0:
        pos = predecessors[pos]
        y,x = getCoord(pos,maxx)
        path.append(getNodeName(y,x))

    return path


#
# Main
#
def main():
    global inputGrid, maxY, maxX

    args = sys.argv[1:]
    if len(args) != 1:
        print("Usage: " + sys.argv[0] + " inputfile");
        return
    filename = args[0]
    print("Input File:", filename)

    # Load data
    lines = loadData(filename)
    print(" Lines Read: ", lines)
    print("      Max Y: ", maxY)
    print("      Max X: ", maxX)
    print()

    # Do Part 1 work
    printGrid(inputGrid)

    #
    # Dijkstra algorithm with arrays
    #
    # slow
    #
    #nodes, init_graph = buildGraph()
    #graph = Graph(nodes, init_graph)
    #previous_nodes, shortest_path = dijkstra_algorithm(graph=graph, start_node=getNodeName(0,0))
    #path = print_result(previous_nodes, shortest_path, start_node=getNodeName(0,0), target_node=getNodeName(maxY-1, maxX-1))
    #printGrid(path)
    #riskScore = sumRisk(path, shortest_path)

    part1 = False
    part2 = True
    #
    # Use Sci Py and matrix processing
    #
    # fast
    #
    if part1:
        maxy = len(inputGrid)
        maxx = len(inputGrid[0])
        array = buildDokArray(inputGrid)
        print()
        print("array")
        print(array)
        graph = array.tocsr()
        print()
        print("graph")
        print(graph)
        dist_matrix, predecessors = shortest_path(csgraph=array, directed=True, indices=0, return_predecessors=True)
        print()
        print("dist_matrix")
        print(dist_matrix)
        print()
        print("predecessors")
        print(predecessors)
        path = buildPath(predecessors,maxx)
        printGrid(inputGrid, path)
        fromPos = getPos(0,0,maxx)
        toPos = getPos(maxy-1, maxx-1, maxx)
        riskScore = dist_matrix[toPos]
        print()
        print("{}Part 1 Risk Score: {}{}{}".format(color.CYAN, color.YELLOW, riskScore, color.END))

    # Do Part 2 work
    if part2:
        print()
        origNodes = buildNodeList(inputGrid)
        grid = expandGrid(inputGrid,5)
        #printGrid(grid, origNodes)
        maxy = len(grid)
        maxx = len(grid[0])
        array = buildDokArray(grid)
        print()
        print("array")
        print(array)
        dist_matrix, predecessors = shortest_path(csgraph=array, directed=True, indices=0, return_predecessors=True)
        print()
        print("dist_matrix")
        print(dist_matrix)
        print()
        print("predecessors")
        print(predecessors)
        toPos = getPos(maxy-1, maxx-1, maxx)
        riskScore = dist_matrix[toPos]
        print()
        print("{}Part 2 Risk Score: {}{}{}".format(color.CYAN, color.YELLOW, riskScore, color.END))


if __name__ == "__main__":
    main()
