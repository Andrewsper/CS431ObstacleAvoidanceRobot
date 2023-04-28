
1. Pseudocode to describe the project/program, including the AvoidObstacle() function.

```AvoidanceRobot class

    initialize
            
    input:none
    output:initialized AvoidanceRobot
            
        init a threading Condition to protect lds data
                
        create an array of lds ranges initialized to 0
                
        initialize a ros node for AvoidanceRobot
                
        initialize a ros subscriber for AvoidanceRobot's lds sensors that calls ros_lds_callback when it receives data
        
        initialize a ros publisher for AvoidanceRobot to send twist messages to the /cmd_vel topic

        create a rospy clock with a rate of 10Hz		
                
        create AvoidanceRobot's Twist object and initialize its linear.x and angular.z values to 0.0

        calculate the optimal detection range given the robot radius and the requested collision distance called theta

        initialize turn left and turn right to False

        create a thread to run the control loop

        create a thread to listen to the /scan messages


    ros_lds_callback 

    input: msg (array of LaserScan messages)
    output: updates robot ranges array
        acquire the lds data condition

        set AvoidanceRobot's range array to the new set of lds ranges
        
        set any range with inf to 0
       
        notify the lds data condition
    

    control_loop

    input: none
    output: none

        while rospy is not shutdown:

            gather twist decision information from avoid_obstacle

            set AvoidanceRobot's linear and angular velocity to the decision values

            publish the twist message to the velocity publisher
            
            sleep for a rate of 10 Hz
            
       Join control_loop thread
       Join subscriber_thread


    subscriber_thread

    input: none
    output: none

        run rospy spin to so start listening to /scan topic


    avoid_obstacle

    input: none
    output: decision array [linear_velocity, angular_velocity]

        acquire the scan data lock
        check for collision in the range of 0 to theta degrees and 360-theta to 360 degrees

        if collision not detected:
            set go_left and go_right to False
            release the scan data lock
            return the decision array with the angular velocity to 0.0 and the linear velocity to 0.1

        else

            if go_left:
                set angular velocity to 0.2
            else if go_right:
                set angular velocity to -0.2

            normalize the ranges

            set the values of 0 to 180 degrees that are equal to zero to 1

            set the values of 180 to 360 degrees that are equal to zero to -1

            calculate the sum of the normalized ranges

            if the sum is less than greater than or equal to 0, set the angular velocity to 0.2 and the linear velocity to 0.0 and set go_left to True

            if the sum is less than 0, set the angular velocity to -0.2 and the linear velocity to 0.0 and set go_right to true

            release the scan data lock

            return the decision array


    start

    input: none
    output: none

        start the control_thread
        start the subscriber thread
        start the pygame thread
        start the camera subscriber thread
     
```

2. To run the code start up your desired turtle_bot simulation and then run `avoidance.py` script 

```sh   
source ./devel/setup.bash
export TURTLEBOT3_MODEL=waffle_pi
roslaunch turtlebot3_gazebo turtlebot3_house.launch
```

```sh
cd auto_turtle/src/scripts
./avoidance.py
```

3. The result should be a turtle_bot that drives straight until it detects a collision imminent and then turns right or left depending on
whether the sum of the normalized ranges is negative or positive to avoid the collision. The LiDAR
scan will be displayed in a Pygame window and the built-in turtlebot camera will be shown in a
OpenCV window. 

4. There is one Condition sync primitive that protects the LiDAR scan ranges array and signals the control loop when to calculate the next decision to be published to
/cmd_vel. The synchronization primitive also signals the pygame thread to update the LiDAR scan display. Next, there is a lock primitive that protects the OpenCV camera display due to the
multithreaded nature of this application. 

5. See Pseudocode and diagrams

6. The robot is able to avoid getting stuck in a corner based on the specified buffer that considers the geometry of the robot and the requested collision distance. 


