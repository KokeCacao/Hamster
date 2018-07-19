'''
* =======================================================================
   (c) 2015, Kre8 Technology, Inc.
   This is a program that is provided to students in Robot AI class.
   Students use this it to build different Hamster behaviors.

   Name:          tk_behaviors_starter.py
   By:            Qin Chen
   Last Updated:  5/10/18

   PROPRIETARY and CONFIDENTIAL
   ========================================================================*/
'''
import sys
import time
import threading
import Tkinter as tk
from HamsterAPI.comm_ble import RobotComm  # no dongle
#from HamsterAPI.comm_usb import RobotComm # yes dongle

################################
# Hamster control
################################
class RobotBehaviorThread(threading.Thread):
  def __init__(self, robotList):
    super(RobotBehaviorThread, self).__init__()
    self.go = False
    self.done = False
    self.robotList = robotList
    return

  def run(self):
    robot=None
    while not self.done:
      for robot in self.robotList:
        if robot and self.go:
          proximity_left = robot.get_proximity(0)
          proximity_right = robot.get_proximity(1)
          floor_left = robot.get_floor(0)
          floor_right = robot.get_floor(1)
          light = robot.get_light()
          wheel_left = 0
          wheel_right = 0
          left_detection = (floor_left > 50)
          right_detection = (floor_right > 50)
          #############################################
          # START OF YOUR WORKING AREA!!!
          #############################################
          # Quad
          # robot.set_wheel(0, 30)
          # robot.set_wheel(1, 30)
          # time.sleep(100) #run time
          # robot.set_wheel(0, 0)
          # time.sleep(100) #turn time

          # Shy -- Tested
          # if (proximity_left > 10 or proximity_right > 10):
          #   wheel_left = -proximity_left *10
          #   wheel_right = -proximity_right *10
          # Dance -- Tested
          # if proximity_left > 10: #too close
          #   wheel_left = -100
          # else:
          #   wheel_left = 100
          # if proximity_right > 10: #too close
          #   wheel_right = -100
          # else:
          #   wheel_right = 100

          # Follow -- Tested
          # if (proximity_left > 20 or proximity_right > 20):
          #   wheel_left = proximity_left *10
          #   wheel_right = proximity_right *10
          # # Line Follow
          if left_detection == True and right_detection == False:
            wheel_left = 50 #turning left
            wheel_right = 10
          elif left_detection == False and right_detection == True:
            wheel_left = 10
            wheel_right = 50 #turning right
          else: # IDK what to do
            wheel_left = 50
            wheel_right = 50

          robot.set_wheel(0, wheel_left)
          robot.set_wheel(1, wheel_right)
          #############################################
          # END OF YOUR WORKING AREA!!!
          #############################################
    # stop robot activities, such as motion, LEDs and sound
    # clean up after exit button pressed
    if robot:
      robot.reset()
      time.sleep(0.1)
    return

class GUI(object):
  def __init__(self, root, robot_control):
    self.root = root
    self.robot_control = robot_control
    root.geometry('250x30')
    root.title('Hamster Control')

    b1 = tk.Button(root, text='Go')
    b1.pack(side='left')
    b1.bind('<Button-1>', self.startProg)

    b2 = tk.Button(root, text='Exit')
    b2.pack(side='left')
    b2.bind('<Button-1>', self.stopProg)
    return

  def startProg(self, event=None):
    self.robot_control.go = True
    return

  def stopProg(self, event=None):
    self.robot_control.done = True
    self.root.quit()  # close window
    return

#################################
# Don't change any code below!! #
#################################

def main():
    # instantiate COMM object
    gMaxRobotNum = 1; # max number of robots to control
    comm = RobotComm(gMaxRobotNum)
    comm.start()
    print 'Bluetooth starts'
    robotList = comm.robotList

    behaviors = RobotBehaviorThread(robotList)
    behaviors.start()

    frame = tk.Tk()
    GUI(frame, behaviors)
    frame.mainloop()

    comm.stop()
    comm.join()
    print("terminated!")

if __name__ == "__main__":
    sys.exit(main())
