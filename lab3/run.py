'''
/* =======================================================================
   (c) 2015, Kre8 Technology, Inc.

   Name:          Robot Escape
   By:            Qin Chen
   Last Updated:  6/10/18

   PROPRIETARY and CONFIDENTIAL
   ========================================================================*/
'''
# This program shows how threads can be created using Thread class and your
# own functions. Another way of creating threads is subclass Thread and override
# run().
# 
import sys
sys.path.append('../')
import time  # sleep
import threading
import Tkinter as tk
import Queue
# noinspection PyUnresolvedReferences
from HamsterAPI.comm_ble import RobotComm

# logging.basicConfig(level=logging.DEBUG,format='(%(threadName)-10s) %(message)s',)

class Event(object):
    def __init__(self, event_type, event_data):
      self.type = event_type #string
      self.data = event_data #list of number or character depending on type

class BehaviorThreads(object):
    Threshold_border = 20   # if floor sensor reading falls equal or below this value, border is detected
    Threshold_obstacle = 40   # if prox sensor reading is equal or higher than this, obstacle is detected
    
    def __init__(self, robot_list):
        self.robot_list = robot_list
        self.go = False
        self.quit = False
        self.finished = False

        # events queues for communication between threads
        self.alert_q = Queue.Queue()  # has alert[x, y] (UI), free[], boarder[x, y] only for UI
        self.motion_q = Queue.Queue()  # has obstacle[x, y], free[], boarder[x, y]

        self.t_robot_listener = None     # thread handles
        self.t_motion_listener = None
        # start a watcher thread
        print("start detecting thread")
        temp_t_robot_listener = threading.Thread(name='t_robot_listener', target=self.robot_event_firer, args=(self.alert_q, self.motion_q))
        temp_t_robot_listener.daemon = True
        temp_t_robot_listener.start()
        self.t_robot_listener = temp_t_robot_listener

        ###################################
        # start a motion handler thread
        ###################################
        temp_t_motion_listener = threading.Thread(name='t_motion_listener', target=self.robot_motion_handler, args=(self.motion_q, ))
        temp_t_motion_listener.daemon = True
        temp_t_motion_listener.start()
        self.t_motion_listener = temp_t_motion_listener

        return

    ###################################
    # This function is called when border is detected
    ###################################
    def get_out(self, robot):
        self.finished = True
        robot.reset()

        for i in range(89):
            robot.set_musical_note(self, i)
            time.sleep(0.01)

    def avoid_obstacle(self, robot, prox_left, prox_right):
        distance_left = 50 - prox_left
        distance_right = 50 - prox_right

        if (distance_left > distance_right ):  # turn left
            robot.set_wheel(0, 0)
            robot.set_wheel(1, 30)
        else:  # turn right
            robot.set_wheel(0, 30)
            robot.set_wheel(1, 0)
        return

    # This function monitors the sensors
    def robot_event_firer(self, alert_q, motion_q):  # thread
        count = 0
        # logging.debug('starting...')
        print("start fire events")
        while (not self.quit) and (not self.finished):
            print("fire")
            for robot in self.robot_list:
                if self.go and robot:
                    prox_l = robot.get_proximity(0)
                    prox_r = robot.get_proximity(1)
                    line_l = robot.get_floor(0)
                    line_r = robot.get_floor(1)
                    if (prox_l > BehaviorThreads.Threshold_obstacle or prox_r > BehaviorThreads.Threshold_obstacle):
                        alert_event = Event("alert", [prox_l,prox_r])
                        alert_q.put(alert_event)
                        #logging.debug("alert event %s, %s, %s, %s", prox_l, prox_r, line_l, line_r)
	                    #time.sleep(0.01)
                        count += 1
	                    #update movement every 5 ticks
                        if (count % 5 == 0):
                            #logging.debug("obstacle detected, q2: %d %d" % (prox_l, prox_r))
                            obs_event = Event("obstacle", [prox_l, prox_r])
                            motion_q.put(obs_event)
                    else:
                        if (count > 0):
                        	# free event is created when robot goes from obstacle to no obstacle
                            # logging.debug("free of obstacle")
                            free_event = Event("free",[])
                            motion_q.put(free_event)  # put event in motion queue
                            alert_q.put(free_event)  # put event in alert queue
                            count = 0
                    if (line_l < BehaviorThreads.Threshold_border or line_r < BehaviorThreads.Threshold_border):
	                    #logging.debug("border detected: %d %d" % (line_l, line_r))
                        border_event = Event("border", [line_l, line_r])
                        alert_q.put(border_event)
                        motion_q.put(border_event)
                    
                else:
                    print 'waiting ...'
            time.sleep(0.01)	# delay to give alert thread more processing time. Otherwise, it doesn't seem to have a chance to serve 'free' event
        return

    ##############################################################
    # Implement your motion handler. You need to get event using the passed-in queue handle and
    # decide what Hamster should do. Hamster needs to avoid obstacle while escaping. Hamster
    # stops moving after getting out of the border and remember to flush the motion queue after getting out.
    #############################################################
    def robot_motion_handler(self, motion_q):  # thread
        # obstacle[x, y], free[], boarder[x, y]

        print "debug: getting data from robot_motion_handler"

        event = motion_q.get()
        type = event.type()
        data = event.data()

        while (not self.quit) and (not self.finished):
            print("detected package")
            if type == "obstacle":
                for robot in self.robot_list:
                    if self.go and robot:
                        self.avoid_obstacle(robot, data[0], data[1])
            elif type == "free":
                pass
            elif type == "boarder":
                for robot in self.robot_list:
                    if self.go and robot:
                        self.get_out(robot)
                        with self.motion_q.mutex: self.motion_q.queue.clear()
            time.sleep(0.01)

