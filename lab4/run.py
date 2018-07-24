'''
/* =======================================================================
   (c) 2015, Kre8 Technology, Inc.
   Stater program of 3-state obstacle avoidance using FSM.

   Name:          starter_tk_3state_avoid.py
   By:            Qin Chen
   Last Updated:  6/10/18

   PROPRIETARY and CONFIDENTIAL
   ========================================================================*/
'''
import sys
import time
import threading
import Tkinter as tk
# import Queue
from collections import deque
# noinspection PyUnresolvedReferences
# from HamsterAPI.comm_ble import RobotComm  # no dongle
from HamsterAPI.comm_usb import RobotComm  # yes dongle


class Event(object):
    def __init__(self, event_type, floor_left, floor_right, distance_left, distance_right):
        self.event_type = event_type
        self.floor_left = floor_left
        self.floor_right = floor_right
        self.distance_left = distance_left
        self.distance_right = distance_right

    def get_floor_left(self):
        return self.floor_left
    def get_floor_right(self):
        return self.floor_right
    def get_distance_left(self):
        return self.distance_left
    def get_distance_right(self):
        return self.distance_right
    def get_event_type(self):
        return self.event_type


##############################
# Finite state machine engine
##############################
class StateMachine(object):
    def __init__(self, name, eventQ_handle):
        self.name = name  # machine name
        self.states = []  # list of lists, [[state name, event, transition, next_state],...]
        self.start_state = None
        self.end_states = []  # list of name strings
        self.q = eventQ_handle
        return

    def set_start_state(self, state_name):
        self.start_state = state_name
        return

    def get_start_state(self):
        return self.start_state

    def add_end_state(self, state_name):
        self.end_states.append(state_name)
        return

    def add_state(self, state, event, callback, next_state):
        self.states.append([state, event, callback, next_state])  # append to list
        return

    # you must set start state before calling run()
    def run(self):
        current_state = self.start_state
        # while not self.q.empty(): # for a machine that has end states
        while True:
            if current_state in self.end_states:
                break
            if self.q:
                e = self.q.pop()
                print "pop"
                for c in self.states:
                    if c[0] == current_state and c[1] == e.event_type:
                        c[2]()  # invoke callback function
                        current_state = c[3]  # next state
                        break  # get out of inner for-loop
            time.sleep(0.001)
        return


