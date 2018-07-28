import Tkinter as tk
import time
import math
import uuid

class TempNode(object):
    def __init__(self, cell_id, orientation, x, y):
        self.cell_id = cell_id
        self.orientation = orientation
        self.x = x
        self.y = y

        # note that the index of node and distance should pair up
        self.to_node = []
        self.to_distance = []
        self.dictionary = dict()

        # running variables
        '''
        Warning! You need to update current_loss
       '''
        self.best_loss = -1
        self.best_distance_walked = -1
        self.predicted_distance_to_end = -1
    def get_next_nodes(self, path, distance_walked, end_point):
        # Loss Function: update node's memory
        new_distance_walked = distance_walked
        if new_distance_walked < self.best_distance_walked:
            self.best_distance_walked = new_distance_walked
        self.predicted_distance_to_end = get_distance(self.get_coordinate(), end_point)
        self.best_loss = self.best_distance_walked + self.predicted_distance_to_end

        # update dictionary


        x = self.dictionary
        import operator
        list_of_tuples_such_that_first_element_is_sorted_by_the_second_element = sorted(x.items(), key=operator.itemgetter(1))
        next_nodes = []
        for node_distance_tuples in list_of_tuples_such_that_first_element_is_sorted_by_the_second_element:
            node = node_distance_tuples[0]
            distance = node_distance_tuples[1]
            next_nodes.append(node)
        return next_nodes
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def get_coordinate(self):
        return self.x, self.y
    def get_dictionary(self):
        return self.dictionary
    def add_dictionary(self, dictionary):
        self.dictionary = merge_two_dicts(self.dictionary, dictionary)
    def add_connection(self, to_node, distance):
        self.to_node.append(to_node)
        self.to_distance.append(distance)
        self.refresh_dictionary()
    def refresh_dictionary(self):
        self.dictionary[self.to_node] = self.to_distance

class CellBox(object):
    def __init__(self, cell_id, x1, y1, x2, y2, start_point, end_point):
        self.cell_id = cell_id
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.start_point = None
        self.start_node = None
        self.end_point = None
        self.end_node = None
        if self.has_cover_point(start_point[0], start_point[1]):
            self.start_point = start_point
        if self.has_cover_point(end_point[0], end_point[1]):
            self.end_point = end_point

        # create temp nodes
        self.right_node = TempNode(self.cell_id, 0, x2, y2/2)
        self.up_node = TempNode(self.cell_id, 1, x2/2, y1)
        self.left_node = TempNode(self.cell_id, 2, x1, y2/2)
        self.down_node = TempNode(self.cell_id, 3, x2/2, y2)
        self.nodes = [self.right_node, self.up_node, self.left_node, self.down_node]

        if self.start_point is not None:
            self.start_node = TempNode(self.cell_id, 4, self.start_point[0], self.start_point[1])
            self.nodes.append(self.start_node)
        if self.end_point is not None:
            self.end_node = TempNode(self.cell_id, 5, self.end_point[0], self.end_point[1])
            self.nodes.append(self.end_node)

        # create temp connections
        for from_node in self.nodes:
            for to_node in self.nodes:
                if from_node != to_node:
                    to_distance = self.get_distance(from_node.get_coordinate(), to_node.get_coordinate())
                    from_node.add_connection(to_node, to_distance)

    def has_cover_point(self, x, y):
        return self.x2>x>self.x1 and self.y2>y>self.y1
    def get_cell_id(self):
        return self.cell_id
    def get_x1(self):
        return self.x1
    def get_y1(self):
        return self.y1
    def get_x2(self):
        return self.x2
    def get_y2(self):
        return self.y2
    def get_up_node(self):
        return self.up_node
    def get_down_node(self):
        return self.down_node
    def get_left_node(self):
        return self.left_node
    def get_right_node(self):
        return self.right_node
    def get_start_node(self):
        return self.start_node
    def get_end_node(self):
        return self.end_node
    def get_all_nodes(self):
        return self.nodes


