from scservo_sdk import *

# Most of the functions has NOT been implemented yet.


# Address table
ADDR_SCS_TORQUE_ENABLE = 40
ADDR_SCS_GOAL_ACC = 41
ADDR_SCS_GOAL_POSITION = 42
ADDR_SCS_GOAL_SPEED = 46
ADDR_SCS_PRESENT_POSITION = 56

# Servo attribute.
SCS_MINIMUM_POSITION_VALUE = 0           # SCServo will rotate between this value
# and this value (note that the SCServo would not move when the position value is out of movable range. Check e-manual about the range of the SCServo you use.)
SCS_MAXIMUM_POSITION_VALUE = 4095
SCS_MOVING_STATUS_THRESHOLD = 20          # SCServo moving status threshold
SCS_MOVING_SPEED = 0           # SCServo moving speed
SCS_MOVING_ACC = 0           # SCServo moving acc
protocol_end = 0           # SCServo bit end(STS/SMS=0, SCS=1)


class servo:

    def __init__(self, ID, packet, port):
        self.ID = ID
        self.portHandler = port
        self.packetHandler = packet

        self.pos_set = 0
        self.present_position = 0
        self.present_speed = 0

    def set_target_position(self, pos):
        pos = min(pos, SCS_MAXIMUM_POSITION_VALUE)
        pos = max(SCS_MINIMUM_POSITION_VALUE, pos)
        self.target_position = pos

    def update(self):
        # update feedback
        present_position_speed, scs_comm_result, scs_error = self.packetHandler.read4ByteTxRx(
            self.portHandler, self.ID, ADDR_SCS_PRESENT_POSITION) #request feedback
        self.present_position = SCS_LOWORD(present_position_speed)
        self.present_speed = SCS_HIWORD(present_position_speed)
        
        # set position
        self.packetHandler.write2ByteTxRx(
            self.portHandler, self.ID, ADDR_SCS_GOAL_POSITION, self.target_position)
        print(self.present_position)

    def reached_target_pos(self):
        return abs(self.target_position - self.present_position) < SCS_MOVING_STATUS_THRESHOLD
