import networkx as nx
import matplotlib.pyplot as plt
import random

class networkVisualization:
    def __init__(self):
        self.edges = []
        self.nodes = []
        self.edge_labels = []

    def Clear(self):
        self.edges = []
        self.nodes = []
        self.edge_labels = []

    def GetUnusedLetter(self):
        from string import ascii_uppercase as alphabet
        for letter in alphabet:
            if not self.nodes.__contains__(letter):
                return letter

        # all letters taken up, add new letters to end (i.e. AA, BB, etc)
        for letterA in alphabet:
            for letterB in alphabet:
                combination = letterA + letterB
                if not self.nodes.__contains__(combination):
                    return combination

    def AddEdge(self, a, b, distance=None):
        # set a random distance if none is provided
        if distance == None:
            distance = random.randint(1, 10)
        if not self.EdgeExists(a, b):
            # add node a if it doesnt exist
            if not self.nodes.__contains__(a):
                self.nodes.append(a)

            # add node b if it doesnt exist
            if not self.nodes.__contains__(b):
                self.nodes.append(b)

            # add edge a, b and give it a distance
            self.edges.append([a, b])
            self.edge_labels.append(distance)

    def EdgeExists(self, a, b):
        if self.edges.__contains__([a, b]):
            return True
        if self.edges.__contains__([b, a]):
            return True
        return False

    def AddNode(self, a=None):
        if a == None:
            a = self.GetUnusedLetter()
            self.nodes.append(a)
            return a
        if not self.nodes.__contains__(a):
            self.nodes.append(a)
            return a
        return None

    def PrintAll(self):
        print("Nodes: ", self.nodes)
        print("Edges: ")
        for i in range(0, len(self.edges)):
            print(self.edges[i][0], "-", self.edge_labels[i], "-> ", self.edges[i][1])

    def GetEdgeDistance(self, a, b):
        if self.edges.__contains__([a, b]):
            index = self.edges.index([a, b])
            return self.edge_labels[index]
        elif self.edges.__contains__([b, a]):
            index = self.edges.index([b, a])
            return self.edge_labels[index]
        return None

    def GetConnectedNodes(self, a):
        # return none if node doesnt exist
        if not self.nodes.__contains__(a):
            return None

        listOfNodes = []
        listOfNodeDistances = []
        for edge in self.edges:
            if edge.__contains__(a):
                for node in edge:
                    if node != a:
                        # append the nodes from the edge not equal to a
                        listOfNodes.append(node)

                        # append the distance from a to the other nodes
                        dist = self.GetEdgeDistance(a, node)
                        listOfNodeDistances.append(dist)

                        # Debug print
                        #print("Node ", node, " is connected to node ", a, ". Distance = ", dist)
        return listOfNodes, listOfNodeDistances

    def GenerateRandomGraph(self, numberOfNodes, numberOfEdges):
        # check for impossible node/edge config
        if numberOfEdges > (numberOfNodes * (numberOfNodes - 1)):
            print("Error: Impossible number of edges was given!")
            return None

        # check if only one node
        if numberOfNodes == 1:
            self.AddNode()
            return self.nodes

        # add nodes equal to number of nodes
        for i in range(0, numberOfNodes):
            self.AddNode()

        # add random edges equal to number of edges
        if numberOfEdges == 0:
            return None

        for i in range(0, numberOfEdges):
            self.GenerateUniqueEdge()

        # ensure that each node has at least one connection
        for node in self.nodes:
            for edge in self.edges:
                if edge.__contains__(node):
                    break
            # no edges with this node
            listOfOtherNodes = self.nodes.copy()
            listOfOtherNodes.remove(node)
            self.AddEdge(node, random.choice(listOfOtherNodes))

    def GenerateUniqueEdge(self):
        validNodeList = self.nodes.copy()

        # for each node, if it is connected to all other nodes already, remove it from possible options
        nodesToRemove = []
        for node in validNodeList:
            allOtherNodes = validNodeList.copy()
            allOtherNodes.remove(node)
            if self.GetConnectedNodes(node)[0] == allOtherNodes:
                nodesToRemove.append(node)
        for node in nodesToRemove:
            validNodeList.remove(node)

        # choose a random node from the list
        node1 = random.choice(validNodeList)
        validNodeList.remove(node1)

        # remove each node from the valid node list that already has an edge with the selected node
        nodesToRemove.clear()
        for node in validNodeList:
            if self.EdgeExists(node1, node):
                nodesToRemove.append(node)
        for node in nodesToRemove:
            validNodeList.remove(node)

        # choose a random node from whats left
        node2 = random.choice(validNodeList)

        # create an edge
        self.AddEdge(node1, node2)
        return [node1, node2]

    def RemoveNode(self, a):
        if not self.nodes.__contains__(a):
            return None

        # remove all edges that contain the node
        edgesToRemove = []
        for edge in self.edges:
            if edge.__contains__(a):
                edgesToRemove.append(edge)
        for edge in edgesToRemove:
            self.RemoveEdge(edge[0], edge[1])

        # remove the node itself
        self.nodes.remove(a)

    def RemoveEdge(self, a, b):
        if not self.EdgeExists(a, b):
            return None
        edge_index = self.edges.index([a, b])
        self.edges.pop(edge_index)
        self.edge_labels.pop(edge_index)

    def RemoveRandomNode(self):
        nodeToRemove = random.choice(self.nodes)
        self.RemoveNode(nodeToRemove)

    def DrawGraph(self):
        G = nx.Graph()
        G.add_edges_from(self.edges)
        G.add_nodes_from(self.nodes)
        nx.draw_circular(G, with_labels=True, edge_color='black', width=1, linewidths=1,
                         node_size=500, node_color='cyan')

        edges_copy = self.edges.copy()
        labels_copy = self.edge_labels.copy()

        edge_dict = {}
        for key in edges_copy:
            for value in labels_copy:
                edge_dict[tuple(key)] = value
                labels_copy.remove(value)
                break

        print(edge_dict)

        nx.draw_networkx_edge_labels(
            G, nx.circular_layout(G),
            edge_labels=edge_dict
        )
        plt.show()