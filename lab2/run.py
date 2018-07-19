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
class RobotControler(object):
    def __init__(self, robotid):
        self.robotid = robotid
        self.task = -1

        self.proximity_left = 0
        self.proximity_right = 0
        self.floor_left = 0
        self.floor_right = 0
        self.light = 0
        self.wheel_left = 0
        self.wheel_right = 0
        self.detection_left = 0
        self.detection_right = 0
    def move_forward(self, event=None):
        self.wheel_left = 50
        self.wheel_right = 50
    def move_backward(self, event=None):
        self.wheel_left = -50
        self.wheel_right = -50
    def move_left(self, event=None):
        self.wheel_left = 0
        self.wheel_right = 50
    def move_right(self, event=None):
        self.wheel_left = 50
        self.wheel_right = 0

    def get_prox_left(self, event=None):
        return self.proximity_left
    def get_prox_right(self, event=None):
        return self.proximity_right

    def get_floor_left(self, event=None):
        return self.floor_left
    def get_floor_right(self, event=None):
        return self.floor_right

    def stop_move(self, event=None):
        self.wheel_left = 0
        self.wheel_right = 0

    def reset_robot(self, event=None): # use Hamster API reset()
        pass

    def refresh(self, event=None, task=-1, proximity_left, proximity_right, floor_left, floor_right, light, wheel_left, wheel_right, detection_left, detection_right):
        self.task = task
        self.proximity_left = proximity_left
        self.proximity_right = proximity_right
        self.floor_left = floor_left
        self.floor_right = floor_right
        self.light = light
        self.wheel_left = wheel_left
        self.wheel_right = wheel_right
        self.detection_left = detection_left
        self.detection_right = detection_right


class Robots(object):
    def __init__(self, robotList):
        self.robotList = robotList
        self.go = False
        self.done = False

        self.robotControllers = []
        for robotid in range(len(robotList)-1):
            self.robotControllers.append(RobotControler(robotid))
        return
    def refreshRobots(self):
        for controller in self.robotControllers:
          proximity_left = robot.get_proximity(0)
          proximity_right = robot.get_proximity(1)
          floor_left = robot.get_floor(0)
          floor_right = robot.get_floor(1)
          light = robot.get_light()
          wheel_left = 0
          wheel_right = 0
          detection_left = (self.floor_left > 50)
          detection_right = (self.floor_right > 50)
          controller.refresh(proximity_left, proximity_right, floor_left, floor_right, light, wheel_left, wheel_right, detection_left, detection_right)
  def getController(self):
    return self.robotControllers[0]

  def run(self):
    robot=None
    while not self.done:
      refreshRobots(self)
      for robot in self.robotList:
        if robot and self.go:
          #############################################
          # START OF YOUR WORKING AREA!!!
          #############################################
          robot.set_wheel(0, self.robotControllers[0].wheel_left) #WARNING! Robotid =0
          robot.set_wheel(1, self.robotControllers[0].wheel_right)
          #############################################
          # END OF YOUR WORKING AREA!!!
          #############################################
    # stop robot activities, such as motion, LEDs and sound
    # clean up after exit button pressed
    if robot:
      robot.reset()
      time.sleep(0.01)
    return
