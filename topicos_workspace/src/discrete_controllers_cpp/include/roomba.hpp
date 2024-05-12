#include <nav_msgs/msg/odometry.hpp>
#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/laser_scan.hpp>

class Roomba : public rclcpp::Node {
 public:
  Roomba();

 private:
  int isDone;
  rclcpp::Subscription<nav_msgs::msg::Odometry>::SharedPtr odomSubscription;
  rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr
      laserSubscription;
  void odom_callback(const nav_msgs::msg::Odometry&);
  void scan_callback(const sensor_msgs::msg::LaserScan&);
};
