'''
/* =======================================================================
   (c) 2015, Kre8 Technology, Inc.

   Name:          bfs_engine.py
   By:            Qin Chen
   Last Updated:  6/10/18

   PROPRIETARY and CONFIDENTIAL
   ========================================================================*/
'''
import sys


class BFS(object):
    def __init__(self, graph):
        self.graph = graph
        return

    ######################################################
    # this function returns the shortest path for given start and goal nodes
    ######################################################
    def bfs_shortest_path(self, start, goal):
        pass

    ######################################################
    # this function returns all paths for given start and goal nodes
    ######################################################
    def bfs_paths(self, start, goal):
        pass

    #########################################################
    # This function returns the shortest paths for given list of paths
    #########################################################
    def shortest(self, paths):
        pass

    #########################################################
    # THis function traverses the graph from given start node
    # return order of nodes visited
    #########################################################
    def bfs(self, start):
        pass


def main():
    graph = {'A': {'B', 'C'},
             'B': {'A', 'E', 'D'},
             'C': {'A', 'F', 'G'},
             'D': {'B', 'H'},
             'E': {'B', 'I', 'J'},
             'F': {'C', 'K'},
             'G': {'C'},
             'H': {'D'},
             'I': {'E'},
             'J': {'E'},
             'K': {'F'}}

    bfs = BFS(graph)

    start_node = 'A'
    end_node = 'E'

    order = bfs.bfs(start_node)
    print "\n##########traverse order:", order

    return


if __name__ == "__main__":
    sys.exit(main())