################################
# Hamster control
################################
class RobotBehavior(object):
    def __init__(self, robot_list):
        # set by GUI button
        self.done = False
        self.go = False

        # setup robot
        self.robot_list = robot_list
        self.robot = None

        # count number
        self.number_of_finished = 0

        # init queue
        self.q = deque()
        self.spawn_threads()
        return

    def spawn_threads(self):
        ###########################################################
        # Two threads are created here.
        # 1. create a watcher thread that reads sensors and registers events: obstacle on left, right or no obstacle. This
        # 	thread runs the method event_watcher() you are going to implement below.
        # 2. Instantiate StateMachine and populate it with avoidance states, triggers, etc. Set start state.
        # 3. Create a thread to run FSM engine.
        ###########################################################

        sm = StateMachine('State Machine', self.q)

        # input: line_left, line_right, line_no, obj_no, obj_front, obj_left, obj_left
        # states: AvoidLeft, AvoidRight, TurningLeft, TurningRight, MovingForward, FinalTouch, MovingObj
        sm.add_state('MovingForward', 'line_left', self.avoid_left, 'AvoidLeft')
        sm.add_state('MovingForward', 'line_right', self.avoid_right, 'AvoidRight')
        sm.add_state('MovingForward', 'line_both', self.avoid_both, 'MovingForward')
        sm.add_state('MovingForward', 'line_no', self.avoid_right, 'MovingForward')
        sm.add_state('MovingForward', 'obj_left', self.turning_left_first_time, 'TurningLeft')
        sm.add_state('MovingForward', 'obj_right', self.turning_right_first_time, 'TurningRight')
        sm.add_state('MovingForward', 'obj_no', self.moving_forward, 'MovingForward')
        sm.add_state('MovingForward', 'obj_front', self.moving_object_first_time, 'MovingObj')
        sm.add_state('MovingForward', 'finish_final', self.throw_error, 'MovingForward')

        # only care about line
        sm.add_state('AvoidLeft', 'line_left', self.avoid_left, 'AvoidLeft')
        sm.add_state('AvoidLeft', 'line_right', self.avoid_left, 'AvoidLeft')
        sm.add_state('AvoidLeft', 'line_no', self.avoid_left, 'MovingForward')
        sm.add_state('AvoidLeft', 'line_both', self.avoid_both, 'MovingForward')
        sm.add_state('AvoidLeft', 'obj_left', self.avoid_left, 'AvoidLeft')
        sm.add_state('AvoidLeft', 'obj_right', self.avoid_left, 'AvoidLeft')
        sm.add_state('AvoidLeft', 'obj_no', self.moving_forward, 'MovingForward')  # avoid successfully
        sm.add_state('AvoidLeft', 'obj_front', self.moving_object_first_time, 'MovingObj')
        sm.add_state('AvoidLeft', 'finish_final', self.throw_error, 'AvoidLeft')

        # only care about line
        sm.add_state('AvoidRight', 'line_left', self.avoid_right, 'AvoidRight')
        sm.add_state('AvoidRight', 'line_right', self.avoid_right, 'AvoidRight')
        sm.add_state('AvoidRight', 'line_no', self.moving_forward, 'MovingForward')
        sm.add_state('AvoidRight', 'line_both', self.avoid_both, 'MovingForward')
        sm.add_state('AvoidRight', 'obj_left', self.avoid_right, 'AvoidRight')
        sm.add_state('AvoidRight', 'obj_right', self.avoid_right, 'AvoidRight')
        sm.add_state('AvoidRight', 'obj_no', self.moving_forward, 'MovingForward')  # avoid successfully
        sm.add_state('AvoidRight', 'obj_front', self.moving_object_first_time, 'MovingObj')
        sm.add_state('AvoidRight', 'finish_final', self.throw_error, 'AvoidRight')
        # No FinalTouch

        sm.add_state('TurningLeft', 'line_left', self.final_touching, 'FinalTouch')
        sm.add_state('TurningLeft', 'line_right', self.final_touching, 'FinalTouch')
        sm.add_state('TurningLeft', 'line_no', self.turning_left, 'TurningLeft')
        sm.add_state('TurningLeft', 'line_both', self.final_touching, 'FinalTouch')
        sm.add_state('TurningLeft', 'obj_left', self.turning_left, 'TurningLeft')
        sm.add_state('TurningLeft', 'obj_right', self.moving_object, 'MovingObj')
        # there is no way I can lose the object, sensor must be too close
        sm.add_state('TurningLeft', 'obj_no', self.moving_object, 'MovingObj')
        sm.add_state('TurningLeft', 'obj_front', self.moving_object, 'MovingObj')
        sm.add_state('TurningLeft', 'finish_final', self.throw_error, 'TurningLeft')

        sm.add_state('TurningRight', 'line_left', self.final_touching, 'FinalTouch')
        sm.add_state('TurningRight', 'line_right', self.final_touching, 'FinalTouch')
        sm.add_state('TurningRight', 'line_no', self.turning_right, 'TurningRight')
        sm.add_state('TurningRight', 'line_both', self.final_touching, 'FinalTouch')
        sm.add_state('TurningRight', 'obj_left', self.moving_object, 'MovingObj')
        sm.add_state('TurningRight', 'obj_right', self.turning_right, 'TurningRight')
        # there is no way I can lose the object, sensor must be too close
        sm.add_state('TurningRight', 'obj_no', self.moving_object, 'MovingObj')
        sm.add_state('TurningRight', 'obj_front', self.moving_object, 'MovingObj')
        sm.add_state('TurningRight', 'finish_final', self.throw_error, 'TurningRight')

        sm.add_state('MovingObj', 'line_left', self.final_touching, 'FinalTouch')
        sm.add_state('MovingObj', 'line_right', self.final_touching, 'FinalTouch')
        sm.add_state('MovingObj', 'line_no', self.moving_object, 'MovingObj')
        sm.add_state('MovingObj', 'line_both', self.final_touching, 'FinalTouch')
        sm.add_state('MovingObj', 'obj_left', self.turning_left, 'TurningLeft')
        sm.add_state('MovingObj', 'obj_right', self.turning_right, 'TurningRight')
        # there is no way I can lose the object, sensor must be too close
        sm.add_state('MovingObj', 'obj_no', self.moving_object, 'MovingObj')
        sm.add_state('MovingObj', 'obj_front', self.moving_object, 'MovingObj')
        sm.add_state('MovingObj', 'finish_final', self.moving_object, 'MovingObj')

        sm.add_state('FinalTouch', 'line_left', self.waiting, 'FinalTouch')
        sm.add_state('FinalTouch', 'line_right', self.waiting, 'FinalTouch')
        sm.add_state('FinalTouch', 'line_no', self.waiting, 'FinalTouch')
        sm.add_state('FinalTouch', 'line_both', self.waiting, 'FinalTouch')
        sm.add_state('FinalTouch', 'obj_left', self.waiting, 'FinalTouch')
        sm.add_state('FinalTouch', 'obj_right', self.waiting, 'FinalTouch')
        sm.add_state('FinalTouch', 'obj_no', self.waiting, 'FinalTouch')
        sm.add_state('FinalTouch', 'obj_front', self.waiting, 'FinalTouch')
        sm.add_state('FinalTouch', 'finish_final', self.moving_forward, 'MovingForward')

        sm.set_start_state('MovingForward')  # this must be done before starting machine

        # start the first command!
        sensor_thread = threading.Thread(name='Sensor Thread', target=self.event_watcher)
        sensor_thread.daemon = True
        sensor_thread.start()
        state_thread = threading.Thread(name='State Thread', target=sm.run)
        state_thread.daemon = True
        state_thread.start()

    def event_watcher(self):
        print "start watching"
        while not self.done:
            if self.robot_list and self.go:
                self.robot = self.robot_list[0]

                ###########################################################
                # Implement event producer here. The events are obstacle on left, right or no obstacle. Design your
                # logic for what event gets created based on sensor readings.
                ###########################################################

                # get sensor
                floor_left = self.robot.get_floor(0)
                floor_right = self.robot.get_floor(1)
                distance_left = 50 - self.robot.get_proximity(0)
                distance_right = 50 - self.robot.get_proximity(1)

                # constance
                distance_difference_threshold = 20
                distance_pushing_threshold = 10
                floor_threshold = 50
                sleep_time = 0.01


                # distance flow
                if abs(distance_left - distance_right) < distance_difference_threshold:
                    # self.moving_forward()
                    if distance_left > distance_pushing_threshold and distance_right > distance_pushing_threshold:
                        event = Event("obj_no", floor_left, floor_right, distance_left, distance_right)
                        self.q.append(event)
                        print "send obj_no, but maybe it is infront"
                    elif distance_left < distance_pushing_threshold and distance_right < distance_pushing_threshold:
                        event = Event("obj_front", floor_left, floor_right, distance_left, distance_right)
                        self.q.append(event)
                        print "send obj_front"
                else:
                    if distance_left > distance_right:
                        # self.turning_right()
                        event = Event("obj_right", floor_left, floor_right, distance_left, distance_right)
                        self.q.append(event)
                        print "send obj_right"
                    else:
                        # self.turning_left()
                        event = Event("obj_left", floor_left, floor_right, distance_left, distance_right)
                        self.q.append(event)
                        print "send obj_left"


                # line flow
                if floor_left < floor_threshold and not floor_right < floor_threshold:
                    event = Event("line_left", floor_left, floor_right, distance_left, distance_right)
                    self.q.append(event)
                    print "send line_left"
                if floor_right < floor_threshold and not floor_left < floor_threshold:
                    event = Event("line_right", floor_left, floor_right, distance_left, distance_right)
                    self.q.append(event)
                    print "send line_right"

                if floor_right < floor_threshold and floor_left < floor_threshold:
                    event = Event("line_both", floor_left, floor_right, distance_left, distance_right)
                    self.q.append(event)
                    print "send line_both"
                time.sleep(sleep_time)
        return

    #######################################
    # Implement Hamster movements to avoid obstacle
    #######################################
    def turning_left(self):
        print "TURNING: left"
        if not self.done:
            if self.robot_list and self.go:
                self.robot = self.robot_list[0]
                self.robot.set_wheel(0,-10)  # + speed
                self.robot.set_wheel(1,30)  # + speed
    def turning_left_first_time(self):
        print "TURNING: left"
        if not self.done:
            if self.robot_list and self.go:
                self.robot = self.robot_list[0]

                music_thread = threading.Thread(name='Music Thread', target=self.music_node)
                music_thread.daemon = True
                music_thread.start()

                self.robot.set_wheel(0,-10)  # + speed
                self.robot.set_wheel(1,30)  # + speed
    def turning_right(self):
        print "TURNING: right"
        if not self.done:
            if self.robot_list and self.go:
                self.robot = self.robot_list[0]
                self.robot.set_wheel(0,30)  # + speed
                self.robot.set_wheel(1,-10)  # + speed
    def turning_right_first_time(self):
        print "TURNING: right first time"
        if not self.done:
            if self.robot_list and self.go:
                self.robot = self.robot_list[0]

                music_thread = threading.Thread(name='Music Thread', target=self.music_node)
                music_thread.daemon = True
                music_thread.start()

                self.robot.set_wheel(0,30)  # + speed
                self.robot.set_wheel(1,-10)  # + speed
    def avoid_left(self):
        print "AVOID: right"
        if not self.done:
            if self.robot_list and self.go:
                self.robot = self.robot_list[0]
                self.robot.set_wheel(0,20)
                self.robot.set_wheel(1,-20)
                time.sleep(0.1)
                self.q.clear()
    def avoid_right(self):
        print "AVOID: left"
        if not self.done:
            if self.robot_list and self.go:
                self.robot = self.robot_list[0]
                self.robot.set_wheel(0,-20)
                self.robot.set_wheel(1,20)
                time.sleep(0.1)
                self.q.clear()
    def avoid_both(self):
        print "AVOID: both"
        if not self.done:
            if self.robot_list and self.go:
                self.robot = self.robot_list[0]
                self.robot.set_wheel(0,-20)
                self.robot.set_wheel(1,-20)
                time.sleep(0.2)
                self.q.clear()
                self.robot.set_wheel(0,-100)
                self.robot.set_wheel(1,100)
                time.sleep(0.5)
                self.q.clear()
    def moving_forward(self):
        print "MOVING: forward"
        if not self.done:
            if self.robot_list and self.go:
                self.robot = self.robot_list[0]
                self.robot.set_wheel(0,20)
                self.robot.set_wheel(1,20)
    def moving_object(self):
        print "MOVING: object"
        if not self.done:
            if self.robot_list and self.go:
                self.robot = self.robot_list[0]
                self.robot.set_wheel(0,40)
                self.robot.set_wheel(1,40)
    def moving_object_first_time(self):
        print "MOVING: object first time"
        if not self.done:
            if self.robot_list and self.go:
                self.robot = self.robot_list[0]

                music_thread = threading.Thread(name='Music Thread', target=self.music_node)
                music_thread.daemon = True
                music_thread.start()

                self.robot.set_wheel(0,40)
                self.robot.set_wheel(1,40)
    def music_node(self):
        if not self.done:
            if self.robot_list and self.go:
                self.robot.set_musical_note(80)
                time.sleep(2)
                self.robot.set_musical_note(0)

    def final_touching(self):
        print "FINISH TOUCH"
        if not self.done:
            if self.robot_list and self.go:
                self.number_of_finished = self.number_of_finished + 1

                self.robot = self.robot_list[0]
                self.robot.set_wheel(0,100)
                self.robot.set_wheel(1,100)
                time.sleep(1)
                self.q.clear()
                self.robot.set_wheel(0,-100)
                self.robot.set_wheel(1,-100)
                time.sleep(1)
                self.q.clear()
                self.robot.set_wheel(0,0)
                self.robot.set_wheel(1,0)
                # making sound
                for i in range(self.number_of_finished):
                    self.robot.set_musical_note(40 + i)
                    time.sleep(0.2)
                    self.q.clear()
                    self.robot.set_musical_note(0)
                    time.sleep(0.2)
                    self.q.clear()
                self.avoid_both()
                event = Event("finish_final", None, None, None, None)
                self.q.append(event)
    def waiting(self):
        print "waiting"
    def throw_error(self):
        print "ERROR"


class GUI(object):
    def __init__(self, root, robot_control):
        self.root = root
        self.robot_control = robot_control

        canvas = tk.Canvas(root, bg="white", width=300, height=250)
        canvas.pack(expand=1, fill='both')
        canvas.create_rectangle(175, 175, 125, 125, fill="green")

        b1 = tk.Button(root, text='Go')
        b1.pack()
        b1.bind('<Button-1>', self.startProg)

        b2 = tk.Button(root, text='Exit')
        b2.pack()
        b2.bind('<Button-1>', self.stopProg)
        return

    def startProg(self, event=None):
        self.robot_control.go = True
        return
    def stopProg(self, event=None):
        self.robot_control.done = True
        self.root.quit()  # close window
        return


def main():
    gMaxRobotNum = 1  # max number of robots to control
    comm = RobotComm(gMaxRobotNum)
    comm.start()
    print 'Bluetooth starts'

    robot_list = comm.robotList
    behaviors = RobotBehavior(robot_list)

    frame = tk.Tk()
    GUI(frame, behaviors)
    frame.mainloop()

    comm.stop()
    comm.join()
    return


if __name__ == "__main__":
    sys.exit(main())
