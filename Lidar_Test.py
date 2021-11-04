import PyLidar3
import time # Time module
import Motor_Funcs

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
        while (time.time() - t) < 30: #scan for 30 seconds
            data = next(gen)
            forward_dist = gen[0]   #distance between lidar and front wall. if this doesn't work, make it 90
            backward_dist = gen[180] #distance between lidar and back wall. if this doesn't work, make it 270
            if forward_dist < .5:  #if we are closer than .5 meters to a wall
                print("front wall is close")
                Motor_Funcs.motor_backward() #tell the wheels to go backward
            elif backward_dist < .5:
                print("back wall is close")
                Motor_Funcs.motor_forward()
            else:
                print("both walls are far")
                Motor_Funcs.motor_forward()
            time.sleep(0.5)
        Obj.StopScanning()
        Obj.Disconnect()
    else:
        print("Error connecting to device")