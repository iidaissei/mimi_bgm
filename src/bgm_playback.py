#!/usr/bin/env python
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------
# Title: mimiのbgm再生用ROSノード
# Author: Issei Iida
# Date: 2019/12/06
# Memo: ここで指定したファイルしか再生できない仕様（今後複数の
#       ファイルを再生できるようにする予定）
#---------------------------------------------------------------------

# Python
import sys
from mutagen.mp3 import MP3 as mp3
import pygame
import time
# ROS
import rospy
from std_msgs.msg import String, Bool


class Mp3Playback():
    def __init__(self):
        # Subscriber
        self.sub_playfile = rospy.Subscriber('/mimi_bgm/play_start', Bool, self.filenameCB)
        # Value
        self.play_flg = False

    def filenameCB(self, receive_msg):
        self.play_flg = receive_msg

    def playback(self):
        while not rospy.is_shutdown() and self.play_flg is False:
            rospy.loginfo('Waiting for filename')
            rospy.sleep(1.0)
        self.play_flg = True
        # 再生処理
        filename = '/home/issei/catkin_ws/src/mimi_bgm/mp3_file/ElectrricalParade.mp3'
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.load(filename)
        mp3_length = mp3(filename).info.length
        pygame.mixer.music.play(1)
        rospy.sleep(mp3_length)
        pygame.mixer.music.fedeout(5.0)


def main():
    try:
        rospy.loginfo('Start bgm_playback')
        mp3_pb = Mp3Playback()
        mp3_pb.playback()
    except rospy.ROSInterruptException:
        rospy.loginfo('**Interrupted**')
        pass


if __name__ == '__main__':
    rospy.init_node('bgm_playback', anonymous = True)
    main()
