'''
/* =======================================================================
   (c) 2015, Kre8 Technology, Inc.

   PROPRIETARY and CONFIDENTIAL

   This file contains source code that constitutes proprietary and
   confidential information created by David Zhu

   Kre8 Technology retains the title, ownership and intellectual property rights
   in and to the Software and all subsequent copies regardless of the
   form or media.  Copying or distributing any portion of this file
   without the written permission of Kre8 Technology is prohibited.

   Use of this code is governed by the license agreement,
   confidentiality agreement, and/or other agreement under which it
   was distributed. When conflicts or ambiguities exist between this
   header and the written agreement, the agreement supersedes this file.
   ========================================================================*/
'''

import Tkinter as tk
import time
import math
import pdb

# 40 by 40 (28 is the middle to vertex)
class virtual_robot:
    def __init__(self):
        # self.robot = None
        self.l = 20 * math.sqrt(2)  # half diagonal - robot is 40 mm square
        self.x = 0  # x coordinate
        self.y = 0  # y coordinate
        self.a = 0  # angle of the robot, 0 when aligned with verticle axis
        self.dist_l = False
        self.dist_r = False  # distance
        self.floor_l = False
        self.floor_r = False
        self.sl = 0  # speed of left wheel
        self.sr = 0  # speed of right wheel
        self.t = 0  # last update time
    def reset_robot(self):
        self.x = 0  # x coordinate
        self.y = 0  # y coordinate
        self.a = 0  # angle of the robot, 0 when aligned with verticle axis
        self.dist_l = False
        self.dist_r = False  #
        self.floor_l = False
        self.floor_r = False
        self.sl = 0  # speed of left wheel
        self.sr = 0  # speed of right wheel
        self.t = 0  # last update time
    def set_robot_speed(self, w_l, w_r):
        self.sl = w_l
        self.sr = w_r
    def set_robot_pose(self, a, x, y):
        self.a = a
        self.x = x
        self.y = y
    def set_robot_prox_dist(self, dist_l, dist_r):
        self.dist_l = dist_l
        self.dist_r = dist_r
    def set_robot_floor(self, floor_l, floor_r):
        self.floor_l = floor_l
        self.floor_r = floor_r
    def get_angle(self):
        return self.a
    def get_location(self):
        return self.x, self.y
    # add: get robot model
    # def get_robot_corner_upper_left:


