import PyLidar3
import time # Time module
import Motor_Funcs

forward_angle = 0
backward_angle = 180 + forward_angle
right_angle = forward_angle + 270
left_angle = forward_angle + 90
forward_right_angle = forward_angle + (360-45)
forward_left_angle = forward_angle + 45

#Serial port to which lidar connected, Get it from device manager windows
#In linux type in terminal -- ls /dev/tty*
def test_lidar():
    port = input("Enter port name which lidar is connected:") #windows
    #port = "/dev/ttyUSB0" #linux
    Obj = PyLidar3.YdLidarX4(port) #PyLidar3.your_version_of_lidar(port,chunk_size)
    if(Obj.Connect()):
        print(Obj.GetDeviceInfo())
        gen = Obj.StartScanning()
        t = time.time() # start time

        state = "Forward"
        while (time.time() - t) < 30: #scan for 30 seconds
            data = next(gen)
            Stage_1(data)

            #state = Stage_2(data, state)

            #state = Stage_3(data, state)

            time.sleep(0.5)
        Obj.StopScanning()
        Obj.Disconnect()
    else:
        print("Error connecting to device")

def Stage_1(data):
    """
    Stage 1 testing:
    desc: will hug the front wall
    """
    forward_dist = data[forward_angle]  # distance between lidar and front wall. if this doesn't work, make it 90
    backward_dist = data[backward_angle]  # distance between lidar and back wall. if this doesn't work, make it 270
    if forward_dist < .5:  # if we are closer than .5 meters to a wall
        print("front wall is close")
        Motor_Funcs.motor_backward()  # tell the wheels to go backward
    elif backward_dist < .5:
        print("back wall is close")
        Motor_Funcs.motor_forward()
    else:
        print("both walls are far")
        Motor_Funcs.motor_forward()

    """
    End Stage 1:
    """

def Stage_2(data, prev_state):

    forward_dist = data[forward_angle]  # distance between lidar and front wall. if this doesn't work, make it 90
    backward_dist = data[backward_angle]  # distance between lidar and back wall. if this doesn't work, make it 270

    """
    Start Stage 2:
    desc: will touch wall to wall in a hallway
    """

    state = "Forward"
    if forward_dist < .5:  # if we are closer than .5 meters to a wall
        print("front wall is close")
        state = "Backward"
        Motor_Funcs.motor_backward()  # tell the wheels to go backward

    elif backward_dist < .5:
        print("back wall is close")
        Motor_Funcs.motor_forward()
        state = "Forward"
    else:
        print("both walls are far")
        if prev_state == "Forward":
            Motor_Funcs.motor_forward()
        else:
            Motor_Funcs.motor_backward()
    """
    End Stage 2:
    """
    return state

def Stage_3(data, prev_state):

    forward_dist = data[forward_angle]  # distance between lidar and front wall. if this doesn't work, make it 90
    backward_dist = data[backward_angle]  # distance between lidar and back wall. if this doesn't work, make it 270

    min_forward_dist = 999999
    for angle in range(forward_angle, (forward_angle + 10) % 360):
        dist = data[angle]
        if dist < min_forward_dist:
            min_forward_dist = dist

    for angle in range((forward_angle + 359) % 360, (forward_angle + 359 - 10) % 360):
        dist = data[angle]
        if dist < min_forward_dist:
            min_forward_dist = dist

    min_backward_dist = 999999
    for angle in range(backward_angle, (backward_angle + 10) % 360):
        dist = data[angle]
        if dist < min_backward_dist:
            min_backward_dist = dist

    for angle in range((backward_angle + 359) % 360, (forward_angle + 359 - 10) % 360):
        dist = data[angle]
        if dist < min_backward_dist:
            min_backward_dist = dist

    """
    Start Stage 3:
    desc: Will check within 20 degrees backwards and forwards
    """

    state = "Forward"
    if min_forward_dist < .5:  # if we are closer than .5 meters to a wall
        print("front wall is close")
        state = "Backward"
        Motor_Funcs.motor_backward()  # tell the wheels to go backward

    elif min_backward_dist < .5:
        print("back wall is close")
        Motor_Funcs.motor_forward()
        state = "Forward"
    else:
        print("both walls are far")
        if prev_state == "Forward":
            Motor_Funcs.motor_forward()
        else:
            Motor_Funcs.motor_backward()
    """
    End Stage 3:
    """
    return state