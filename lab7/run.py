import Tkinter as tk
import time
import math
import uuid

class CellBox:
    def __init__(self, cell_id, x1, y1, x2, y2):
        self.cell_id = cell_id
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        # node_id = (cell_id, node_orientation}
        # node_orientation: right = 0, up = 1, left = 2, down = 3
        self.connection_map = dict()  # {cell-id-}
        temp_node_orientations = {0, 1, 2, 3}

        # create nodes
        self.right_node = (self.cell_id, 0, x2, y2/2)
        self.up_node = (self.cell_id, 1, x2/2, y1)
        self.left_node = (self.cell_id, 2, x1, y2/2)
        self.down_node = (self.cell_id, 3, x2/2, y2)
        self.nodes = [self.right_node, self.up_node, self.left_node, self.down_node]

        '''
            dict = {
            "from": [((cell_id, orientation, x, y), distance), ((cell_id, orientation, x, y), distance), ((cell_id, orientation, x, y), distance)],
            "from": [((cell_id, orientation, x, y), distance), ((cell_id, orientation, x, y), distance), ((cell_id, orientation, x, y), distance)],
            "from": [((cell_id, orientation, x, y), distance), ((cell_id, orientation, x, y), distance), ((cell_id, orientation, x, y), distance)],
            "from": [((cell_id, orientation, x, y), distance), ((cell_id, orientation, x, y), distance), ((cell_id, orientation, x, y), distance)]
            }
       '''
        for from_node in self.nodes:
            for to_node in self.nodes:
                if from_node != to_node:
                    distance = self.get_distance(from_node, to_node)
                    node_with_distance = (to_node, distance)
                    self.connection_map[from_node] = list(self.connection_map[from_node]) + [node_with_distance]
        print str(self.connection_map)

    def get_distance(self, from_node, to_node):
        x1 = from_node[0]
        y1 = from_node[1]
        x2 = to_node[0]
        y2 = to_node[1]
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    def get_cell_id(self):
        return self.cell_id
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def get_up_node(self):
        return self.up_node
    def get_down_node(self):
        return self.down_node
    def get_left_node(self):
        return self.left_node
    def get_right_node(self):
        return self.right_node
    def get_all_nodes(self):
        return self.nodes
    def get_connection_map(self):
        return self.connection_map


class Map(object):
    def __init__(self, blocks):
        # ATTENTION: Blocks should be in my coordinate system
        self.blocks = blocks  # a list of blocks [x1, y1, x2, y2]

        # transform block to one dimension
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

        boxes = []
        connection_map = dict()
        for i, point in enumerate(self.all_points):
            x = point[0]
            y = point[1]
            # if it is not the last point that I cannot connect to
            if i+1 < len(self.all_points):
                cell_id = uuid.uuid4()
                box = CellBox(cell_id, x, y, x+1, y+1)
                boxes.append(box)
                connection_map = merge_two_dicts(connection_map, box.get_connection_map())

def merge_two_dicts(x, y):
    z = x.copy()  # start with x's keys and values
    z.update(y)  # modifies z with y's keys and values & returns None
    return z


