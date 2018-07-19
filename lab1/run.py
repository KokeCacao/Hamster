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


    self.proximity_left = 0
    self.proximity_right = 0
    self.floor_left = 0
    self.floor_right = 0
    self.light = 0
    self.wheel_left = 0
    self.wheel_right = 0
    self.left_detection = 0
    self.right_detection = 0
    return

  def quad(self, robot):
    robot.set_wheel(0, 30)
    robot.set_wheel(1, 30)
    time.sleep(100) #run time
    robot.set_wheel(0, 0)
    time.sleep(100) #turn time
  def shy(self, robot):
    if (proximity_left > 10 or proximity_right > 10):
      self.wheel_left = -self.proximity_left *10
      self.wheel_right = -self.proximity_right *10

  def dance(self, robot):
    if self.proximity_left > 10: #too close
      self.wheel_left = -100
    else:
      self.wheel_left = 100
    if self.proximity_right > 10: #too close
      self.wheel_right = -100
    else:
      self.wheel_right = 100

  def follow(self, robot):
    if (self.proximity_left > 20 or self.proximity_right > 20):
        self.wheel_left = self.proximity_left *10
        self.wheel_right = self.proximity_right *10

  def line_follow(self, robot):
    if self.left_detection == False and self.right_detection == True:
      self.wheel_left = 10 #turning left
      self.wheel_right = 50
    elif self.left_detection == True and self.right_detection == False:
      self.wheel_left = 50
      self.wheel_right = 10 #turning right
    else: # IDK what to do
      self.wheel_left = 40
      self.wheel_right = 40

  def run(self):
    robot=None
    while not self.done:
      for robot in self.robotList:
        if robot and self.go:
          self.proximity_left = robot.get_proximity(0)
          self.proximity_right = robot.get_proximity(1)
          self.floor_left = robot.get_floor(0)
          self.floor_right = robot.get_floor(1)
          self.light = robot.get_light()
          self.wheel_left = 0
          self.wheel_right = 0
          self.left_detection = (self.floor_left > 50)
          self.right_detection = (self.floor_right > 50)
          #############################################
          # START OF YOUR WORKING AREA!!!
          #############################################
          self.shy(robot)

          robot.set_wheel(0, self.wheel_left)
          robot.set_wheel(1, self.wheel_right)
          #############################################
          # END OF YOUR WORKING AREA!!!
          #############################################
    # stop robot activities, such as motion, LEDs and sound
    # clean up after exit button pressed
    if robot:
      robot.reset()
      time.sleep(0.01)
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
