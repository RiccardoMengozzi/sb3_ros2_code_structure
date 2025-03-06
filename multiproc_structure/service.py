from rclpy.node import Node
from std_srvs.srv import Trigger
import time
import rclpy



class Service(Node):
    def __init__(self):
        super().__init__(node_name='test_service')
        self.get_logger().info(f'[{self.get_namespace()[1:]}] Service initialized')
        self.service = self.create_service(Trigger, 'test_service', self.service_callback)


    def service_callback(self, request, response):
        self.get_logger().info(f'[{self.get_namespace()[1:]}] Executing service')
        time.sleep(5.0)
        self.get_logger().info(f'[{self.get_namespace()[1:]}] Service Executed')
        response.success = True
        response.message = 'Service executed'
        return  response
    


def main(args=None):
    rclpy.init(args=args)
    service = Service()
    rclpy.spin(service)
    service.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()