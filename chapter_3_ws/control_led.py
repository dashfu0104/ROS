# -*- coding: utf-8 -*-
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from time import sleep
import random
import Jetson.GPIO as GPIO
RED_LED_PIN = 23
YELLOW_LED_PIN = 8
GREEN_LED_PIN = 18
def setup_leds():
  
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RED_LED_PIN, GPIO.OUT)
    GPIO.setup(YELLOW_LED_PIN, GPIO.OUT)
    GPIO.setup(GREEN_LED_PIN, GPIO.OUT)
    GPIO.output(RED_LED_PIN, GPIO.LOW)
    GPIO.output(YELLOW_LED_PIN, GPIO.LOW)
    GPIO.output(GREEN_LED_PIN, GPIO.LOW)
setup_leds()
def traffic_light():
    rospy.init_node('traffic_light_node', anonymous=True)
    light_pub = rospy.Publisher('/traffic_light', String, queue_size=10)
    cmd_vel_pub = rospy.Publisher('/robot_base_velocity_controller/cmd_vel', Twist, queue_size=10)
    lights = ['red', 'green', 'yellow']
    light_index = 0
    cmd_vel_msg = Twist()

    while not rospy.is_shutdown():
        light_pub.publish(lights[light_index])

        if lights[light_index] == 'red':
	    turn_on_led(RED_LED_PIN)
            rospy.loginfo('Red Light: Stop!')
            cmd_vel_msg.linear.x = 0.0 
            cmd_vel_pub.publish(cmd_vel_msg)
            sleep(5)
	    turn_off_led(RED_LED_PIN)
        elif lights[light_index] == 'green':
	    turn_on_led(GREEN_LED_PIN)
            rospy.loginfo('Green Light: Go!')
            start_time = rospy.Time.now()
            duration = rospy.Duration(5.0) 
            while rospy.Time.now() - start_time < duration:
                cmd_vel_msg.linear.x = 0.8  
                cmd_vel_pub.publish(cmd_vel_msg)
                sleep(0.1) 
	    turn_off_led(GREEN_LED_PIN)
        elif lights[light_index] == 'yellow':
	    turn_on_led(YELLOW_LED_PIN)
            rospy.loginfo('Yellow Light: Slow down!')
            start_time = rospy.Time.now()
            duration = rospy.Duration(5.0) 
	
            while rospy.Time.now() - start_time < duration:
                cmd_vel_msg.linear.x = 0.4 
                cmd_vel_pub.publish(cmd_vel_msg)
                sleep(0.1)  
	    turn_off_led(YELLOW_LED_PIN)
        if random.random() < 0.01:
            rospy.loginfo('No Traffic Light: Slow down!')
            start_time = rospy.Time.now()
            duration = rospy.Duration(1.0)  

            while rospy.Time.now() - start_time < duration:
                cmd_vel_msg.linear.x = 0.1  
                cmd_vel_pub.publish(cmd_vel_msg)
                light_pub.publish('none')
                sleep(0.1)  
            light_index = (light_index + 1) % len(lights)
        else:
            light_index = (light_index + 1) % len(lights)
def turn_on_led(led_pin):
    GPIO.output(led_pin, GPIO.HIGH)
def turn_off_led(led_pin):
    GPIO.output(led_pin, GPIO.LOW)

if __name__ == '__main__':
    try:
        traffic_light()
    except rospy.ROSInterruptException:
        pass
