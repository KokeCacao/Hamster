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
# from HamsterAPI.comm_ble import RobotComm  # no dongle
# noinspection PyUnresolvedReferences
from HamsterAPI.comm_usb import RobotComm # yes dongle

################################
# Hamster control
################################
class RobotBehaviorThread(threading.Thread):
  def __init__(self, robotList):
    super(RobotBehaviorThread, self).__init__()
    self.go = False
    self.done = False
    self.robotList = robotList

    self.task = -1
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

  def square(self, robot):
    # self.wheel_left = 50
    # self.wheel_right = 50
    # robot.set_wheel(0, self.wheel_left)
    # robot.set_wheel(1, self.wheel_right)
    # time.sleep(2)
    #
    # self.wheel_left = 50
    # self.wheel_right = 0
    # robot.set_wheel(0, self.wheel_left)
    # robot.set_wheel(1, self.wheel_right)
    #
    # self.wheel_left = -50
    # self.wheel_right = 50
    # robot.set_wheel(0, self.wheel_left)
    # robot.set_wheel(1, self.wheel_right)
    # time.sleep(0.29850746268656716417910447761194 *2) # 25 circle + 45 degree = 9045 degree. sleep(1)=150.75 degree, 45 degree = 0.29850746268656716417910447761194
    # self.wheel_left = 0
    # self.wheel_right = 0
    # robot.set_wheel(0, self.wheel_left)
    # robot.set_wheel(1, self.wheel_right)
    # time.sleep(10)

    time.sleep(0.5 * (90/35)) #turn time, 0.5=35 degree with 50,0 as speed
  def shy(self, robot):
    if (self.proximity_left > 10 or self.proximity_right > 10):
      self.wheel_left = -self.proximity_left *10
      self.wheel_right = -self.proximity_right *10

  def dance(self, robot):
    # if self.proximity_left > 10: #too close
    #   self.wheel_left = -50
    # elif self.proximity_left < 5:
    #   self.wheel_left = 0
    # else:
    #   self.wheel_left = 50
    # if self.proximity_right > 10: #too close
    #   self.wheel_right = -50
    # elif self.proximity_right < 5:
    #   self.wheel_right = 0
    # else:
    #   self.wheel_right = 50
    distance = 50 - self.proximity_left
    if distance > 45:
      self.wheel_left = 50
      self.wheel_right = 50
    elif distance > 25 and distance < 45: # too far
      self.wheel_left = 50
      self.wheel_right = 50
      # robot.set_musical_note(80)
      time.sleep(0.2)
      self.wheel_left = 0
      self.wheel_right = 0
      time.sleep(0)
      robot.set_musical_note(0)
    elif distance > 1 and distance < 25: # too close
      self.wheel_left = -50
      self.wheel_right = -50
      # robot.set_musical_note(88)
      time.sleep(0.2)
      self.wheel_left = 0
      self.wheel_right = 0
      time.sleep(0)
      robot.set_musical_note(0)

    # if self.proximity_left > 20 and self.proximity_left < 48: # too close
    # elif self.proximity_left < 10:  # too far
    # elif self.proximity_left < 48:
    #   self.wheel_left = 50
    #   self.wheel_right = 50
    # else:
    #   robot.set_musical_note(0)
    #   self.wheel_left = 50
    #   self.wheel_right = 50

  def follow(self, robot):
    if (self.proximity_left > 20 or self.proximity_right > 20):
        self.wheel_right = self.proximity_left *10
        self.wheel_left = self.proximity_right *10

  def line_follow(self, robot):
    if self.left_detection == False and self.right_detection == True:
      self.wheel_left = 0 #turning left
      self.wheel_right = 50
    elif self.left_detection == True and self.right_detection == False:
      self.wheel_left = 50
      self.wheel_right = 0 #turning right
    else: # IDK what to do
      self.wheel_left = 20
      self.wheel_right = 20

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
          if self.task == 0: self.square(robot)
          if self.task == 1: self.shy(robot)
          if self.task == 2: self.dance(robot)
          if self.task == 3: self.follow(robot)
          if self.task == 4: self.line_follow(robot)
          # switch={
          # -1: self.dance(robot),
          # 0: self.square(robot),
          # 1: self.shy(robot),
          # 2: self.dance(robot),
          # 3: self.follow(robot),
          # 4: self.line_follow(robot)
          # }
          # # self.shy(robot)
          # # self.square(robot)
          # if self.task != -1:
          #   switch[self.task](robot)

          robot.set_wheel(0, self.wheel_left)
          robot.set_wheel(1, self.wheel_right)
          #############################################
          # END OF YOUR WORKING AREA!!!
          #############################################
    # stop robot activities, such as motion, LEDs and sound
    # clean up after exit button pressed
    if robot:
      robot.reset()
      time.sleep(0.001)
    return

class GUI(object):
  def __init__(self, root, robot_control):
    self.root = root
    self.robot_control = robot_control
    root.geometry('500x30')
    root.title('Hamster Control')

    b1 = tk.Button(root, text='Go')
    b1.pack(side='left')
    b1.bind('<Button-1>', self.startProg)

    b2 = tk.Button(root, text='Square')
    b2.pack(side='left')
    b2.bind('<Button-1>', self.task0)

    b3 = tk.Button(root, text='Shy')
    b3.pack(side='left')
    b3.bind('<Button-1>', self.task1)

    b4 = tk.Button(root, text='Dance')
    b4.pack(side='left')
    b4.bind('<Button-1>', self.task2)

    b5 = tk.Button(root, text='Follow')
    b5.pack(side='left')
    b5.bind('<Button-1>', self.task3)

    b6 = tk.Button(root, text='FollowLine')
    b6.pack(side='left')
    b6.bind('<Button-1>', self.task4)

    b7 = tk.Button(root, text='Exit')
    b7.pack(side='left')
    b7.bind('<Button-1>', self.stopProg)
    return

  def startProg(self, event=None):
    self.robot_control.go = True
    return

  def task0(self, event=None):
    self.robot_control.go = True
    self.robot_control.task = 0
    return
  def task1(self, event=None):
    self.robot_control.go = True
    self.robot_control.task = 1
    return
  def task2(self, event=None):
    self.robot_control.go = True
    self.robot_control.task = 2
    return
  def task3(self, event=None):
    self.robot_control.go = True
    self.robot_control.task = 3
    return
  def task4(self, event=None):
    self.robot_control.go = True
    self.robot_control.task = 4
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
    gMaxRobotNum = 1 # max number of robots to control
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
