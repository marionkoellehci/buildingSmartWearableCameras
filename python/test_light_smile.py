#!/home/pi/.virtualenvs/py3cv4/bin/python3

# you have to use this: sudo -E ./test_light_smile.py
# to run the script
import io
import time
import picamera
import numpy as np
import cv2
from Faces import Face
from imutils.video import VideoStream
import LightStrip as ls
from collections.abc import Iterable

from gpiozero import Button

class smile_light():
    """docstring for smile_light."""

    shouldRun = True
    store_next_img = False
    _median_list = []
    _average_median = [7, 5, 3]

    def btn_callback(self):
        """ Sets flag to save the next image - turns leds white """
        self.shouldRun = False
        self.store_next_img = True
        # ALL Led white for 5 seconfs
        ls.flash(5)
        self.shouldRun = True

    @staticmethod
    def _rotate(l, n):
        return l[n:] + l[:n]

    def _movingMedianHelper(self, val):
        """ calculate the average of the moving medians """

        while len(self._median_list) < self._average_median[0]:
            self._median_list.append(0)

        self._median_list[0] = val
        average = []
        for l in self._average_median:
            average.append(np.median(self._median_list[0:l]))
        self._median_list = self._rotate(self._median_list, -1)
        return np.average(average)

    def movingMedian(self,val):
        """ calculate the next value for the smile confidence - which is the average of moving medians """
        if isinstance(val, Iterable):
            average = 0
            for v in val:
                average = self._movingMedianHelper(v)
            return average
        else:
            return self._movingMedianHelper(val)


    def run(self):
        """ Lightbar for confidence of smile """

        hight = int(480 / 2)
        width = int(640 / 2)
        vs = VideoStream(usePiCamera = True, resolution = (width, hight), framerate = 10).start()
        vs.shutter_speed = 70
        time.sleep(3.0)
        counter = 0
        doSecondRescale = True
        while 1:
            frame = vs.read()
            if self.store_next_img:
                self.store_next_img = False
                name = str(time.time()) + ".png"
                cv2.imwrite(name, frame)

            # for usage without gui comment next line
            cv2.imshow("video", frame)
            cv2.waitKey(1)
            counter += 1
            print(counter, end = "\t")
            if counter % 1 == 0:

                scale = 1.25 if doSecondRescale else 1.3
                smiles = Face.smile(img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), doSecondRescale = doSecondRescale, scale = scale)
                average = self.movingMedian(0) if len(smiles) == 0 else self.movingMedian(smiles[0])
                print(" Average: ", end="")
                # Debug output - the last measured smile confidences, used for median
                print(self._median_list)
                average = min(average, 5)
                if self.shouldRun:
                    ls.bar(average / 5, 100, 0, 0)


def main():
    smile = smile_light()
    btn = Button(23)
    btn.when_pressed = smile.btn_callback
    smile.run()

if __name__ == '__main__':
    main()
