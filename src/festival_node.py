#!/usr/bin/env python
#
# Software License Agreement (GPLv2 License)
#
# Copyright (c) 2012 OpenQbo, Inc.
#
# This program is free software; you can redistribute it and/or 
# modify it under the terms of the GNU General Public License as 
# published by the Free Software Foundation; either version 2 of
# the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License 
# along with this program; if not, write to the Free Software 
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, 
# MA 02110-1301, USA.
#
# Authors: Miguel Angel Julian <miguel.a.j@openqbo.com>; 
#

import roslib; roslib.load_manifest('qbo_talk')
import rospy
import pyFestival
import time
from qbo_talk.srv import Text2Speach

class festival_node(object):

    def processCommand(self,req):
        self.festivalClient.send(req.command)
        return True

    def say(self,req):
        self.festivalClient.say(req.command.replace(".",". silencebreak "))
        return True

    def sayNoWait(self,req):
        self.festivalClient.say(req.command.replace(".",". silencebreak "),False)
        return True

    def changeLanguage(self,req):
        self.festivalClient.setVoice(req.command)
        return True

    def changeSpeed(self,req):
        self.festivalClient.setDuration(float(req.command))
        return True

    def __init__(self):
        rospy.init_node('festival_server')
        self.festivalServer = pyFestival.FestivalServer()
        time.sleep(2)
        self.festivalClient = pyFestival.FestivalClient()
        self.festivalClient.open()
        #self.festivalClient.setVoice("cmu_us_clb_arctic_clunits")
        #self.festivalClient.setVoice("cmu_us_awb_arctic_clunits")
        #self.festivalClient.setVoice("voice_kal_diphone")
        command_service = rospy.Service('/qbo_talk/festival_command', Text2Speach, self.processCommand)
        talk_service = rospy.Service('/qbo_talk/festival_say', Text2Speach, self.say)
        talk_service_no_wait = rospy.Service('/qbo_talk/festival_say_no_wait', Text2Speach, self.sayNoWait)
        language_service = rospy.Service('/qbo_talk/festival_language', Text2Speach, self.changeLanguage)
        duration_service = rospy.Service('/qbo_talk/festival_speed', Text2Speach, self.changeSpeed)
        self.festivalClient.say("Hello");
        rospy.spin()
        self.festivalClient.close()
        self.festivalServer.stop()

if __name__=="__main__":
    node=festival_node()
