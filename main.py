# Output sample of the jetson inference
"""
ClassID: 1
   -- Confidence: 0.749023
   -- Left:    263.906
   -- Top:     209.883
   -- Right:   636.875
   -- Bottom:  475.312
   -- Width:   372.969
   -- Height:  265.43
   -- Area:    98997
   -- Center:  (450.391, 342.598)
"""

"""

"""

# importing required libraries

# cleaning GPIO
import Jetson.GPIO as GPIO
import cv2
from termios import TABDLY
import jetson.inference
import jetson.utils
import threading as th
import numpy as np
from datetime import datetime
import time
from pip import main


GPIO.cleanup()

# Getting pretrained SSD-Mobilenet-v2 model
net = jetson.inference.detectNet("SSD-Mobilenet-v2", threshold=0.5)

# initializing the capture instance for inference
cap = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)
resw, resh = 640, 480
iw = int(resw)
ih = int(resh)
cap.set(3, int(resw))
cap.set(4, int(resh))
cap2.set(3, int(resw))
cap2.set(4, int(resh))
print("capdata:", cap)

# Defining boxes Lane1 of the road
waiting_area = np.array(
    [[10, 240], [160, 250], [160, 480], [10, 480]], np.int32)
pts = waiting_area.reshape((-1, 1, 2))
main_area = np.array(
    [[230, 240], [400, 240], [400, 480], [230, 480]], np.int32)
pts_2 = main_area.reshape((-1, 1, 2))
waiting_area_2 = np.array(
    [[450, 240], [640, 240], [640, 480], [450, 480]], np.int32)
pts_3 = waiting_area_2.reshape((-1, 1, 2))
isClosed = True
waiting_1 = False
main_1 = False
waiting_2 = False
count_t_1 = 0
count_f_1 = 0
count_t_2 = 0
count_f_2 = 0
count_f_3 = 0
count_t_3 = 0
pause_1 = 0
pause_2 = 0
pause_3 = 0
counter_delay = 0
cx = []
cy = []
led_pin_1 = 37  # pedestrian
led_pin_2 = 13  # vehicle red
led_pin_5 = 14  # vehicle green
frame_delay_1 = 15
frame_delay_2 = 15

# Defining boxes lane 2 c block side
waiting_area_lane2 = np.array(
    [[10, 240], [160, 250], [160, 480], [10, 480]], np.int32)
pts_lane2 = waiting_area_lane2.reshape((-1, 1, 2))
main_area_lane2 = np.array(
    [[230, 240], [400, 240], [400, 480], [230, 480]], np.int32)
pts_2_lane2 = main_area_lane2.reshape((-1, 1, 2))
waiting_area_2_lane2 = np.array(
    [[450, 240], [640, 240], [640, 480], [450, 480]], np.int32)
pts_3_lane2 = waiting_area_2_lane2.reshape((-1, 1, 2))
isClosed_lane2 = True
waiting_1_lane2 = False
main_1_lane2 = False
waiting_2_lane2 = False
count_t_1_lane2 = 0
count_f_1_lane2 = 0
count_t_2_lane2 = 0
count_f_2_lane2 = 0
count_f_3_lane2 = 0
count_t_3_lane2 = 0
pause_1_lane2 = 0
pause_2_lane2 = 0
pause_3_lane2 = 0
counter_delay_lane2 = 0
cx_lane2 = []
cy_lane2 = []
led_pin_3 = 15  # pedestrian lane2
led_pin_4 = 35  # vehicle red lane2
led_pin_6 = 16  # vehicle green lane 2
frame_delay_1_lane2 = 15
frame_delay_2_lane2 = 15

