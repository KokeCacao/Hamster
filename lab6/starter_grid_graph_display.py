# Robot Programming
# breadth first search
# by Dr. Qin Chen
# May, 2016

import sys
import Tkinter as tk

##############
# This class supports display of a grid graph. The node location on canvas
# is included as a data field of the graph, graph.node_display_locations.
##############

class GridGraphDisplay(object):
    def __init__(self, frame, graph):
        self.node_dist = 60
        self.node_size = 20
        self.gui_root = frame
        self.canvas = None
        self.graph = graph
        self.nodes_location = graph.node_display_locations
        self.start_node = graph.startNode
        self.goal_node = graph.goalNode
        return

    # draws nodes and edges in a graph
    def display_graph(self):        
        pass

    # path is a list of nodes ordered from start to goal node
    def highlight_path(self, path):
        pass
  
    # draws a node in given color. The node location info is in passed-in node object
    def draw_node(self, node, n_color):
        pass

    # draws an line segment, between two given nodes, in given color
    def draw_edge(self, node1, node2, e_color):
        pass
