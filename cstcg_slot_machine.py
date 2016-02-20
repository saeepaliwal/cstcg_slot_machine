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

testing = False
response_box = True
currency = 'points'

# Initialize response box:
if response_box: 
    if platform.system() == 'Darwin': # Mac
        RTB = serial.Serial(baudrate=115200, port='/dev/tty.usbserial-142', timeout=0)
    elif platform.system() == 'Windows': # Windows
        RTB = serial.Serial(baudrate=115200, port='COM4', timeout=0)

# Define special characters
ae = u"ä";
ue = u"ü";

# Define colors:
GOLD   = ( 254, 195,  13)

leversound = pygame.mixer.Sound('./sounds/lever.wav')
background_music = pygame.mixer.Sound('./sounds/machine1_music.wav')
background_music.set_volume(0.1)

c = ChoiceTask(background_color=( 20, 20, 20), 
    title  = pygame.font.Font('./fonts/Lobster.ttf', 60),
    body  = pygame.font.Font('./fonts/Oswald-Bold.ttf', 30),
    header = pygame.font.Font('./fonts/Oswald-Bold.ttf', 40),
    instruction = pygame.font.Font('./fonts/GenBasR.ttf',30),
    choice_text = pygame.font.Font('./fonts/GenBasR.ttf', 30),
    button = pygame.font.Font('./fonts/Oswald-Bold.ttf',30))

(subjectname) = c.subject_information_screen()
subject = subjectname.replace(" ","")
matlab_output_file = c.create_output_file(subjectname)

# Task trace:
result_sequence = []
wheel_hold_bool = [False, True]
block_order = []
control_seq = []

# Pull in training trials:
with open ('taskBackend_training.txt','r') as f:
        probability_trace = f.read().replace('\n', '')
result_sequence = probability_trace.split(',')

# Randomize blocks for real trials
for j in range(4):
    block_order.append(random.randint(1,4));

for b in block_order:
    with open ('taskBackend_' + str(b) + '.txt','r') as f:
        probability_trace = f.read().replace('\n', '')
    block_sequence = probability_trace.split(',')
    if block_sequence[0] == 'CONTROL':
        wheel_hold_bool.append(True)
        control_seq.append(1)
    elif block_sequence[0] == 'NOCONTROL':
        wheel_hold_bool.append(False)
        control_seq.append(0)
    block_sequence = block_sequence[1:]
    result_sequence = result_sequence + block_sequence

NUM_TRIALS = len(result_sequence)-1

# Define dictionary of task attributes:
task = {'bet_size': np.zeros(NUM_TRIALS).astype('int'),
        'account': np.zeros(NUM_TRIALS).astype('int'),
        'did_gamble': np.zeros(NUM_TRIALS).astype('int'),
        'result_sequence': result_sequence,
        'machine_sequence': np.zeros(NUM_TRIALS).astype('int'),
        'reward_grade': np.zeros(NUM_TRIALS).astype('int'),
        'winloss': np.zeros(NUM_TRIALS).astype('int'),
        'pressed_stop': np.zeros(NUM_TRIALS).astype('int'),
        'guess_trace': np.zeros(NUM_TRIALS).astype('int'),
        }

# Start with initial account and machine
task['account'][0] = 500
task['currency'] = currency
task['block_order'] = block_order
task['control_seq'] = control_seq

# Times
task['inter_wheel_interval'] = 700
task['win_banner_interval'] = 1500
task['win_screen_interval'] = 1500

# Individual wheel hold buttons:
task['wheel_hold_buttons'] = wheel_hold_bool[0]
task['wheel1'] = False
task['wheel2'] = False
task['wheel3'] = False

task['training'] = True

# Set up initial screen 
positions, buttons, sizes = get_screen_elements(c, task)

if not testing:
    instruction_screen(c,positions,sizes,RTB)
    welcome_screen(c)

