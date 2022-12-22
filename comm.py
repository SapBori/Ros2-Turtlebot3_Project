import rclpy

from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from sensor_msgs.msg import LaserScan
from cv_bridge import CvBridge

class ClientPublisher(Node):
    def __init__(self):
        super().__init__('my_bot_pub')
        self.publisher = self.create_publisher(Twist, '/cmd_vel',10)
        timer_period = 0.5
        self.__LinearVel =0.0
        self.__AngularVel = 0.0
        self.timer = self.create_timer(timer_period,self.timer_callback)
        
    def set_vel(self, linear_Vel, angular_Vel):
        self.__LinearVel = linear_Vel
        self.__AngularVel = angular_Vel

    def timer_callback(self):
        msg = Twist()
        msg.linear.x = self.__LinearVel
        msg.angular.z = self.__AngularVel
        self.publisher.publish(msg)
        #self.get_logger().info("Publishing: %s" % msg)

class ClientSubscriber(Node):
    
    def __init__(self):
        super().__init__('my_bot_cam_sub')
        self.subscriberImg = self.create_subscription(Image, '/camera/image_raw',self.listener_img_callback,10)
        #self.subscriberImu = self.create_subscription(Imu, '/imu',self.listener_Imu_callback,10)
        self.subscriberScan =self.create_subscription(LaserScan,'/scan',self.listener_Scan_callback,10)
        self.Cv2Image= None 
        self.CvBridge= CvBridge()
        self.Lidar = LaserScan()
        self.Lidarrange= [0,0,0,0,0,0,0,0,0,0,0,0]
        self.color = 0
        

    def listener_img_callback(self,msg):
        #self.get_logger().info('Subscribed width: %s' % msg.width)
        #self.get_logger().info('Subscribed height: %s' % msg.height)
        #self.get_logger().info('color: %s' % msg.data)
        self.Cv2Image = self.CvBridge.imgmsg_to_cv2(msg,"bgr8")
        self.color = msg.data[630000]

    #def listener_Imu_callback(self,msg):
        #self.get_logger().info('Subscribed imu: %s' % msg.linear_acceleration)
    def listener_Scan_callback(self,msg):
        #self.get_logger().info('Scanning ranges: %s' % msg.ranges)
        for i in range(0,12):
            self.Lidarrange[i]=msg.ranges[30*i] 
    def get_img(self):
        return self.Cv2Image
    def get_range(self):
        return self.Lidarrange
    def get_color(self):
        return self.color
    