'''
/* =======================================================================
   (c) 2015, Kre8 Technology, Inc.

   Name:          Joystick for Hamster
   By:            Qin Chen
   Last Updated:  5/10/18

   PROPRIETARY and CONFIDENTIAL
   ========================================================================*/
'''
import sys
import Tkinter as tk
# noinspection PyUnresolvedReferences
from HamsterAPI.comm_ble import RobotComm
#for PC, need to import from commm_usb

class Robots(object):
    def __init__(self, robotList):
        self.robotList = robotList
        return

    def move_degree(self, degree=None, move_x=None, move_y=None, event=None):
        if degree == 0:
            self.move_right()
        elif degree == 45:
            self..move_right()
        elif degree == 90:
            self.move_forward()
        elif degree == 135:
            self.move_left()
        elif degree == 180:
            self.move_left()
        elif degree == 225:
            self.move_back_left()
        elif degree == 270:
            self.move_backward()
        elif degree == 315:
            self.move_back_right()

        # front
            # 180-90: left stop -> move, the other move
            # 0-90: right stop -> move, the other move
        # back
            # 180-270: left stop - move, the other move
            # 360-270: right stop - move, the other move
        # if move_x or move_y or degree:
        #     temp_left = 0
        #     temp_right = 1
        #
        #     if 0 <= degree <= 180:  # front
        #         if 180 >= degree > 90:  # left
        #             temp_left = (-degree + 180) * (100/90)
        #             temp_right = 100
        #         elif degree == 90:  # straight
        #             temp_left = 100
        #             temp_right = 100
        #         elif 90 > degree >= 0: # right
        #             temp_left = 100
        #             temp_right = degree * (100/90)
        #     if 180 < degree < 360:
        #         if 180 < degree < 270:
        #             temp_left = -(degree - 180) * (100/90)
        #             temp_right = -100
        #         elif degree == 270:
        #             temp_left = -100
        #             temp_right = -100
        #         elif 270 < degree < 360:
        #             temp_left = -100
        #             temp_right = -(-degree + 180) * (100/90)
        #
        #     if self.robotList:
        #         for robot in self.robotList:
        #             robot.set_wheel(0,temp_left)
        #         robot.set_wheel(1,temp_right)

    def move_forward(self, event=None):
        if self.robotList:
            for robot in self.robotList:
                robot.set_wheel(0,30)
                robot.set_wheel(1,30)

    def move_backward(self, event=None):
        if self.robotList:
            for robot in self.robotList:
                robot.set_wheel(0,-30)
                robot.set_wheel(1,-30)

    def move_left(self, event=None):
        if self.robotList:
            for robot in self.robotList:
                robot.set_wheel(0,0)
                robot.set_wheel(1,30)

    def move_back_left(self, event=None):
        if self.robotList:
            for robot in self.robotList:
                robot.set_wheel(0,0)
                robot.set_wheel(1,-30)

    def move_right(self, event=None):
        if self.robotList:
            for robot in self.robotList:
                robot.set_wheel(0,30)
                robot.set_wheel(1,0)

    def move_back_right(self, event=None):
        if self.robotList:
            for robot in self.robotList:
                robot.set_wheel(0,-30)
                robot.set_wheel(1,0)

    def get_prox_l(self, event=None):
        if self.robotList:
            for robot in self.robotList:
                return robot.get_proximity(0)  # only get first robot

    def get_prox_r(self, event=None):
        if self.robotList:
            for robot in self.robotList:
                return robot.get_proximity(1)  # only get first robot

    def get_floor_l(self, event=None):
        if self.robotList:
            for robot in self.robotList:
                return robot.get_floor(0)  # only get first robot

    def get_floor_r(self, event=None):
        if self.robotList:
            for robot in self.robotList:
                return robot.get_floor(1)  # only get first robot

    def get_battery(self, event=None):
        if self.robotList:
            for robot in self.robotList:
                return robot.get_battery()  # only get first robot

    def get_light(self, event=None):
        if self.robotList:
            for robot in self.robotList:
                return robot.get_light()  # only get first robot

    def get_temperature(self, event=None):
        if self.robotList:
            for robot in self.robotList:
                return robot.get_temperature()  # only get first robot

    def stop_move(self, event=None):
        if self.robotList:
            for robot in self.robotList:
                robot.set_wheel(0,0)
                robot.set_wheel(1,0)

    def reset_robot(self, event=None):  # use Hamster API reset()
        if self.robotList:
            for robot in self.robotList:
                robot.reset()

