import numpy as np
import cv2
import random
from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


GPIO.setup([8,10], GPIO.OUT)

def setServoAngle(x, y):
    pwm = GPIO.PWM(8, 50)
    pwm.start(8)
    pwm_l= GPIO.PWM(10, 50)
    pwm_l.start(10)
    x = x / 18 + 3
    y = y / 18 + 3
    pwm.ChangeDutyCycle(x)
    pwm_l.ChangeDutyCycle(y)
    sleep(0.2)
    pwm.stop()
    pwm_l.stop()



face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)

width = cap.get(3)
height = cap.get(4)

new_x = 0
new_y = 0



while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h),
                      (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]
        print(new_x, new_y)
        new_x = int(x / width * 256)
        new_y = int(y / height * 256)
        setServoAngle(new_x,new_y)

    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
