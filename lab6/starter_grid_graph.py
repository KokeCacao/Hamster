'''
/* =======================================================================
   (c) 2015, Kre8 Technology, Inc.

   Name:          grid_graph_starter.py
   By:            Qin Chen
   Last Updated:  6/10/18
    
   Definition of class GridGraph. Description of all the methods is
   provided. Students are expected to implement the methods for Lab#6.
   ========================================================================*/
'''
import Tkinter as tk


class Node(object):
    def __init__(self, x, y, blocks, grid_map, path=None):
        if path is None:
            path = []
        self.x = x
        self.y = y
        self.node = (self.x, self.y)
        self.blocks = blocks  # set of all the blocks in the map (black list)
        self.grid_map = grid_map  # set of all possible nodes you can get to, including blocks (white list)

        self.path = path  # a list of nodes path it come from (without this node)
        self.next_nodes = set()  # a set of connected nodes from this node

        # removing black list
        temp_next_nodes = {(self.x + 1, self.y + 0), (self.x - 1, self.y + 0), (self.x + 0, self.y + 1),
                           (self.x + 0, self.y - 1)}
        self.next_nodes = temp_next_nodes - self.blocks

        # removing white list
        temp_nodes_out_of_map = set()
        for next_node in self.next_nodes:
            if next_node not in self.grid_map:
                temp_nodes_out_of_map.add(next_node)
        self.next_nodes = self.next_nodes - temp_nodes_out_of_map

    def get_node(self):
        return self.node

    def get_next_nodes(self):
        return self.next_nodes

    def get_next_explore(self):
        return self.get_next_nodes() - set(self.get_path()) - set(self.get_node())

    def get_map(self):
        return self.grid_map

    def get_blocks(self):
        return self.blocks

    def get_path(self):
        return self.path

    def run(self):
        print str(self.get_node()) + " -> " + str(self.get_next_explore()) + " path = " + str(self.get_path())
        if len(self.get_next_explore()) is not 0:
            for next_node in self.get_next_explore():
                # print "trying to append", str(self.get_path()), "with", str(self.get_node())
                next_path = self.get_path() + [self.get_node()]  # BUG: inplace bug, be careful because .append() does not create a new list
                node = Node(x=next_node[0], y=next_node[1], blocks=self.get_blocks(), grid_map=self.get_map(), path=next_path)
                path = node.run()
                # return path  # catch local return
        else:
            path = self.path + [self.node]
            print "path finished with", str(path)
            # return path  # local return

class Path(object):
    def __init__(self, path):
        self.path = path
    def get_path(self):
        return self.path
    def get_length(self):
        return len(self.path)

class GridGraph(object):
    def __init__(self):
        self.nodes = set()  # {node_name: set(neighboring nodes), ...}
        self.startNode = None  # string
        self.goalNode = None  # string
        self.grid_rows = None
        self.grid_columns = None
        self.obs_list = []
        self.node_display_locations = []
        return

    # set number of rows in the grid
    def set_grid_rows(self, rows):
        pass

    # set number of columns in the grid
    def set_grid_cols(self, cols):
        pass

    # this method is used by make_grid() to create a key-value pair in self.nodes{},
    # where value is created as an empty set which is populated later while connecting
    # nodes.
    def add_node(self, name):
        pass

    # set start node name
    def set_start(self, name):
        pass

    # returns start node name
    def get_start_node(self):
        pass

    # set goal node name
    def set_goal(self, name):
        pass

    # return goal node name
    def get_goal_node(self):
        pass

    # Given two neighboring nodes. Put them to each other's neighbors-set. This
    # method is called by self.connect_nodes() 
    def add_neighbor(self, node1, node2):
        pass

    # populate graph with all the nodes in the graph, excluding obstacle nodes
    def make_grid(self):
        pass

    # Based on node's name, this method identifies its neighbors and fills the 
    # set holding neighbors for every node in the graph.
    def connect_nodes(self):
        pass

    # For display purpose, this function computes grid node location(i.e., offset from upper left corner where is (1,1)) 
    # of display area. based on node names.
    # Node '0-0' is displayed at bottom left corner 
    def compute_node_locations(self):
        pass

    def testing(self):
        # x=4, y=5 (rectangle grid) from left_down corner (0, 0) to right_up corner (4, 3)
        # block: (1, 1), (2, 3), (3, 2), (3. 0)
        # Your task is to generate a graph
        map_x = 4
        map_y = 5
        block = {(1, 1), (2, 3), (3, 2), (3, 0)}
        graph = dict()


###########################################################
#  A testing program of your implementaion of GridGraph class.
###########################################################
def main():
    # graph = GridGraph()
    # # grid dimension
    # graph.set_grid_rows(4)
    # graph.set_grid_cols(3)
    #
    # # origin of grid is (0, 0) lower left corner
    # # graph.obs_list = ([1,1],)    # in case of one obs. COMMA
    # graph.obs_list = ([1,1], [3,0], [2,2])
    #
    # graph.set_start('0-0')
    # graph.set_goal('2-1')
    #
    # graph.make_grid()
    # graph.connect_nodes()
    rows = 4
    cols = 3
    grid_map = set()
    for row in range(rows):
        for col in range(cols):
            grid_map.add((row, col))

    node = Node(x=0, y=0, blocks={(1, 1), (3, 0), (2, 2)}, grid_map=grid_map, path=[(-1, -1)])
    node.run()

    return


if __name__ == "__main__":
    main()