class UI(object):
    def __init__(self, root, robot_handle):
        self.root = root
        self.robot_handle = robot_handle  # handle to robot commands

        # visualization id
        self.canvas = None
        self.exit = None
        self.prox_l_id = None
        self.prox_r_id = None
        self.floor_l_id = None
        self.floor_r_id = None
        self.canvas_robot_id = None
        self.canvas_flool_id = None
        self.canvas_floor_id = None
        self.canvas_proxl_id = None
        self.canvas_proxr_id = None

        # 2D reconstruction
        self.dotList = []
        self.move_degree = 90 # relative vector
        self.move_x = 0  # relative vector
        self.move_y = 0  # relative vector
        self.key_strength = 1

        self.x = 0
        self.y = 0
        self.orientation = 90

        # robot data: key press
        self.key_w = False
        self.key_a = False
        self.key_s = False
        self.key_d = False

        # run robot and displacer using key frames
        self.initUI()
        self.display_sensor()
        return

    def initUI(self):
        ###################################################################
        # Create a Hamster joystick window which contains
        # 1. a canvas widget where "sensor readings" are displayed
        # 2. a square representing Hamster
        # 3. 4 canvas items to display floor sensors and prox sensors
        # 4. a button for exit, i.e., a call to stopProg(), given in this class
        # 5. listen to key press and key release when focus is on this window
        ###################################################################

        # canvas calculation
        canvas_width = 1280/2
        canvas_height = 720/2
        # robot calculation
        robot_side = 100
        robot_center_x = canvas_width/2
        robot_center_y = canvas_height/2
        robot_x1 = robot_center_x - robot_side/2
        robot_y1 = robot_center_y - robot_side/2
        robot_x2 = robot_center_x + robot_side/2
        robot_y2 = robot_center_y + robot_side/2
        # floor left calculation
        floor_side = 10
        floorl_x1 = robot_x1
        floorl_y1 = robot_y1
        floorl_x2 = robot_x1 + floor_side
        floorl_y2 = robot_y1 + floor_side
        # floor right calculation
        floorr_x1 = robot_x1 + robot_side - floor_side
        floorr_y1 = robot_y1
        floorr_x2 = floorr_x1 + floor_side
        floorr_y2 = floorr_y1 + floor_side
        # prox calculation
        prox_l_x = floorl_x1
        prox_l_y = floorl_y1
        prox_r_x = floorr_x2
        prox_r_y = floorr_y2 - floor_side


        self.exit = tk.Button(self.root, text='Exit', commands=self.stopProg())
        self.exit.pack(side='left')

        # init everything
        self.root.title("Hamster")
        self.root.geometry("1280x720+0+0")
        self.floor_l_id = tk.Label(self.root, text="FloorLeft: N/A")
        self.floor_l_id.pack()
        self.floor_r_id = tk.Label(self.root, text="FloorRight: N/A")
        self.floor_r_id.pack()
        self.prox_l_id = tk.Label(self.root, text="ProxLeft: N/A")
        self.prox_l_id.pack()
        self.prox_r_id = tk.Label(self.root, text="ProxRight: N/A")
        self.prox_r_id.pack()
        self.canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height, bg="white")
        self.canvas_robot_id = self.canvas.create_rectangle(robot_x1, robot_y1, robot_x2, robot_y2, fill="gold")
        self.canvas_floorl_id = self.canvas.create_rectangle(floorl_x1, floorl_y1, floorl_x2, floorl_y2, fill="black")
        self.canvas_floorr_id = self.canvas.create_rectangle(floorr_x1, floorr_y1, floorr_x2, floorr_y2, fill="black")
        self.canvas_proxl_id = self.canvas.create_line(prox_l_x, prox_l_y, prox_l_x, prox_l_y, fill="black", width=4)
        self.canvas_proxr_id = self.canvas.create_line(prox_r_x, prox_r_y, prox_r_x, prox_r_y, fill="black", width=4)
        self.canvas.pack()

        # add key listeners
        self.root.bind('<KeyPress>', self.keydown)
        self.root.bind('<KeyRelease>', self.keyup)

    ######################################################
    # This function refreshes floor and prox sensor display every 100 milliseconds.
    # Register callback using Tkinter's after method().
    ######################################################
    def display_sensor(self):
        # canvas calculation
        canvas_width = 1280/2
        canvas_height = 720/2
        # robot calculation
        robot_side = 100
        robot_center_x = canvas_width/2
        robot_center_y = canvas_height/2
        robot_x1 = robot_center_x - robot_side/2
        robot_y1 = robot_center_y - robot_side/2
        robot_x2 = robot_center_x + robot_side/2
        robot_y2 = robot_center_y + robot_side/2
        # floor left calculation
        floor_side = 10
        floorl_x1 = robot_x1
        floorl_y1 = robot_y1
        floorl_x2 = robot_x1 + floor_side
        floorl_y2 = robot_y1 + floor_side
        # floor right calculation
        floorr_x1 = robot_x1 + robot_side - floor_side
        floorr_y1 = robot_y1
        floorr_x2 = floorr_x1 + floor_side
        floorr_y2 = floorr_y1 + floor_side
        # prox calculation
        prox_l_x = floorl_x1
        prox_l_y = floorl_y1
        prox_r_x = floorr_x2
        prox_r_y = floorr_y2 - floor_side

        # update data
        floor_l = self.robot_handle.get_floor_l()
        if floor_l == None: floor_l=0
        floor_r = self.robot_handle.get_floor_r()
        if floor_r == None: floor_r=0
        prox_l = self.robot_handle.get_prox_l()
        if prox_l == None: prox_l=0
        prox_r = self.robot_handle.get_prox_r()
        if prox_r == None: prox_r=0

        # update floor and prox text
        self.floor_l_id.config(text="FloorLeft: " + str(floor_l))
        self.floor_r_id.config(text="FloorRight: " + str(floor_r))
        self.prox_l_id.config(text="ProxLeft: " + str(prox_l))
        self.prox_r_id.config(text="ProxRight: " + str(prox_r))

        # update floor and prox visualization
        if floor_l > 50:
            self.canvas.itemconfig(self.canvas_floorl_id, fill="white")
        else:
            self.canvas.itemconfig(self.canvas_floorl_id, fill="black")
        if floor_r > 50:
            self.canvas.itemconfig(self.canvas_floorr_id, fill="white")
        else:
            self.canvas.itemconfig(self.canvas_floorr_id, fill="black")
        self.canvas.coords(self.canvas_proxl_id, prox_l_x, prox_l_y, prox_l_x, prox_l_y - (50-prox_l))
        self.canvas.coords(self.canvas_proxr_id, prox_r_x, prox_r_y, prox_r_x, prox_r_y - (50-prox_r))

        # loop
        self.root.after(100, self.display_sensor)

    ####################################################
    # Implement callback function when key press is detected
    # http://www.tcl.tk/man/tcl8.4/TkCmd/keysyms.htm
    ####################################################
    def keydown(self, event):
        key = event.keycode
        print "keycode down =",str(key)
        # small, big
        if key == 97 or key == 64:
            self.key_a = True
            print "key a"
        if key == 115 or key == 83 or key == 65651:
            self.key_s = True
            print "key s"
        if key == 119 or key == 87 or key == 852087:
            self.key_w = True
            print "key w"
        if key == 100 or key == 68 or key == 131172:
            self.key_d = True
            print "key d"

        self.key_refresh()
    #####################################################
    # Implement callback function when key release is detected
    # http://www.tcl.tk/man/tcl8.4/TkCmd/keysyms.htm
    #####################################################
    def keyup(self, event):
        key = event.keycode
        print "keycode up =",str(key)
        # small, big
        if key == 97 or key == 64:
            self.key_a = False
            print "keyup a"
        if key == 115 or key == 83 or key == 65651:
            self.key_s = False
            print "keyup s"
        if key == 119 or key == 87 or key == 852087:
            self.key_w = False
            print "keyup w"
        if key == 100 or key == 68 or key == 131172:
            self.key_d = False
            print "keyup d"

        self.key_refresh()
    def key_refresh(self):
        import math
        temp_move_x = 0
        temp_move_y = 0
        if self.key_w:
            temp_move_y = temp_move_y+self.key_strength
        if self.key_a:
            temp_move_x = temp_move_x-self.key_strength
        if self.key_d:
            temp_move_x = temp_move_x+self.key_strength
        if self.key_s:
            temp_move_y = temp_move_y-self.key_strength

        # update vector caused by the key
        self.move_x = temp_move_x
        self.move_y = temp_move_y

        if self.move_x == 0 and self.move_y == 0:
            self.robot_handle.stop_move()
            return

        self.move_degree = math.atan2(self.move_y, self.move_x)/math.pi*180  # transfer coordinate into degree
        print "degree="+str(self.move_degree)+" and ("+str(self.move_x)+", "+str(self.move_y)+")"
        self.robot_handle.move_degree(degree=self.move_degree, move_x=self.move_x, move_y=self.move_y)

    def stopProg(self, event=None):
        self.root.quit()    # close window
        self.robot_handle.reset_robot()
        return

def main(argv=None):
    gMaxRobotNum = 1 # max number of robots to control
    comm = RobotComm(gMaxRobotNum)
    comm.start()
    print 'Bluetooth starts'
    robotList = comm.robotList

    robot_handle = Robots(robotList)
    m = tk.Tk() #root
    gui = UI(m, robot_handle)

    m.mainloop()

    comm.stop()
    comm.join()

if __name__== "__main__":
    sys.exit(main())