for trial in range(NUM_TRIALS):   

    if trial == 0:
        if not testing:
            begin_training_screen(c)
            background_music.play(100,0)

    if trial < 10:
        task['machine'] = 5
        task['wheel_hold_buttons'] = wheel_hold_bool[0]
    elif 10 <= trial <= 20:
        task['machine'] = 6
        task['wheel_hold_buttons'] = wheel_hold_bool[1]
    elif trial == 21:
        if not testing:
            task['training'] = False
            background_music.stop()
            end_training_screen(c)
            task['account'][trial] = 2000
            task['machine'] = block_order[0]
            task['current_block'] = block_order[0]
            task['wheel_hold_buttons'] = wheel_hold_bool[2]
            welcome_screen(c)
            background_music.play(100,0)
            c.log('Starting block ' + str(block_order[0]) + ' at ' + repr(time.time()) + '\n')
            c.log('Machine ' + str(task['machine']) + 'at ' + repr(time.time()) + '\n')
            c.log('Wheel hold buttons are ' + str(wheel_hold_bool[3]) + ' at ' + repr(time.time()) + '\n')
    elif trial == 65:
        change_machine_screen(c)
        task['machine'] = block_order[1]
        task['current_block'] = block_order[1]
        task['wheel_hold_buttons'] = wheel_hold_bool[3]
        c.log('Starting block ' + str(block_order[1]) + ' at ' + repr(time.time()) + '\n')
        c.log('Machine ' + str(task['machine']) + ' at ' + repr(time.time()) + '\n')
        c.log('Wheel hold buttons are ' + str(wheel_hold_bool[2]) + ' at ' + repr(time.time()) + '\n')
    elif trial == 110:
        change_machine_screen(c)
        task['machine'] = block_order[2]
        task['current_block'] = block_order[2]
        task['wheel_hold_buttons'] = wheel_hold_bool[4]
        c.log('Starting block ' + str(block_order[2]) + ' at ' + repr(time.time()) + '\n')
        c.log('Machine ' + str(task['machine']) + 'at ' + repr(time.time()) + '\n')
        c.log('Wheel hold buttons are ' + str(wheel_hold_bool[3]) + ' at ' + repr(time.time()) + '\n')
    elif trial == 155:
        change_machine_screen(c)
        task['machine'] = block_order[3]
        task['current_block'] = block_order[3]
        task['wheel_hold_buttons'] = wheel_hold_bool[5]
        c.log('Starting block ' + str(block_order[3]) + ' at ' + repr(time.time()) + '\n')
        c.log('Machine ' + str(task['machine']) + 'at ' + repr(time.time()) + '\n')
        c.log('Wheel hold buttons are ' + str(wheel_hold_bool[5]) + ' at ' + repr(time.time()) + '\n')
    next_trial = False


    # Click everything forward
    task['bet_sequence'] = []
    task['trial'] = trial
    task['machine_sequence'][trial] = task['machine']
    task['ungrey_wheel2'] = False
    task['ungrey_wheel3'] = False

    # Set stage and selector
    task['trial_stage'] = 'guess'
    selector_pos = 1

    if trial > 0:
        task['account'][trial] = task['account'][trial-1] 

    task['reward_grade'][trial] = int(str(result_sequence[trial])[1])

    if task['account'][trial] < 5:
        savemat(matlab_output_file,task)
        c.exit_screen("Unfortunately you lost your money and the game is over! Thanks for playing!", font=c.title, font_color=GOLD)

    # EEG: Trial on
    if not task['training']:
        c.log('Trial ' + str(trial) + ': Starting trial now, with condition ' + str(task['current_block']) + ' at ' +  repr(time.time()) + '\n')
    eeg_trigger(c,task,'trial')

    buttons, task = draw_screen(c, positions, buttons, sizes, task)
    selector_pos, selected = selector(c,task,positions,0,selector_pos)

    # EEG: Guess on
    eeg_trigger(c,task,'guess_on')

    while not next_trial:  
        pygame.time.wait(20)
        key_press = RTB.read() 
        if len(key_press):
            key_index = ord(key_press)

            if task['trial_stage'] == 'guess':
                selected = False
                draw_screen(c, positions, buttons, sizes, task)
                selector_pos, selected = selector(c,task,positions,key_index,selector_pos)
                if selected:              
                    eeg_trigger(c,task,'pressed_guess')
                    task['guess_trace'][trial] = selector_pos
                    task['trial_stage'] = 'bet'
                    buttons, task = draw_screen(c, positions, buttons, sizes, task)
            elif task['trial_stage'] != 'guess':
                events = process_rtb(positions,key_index, task['trial_stage'], task['wheel_hold_buttons'])
                if len(events) > 0:
                    pygame.event.post(events[0])
                    pygame.event.post(events[1])

            for event in pygame.event.get():
                if event.type in (MOUSEBUTTONUP, MOUSEBUTTONDOWN):
                    if 'click' in buttons['add_five'].handleEvent(event):  
                        c.press_sound.play()
                        task['trial_stage'] = 'bet'
                        task['bet_size'][trial] += 10
                        eeg_trigger(c,task,'bet+')
                        task['bet_sequence'].append(10)
                        task = update_account(c,positions, sizes, task)
                        display_assets(c,positions,sizes,task)
                        c.log('Trial ' + str(trial) + ': Added 10 to bet. ' + repr(time.time()) + '\n')
                    elif 'click' in buttons['clear'].handleEvent(event):
                        c.press_sound.play()
                        if len(task['bet_sequence']) > 0:   
                            c.log('Trial ' + str(trial) + ': Clearing ' + str(task['bet_sequence'][-1]) + 'from bet. ' + repr(time.time()) + '\n')
                            task['trial_stage'] = 'clear'
                            eeg_trigger(c,task,'bet-')
                            task = clear(c,task)
                            task = update_account(c,positions, sizes, task)
                            display_assets(c,positions,sizes,task)
                    elif 'click' in buttons['pull'].handleEvent(event):
                        if task['bet_size'][trial] > 0:
                            task['trial_stage'] = 'pull'
                            buttons, task = draw_screen(c, positions, buttons, sizes, task)
                            buttons['pull'].draw(c.screen)
                            pygame.display.update()
                            eeg_trigger(c,task,'pressed_pull')
                            leversound.play()
                            c.wait_fun(100)
                            leversound.stop()
                            c.log('Trial ' + str(trial) + ': Pulling wheels ' + repr(time.time()) + '\n')
                            c.log('Summary Trial' + str(trial) + ': Bet:' + str(task['bet_size'][trial]) + 'Account: ' + str([task['account'][trial]]))
                            task['trial_stage'] = 'result'
                           
                            if task['wheel_hold_buttons']:
                                individual_wheel_spin(c,positions,buttons,sizes,task, RTB)
                            else:
                                spin_wheels(c, positions, buttons, task,RTB)
                                show_result(c,positions,buttons,task)

                            task = process_result(c,positions,buttons,sizes,task, RTB)  
                            next_trial = True
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if not next_trial:
                    for key in buttons:
                        buttons[key].draw(c.screen)
                    pygame.display.update()

                savemat(matlab_output_file,task)

savemat(matlab_output_file,task)
background_music.stop()
c.exit_screen("That ends the game! Thank you so much for playing! Goodbye!", font=c.title, font_color=GOLD)



