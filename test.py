import os

from servo import servo

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
    
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

from scservo_sdk import *                    # Uses SCServo SDK library

# Default setting
BAUDRATE                    = 500000           
DEVICENAME                  = 'COM5'   
protocol_end                = 0           # SCServo bit end(STS/SMS=0, SCS=1)

index = 0
goal_position = [0, 4095]         # Goal position

portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(protocol_end)

portHandler.openPort()
portHandler.setBaudRate(BAUDRATE)

servo1 = servo(1,packetHandler,portHandler)
servo2 = servo(2,packetHandler,portHandler)

    
while 1:
    print("Press any key to continue! (or press ESC to quit!)")
    if getch() == chr(0x1b):
        break

    servo1.set_target_position(goal_position[index])
    servo2.set_target_position(goal_position[index])

    while 1:
        
        servo1.update()
        servo2.update()

        if servo1.reached_target_pos() and servo2.reached_target_pos():
            break

    # Change goal position
    if index == 0:
        index = 1
    else:
        index = 0    
