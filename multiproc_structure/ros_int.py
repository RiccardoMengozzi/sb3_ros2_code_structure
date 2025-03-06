from rclpy.node import Node
import time
from rclpy.callback_groups import ReentrantCallbackGroup, MutuallyExclusiveCallbackGroup
import rclpy
import threading
from std_msgs.msg import Int32
from std_srvs.srv import Trigger

class RosInt():
    def __init__(self, namespace):
        rclpy.init()
        self.node = Node(node_name='ros_int', namespace=namespace)  
        self.executor = rclpy.executors.SingleThreadedExecutor()
        self.executor.add_node(self.node)
        self.executor_thread = threading.Thread(target=self.executor.spin, daemon=True)
        self.executor_thread.start()

        self.namespace = self.node.get_namespace()
        self.node.get_logger().info(f'[{self.namespace[1:]}] ROS Interface initialized')
        self.sub = self.node.create_subscription(Int32, f'{self.namespace}/test_topic', self.sub_callback, 10)
        self.cli = self.node.create_client(Trigger, f'{self.namespace}/test_service')

    def sub_callback(self, msg) -> None:
        self.node.get_logger().info(f'[{self.namespace[1:]}] Received: {msg.data}')

    def call_test_service(self) -> bool:
        """Send an async reset request"""
        self.node.get_logger().info(f'[{self.namespace[1:]}] Calling service')
        req = Trigger.Request()
        future = self.cli.call_async(req)
        return future

    def is_reset_done(self, future):
        """Check if reset is complete."""
        return future.done()