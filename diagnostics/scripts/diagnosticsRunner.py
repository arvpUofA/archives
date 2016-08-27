#!/usr/bin/python
from diagnostics.msg import Data, LEDs, Status
from arvp_main.msg import IMU, Depth, MCRaw, KillSig

import rospy
import os
import psutil

lastTs = { 'imu': rospy.Time(0), 'depth': rospy.Time(0), 'motor': rospy.Time(0) }
summary = Data()
ledLastTime = rospy.Time(0)

def imuCb(data):
	lastTs['imu'] = data.header.stamp
	summary.heading = data.heading
	summary.pitch = data.pitch
	summary.roll = data.roll

def depthCb(data):
	lastTs['depth'] = data.header.stamp
	summary.depth = data.depth

def motorCb(data):
	lastTs['motor'] = data.header.stamp
	summary.horLeft = data.horLeft
	summary.horRight = data.horRight
	summary.verLeft = data.verLeft
	summary.verRight = data.verRight

def killSigCb(data):
	summary.kill = data.kill

def main():
	global ledLastTime
	# Ros init
	dataPub = rospy.Publisher('diagnostics/data', Data, queue_size=10)
	statusPub = rospy.Publisher('diagnostics/status', Status, queue_size=10)
	ledPub = rospy.Publisher('diagnostics/leds', LEDs, queue_size=5)
	rospy.init_node( 'diagnostics')
	rospy.Subscriber( "/sensors/imu", IMU, imuCb )
	rospy.Subscriber( "/sensors/depth", Depth, depthCb )
	rospy.Subscriber( "/motor/feedback", MCRaw, motorCb )
	rospy.Subscriber( "/motor/killSig", KillSig, killSigCb )

	# 5Hz in this loop
	rate = rospy.Rate(5)
	while not rospy.is_shutdown():
		# Check status of systems
		hasErrors = False
		notHeard = []
		for item, last in lastTs.items():
			if(rospy.Time.now() - last) > rospy.Duration(1.0):
				notHeard.append(item)
				hasErrors = True
		if notHeard:
			rospy.logerr( "Not getting anything from %s" % notHeard )
		# Publish status
		status = Status()
		status.header.stamp = rospy.Time.now()
		status.imu = not 'imu' in notHeard
		status.depth = not 'depth' in notHeard
		status.motor = not 'motor' in notHeard
		statusPub.publish( status )

		# Publish data
		summary.header.stamp = rospy.Time.now()
		summary.cpuUsage = ( summary.cpuUsage + psutil.cpu_percent() ) / 2.0
		if( summary.cpuUsage > 90.0 ):
			rospy.logwarn( "CPU usage is really high (%.2f%%)" % summary.cpuUsage )
			hasErrors = True
		summary.memUsage = psutil.virtual_memory().percent
		if( summary.memUsage > 90.0 ):
			rospy.logwarn( "Memory usage is really high (%.2f%%)" % summary.memUsage )
			hasErrors = True
		summary.coreURI = os.getenv( 'ROS_MASTER_URI' , '') 
		dataPub.publish( summary )

		# Set LEDs
		if( rospy.Time.now() - ledLastTime > rospy.Duration(1.0)):
			ledLastTime = rospy.Time.now()
			if hasErrors:
				ledMsg = LEDs()
				ledMsg.led_type = LEDs.RED
				ledMsg.timeout = 600
				ledPub.publish( ledMsg )
			if summary.kill == 0:
				ledMsg = LEDs()
				ledMsg.led_type = LEDs.GREEN
				ledMsg.timeout = 600
				ledPub.publish( ledMsg )


		# Reset data
		summary.heading = 0
		summary.pitch = 0
		summary.roll = 0
		summary.depth = 0
		summary.horLeft = 0
		summary.horRight = 0
		summary.verLeft = 0
		summary.verRight = 0
		summary.kill = 1

		rate.sleep()	

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