# setting GPIO mode and initial conditions
GPIO.setmode(GPIO.BOARD)
GPIO.setup(led_pin_1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(led_pin_2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(led_pin_3, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(led_pin_4, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(led_pin_5, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(led_pin_6, GPIO.OUT, initial=GPIO.LOW)


# detection for frame1
def person_detector1(frame1):
    # Defining global variables
    global waiting_1, main_1, waiting_2
    global cx, cy
    global count_t_1, count_f_1, count_t_2, count_f_2, count_f_3, count_t_3
    global pause_1, pause_2, pause_3
    image = frame1
    image_height, image_width, _ = image.shape

    detections = net.Detect(framex)

    for d in detections:
        classID = int(d.ClassID)
        x1, y1, x2, y2 = int(d.Left), int(d.Top), int(d.Right), int(d.Bottom)
        bw, bh = int(d.Width), int(d.Height)
        cx, cy = int(d.Center[0]), int(d.Center[1])
        className = net.GetClassDesc(d.ClassID)
        if classID == 1:  # Filtering out the detection
            # Using polygontest for detection on zebra crossing
            result_1_1 = cv2.pointPolygonTest(pts, (x2, y2), False)
            result_1_2 = cv2.pointPolygonTest(pts, (x1, y1+bh), False)

            result_2_1 = cv2.pointPolygonTest(pts_2, (x2, y2), False)
            result_2_2 = cv2.pointPolygonTest(pts_2, (x1, y1+bh), False)

            result_3_1 = cv2.pointPolygonTest(pts_3, (x2, y2), False)
            result_3_2 = cv2.pointPolygonTest(pts_3, (x1, y1+bh), False)

            if result_1_1 >= 0 or result_1_2 >= 0:
                cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 255), 1)
                cv2.putText(image, className, (x1+5, y1+15),
                            cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 255), 1)
                cv2.putText(frame1, f'FPS: {int(net.GetNetworkFPS())}',
                            (30, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 255), 2)
                cv2.circle(frame1, (x2, y2), 2, (75, 13, 180), -1)
                cv2.circle(frame1, (x1, y1+bh), 2, (75, 13, 180), -1)

                waiting_1 = True
            if result_2_1 >= 0 or result_2_2 >= 0:
                cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 255), 1)
                cv2.putText(image, className, (x1+5, y1+15),
                            cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 255), 1)
                cv2.putText(frame1, f'FPS: {int(net.GetNetworkFPS())}',
                            (30, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 255), 2)
                cv2.circle(frame1, (x2, y2), 2, (75, 13, 180), -1)
                cv2.circle(frame1, (x1, y1+bh), 2, (75, 13, 180), -1)
                main_1 = True
            if result_3_1 >= 0 or result_3_2 >= 0:
                cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 255), 1)
                cv2.putText(image, className, (x1+5, y1+15),
                            cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 255), 1)
                cv2.putText(frame1, f'FPS: {int(net.GetNetworkFPS())}',
                            (30, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 255), 2)
                cv2.circle(frame1, (x2, y2), 2, (75, 13, 180), -1)
                cv2.circle(frame1, (x1, y1+bh), 2, (75, 13, 180), -1)
                waiting_2 = True
    # Detection conditions waiitng_Area

    if waiting_1 == False:
        count_f_1 = count_f_1 + 1
        if (count_f_1 == frame_delay_1):
            pause_1 = 0
        print("False count1", count_f_1)
        if(count_t_1 > 5):
            count_t_1 = 0

    if waiting_1 == True:
        count_t_1 = count_t_1 + 1
        pause_1 = 1
        print("True count1", count_t_1)
        waiting_1 = False
        count_f_1 = 0

    # Detection conditions waiting area 2
    if waiting_2 == False:
        count_f_3 = count_f_3 + 1
        if (count_f_3 == frame_delay_1):
            pause_3 = 0
        print("False count2", count_f_1)
        if(count_t_3 > 5):
            count_t_3 = 0

    if waiting_2 == True:
        count_t_3 = count_t_3 + 1
        pause_3 = 1
        print("True count2", count_t_1)
        waiting_2 = False
        count_f_3 = 0
    # Detection conditions main_Area
    if main_1 == False:
        count_f_2 = count_f_2 + 1
        if (count_f_2 == frame_delay_2):
            pause_2 = 0
        print("False count3", count_f_2)
        if(count_t_2 > 5):
            count_t_2 = 0

    if main_1 == True:
        count_t_2 = count_t_2 + 1
        if(count_t_2 > 2):
            pause_2 = 1
        print("True count3", count_t_2)
        main_1 = False
        count_f_2 = 0

    # Detecting conditions

    return frame1

