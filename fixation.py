# -*- coding: utf-8 -*-    
from __future__ import division
import serial
from choice_task import ChoiceTask
import pygame
from pygame.locals import *
from cstcg_slot_functions import *
import random
import numpy as np
from scipy.io import savemat
import platform
pygame.init()


trigger_off = 0

if platform.system() == 'Windows': # Windows
    from ctypes import windll
    port = windll.inpoutx64
    address = 45072

if platform.system() == 'Darwin': # Mac
    RTB = serial.Serial(baudrate=115200, port='/dev/tty.usbserial-142', timeout=0)
elif platform.system() == 'Windows': # Windows
    RTB = serial.Serial(baudrate=115200, port='COM4', timeout=0)
#Send trigger
# port.Out32(address,1)
# core.wait(0.05)
# port.Out32(address,trigger_off)

attn = pygame.image.load('./images/attn_cross.png')

c = ChoiceTask(background_color=( 20, 20, 20), 
    title  = pygame.font.Font('./fonts/Lobster.ttf', 60),
    body  = pygame.font.Font('./fonts/Oswald-Bold.ttf', 30),
    header = pygame.font.Font('./fonts/Oswald-Bold.ttf', 40),
    instruction = pygame.font.Font('./fonts/GenBasR.ttf',30),
    choice_text = pygame.font.Font('./fonts/GenBasR.ttf', 30),
    button = pygame.font.Font('./fonts/Oswald-Bold.ttf',30))


c.text_screen('Press 1 to continue', font=c.title, font_color=(255,255,255), valign='top', y_displacement= -45, wait_time=100)  
waiting = True
while waiting:
    key_press = RTB.read() 
    if len(key_press):
        key_index = ord(key_press)

        if key_index == 1:

            #Send trigger
            if platform.system() == 'Windows': 
                port.Out32(address,1)
                core.wait(0.05)
                port.Out32(address,trigger_off)
            elif platform.system() == 'Darwin':
                print "Sent start trigger"

            c.attn_screen(attn=None,wait_time=240000)

            waiting = False

#Send trigger
print "Done"

if platform.system() == 'Windows': 
    port.Out32(address,2)
    core.wait(0.05)
    port.Out32(address,trigger_off)
elif platform.system() == 'Darwin':
    print "Sent endtrigger"
