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
from HamsterAPI.comm_ble import RobotComm
#for PC, need to import from commm_usb

class Robots(object):
    def __init__(self, robotList):
        self.robotList = robotList
        return

    def move_forward(self, event=None):
        if self.robotList:
            for robot in self.robotList:
                robot.set_wheel(0,30)
                robot.set_wheel(1,30)
        else:
            print "waiting for robot"

    def move_backward(self, event=None):
        pass

    def move_left(self, event=None):
        pass

    def move_right(self, event=None):
        pass

    def get_prox_l(self, event=None):
        if self.robotList:
            for robot in self.robotList:
                return robot.get_proximity(0) # only get first robot
        else:
            print "waiting for robot"

    def get_prox_r(self, event=None):
        if self.robotList:
            for robot in self.robotList:
                return robot.get_proximity(1) # only get first robot
        else:
            print "waiting for robot"

    def get_floor_l(self, event=None):
        if self.robotList:
            for robot in self.robotList:
                return robot.get_floor(0) # only get first robot
        else:
            print "waiting for robot"

    def get_floor_r(self, event=None):
        if self.robotList:
            for robot in self.robotList:
                return robot.get_floor(1) # only get first robot
        else:
            print "waiting for robot"

    def stop_move(self, event=None):
        pass

    def reset_robot(self, event=None): # use Hamster API reset()
        if self.robotList:
            for robot in self.robotList:
                return robot.reset() # only get first robot
        else:
            print "waiting for robot"

class UI(object):
    def __init__(self, root, robot_handle):
        self.root = root
        self.robot_handle = robot_handle  # handle to robot commands

        self.canvas = None

        self.prox_l_id = None
        self.prox_r_id = None

        self.floor_l_id = None
        self.floor_r_id = None

        self.canvas_robot_id = None
        self.canvas_flool_id = None
        self.canvas_floor_id = None
        self.canvas_proxl_id = None
        self.canvas_proxr_id = None

        self.exit = None

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
        canvas_width = 1280/2
        canvas_height = 720/2
        robot_side = 100
        robot_center_x = canvas_width/2
        robot_center_y = canvas_height/2
        robot_x1 = robot_center_x - robot_side
        robot_y1 = robot_center_y - robot_side
        robot_x2 = robot_center_x + robot_side
        robot_y2 = robot_center_y + robot_side

        floor_side = 10
        floorl_x1 = robot_x1
        floorl_y1 = robot_y1
        floorl_x2 = robot_x1 + floor_side
        floorl_y2 = robot_y1 + floor_side

        floorr_x1 = robot_x1 + robot_side - floor_side
        floorr_y1 = robot_y1
        floorr_x2 = floorr_x1 + floor_side
        floorr_y2 = floorr_y1 + floor_side

        prox_l_x = floorl_x1
        prox_l_y = floorl_y1
        prox_r_x = floorr_x2
        prox_r_y = floorr_y2 - floor_side


        self.exit = tk.Button(self.root, text='Exit', command=self.stopProg())
        self.exit.pack(side='left')


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

        self.canvas = tk.Canvas(self.root, width=1280, height=720, bg="white")
        self.canvas_robot_id = self.canvas.create_rectangle(robot_x1, robot_y1, robot_x2, robot_y2, fill="gold")
        self.canvas_floorl_id = self.canvas.create_rectangle(floorl_x1, floorl_y1, floorl_x2, floorl_y2, fill="black")
        self.canvas_floorr_id = self.canvas.create_rectangle(floorr_x1, floorr_y1, floorr_x2, floorr_y2, fill="black")
        self.canvas_proxl_id = self.canvas.create_line(prox_l_x, prox_l_y, prox_l_x, prox_l_y, fill="black", width=4)
        self.canvas_proxr_id = self.canvas.create_line(prox_r_x, prox_r_y, prox_r_x, prox_r_y, fill="black", width=4)
        self.canvas.pack()

        self.root.bind('<KeyPress>', self.keydown)
        self.root.bind('<KeyRelease>', self.keyup)

    ######################################################
    # This function refreshes floor and prox sensor display every 100 milliseconds.
    # Register callback using Tkinter's after method().
    ######################################################
    def display_sensor(self):
        canvas_width = 1280/2
        canvas_height = 720/2
        robot_side = 100
        robot_center_x = canvas_width/2
        robot_center_y = canvas_height/2
        robot_x1 = robot_center_x - robot_side
        robot_y1 = robot_center_y - robot_side
        robot_x2 = robot_center_x + robot_side
        robot_y2 = robot_center_y + robot_side

        floor_side = 10
        floorl_x1 = robot_x1
        floorl_y1 = robot_y1
        floorl_x2 = robot_x1 + floor_side
        floorl_y2 = robot_y1 + floor_side

        floorr_x1 = robot_x1 + robot_side - floor_side
        floorr_y1 = robot_y1
        floorr_x2 = floorr_x1 + floor_side
        floorr_y2 = floorr_y1 + floor_side

        prox_l_x = floorl_x1
        prox_l_y = floorl_y1
        prox_r_x = floorr_x2
        prox_r_y = floorr_y2 - floor_side

        floor_l = 0
        floor_r = 0
        prox_l = 0
        prox_r = 0

        floor_l = self.robot_handle.get_floor_l()
        floor_r = self.robot_handle.get_floor_r()
        prox_l = self.robot_handle.get_prox_l()
        prox_r = self.robot_handle.get_prox_r()

        if floor_l or floor_r or prox_l or prox_r:
            self.floor_l_id.config(text="FloorLeft: " + str(floor_l))
            self.floor_r_id.config(text="FloorRight: " + str(floor_r))
            self.prox_l_id.config(text="ProxLeft: " + str(prox_l))
            self.prox_r_id.config(text="ProxRight: " + str(prox_r))

            if floor_l > 50:
                self.canvas.itemconfig(self.canvas_floorl_id, fill="white")
            else:
                self.canvas.itemconfig(self.canvas_floorl_id, fill="black")
            if floor_r > 50:
                self.canvas.itemconfig(self.canvas_floorr_id, fill="white")
            else:
                self.canvas.itemconfig(self.canvas_floorr_id, fill="black")

            self.canvas.coords(self.canvas_proxl_id, prox_l_x, prox_l_y, prox_l_x, prox_l_y - prox_l)
            self.canvas.coords(self.canvas_proxr_id, prox_r_x, prox_r_y, prox_r_x, prox_r_y - prox_r)

        self.root.after(100, self.display_sensor)

    ####################################################
    # Implement callback function when key press is detected
    ####################################################
    def keydown(self, event):
        print "pressed", repr(event.char)
        if repr(event.char) is "W" or "w":
            self.robot_handle.move_forward()
        elif repr(event.char) is "A" or "a":
            self.robot_handle.move_left()
        elif repr(event.char) is "S" or "s":
            self.robot_handle.move_backward()
        elif repr(event.char) is "D" or "d":
            self.robot_handle.move_right()

    #####################################################
    # Implement callback function when key release is detected
    #####################################################
    def keyup(self, event):
        self.robot_handle.stop_move()

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