class Map(object):
    def __init__(self, blocks, start_point, end_point):
        # ATTENTION: Blocks should be in my coordinate system
        self.blocks = blocks  # a list of blocks [x1, y1, x2, y2]
        self.start_point = start_point[0], start_point[1]
        self.start_node = None
        self.end_point = end_point[0], end_point[1]
        self.end_node = None

        # [find all x and y of all blocks and create points]
        # It has to be set() because there are multiple values
        self.all_x = set()
        self.all_y = set()
        for block in self.blocks:
            self.all_x.add(block[0])
            self.all_x.add(block[2])
            self.all_y.add(block[1])
            self.all_y.add(block[3])
        self.all_points = set()
        for x in self.all_x:
            for y in self.all_y:
                self.all_points.add((x, y))

        # create boxes
        boxes = []
        all_temp_nodes = []
        for i, point in enumerate(self.all_points):
            x = point[0]
            y = point[1]
            # if it is not the last point that I cannot connect to
            if i+1 < len(self.all_points):
                cell_id = uuid.uuid4()
                box = CellBox(cell_id, x, y, x+1, y+1)
                boxes.append(box)
                all_temp_nodes = all_temp_nodes + box.get_all_nodes()

        # create physical nodes
        filtered_temp_node = []
        for temp_node in all_temp_nodes:
            old_coord = []
            old_nodes = []
            new_coord = []
            new_nodes = []
            if temp_node.get_coordinate() not in old_coord:
                old_coord.append(temp_node.get_coordinate())
                old_nodes.append(temp_node)
            else:
                new_coord.append(temp_node.get_coordinate())
                new_nodes.append(temp_node)
            for i, old_node in enumerate(old_nodes):
                new_node = new_nodes[i]
                old_node.add_dictionary(new_node.get_dictionary())
            filtered_temp_node = filtered_temp_node + old_nodes
        '''
        Now we have `filtered_temp_node = []`
        Inside, we have connection to each node and distance
        It also contains the start node and end node
        Now, you need to run the map!
       '''

        # remember that start node cannot be the end node
        for node in filtered_temp_node:
            if node.get_coordinate() == self.start_point:
                self.start_node == node
                break
            elif node.get_coordinate() == self.end_point:
                self.end_node == node
                break

        # start the thing!
        path = []
        distance = 0
        nodes_unexplored = [self.start_node]
        while nodes_unexplored:
            '''
            Definition:
                + Explore: looked around for other nodes and get the cost of those nodes, and update itself in terms of path
            Process:
            1. Sort the nodes_unexplored list by cost
            2. Take out the node with smallest cost
            3. Explore the node
                - Calculate the next_nodes' cost using next_node's coordinate and lowest_distance
                - Tell the node path and store inside as a list: it may not be the lowest_distance_path, but it should be the lowest_cost_path
                - Update the lowest_cost, lowest_cost_path, lowest_distance, lowest_distance_path (other paths are not worth to be stored)
                - Node should return a list unexplored nodes for adding to nodes_unexplored list
            4. If the node successfully connect to the end_node, print out the lowest_cost_path
            5. If the nodes_unexplored is empty, terminate search
            6. Otherwise, go to #1 again
           '''
            pass
        for next_node in self.start_node.node.get_next_nodes(path, distance, self.end_point):
            # search next_node (without going to the explored node), tell the node the path, tell the node distance, get next_node
            # the node should update [best path && best distance && fake_distance to get to end note]
            # search next_node (without going to the explored node), get next_node
            # search next_node (without going to the explored node), get next_node
            # search next_node (without going to the explored node), get next_node
            # search next_node (without going to the explored node), get next_node
            # search next_node (without going to the explored node), get next_node
            # until there is no node -> no path
            # or to the end_point -> a path

            pass
# class PhysicalNode(object):
#     def __init__(self, x, y, to_nodes, to_distances, started=False):
#         # the actual coordinate on the map
#         self.x = x
#         self.y = y
#         self.coordinate = (self.x, self.y)
#         # if the node was visited
#         self.to_nodes = to_nodes  # a list of
#         self.to_distances = to_distances  # distance should match to_node
#
#         # internal memory
#         self.started = started
#         self.best_way_to_get_to_me = None  # TODO: make a calculation for best_memories
#         self.best_cost = 999999999
#         self.from_node = None
#
#     def get_visited(self):
#         return self.visited
#     def get_best_path(self):
#         return self.best_path
#     def get_x(self):
#         return self.x
#     def get_y(self):
#         return self.y
#     def get_coordinate(self):
#         return self.coordinate


def translate_teacher_strange_coordinate_system_to_my_clean_coordinate_system(self, teacher_strange_coordinate_x, teacher_strange_coordinate_y):
    # 600 * 400
    return teacher_strange_coordinate_x + 300, -teacher_strange_coordinate_y + 200


def merge_two_dicts(x, y):
    z = x.copy()  # start with x's keys and values
    z.update(y)  # modifies z with y's keys and values & returns None
    return z

def get_distance(from_point, to_point):
    x1 = from_point[0]
    y1 = from_point[1]
    x2 = to_point[0]
    y2 = to_point[1]
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