# detection in lane 2 frame


def person_detector2(frame2):
    # Defining global variables
    global waiting_1_lane2, main_1_lane2, waiting_2_lane2
    global cx_lane2, cy_lane2
    global count_t_1_lane2, count_f_1_lane2, count_t_2_lane2, count_f_2_lane2, count_f_3_lane2, count_t_3_lane2
    global pause_1_lane2, pause_2_lane2, pause_3_lane2
    image2 = frame2
    image_height, image_width, _ = image2.shape

    detections2 = net.Detect(framex2)

    for d in detections2:
        classID = int(d.ClassID)
        x1, y1, x2, y2 = int(d.Left), int(d.Top), int(d.Right), int(d.Bottom)
        bw, bh = int(d.Width), int(d.Height)
        cx_lane2, cy_lane2 = int(d.Center[0]), int(d.Center[1])
        className = net.GetClassDesc(d.ClassID)
        if classID == 1:
            result_1_1_lane2 = cv2.pointPolygonTest(pts_lane2, (x2, y2), False)
            result_1_2_lane2 = cv2.pointPolygonTest(
                pts_lane2, (x1, y1+bh), False)

            result_2_1_lane2 = cv2.pointPolygonTest(
                pts_2_lane2, (x2, y2), False)
            result_2_2_lane2 = cv2.pointPolygonTest(
                pts_2_lane2, (x1, y1+bh), False)

            result_3_1_lane2 = cv2.pointPolygonTest(
                pts_3_lane2, (x2, y2), False)
            result_3_2_lane2 = cv2.pointPolygonTest(
                pts_3_lane2, (x1, y1+bh), False)

            if result_1_1_lane2 >= 0 or result_1_2_lane2 >= 0:
                cv2.rectangle(image2, (x1, y1), (x2, y2), (255, 0, 255), 1)
                cv2.putText(image2, className, (x1+5, y1+15),
                            cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 255), 1)
                cv2.putText(frame2, f'FPS: {int(net.GetNetworkFPS())}',
                            (30, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 255), 2)
                cv2.circle(frame2, (x2, y2), 2, (75, 13, 180), -1)
                cv2.circle(frame2, (x1, y1+bh), 2, (75, 13, 180), -1)

                waiting_1_lane2 = True
            if result_2_1_lane2 >= 0 or result_2_2_lane2 >= 0:
                cv2.rectangle(image2, (x1, y1), (x2, y2), (255, 0, 255), 1)
                cv2.putText(image2, className, (x1+5, y1+15),
                            cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 255), 1)
                cv2.putText(frame2, f'FPS: {int(net.GetNetworkFPS())}',
                            (30, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 255), 2)
                cv2.circle(frame2, (x2, y2), 2, (75, 13, 180), -1)
                cv2.circle(frame2, (x1, y1+bh), 2, (75, 13, 180), -1)
                main_1_lane2 = True
            if result_3_1_lane2 >= 0 or result_3_2_lane2 >= 0:
                cv2.rectangle(image2, (x1, y1), (x2, y2), (255, 0, 255), 1)
                cv2.putText(image2, className, (x1+5, y1+15),
                            cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 255), 1)
                cv2.putText(frame2, f'FPS: {int(net.GetNetworkFPS())}',
                            (30, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 255), 2)
                cv2.circle(frame2, (x2, y2), 2, (75, 13, 180), -1)
                cv2.circle(frame2, (x1, y1+bh), 2, (75, 13, 180), -1)
                waiting_2_lane2 = True
    # Detection conditions waiitng_Area

    if waiting_1_lane2 == False:
        count_f_1_lane2 = count_f_1_lane2 + 1
        if (count_f_1_lane2 == frame_delay_1_lane2):
            pause_1_lane2 = 0
        print("False count1_lane2", count_f_1_lane2)
        if(count_t_1_lane2 > 5):
            count_t_1_lane2 = 0

    if waiting_1_lane2 == True:
        count_t_1_lane2 = count_t_1_lane2 + 1
        pause_1_lane2 = 1
        print("True count1_lane2", count_t_1_lane2)
        waiting_1_lane2 = False
        count_f_1_lane2 = 0

    # Detection conditions waiting area 2
    if waiting_2_lane2 == False:
        count_f_3_lane2 = count_f_3_lane2 + 1
        if (count_f_3_lane2 == frame_delay_1_lane2):
            pause_3_lane2 = 0
        print("False count2_lane2", count_f_1_lane2)
        if(count_t_3_lane2 > 5):
            count_t_3_lane2 = 0

    if waiting_2_lane2 == True:
        count_t_3_lane2 = count_t_3_lane2 + 1
        pause_3_lane2 = 1
        print("True count2_lane2", count_t_1_lane2)
        waiting_2_lane2 = False
        count_f_3_lane2 = 0
    # Detection conditions main_Area
    if main_1_lane2 == False:
        count_f_2_lane2 = count_f_2_lane2 + 1
        if (count_f_2_lane2 == frame_delay_2_lane2):
            pause_2_lane2 = 0
        print("False count3_lane2", count_f_2_lane2)
        if(count_t_2_lane2 > 5):
            count_t_2_lane2 = 0

    if main_1_lane2 == True:
        count_t_2_lane2 = count_t_2_lane2 + 1
        if(count_t_2_lane2 > 2):
            pause_2_lane2 = 1
        print("True count3_lane2", count_t_2_lane2)
        main_1_lane2 = False
        count_f_2_lane2 = 0

    # Detecting conditions

    return frame2


