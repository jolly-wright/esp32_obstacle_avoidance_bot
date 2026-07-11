from machine import Pin, PWM, time_pulse_us
import time

############
#MOTOR PINS#
############

ENA = PWM(Pin(0))
IN1 = Pin(1, Pin.OUT)
IN2 = Pin(2, Pin.OUT)
ENB = PWM(Pin(5))
IN3 = Pin(3, Pin.OUT)
IN4 = Pin(4, Pin.OUT)
ENA.freq(1000)
ENB.freq(1000)
SPEED = 45000

#######
#SERVO#
#######

servo = PWM(Pin(15))
servo.freq(50)

############
#ULTRASONIC#
############

trig = Pin(16, Pin.OUT)
echo = Pin(17, Pin.IN)

################
#SERVO FUNCTION#
################

def set_servo(angle):
    # 0° -> 500us
    # 180° -> 2500us
    us = 500 + (angle / 180) * 2000
    duty = int(us * 65535 / 20000)
    servo.duty_u16(duty)
    time.sleep(0.35)

###################
#DISTANCE FUNCTION#
###################

def distance():
    trig.low()
    time.sleep_us(2)
    trig.high()
    time.sleep_us(10)
    trig.low()
    duration = time_pulse_us(echo, 1, 30000)
    if duration < 0:
        return 999
    dist = duration * 0.0343 / 2
    return dist

#################
#MOTOR FUNCTIONS#
#################

def stop():
    ENA.duty_u16(0)
    ENB.duty_u16(0)

def forward():
    IN1.high()
    IN2.low()
    IN3.high()
    IN4.low()
    ENA.duty_u16(SPEED)
    ENB.duty_u16(SPEED)

def backward():
    IN1.low()
    IN2.high()
    IN3.low()
    IN4.high()
    ENA.duty_u16(SPEED)
    ENB.duty_u16(SPEED)

def left():
    IN1.low()
    IN2.high()
    IN3.high()
    IN4.low()
    ENA.duty_u16(SPEED)
    ENB.duty_u16(SPEED)

def right():
    IN1.high()
    IN2.low()
    IN3.low()
    IN4.high()
    ENA.duty_u16(SPEED)
    ENB.duty_u16(SPEED)

######
#SCAN#
######

CENTER = 90
LEFT = 120
RIGHT = 60

def scan():
    set_servo(LEFT)
    leftDist = distance()
    set_servo(RIGHT)
    rightDist = distance()
    set_servo(CENTER)
    return leftDist, rightDist

#######
#START#
#######

set_servo(CENTER)
while True:
    d = distance()
    print("Front:", d)
    if d > 25:
        forward()
    else:
        stop()
        time.sleep(0.2)
        leftDist, rightDist = scan()
        print("Left :", leftDist)
        print("Right:", rightDist)
        backward()
        time.sleep(0.45)
        stop()
        if leftDist > rightDist:
            left()
            time.sleep(0.55)
        else:
            right()
            time.sleep(0.55)
        stop()
    time.sleep(0.05)