class UI(object):
    def __init__(self, root, robot_handle):
        self.root = root # root = tk.Tk()
        self.robot_handle = robot_handle  # handle to robot commands

        # self.canvas = None
        # self.prox_l_id = None
        # self.prox_r_id = None
        # self.floor_l_id = None
        # self.floor_r_id = None
        self.initUI()
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

        lable_widget_robotid = tk.Lable(self.root, text="RobotID: N/A")
        lable_widget_robotid.pack()
        lable_widget_task = tk.Lable(self.root, text="Task: N/A")
        lable_widget_task.pack()
        lable_widget_proximity_left = tk.Lable(self.root, text="ProxLeft: N/A")
        lable_widget_proximity_left.pack()
        lable_widget_proximity_right = tk.Lable(self.root, text="ProxRight: N/A")
        lable_widget_proximity_right.pack()
        lable_widget_floor_left = tk.Lable(self.root, text="FloorLeft: N/A")
        lable_widget_floor_left.pack()
        lable_widget_floor_right = tk.Lable(self.root, text="FloorRight: N/A")
        lable_widget_floor_right.pack()
        lable_widget_light = tk.Lable(self.root, text="Light: N/A")
        lable_widget_light.pack()
        lable_widget_wheel_left = tk.Lable(self.root, text="WheelLeft: N/A")
        lable_widget_wheel_left.pack()
        lable_widget_wheel_right = tk.Lable(self.root, text="WheelRight: N/A")
        lable_widget_wheel_right.pack()
        lable_widget_detection_left = tk.Lable(self.root, text="DetectionLeft: N/A")
        lable_widget_detection_left.pack()
        lable_widget_detection_right = tk.Lable(self.root, text="DetectionRight: N/A")
        lable_widget_detection_right.pack()


        # # creating button
        # button_widget = tk.Button(self.root, text="press me",  commands=self.sayHi())

        # # arrange wides in one direction only if not specified
        # # grid with pack, you will get nothing. Please use pack() only
        # # pack(side=tk.LEFT) / tk.RIGHT
        # button_widget.pack()

        # # bg="black", fg="green", font="..." (front color, back color, font)
        # lable_widget = tk.Lable(self.root, text="Label widget")
        # lable_widget.pack()
        # # self.label.config(text="hello")

        # # pixel: x increase as go right, y increase as go down
        # canvas_widget = tk.Canvas(self.root, bg="grey")
        # canvas_widget.pack()
        # # canvas_widget.create_rectange(left_x, left_y, right_x, roght_y, fill="green")
        # # canvas_widget.create_line(left_x, left_y, right_x, roght_y, fill="green", width=3)
        # # all these objects are in canvas instance
        # line = canvas_widget.create_line(left_x, left_y, right_x, roght_y, fill="green", width=3)

        # # coords(), itemconfig(), move(), delete()
        # canvas_widget.coords(line, left_x, left_y, right_x, roght_y)
        # canvas_widget.itemconfig(line, fill="white")
        # # move(item, dx, dy)

        # # event: description occurs in the widget (look up on Google)
        #     # "<Botton-1>"
        # # handler: things to do
        # canvas_widget.bind(event, handler)

        # # calculating ball
        # #x1, y1 = (event.x - radius), (event.y-radius)
        # #x2, y2 = (event.x + radius), (event.y+radius)
        # #canvas_widget.coords(ball_id, x1, y1, x2, y2)
        # #pack(expand =YES, fill = BOTH)
        # # oval is a ball
        # # ball_id = canvas_widget.create_oval(300-r, 300-r, 300+r, 300+r)

        # # Timer triggered Events
        # # after(delay_ms, callback=None, (*args for the callback function))
        # # root.after(...), widet.after(...)

        # # button, canvas, checkbutton, entry...
        # # global xxx: something in def that exist globally

    ######################################################
    # This function refreshes floor and prox sensor display every 100 milliseconds.
    # Register callback using Tkinter's after method().
    ######################################################
    def display_sensor(self):
        pass

    ####################################################
    # Implement callback function when key press is detected
    ####################################################
    def keydown(self, event):
        pass

    #####################################################
    # Implement callback function when key release is detected
    #####################################################
    def keyup(self, event):
        pass

    def stopProg(self, event=None):
        self.root.quit()    # close window
        self.robot_handle.reset_robot()
        return
    def refreshUI(self):
        self.lable_widget_robotid.config(text="")
        self.lable_widget_task.config(text="")
        self.lable_widget_proximity_left.config(text="")
        self.lable_widget_proximity_right.config(text="")
        self.lable_widget_floor_left.config(text="")
        self.lable_widget_floor_right.config(text="")
        self.lable_widget_light.config(text="")
        self.lable_widget_wheel_left.config(text="")
        self.lable_widget_wheel_right.config(text="")
        self.lable_widget_detection_left.config(text="")
        self.lable_widget_detection_right.config(text="")
        return

def main(argv=None):
    gMaxRobotNum = 1 # max number of robots to control
    comm = RobotComm(gMaxRobotNum)
    comm.start()
    print 'Bluetooth starts'
    robotList = comm.robotList

    robot_handle = Robots(robotList)
    m = tk.Tk() #m is tk.Tk() and root
    gui = UI(m, robot_handle) #m is tk.Tk() and root

    m.mainloop() # stop the program from ending. mainloop() is in tkinterface

    comm.stop()
    comm.join()

if __name__== "__main__":
    sys.exit(main())
