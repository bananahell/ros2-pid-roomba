#include <functional>
#include <memory>

#include "nav_msgs/msg/odometry.hpp"
#include "rclcpp/rclcpp.hpp"

class Roomba : public rclcpp::Node {
 public:
  Roomba() : Node("roomba_cpp") {
    subscription_ = this->create_subscription<nav_msgs::msg::Odometry>(
        "/odom", 10,
        std::bind(&Roomba::odom_callback, this, std::placeholders::_1));
    this->isDone = false;
  }

 private:
  bool isDone;
  rclcpp::Subscription<nav_msgs::msg::Odometry>::SharedPtr subscription_;
  void odom_callback(const nav_msgs::msg::Odometry& msg) {
    if (!this->isDone) {
      RCLCPP_INFO_STREAM(this->get_logger(), msg.pose.pose.position.x);
      this->isDone = true;
    }
  }
};

int main(int argc, char* argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<Roomba>());
  rclcpp::shutdown();
  return 0;
}