class GUI(object):
    def __init__(self, root, threads_handle):
        self.root = root
        self.t_handle = threads_handle
        self.event_q = threads_handle.alert_q
        # self.t_alert_handler = None

        # visualization id
        self.canvas = None
        self.exit = None
        self.start = None
        self.prox_l_id = None
        self.prox_r_id = None
        self.canvas_robot_id = None
        self.canvas_proxl_id = None
        self.canvas_proxr_id = None

        self.initUI()

    ##########################################################
    # 1. Create a canvas widget and three canvas items: a square, and two lines 
    # representing prox sensor readings.
    # 2. Create two button widgets, for start and exit.
    # // 3. Create a thread for alert handler, which is responsible for displaying prox sensors.
    ##########################################################
    def initUI(self):
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

        # init everything
        self.root.title("Hamster")
        self.root.geometry("1280x720+0+0")
        self.prox_l_id = tk.Label(self.root, text="ProxLeft: N/A")
        self.prox_l_id.pack()
        self.prox_r_id = tk.Label(self.root, text="ProxRight: N/A")
        self.prox_r_id.pack()
        self.canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height, bg="white")
        self.canvas_robot_id = self.canvas.create_rectangle(robot_x1, robot_y1, robot_x2, robot_y2, fill="gold")
        self.canvas_proxl_id = self.canvas.create_line(prox_l_x, prox_l_y, prox_l_x, prox_l_y, fill="black", width=4)
        self.canvas_proxr_id = self.canvas.create_line(prox_r_x, prox_r_y, prox_r_x, prox_r_y, fill="black", width=4)
        self.canvas.pack()

        print "debug:startRobot()"
        self.start = tk.Button(self.root, text='Start', command= lambda: self.startRobot())
        self.start.pack(side='left')
        print "debug:stopRobot()"
        self.exit = tk.Button(self.root, text='Exit', command= lambda: self.stopProg())
        self.exit.pack(side='left')

    def startRobot(self, event=None):
        self.t_handle.go = True
        return

    def stopProg(self, event=None):
        self.t_handle.quit = True
        
        for robot in self.t_handle.robot_list:
            robot.reset()
        
        self.t_handle.t_motion_listener.join()
        self.t_handle.t_robot_listener.join()
        # self.t_alert_handler.join()
        self.root.quit()	# close GUI window

    ###################################################
    # Handles prox sensor display and warning(sound).
    # Query event queue(using passed-in queue handle).
    # If there is an "alert" event, display red beams.
    # Erase the beams when "free" event is in queue.
    # This runs in the main GUI thread. Remember to schedule
    # a callback of itself after 50 milliseconds.
    ###################################################
    def robot_alert_handler(self, alert_q):
        print "debug: getting data from robot_alert_handler"
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

        event = alert_q.get()
        type = event.type
        data = event.data
        if type == "alert":
            # display red beams
            self.canvas.coords(self.canvas_proxl_id, prox_l_x, prox_l_y, prox_l_x, prox_l_y - (50-data[0]))
            self.canvas.coords(self.canvas_proxr_id, prox_r_x, prox_r_y, prox_r_x, prox_r_y - (50-data[1]))
        elif type == "free":
            # erase the beams
            self.canvas.coords(self.canvas_proxl_id, prox_l_x, prox_l_y, prox_l_x, 0)
            self.canvas.coords(self.canvas_proxr_id, prox_r_x, prox_r_y, prox_r_x, 0)

        print "after 50"
        self.root.after(50, self.robot_alert_handler)
        

def main():
    max_robot_num = 1   # max number of robots to control
    comm = RobotComm(max_robot_num)
    comm.start()
    print 'Bluetooth starts'
    robotList = comm.robotList

    root = tk.Tk()
    t_handle = BehaviorThreads(robotList)
    gui = GUI(root, t_handle)
  
    root.mainloop()

    comm.stop()
    comm.join()

if __name__== "__main__":
  sys.exit(main())
  