while cap.isOpened() or cap2.isOpened():

    # try:
    ret1, frame1 = cap.read()
    ret2, frame2 = cap2.read()

    framex = jetson.utils.cudaFromNumpy(frame1)
    framex2 = jetson.utils.cudaFromNumpy(frame2)

    # cv2.rectangle(frame,TL,BR,(20,20,255),3)
    cv2.polylines(frame1, [pts], isClosed, (255, 20, 20), 2)
    cv2.polylines(frame1, [pts_2], isClosed, (255, 20, 20), 2)
    cv2.polylines(frame1, [pts_3], isClosed, (255, 20, 20), 2)

    ##########lane2 polyline ##############
    cv2.polylines(frame2, [pts_lane2], isClosed, (255, 20, 20), 2)
    cv2.polylines(frame2, [pts_2_lane2], isClosed, (255, 20, 20), 2)
    cv2.polylines(frame2, [pts_3_lane2], isClosed, (255, 20, 20), 2)

    frame1 = person_detector1(frame1)
    frame2 = person_detector2(frame2)

    cv2.putText(frame1, 'WAiting area 1', (10, 200),
                cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame1, 'Main area', (300, 200),
                cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame1, 'waiting area 2', (550, 200),
                cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)

    # lane2
    cv2.putText(frame2, 'WAiting area 2_1', (10, 200),
                cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame2, 'Main area2', (300, 200),
                cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame2, 'waiting area2_2', (550, 200),
                cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)

   #############
    # waiting output lane 2
    if ret1:
        if ((pause_1_lane2 == 1) & (pause_2_lane2 == 0) & (pause_3_lane2 == 0)):
            # if (count_t_1 > 2):
            if count_t_1_lane2 == 5:
                GPIO.output(led_pin_3, GPIO.LOW)
                GPIO.output(led_pin_4, GPIO.LOW)
                GPIO.output(led_pin_6, GPIO.LOW)

                cv2.putText(frame2, 'WL2-NO', (10, 100),
                            cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)

            if count_t_1_lane2 == 10:
                GPIO.output(led_pin_3, GPIO.HIGH)
                GPIO.output(led_pin_4, GPIO.LOW)
                GPIO.output(led_pin_6, GPIO.HIGH)

                cv2.putText(frame2, 'WL2-YES', (10, 100),
                            cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)
                count_t_1_lane2 = 0
                count_t_3_lane2 = 0

        elif ((pause_3_lane2 == 1) & (pause_2_lane2 == 0) & (pause_1_lane2 == 0)):

            if count_t_3_lane2 == 5:
                GPIO.output(led_pin_3, GPIO.LOW)
                GPIO.output(led_pin_4, GPIO.LOW)
                GPIO.output(led_pin_6, GPIO.LOW)

                cv2.putText(frame2, 'W2L2-NO', (400, 100),
                            cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)
            if count_t_3_lane2 == 10:
                GPIO.output(led_pin_3, GPIO.HIGH)
                GPIO.output(led_pin_4, GPIO.LOW)
                GPIO.output(led_pin_6, GPIO.HIGH)

                cv2.putText(frame2, 'W2L2-YES', (400, 100),
                            cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)
                count_t_3_lane2 = 0
                count_t_1_lane2 = 0
        elif ((pause_3_lane2 == 1) & (pause_1_lane2 == 1) & (pause_2_lane2 == 0)):
            if count_t_3_lane2 == 5 or count_t_1_lane2 == 5:
                GPIO.output(led_pin_3, GPIO.LOW)
                GPIO.output(led_pin_4, GPIO.LOW)
                GPIO.output(led_pin_6, GPIO.LOW)

                cv2.putText(frame2, 'WL2-NO', (10, 100),
                            cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame2, 'W2L2-NO', (600, 100),
                            cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)
            if count_t_3_lane2 == 10 or count_t_1_lane2 == 10:
                GPIO.output(led_pin_3, GPIO.HIGH)
                GPIO.output(led_pin_4, GPIO.LOW)
                GPIO.output(led_pin_6, GPIO.HIGH)
                cv2.putText(frame2, 'WL2-YES', (10, 100),
                            cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame2, 'W2L2-YES', (600, 100),
                            cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)
                count_t_3_lane2 = 0
                count_t_1_lane2 = 0

        elif ((pause_2_lane2 == 1) & (pause_1_lane2 == 0) & (pause_3_lane2 == 0)):
            GPIO.output(led_pin_4, GPIO.HIGH)
            cv2.putText(frame2, 'M-P-YES', (300, 100),
                        cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)
            GPIO.output(led_pin_3, GPIO.HIGH)
            GPIO.output(led_pin_6, GPIO.LOW)

            cv2.putText(frame2, 'ML-V-NO', (300, 60),
                        cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)
            count_t_1_lane2 = 0
            count_t_3_lane2 = 0

        elif ((pause_2_lane2 == 1) & (pause_1_lane2 == 1) & (pause_3_lane2 == 0)):
            GPIO.output(led_pin_3, GPIO.HIGH)
            cv2.putText(frame2, 'M-P-YES', (300, 100),
                        cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)
            GPIO.output(led_pin_6, GPIO.LOW)
            GPIO.output(led_pin_4, GPIO.HIGH)

            cv2.putText(frame2, 'M-V-NO', (300, 60),
                        cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)
            count_t_1_lane2 = 0
            count_t_3_lane2 = 0
        elif ((pause_1_lane2 == 1) & (pause_2_lane2 == 1) & (pause_3_lane2 == 1)):
            GPIO.output(led_pin_3, GPIO.HIGH)
            cv2.putText(frame2, 'M-P-YES', (300, 100),
                        cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)
            GPIO.output(led_pin_4, GPIO.HIGH)
            GPIO.output(led_pin_6, GPIO.LOW)

            cv2.putText(frame2, 'M-V-NO', (300, 60),
                        cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)
            count_t_1_lane2 = 0
            count_t_3_lane2 = 0
        elif ((pause_1_lane2 == 0) & (pause_2_lane2 == 1) & (pause_3_lane2 == 1)):
            GPIO.output(led_pin_3, GPIO.HIGH)
            cv2.putText(frame2, 'M-P-YES', (300, 100),
                        cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)
            GPIO.output(led_pin_4, GPIO.HIGH)
            GPIO.output(led_pin_6, GPIO.LOW)

            cv2.putText(frame2, 'M-V-NO', (300, 60),
                        cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)
            count_t_1_lane2 = 0
            count_t_3_lane2 = 0

        else:
            GPIO.output(led_pin_3, GPIO.LOW)
            GPIO.output(led_pin_4, GPIO.LOW)
            GPIO.output(led_pin_6, GPIO.HIGH)

            count_t_1_lane2 = 0
            count_t_3_lane2 = 0


