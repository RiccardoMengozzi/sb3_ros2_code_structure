from rclpy.node import Node
from std_msgs.msg import Int32
import rclpy

class Pub(Node):
    def __init__(self):
        super().__init__(node_name='ros_int')
        self.namespace = self.get_namespace()
        self.get_logger().info(f'[{self.namespace[1:]}] Publisher initialized')
        self.pub = self.create_publisher(Int32, f'{self.namespace}/test_topic', 10)
        self.create_timer(0.5, self.timer_callback)
        self.counter = 0

    def timer_callback(self):
        self.pub.publish(Int32(data=self.counter))
        self.counter += 1
        self.get_logger().info(f'[{self.namespace[1:]}] Published {self.counter}')


def main(args=None):
    rclpy.init(args=args)
    pub = Pub()
    rclpy.spin(pub)
    pub.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()