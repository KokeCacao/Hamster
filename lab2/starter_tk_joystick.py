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
        return robot.get_get_proximity(0)

    def get_prox_r(self, event=None):
        return robot.get_get_proximity(1)

    def get_floor_l(self, event=None):
        return robot.get_get_floor(0)

    def get_floor_r(self, event=None):
        return robot.get_get_floor(1)

    def stop_move(self, event=None):
        pass

    def reset_robot(self, event=None): # use Hamster API reset()
        robot.reset()

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

        self.root.title("Hamster")
        self.root.geometry("200x50+0+0")

        self.floor_l_id = tk.Label(self.root, text="FloorLeft: N/A")
        self.floor_l_id.pack()

        self.floor_r_id = tk.Label(self.root, text="FloorRight: N/A")
        self.floor_r_id.pack()

        self.prox_l_id = tk.Label(self.root, text="ProxLeft: N/A")
        self.prox_l_id.pack()

        self.prox_r_id = tk.Label(self.root, text="ProxRight: N/A")
        self.prox_r_id.pack()

        self.canvas = tk.Canvas(self.root, width=1280, height=720, bg="white")
        self.canvas_robot_id = self.canvas.create_rectangle(615, 335, 665, 385, fill="gold")
        self.canvas_floorl_id = self.canvas.create_rectangle(615+5, 335+5, 665+10, 385+10, fill="black")
        self.canvas_floorr_id = self.canvas.create_rectangle(615+5+40, 335+5, 665+10+40, 385+10, fill="black")
        self.canvas_proxl_id = self.canvas.create_line(615+5, 335+5, 615+5, 335+5+0, fill="black", width=4)
        self.canvas_proxr_id = self.canvas.create_line(665+40, 385, 665+40, 385+0, fill="black", width=4)
        self.canvas.pack()

        root.bind('<KeyPress>', self.keydown)
        root.bind('<KeyRelease>', self.keyup)

    ######################################################
    # This function refreshes floor and prox sensor display every 100 milliseconds.
    # Register callback using Tkinter's after method().
    ######################################################
    def display_sensor(self):
        floor_l = self.robot.get_floor_l()
        floor_r = self.robot.get_floor_r()
        prox_l = self.robot.get_prox_l()
        prox_r = self.robot.get_prox_r()

        self.floor_l_id.config(text=str(floor_l))
        self.floor_r_id.config(text=str(floor_r))
        self.prox_l_id.config(text=str(prox_l))
        self.prox_r_id.config(text=str(prox_r))

        if floor_l > 50:
            self.canvas.itemconfig(self.canvas_floorl_id, fill="white")
        else:
            self.canvas.itemconfig(self.canvas_floorl_id, fill="black")
        if floor_r > 50:
            self.canvas.itemconfig(self.canvas_floorr_id, fill="white")
        else:
            self.canvas.itemconfig(self.canvas_floorr_id, fill="black")

        self.canvas.itemconfig(self.canvas_proxl_id, 615+5, 335+5, 615+5, 335+5+prox_l)
        self.canvas.itemconfig(self.canvas_proxr_id, 615+5, 335+5, 615+5, 335+5+prox_r)

        self.root.after(10, self.display_sensor())

    ####################################################
    # Implement callback function when key press is detected
    ####################################################
    def keydown(self, event):
        print "pressed", repr(event.char)
        if repr(event.char) is "W" or "w":
            self.robot.move_forward()
        elif repr(event.char) is "A" or "a":
            self.robot.move_left()
        elif repr(event.char) is "S" or "s":
            self.robot.move_backward()
        elif repr(event.char) is "D" or "d":
            self.robot.move_right()

    #####################################################
    # Implement callback function when key release is detected
    #####################################################
    def keyup(self, event):
        self.robot.stop_move()

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
