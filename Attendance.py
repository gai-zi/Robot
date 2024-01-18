#!/usr/bin/env python
import rospy
from sound_play.libsoundplay import SoundClient
from opencv_apps.msg import FaceArrayStamped

class Attendance:
    def __init__(self):
        rospy.init_node('attendance')
        rospy.on_shutdown(self.cleanup)

        self.soundhandle = SoundClient()
        rospy.sleep(1)

        self.soundhandle.stopAll()
		# rospy.loginfo("Ready, waiting for commands...")
        
        # Subscribe to the face detection output and set the callback function
        rospy.Subscriber('/face_recognition/output', FaceArrayStamped, self.face_recognition_callback)
        
        # Initialize a set to keep track of unique labels
        self.unique_labels = set()
    
    def cleanup(self):
        self.soundhandle.stopAll()
        rospy.loginfo("Shutting down node...")

    def face_recognition_callback(self, data):
        if data.faces:
            label = data.faces[0].label
            # self.soundhandle.say("Good morning. How can I help you?")
            if label not in self.unique_labels:
                file_path = '/home/mustar/Documents/attendance.txt'

                with open(file_path, 'a') as txtfile:
                    txtfile.write("{}\n".format(label))

                self.unique_labels.add(label)
                rospy.loginfo("Label '{}' added to text file.".format(label))
                self.soundhandle.say("Attendance recorded")

if __name__=="__main__":
    try:
        Attendance()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("Partybot node terminated.")

