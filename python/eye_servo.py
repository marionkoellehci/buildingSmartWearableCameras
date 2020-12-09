#!/home/pi/.virtualenvs/py3cv4/bin/python3

import io
import time
import picamera
import numpy as np
import cv2
from Faces import Face
from threading import Thread
from imutils.video import VideoStream
import imutils
import sys
import termcolor
import servos
import time

class eye_servo():
    """ Closes the eye as soon as a face is detected """

    eye_closed = False
    cooldown_time = 10 #time for which the eye remains shut
    every = 1 # process every xth picture

    def __init__(self):
        """ Initialze - init servos"""
        channels = [8, 9]
        servos.initChannel(channels)
        servos.open()

    def toggle_eye(self):
        self.eye_closed = !self.eye_closed
        if not self.eye_closed:
            servos.open()
        else:
            servos.close()


    def run(self):

        # size of video
        hight = int(480 / 2)
        width = int(640 / 2)

        start_time = time.monotonic()
        #camera = picamera.PiCamera()
        vs = VideoStream(usePiCamera = True, resolution = (width, hight), framerate = 10).start()
        vs.shutter_speed = 70
        time.sleep(3.0)
        counter = 0
        doSecondRescale = True
        while 1:
            frame = vs.read()
            if self.eye_closed:
                if time.monotonic() - start_time >= self.cooldown_time:
                    # open eye after cooldown time
                    if self.eye_closed:
                        print("opening now")
                        servos.open()
                    self.eye_closed = False
                    continue #we want the next frame, this one was done with closed lense, no need processing it

            # comment next 2 lines if you do not wish for graphical output
            cv2.imshow("video", frame)
            cv2.waitKey(1)
            counter += 1
            print(counter)
            if counter % self.every == 0:
                if self.eye_closed:
                    continue

                scale = 1.25 if doSecondRescale else 1.3
                # search frame for faces
                status = Face.faceInPicture(img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), doSecondRescale = doSecondRescale, scale = scale)

                if status == 2:
                    text = termcolor.colored("FoundFace", 'green')
                    print(text)
                    servos.close()
                    self.eye_closed = True
                    start_time = time.monotonic()
                    print("Closed - sleeping 10 seconds")
                elif status == 1:
                    text = termcolor.colored("Maybe", 'yellow')
                    doSecondRescale = False
                    print(text)
                else:
                    text = termcolor.colored("No", 'cyan')
                    doSecondRescale = True
                    print(text)

def main():
    stream = eye_servo()
    btn = Button(23)
    btn.when_pressed = stream.toggle_eye
    stream.run()

if(__name__=='__main__'):
    main()
