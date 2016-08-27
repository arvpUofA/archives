#!/usr/bin/env python
import roslib
import rospy
import smach
import smach_ros
from buoy_task import BuoyTask
from buoy_start import BuoyStart
from vision_temp.msg import *
from actionlib import *
from actionlib_msgs.msg import GoalStatus
from smach import State

"""
Mission planner for robot

Uses SMACH finite state machine for handling switching
between tasks
"""
def main():
	rospy.init_node('buoy_task_state_machine')

	# Create a SMACH state machine
	sm0 = smach.StateMachine(outcomes=['succeeded','aborted','preempted'])
	sm0.userdata.color = "None"
	rospy.loginfo("Starting state machine")
	rospy.loginfo("woooo")

	with sm0:
		def buoy_result_cb(userdata, status, result):
			"""
			Result callback for BUOY_START state
			"""
			if status == GoalStatus.SUCCEEDED:
				if(result.color == "red"):
					return 'red_task'
		  		elif(result.color == "yellow"):
					return 'yellow_task'
		  		elif(result.color == "green"):
					return 'green_task'
		  	else:
	  			return "aborted"

		def buoy_goal_cb(userdata, goal):
		  	"""
	  		Goal callback for BUOY_START state
	  		"""
			goal = BuoyStartGoal()
			goal.last = userdata.color
			rospy.loginfo("Last goal: " + goal.last)
			if(goal.last is "None"):
				goal.color = "red"
			elif(goal.last is 'red'):
				goal.color = "yellow"
			else:
				goal.color = "yellow"

			return goal


		def buoy_task_result_cb(userdata, status, result):
			"""
			Result callback for color states
			"""
			userdata.color_output = result.color
			return 'succeeded'

		smach.StateMachine.add('BUOY_START',
								smach_ros.SimpleActionState('buoy_start', BuoyStartAction,
								result_cb=buoy_result_cb,goal_cb=buoy_goal_cb,
								input_keys=['color_input'],outcomes=['red_task','yellow_task','green_task'],
								remapping={'color_input':'color'}),
								{'red_task':'RED_BUOY','yellow_task':'YELLOW_BUOY',
												'green_task':'GREEN_BUOY'})

		smach.StateMachine.add('RED_BUOY',
								smach_ros.SimpleActionState('buoy_task', BuoyTaskAction,
								goal = BuoyTaskGoal(color='red'),result_cb=buoy_task_result_cb,
								output_keys=['color_output'],
								remapping={'color_output':'color'}),
								{'succeeded':'BUOY_START'})

		smach.StateMachine.add('YELLOW_BUOY',
								smach_ros.SimpleActionState('buoy_task', BuoyTaskAction,
								goal = BuoyTaskGoal(color='yellow'),result_cb=buoy_task_result_cb,
								output_keys=['color_output'],
								remapping={'color_output':'color'}),
								{'succeeded':'BUOY_START'})

		smach.StateMachine.add('GREEN_BUOY',
								smach_ros.SimpleActionState('buoy_task', BuoyTaskAction,
								goal = BuoyTaskGoal(color='green'),result_cb=buoy_task_result_cb,
								output_keys=['color_output'],
								remapping={'color_output':'color'}),
								{'succeeded':'aborted'})

	# Start introspection server for debugging
	sis = smach_ros.IntrospectionServer('server_name', sm0, '/SM_ROOT')
	sis.start()

	outcome = sm0.execute()

	rospy.spin()
	sis.stop()
	rospy.signal_shutdown('All done.')

if __name__ == '__main__':
    main()
