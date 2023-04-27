
1. Pseudocode to describe the project/program, including the AvoidObstacle() function.

AvoidanceRobot class

    initialize
            
    input:none
    output:initialized AvoidanceRobot
            
        init a threading Condition to protect lds data
                
        create an array of lds ranges initialized to 0
                
        initialize a ros node for AvoidanceRobot
                
        initialize a ros subscriber for AvoidanceRobot's lds sensors that calls ros_lds_callback when it recieves data
        
        initialize a ros publisher for AvoidanceRobot to send twist messages to the /cmd_vel topic

        create a rospy clock with a rate of 10Hz		
                
        create AvoidanceRobot's Twist object and initialize its linear.x and angular.z values to 0.0

        calculate the optimal detection range given the robot radius and the requested collison distance called theta

        create a thread to run the control loop

        create a thread to listen to the /scan messages





    ros_lds_callback

    input: msg (array of LaserScan messages)

    output: updates robot ranges array

        aquire the lds data condition

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

            release the scan data lock
            return the decision array with the angular velocity to 0.0 and the linear velocity to 0.1

        else

            normalize the ranges

            set the values of 360-theta to 360 degrees to negative values

            calculate the sum of the normalized ranges

            if the sum is less than 0, set the angular velocity to 0.2 and the linear velocity to 0.0

            if the sum is greater than 0, set the angular velocity to -0.2 and the linear velocity to 0.0

            release the scan data lock

            return the decision array


    start

    input: none
    output: none

        start the control_thread
        start the subscriber thread

2.to run the code start up your desired turtle_bot simulation and then run ./avoidance.py

3. the result should be a turtle_bot that drives straight until it detects a collision immenent and then turns right or left depending on
whether the sum of the normalized ranges is negative or positive to avoid the collision

4. There is one Condition sync primative that protects the ranges array and signals the control loop when to calculate the next decision to be published to
/cmd_vel

5.see Pseudocode and diagrams

6. at the moment the robot ussally is able to turn before it collides with a corner.


