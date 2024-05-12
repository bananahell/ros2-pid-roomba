#include <nav_msgs/msg/odometry.hpp>
#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/laser_scan.hpp>

using namespace std;
using namespace rclcpp;
using namespace nav_msgs::msg;
using namespace sensor_msgs::msg;

class Roomba : public Node {
 public:
  Roomba() : Node("roomba_cpp") {
    odomSubscription = this->create_subscription<Odometry>(
        "/odom", 10, bind(&odom_callback, this, placeholders::_1));
    laserSubscription = this->create_subscription<LaserScan>(
        "/scan", 10, bind(&scan_callback, this, placeholders::_1));
    isDone = 0;
  }

 private:
  int isDone;

  Subscription<Odometry>::SharedPtr odomSubscription;

  Subscription<LaserScan>::SharedPtr laserSubscription;

  void odom_callback(const Odometry& msg) {
    if (isDone < 2) {
      RCLCPP_INFO_STREAM(this->get_logger(), msg.pose.pose.position.x);
      isDone++;
    }
  }

  void scan_callback(const LaserScan& msg) {
    if (isDone < 2) {
      RCLCPP_INFO_STREAM(this->get_logger(), msg.ranges[0]);
      isDone++;
    }
  }
};

int main(int argc, char* argv[]) {
  int a = 0;
  init(argc, argv);
  spin(make_shared<Roomba>());
  shutdown();
  return 0;
}