class virtual_world:
    def __init__(self):

        # Test Code
        self.test_lines = []


        self.real_robot = False
        self.go = False  # activate robot behavior
        self.vrobot = virtual_robot()
        self.canvas = None
        self.canvas_width = 0
        self.canvas_height = 0
        self.area = []
        self.map = []
        # self.cobs = []
        self.f_cell_list = []
        self.goal_list = []
        self.goal_list_index = 0
        self.goal_t = "None"
        self.goal_x = 0
        self.goal_y = 0
        self.goal_a = 0
        self.goal_achieved = True
        self.trace = False  # leave trace of robot
        self.prox_dots = False  # draw obstacles detected as dots on map
        self.floor_dots = False
        self.localize = False
        self.glocalize = False
    def add_obstacle(self, rect):
        self.map.append(rect)
        return
    def draw_map(self):
        canvas_width = self.canvas_width
        canvas_height = self.canvas_height
        for rect in self.map:
            x1 = canvas_width + rect[0]
            y1 = canvas_height - rect[1]
            x2 = canvas_width + rect[2]
            y2 = canvas_height - rect[3]
            self.canvas.create_rectangle([x1, y1, x2, y2], outline="grey", fill="grey")

        # for cobs in self.cobs:
        #     x1 = canvas_width + cobs[0]
        #     y1= canvas_height - cobs[1]
        #     x2= canvas_width + cobs[2]
        #     y2 = canvas_height - cobs[3]
        # self.canvas.create_rectangle([x1,y1,x2,y2], fill=None)
    def draw_robot(self):
        canvas_width = self.canvas_width
        canvas_height = self.canvas_height
        pi4 = 3.1415 / 4  # quarter pi
        vrobot = self.vrobot
        a1 = vrobot.a + pi4
        a2 = vrobot.a + 3 * pi4
        a3 = vrobot.a + 5 * pi4
        a4 = vrobot.a + 7 * pi4

        x1 = canvas_width + vrobot.l * math.sin(a1) + vrobot.x
        x2 = canvas_width + vrobot.l * math.sin(a2) + vrobot.x
        x3 = canvas_width + vrobot.l * math.sin(a3) + vrobot.x
        x4 = canvas_width + vrobot.l * math.sin(a4) + vrobot.x

        y1 = canvas_height - vrobot.l * math.cos(a1) - vrobot.y
        y2 = canvas_height - vrobot.l * math.cos(a2) - vrobot.y
        y3 = canvas_height - vrobot.l * math.cos(a3) - vrobot.y
        y4 = canvas_height - vrobot.l * math.cos(a4) - vrobot.y

        points = (x1, y1, x2, y2, x3, y3, x4, y4)
        poly_id = vrobot.poly_id
        self.canvas.coords(poly_id, points)

        if (self.trace):
            pi3 = 3.1415 / 3
            a1 = vrobot.a
            a2 = a1 + 2 * pi3
            a3 = a1 + 4 * pi3
            x1 = canvas_width + 3 * math.sin(a1) + vrobot.x
            x2 = canvas_width + 3 * math.sin(a2) + vrobot.x
            x3 = canvas_width + 3 * math.sin(a3) + vrobot.x
            y1 = canvas_height - 3 * math.cos(a1) - vrobot.y
            y2 = canvas_height - 3 * math.cos(a2) - vrobot.y
            y3 = canvas_height - 3 * math.cos(a3) - vrobot.y
            self.canvas.create_polygon([x1, y1, x2, y2, x3, y3], outline="blue")
    def radial_intersect(self, a_r, x_e, y_e):
        shortest = False
        p_intersect = False
        p_new = False

        for obs in self.map:
            x1 = obs[0]
            y1 = obs[1]
            x2 = obs[2]
            y2 = obs[3]
            # first quadron
            if (a_r >= 0) and (a_r < 3.1415 / 2):
                # print "radial intersect: ", x_e, y_e
                if (y_e < y1):
                    x_i = x_e + math.tan(a_r) * (y1 - y_e)
                    y_i = y1
                    if (x_i > x1 and x_i < x2):
                        p_new = [x_i, y_i, 1]  # 1 indicating intersecting a bottom edge of obs
                if (x_e < x1):
                    x_i = x1
                    y_i = y_e + math.tan(3.1415 / 2 - a_r) * (x1 - x_e)
                    if (y_i > y1 and y_i < y2):
                        p_new = [x_i, y_i, 2]  # left edge of obs
            # second quadron
            if (a_r >= 3.1415 / 2) and (a_r < 3.1415):
                if (y_e > y2):
                    x_i = x_e + math.tan(a_r) * (y2 - y_e)
                    y_i = y2
                    if (x_i > x1 and x_i < x2):
                        p_new = [x_i, y_i, 3]  # top edge
                if (x_e < x1):
                    x_i = x1
                    y_i = y_e + math.tan(3.1415 / 2 - a_r) * (x1 - x_e)
                    if (y_i > y1 and y_i < y2):
                        p_new = [x_i, y_i, 2]  # left edge
            # third quadron
            if (a_r >= 3.1415) and (a_r < 1.5 * 3.1415):
                if (y_e > y2):
                    x_i = x_e + math.tan(a_r) * (y2 - y_e)
                    y_i = y2
                    if (x_i > x1 and x_i < x2):
                        p_new = [x_i, y_i, 3]  # top edge
                if (x_e > x2):
                    x_i = x2
                    y_i = y_e + math.tan(3.1415 / 2 - a_r) * (x2 - x_e)
                    if (y_i > y1 and y_i < y2):
                        p_new = [x_i, y_i, 4]  # right edge
            # fourth quadron
            if (a_r >= 1.5 * 3.1415) and (a_r < 6.283):
                if (y_e < y1):
                    x_i = x_e + math.tan(a_r) * (y1 - y_e)
                    y_i = y1
                    if (x_i > x1 and x_i < x2):
                        p_new = [x_i, y_i, 1]  # bottom edge
                if (x_e > x2):
                    x_i = x2
                    y_i = y_e + math.tan(3.1415 / 2 - a_r) * (x2 - x_e)
                    if (y_i > y1 and y_i < y2):
                        p_new = [x_i, y_i, 4]  # right edge
            if p_new:
                dist = abs(p_new[0] - x_e) + abs(p_new[1] - y_e)
                if shortest:
                    if dist < shortest:
                        shortest = dist
                        p_intersect = p_new
                else:
                    shortest = dist
                    p_intersect = p_new
            p_new = False

        if p_intersect:
            return p_intersect
        else:
            return False
    def get_vrobot_prox(self, side):
        vrobot = self.vrobot

        a_r = vrobot.a  # robot is orientation, same as sensor orientation
        if (a_r < 0):
            a_r += 6.283
        if (side == "left"):
            a_e = vrobot.a - 3.1415 / 4.5  # emitter location
        else:
            a_e = vrobot.a + 3.1415 / 4.5  # emitter location
        x_e = (vrobot.l - 2) * math.sin(a_e) + vrobot.x  # emiter pos of left sensor
        y_e = (vrobot.l - 2) * math.cos(a_e) + vrobot.y  # emiter pos of right sensor

        intersection = self.radial_intersect(a_r, x_e, y_e)

        if intersection:
            x_i = intersection[0]
            y_i = intersection[1]
            if (side == "left"):
                vrobot.dist_l = math.sqrt((y_i - y_e) * (y_i - y_e) + (x_i - x_e) * (x_i - x_e))
                if vrobot.dist_l > 120:
                    vrobot.dist_l = False
                return vrobot.dist_l
            else:
                vrobot.dist_r = math.sqrt((y_i - y_e) * (y_i - y_e) + (x_i - x_e) * (x_i - x_e))
                if vrobot.dist_r > 120:
                    vrobot.dist_r = False
                return vrobot.dist_r
        else:
            if (side == "left"):
                vrobot.dist_l = False
                return False
            else:
                vrobot.dist_r = False
                return False
    def draw_prox(self, side):
        canvas_width = self.canvas_width
        canvas_height = self.canvas_height
        vrobot = self.vrobot
        if (side == "left"):
            a_e = vrobot.a - 3.1415 / 5  # emitter location
            prox_dis = vrobot.dist_l
            prox_l_id = vrobot.prox_l_id
        else:
            a_e = vrobot.a + 3.1415 / 5  # emitter location
            prox_dis = vrobot.dist_r
            prox_l_id = vrobot.prox_r_id
        if (prox_dis):
            x_e = (vrobot.l - 4) * math.sin(a_e) + vrobot.x  # emiter pos of left sensor
            y_e = (vrobot.l - 4) * math.cos(a_e) + vrobot.y  # emiter pos of right sensor
            x_p = prox_dis * math.sin(vrobot.a) + x_e
            y_p = prox_dis * math.cos(vrobot.a) + y_e
            if (self.prox_dots):
                self.canvas.create_oval(canvas_width + x_p - 1, canvas_height - y_p - 1, canvas_width + x_p + 1,
                                        canvas_height - y_p + 1, outline='red')
            point_list = (canvas_width + x_e, canvas_height - y_e, canvas_width + x_p, canvas_height - y_p)
            self.canvas.coords(prox_l_id, point_list)
        else:
            point_list = (0, 0, 0, 0)
            self.canvas.coords(prox_l_id, point_list)
    def draw_floor(self, side):
        canvas_width = self.canvas_width
        canvas_height = self.canvas_height
        vrobot = self.vrobot
        if (side == "left"):
            border = vrobot.floor_l
            floor_id = vrobot.floor_l_id
            a = vrobot.a - 3.1415 / 7  # rough position of the left floor sensor
        else:
            border = vrobot.floor_r
            floor_id = vrobot.floor_r_id
            a = vrobot.a + 3.1415 / 7  # rough position of the left floor sensor
        x_f = (vrobot.l - 12) * math.sin(a) + vrobot.x
        y_f = (vrobot.l - 12) * math.cos(a) + vrobot.y
        points = (canvas_width + x_f - 2, canvas_height - y_f - 2, canvas_width + x_f + 2, canvas_height - y_f + 2)
        self.canvas.coords(floor_id, points)
        if (border):
            self.canvas.itemconfig(floor_id, outline="black", fill="black")
            if (self.floor_dots):
                self.canvas.create_oval(canvas_width + x_f - 2, canvas_height - y_f - 2, canvas_width + x_f + 2,
                                        canvas_height - y_f + 2, fill='black')
        else:
            self.canvas.itemconfig(floor_id, outline="white", fill="white")
    def get_robot_shape(self):
        canvas_width = self.canvas_width
        canvas_height = self.canvas_height
        pi4 = 3.1415 / 4  # quarter pi
        vrobot = self.vrobot
        a1 = vrobot.a + pi4
        a2 = vrobot.a + 3 * pi4
        a3 = vrobot.a + 5 * pi4
        a4 = vrobot.a + 7 * pi4

        x1 = canvas_width + vrobot.l * math.sin(a1) + vrobot.x
        x2 = canvas_width + vrobot.l * math.sin(a2) + vrobot.x
        x3 = canvas_width + vrobot.l * math.sin(a3) + vrobot.x
        x4 = canvas_width + vrobot.l * math.sin(a4) + vrobot.x

        y1 = canvas_height - vrobot.l * math.cos(a1) - vrobot.y
        y2 = canvas_height - vrobot.l * math.cos(a2) - vrobot.y
        y3 = canvas_height - vrobot.l * math.cos(a3) - vrobot.y
        y4 = canvas_height - vrobot.l * math.cos(a4) - vrobot.y

        points = [x1, y1, x2, y2, x3, y3, x4, y4]
        # if self.canvas: testing = self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4, outline="red", fill="red")
        return points
    def get_robot_shape_lines(self):
        shape_list = self.get_robot_shape()
        x1 = shape_list[0]
        y1 = shape_list[1]
        x2 = shape_list[2]
        y2 = shape_list[3]
        x3 = shape_list[4]
        y3 = shape_list[5]
        x4 = shape_list[6]
        y4 = shape_list[7]
        # print "robot shape:", str([[(x1, y1), (x2, y2)], [(x2, y2), (x3, y3)], [(x3, y3), (x4, y4)], [(x4, y4), (x1, y1)]])
        return [[(x1, y1), (x2, y2)], [(x2, y2), (x3, y3)], [(x3, y3), (x4, y4)], [(x4, y4), (x1, y1)]]
    ######################################################################
    # This function returns True when simulated robot would collide with 
    # one of the obstacles at given pose(a,x,y)
    ######################################################################
    # implemented from https://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect
    # def ccw(self, A, B, C):
    #     return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])
    def intersect(self, line_A, line_B):

        # # print "line_A", str(line_A)
        # # print "line_B", str(line_B)
        # line A
        A = line_A[0][1], line_A[0][1]
        B = line_A[1][0], line_A[1][1]

        # line B
        C = line_B[0][0], line_B[0][1]
        D = line_B[1][0], line_B[1][1]
        # # print "A:"+str(A)
        # # print "B:"+str(B)
        # # print "C:"+str(C)
        # # print "D:"+str(D)
        # Y has to be negative because of strange computer system
        X1 = A[0]
        Y1 = -A[1]
        X2 = B[0]
        Y2 = -B[1]
        X3 = C[0]
        Y3 = -C[1]
        X4 = D[0]
        Y4 = -D[1]

        # Segment1 = {(X1, Y1), (X2, Y2)}
        # Segment2 = {(X3, Y3), (X4, Y4)}
        if (max(X1, X2) < min(X3, X4)):
            return False # no mutual abcisses

        A1 = (Y1 - Y2) / (X1 - X2 + 0.0001) # no 0
        A2 = (Y3 - Y4) / (X3 - X4 + 0.0001) # no 0
        b1 = Y1 - A1 * X1 #= Y2 - A1 * X2
        b2 = Y3 - A2 * X3 #= Y4 - A2 * X4
        if (A1 == A2):
            return False # Parallel segment

        Xa = (b2 - b1) / (A1 - A2 + 0.0001) # no 0
        Ya = A1 * Xa + b1
        Ya = A2 * Xa + b2
        # A1 * Xa + b1 = A2 * Xa + b2
        if ((Xa < max(min(X1, X2), min(X3, X4))) or (Xa > min(max(X1, X2), max(X3, X4)))):
            return False # out of bound
        else:
            return True

        # # point AB, CD
        # return self.ccw(A, C, D) != self.ccw(B, C, D) and self.ccw(A, B, C) != self.ccw(A, B, D)
    def in_collision(self, a, x, y):
        # copied from def create_world(self)
        # x1, y1, x2, y2
        half_width = self.canvas_width
        half_height = self.canvas_height

        # x1 = canvas_width + rect[0]
        # y1 = canvas_height - rect[1]
        # x2 = canvas_width + rect[2]
        # y2 = canvas_height - rect[3]

        rect1 = (-100 + half_width, --180 + half_height, 0 + half_width, --140 + half_height)
        rect2 = (-140 + half_width, --180 + half_height, -100 + half_width, --80 + half_height)
        rect3 = (-100 + half_width, -140 + half_height, 0 + half_width, -180 + half_height)
        rect4 = (-140 + half_width, -80 + half_height, -100 + half_width, -180 + half_height)
        rect5 = (0 + half_width, --50 + half_height, 40 + half_width, -50 + half_height)
        rect6 = (-260 + half_width, --20 + half_height, -220 + half_width, -20 + half_height)
        rect7 = (40 + half_width, -60 + half_height, 140 + half_width, -100 + half_height)
        # if self.canvas: self.canvas.create_rectangle(rect1, outline="red", fill="red")
        # if self.canvas: self.canvas.create_rectangle(rect2, outline="red", fill="red")
        # if self.canvas: self.canvas.create_rectangle(rect3, outline="red", fill="red")
        # if self.canvas: self.canvas.create_rectangle(rect4, outline="red", fill="red")
        # if self.canvas: self.canvas.create_rectangle(rect5, outline="red", fill="red")
        # if self.canvas: self.canvas.create_rectangle(rect6, outline="red", fill="red")
        # if self.canvas: self.canvas.create_rectangle(rect7, outline="red", fill="red")

        temp_rects = [rect1, rect2, rect3, rect4, rect5, rect6, rect7]

        object_lines_with_each_rectangle = []  # init all rectangles in the map
        for rect in temp_rects:
            object_lines_with_each_rectangle.append(RectangleModel(rect).get_all_lines())

        # print "object_lines all together:" + str(object_lines_with_each_rectangle)
        robot_lines = self.get_robot_shape_lines()

        object_lines_all_together = []
        for object_lines in object_lines_with_each_rectangle:
            for object_line in object_lines:
                object_lines_all_together.append(object_line)
        # print "object_lines" + str(object_lines_all_together)


        # testing code
        for object_line in object_lines_all_together:
            if len(self.test_lines) < 50 and self.canvas is not None:
                print "I AM:" + str(object_line[0][0]) + str(object_line[0][1]) + str(object_line[1][0]) + str(object_line[1][1])
                line = self.canvas.create_line(object_line[0][0], object_line[0][1], object_line[1][0], object_line[1][1])
                self.test_lines.append(line)
        for robot_line in robot_lines:
            if len(self.test_lines) < 50 and self.canvas is not None:
                line = self.canvas.create_line(robot_line[0][0], robot_line[0][1], robot_line[1][0], robot_line[1][1])
                self.test_lines.append(line)


        for robot_line in robot_lines:
            for object_line in object_lines_all_together:
                if self.intersect(robot_line, object_line):
                    print "collision!"
                    return True
                    break
        return False

# class RobotCollision:


class RectangleModel:
    def __init__(self, rectangle):
        self.x1 = rectangle[0]
        self.y1 = rectangle[1]
        self.x2 = rectangle[2]
        self.y2 = rectangle[3]
    # point = (x, y)
    def get_upper_left_point(self):
        return self.x1, self.y1
    def get_upper_right_point(self):
        return self.x2, self.y1
    def get_lower_left_point(self):
        return self.x1, self.y2
    def get_lower_right_point(self):
        return self.x2, self.y2
    # line = [x1, y1, x2, y2]
    def get_up_line(self):
        return [self.get_upper_left_point(), self.get_upper_right_point()]
    def get_left_line(self):
        return [self.get_upper_left_point(), self.get_lower_left_point()]
    def get_right_line(self):
        return [self.get_upper_right_point(), self.get_lower_right_point()]
    def get_down_line(self):
        return [self.get_lower_left_point(), self.get_lower_right_point()]
    def get_all_lines(self):
        return self.get_up_line(), self.get_left_line(), self.get_right_line(), self.get_down_line()