####
    # waiting output lane 1
    if ret2:
        if ((pause_1 == 1) & (pause_2 == 0) & (pause_3 == 0)):
            # if (count_t_1 > 2):
            if count_t_1 == 5:
                GPIO.output(led_pin_1, GPIO.LOW)
                GPIO.output(led_pin_5, GPIO.LOW)
                GPIO.output(led_pin_2, GPIO.LOW)
            if count_t_1 == 10:
                GPIO.output(led_pin_1, GPIO.HIGH)
                GPIO.output(led_pin_5, GPIO.HIGH)
                GPIO.output(led_pin_2, GPIO.LOW)
                count_t_1 = 0
                count_t_3 = 0

        elif ((pause_3 == 1) & (pause_2 == 0) & (pause_1 == 0)):

            if count_t_3 == 5:
                GPIO.output(led_pin_1, GPIO.LOW)
                GPIO.output(led_pin_5, GPIO.LOW)
                GPIO.output(led_pin_2, GPIO.LOW)
            if count_t_3 == 10:
                GPIO.output(led_pin_1, GPIO.HIGH)
                GPIO.output(led_pin_5, GPIO.HIGH)
                GPIO.output(led_pin_2, GPIO.LOW)
                count_t_3 = 0
                count_t_3 = 0

        elif ((pause_1 == 0) & (pause_2 == 1) & (pause_3 == 0)):
            GPIO.output(led_pin_2, GPIO.HIGH)
            GPIO.output(led_pin_1, GPIO.HIGH)
            GPIO.output(led_pin_5, GPIO.LOW)
            count_t_1 = 0
            count_t_3 = 0

        elif ((pause_1 == 1) & (pause_2 == 1) & (pause_3 == 0)):
            GPIO.output(led_pin_2, GPIO.HIGH)
            GPIO.output(led_pin_1, GPIO.HIGH)
            GPIO.output(led_pin_5, GPIO.LOW)
            count_t_1 = 0
            count_t_3 = 0

        elif ((pause_3 == 1) & (pause_1 == 1) & (pause_2 == 0)):
            if (count_t_3 == 5 or count_t_1 == 5):
                GPIO.output(led_pin_1, GPIO.LOW)
                GPIO.output(led_pin_5, GPIO.LOW)
                GPIO.output(led_pin_2, GPIO.LOW)
            if (count_t_3 == 10 or count_t_1 == 10):
                GPIO.output(led_pin_1, GPIO.HIGH)
                GPIO.output(led_pin_5, GPIO.HIGH)
                GPIO.output(led_pin_2, GPIO.LOW)
                count_t_1 = 0
                count_t_3 = 0
        elif ((pause_3 == 1) & (pause_1 == 1) & (pause_2 == 1)):
            GPIO.output(led_pin_2, GPIO.HIGH)
            GPIO.output(led_pin_1, GPIO.HIGH)
            GPIO.output(led_pin_5, GPIO.LOW)
            count_t_1 = 0
            count_t_3 = 0

        elif ((pause_1 == 0) & (pause_2 == 1) & (pause_3 == 1)):
            GPIO.output(led_pin_2, GPIO.HIGH)
            GPIO.output(led_pin_1, GPIO.HIGH)
            GPIO.output(led_pin_5, GPIO.LOW)
            count_t_1 = 0
            count_t_3 = 0
        else:

            GPIO.output(led_pin_1, GPIO.LOW)
            GPIO.output(led_pin_2, GPIO.LOW)
            GPIO.output(led_pin_5, GPIO.HIGH)
            count_t_1 = 0
            count_t_3 = 0

    cv2.imshow("Image", frame1)
    cv2.imshow("image2", frame2)

    if cv2.waitKey(1) & 0xFF == ord('x'):
        break


# window.close()
cv2.destroyAllWindows()
GPIO.cleanup()
cap.release()
cap2.release()
