from enum import Enum
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist


class RoombaState(Enum):
  START = 0
  MOVING = 1
  TURNING = 2
  ERROR = 3


class Roomba(Node):

  odomMsg = None
  scanMsg = None

  def __init__(self):
    super().__init__('roomba_loop')
    self.subscription = self.create_subscription(
        Odometry, '/odom', self.odom_callback, 10)
    self.subscription = self.create_subscription(
        LaserScan, '/scan', self.scan_callback, 10)
    self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)

  def odom_callback(self, msg):
    self.odomMsg = msg

  def scan_callback(self, msg):
    self.scanMsg = msg

  def roomba_states(self, currentState, roombaNode, forwardIndexes, minForwardRange):
    forwardRanges = []
    for i in forwardIndexes:
      forwardRanges.append(self.scanMsg.ranges[i])
    match currentState:
      case RoombaState.START:
        print("MOVING - START")
        currentState = RoombaState.MOVING
      case RoombaState.MOVING:
        if (min(forwardRanges) > minForwardRange):
          self.roomba_twist(999.0, 0.0, roombaNode)
        else:
          print("TURNING - START")
          currentState = RoombaState.TURNING
      case RoombaState.TURNING:
        if (min(forwardRanges) < minForwardRange):
          self.roomba_twist(0.0, 999.0, roombaNode)
        else:
          print("MOVING - START")
          currentState = RoombaState.MOVING
      case RoombaState.ERROR:
        print("ERROR")
      case _:
        print("_")
    return currentState

  def roomba_twist(self, linear, angular, roombaNode):
    msg = Twist()
    msg.linear.x = linear
    msg.linear.y = 0.0
    msg.linear.z = 0.0
    msg.angular.x = 0.0
    msg.angular.y = 0.0
    msg.angular.z = angular
    roombaNode.publisher.publish(msg)

  def roomba_loop(self, roombaNode):
    minForwardRange = 1
    fovRange = 70
    exitRequest = False
    # TODO como calcular? =/// -scanMsg.angle_min/scanMsg.angle_increment
    forwardIndex = 160
    # TODO cagado, estatico, ta, mas 160 tambem ta estatico, entao fodas
    forwardIndexes = list(
        range(forwardIndex - fovRange, forwardIndex + fovRange))
    currentState = RoombaState.START
    print("MAIN LOOP - START")
    while (exitRequest != True):
      rclpy.spin_once(roombaNode)
      if (self.scanMsg != None and self.odomMsg != None):
        currentState = self.roomba_states(
            currentState, roombaNode, forwardIndexes, minForwardRange)


def main(args=None):
  rclpy.init(args=args)
  roombaNode = Roomba()
  roombaNode.roomba_loop(roombaNode)
  roombaNode.destroy_node()
  rclpy.shutdown()


if __name__ == '__main__':
  main()
