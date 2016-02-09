# -*- coding: utf-8 -*-    
# CODE for the Compulsivity Game
# Date: 29.08.2013
# Last change: 16.10.2013

### GET THINGS SET UP

# Import libraries
import pygame, os, time, string
from cstcg_buttons import CSTCGButton as TaskButton
from pygame.locals import *
import numpy
import random 
import sys
pygame.init()
import pdb
from time import strftime,localtime
from pygame import gfxdraw

class ChoiceTask():
    print "I'm here"
    # Define a full-screen display for the paradigm
    screen = pygame.display.set_mode((pygame.display.Info().current_w,pygame.display.Info().current_h))
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    # screen_width = 900
    # screen_height = 600
    # screen = pygame.display.set_mode((screen_width,screen_height))

    center_x = screen_width/2
    left_x = screen_width/20
    right_x = screen_width*9/10
    left_center_x = screen_width/4
    right_center_x = 3*screen_width/4
    top_y = screen_height/10
    center_y = screen_height/2
    bottom_y = 2*screen_height/3
    banner_y = screen_height/6

    def __init__(self, **kwds):
    
        # Position the display flush against the upper right corner
        x = 100
        y = 0
        os.environ['SDL_VIDEO_WINDOW_POS']= '%d,%d' % (x,y) # screen position

        # # Access outputfile
        # of = open(output_file, 'w')

        # Define 3 system fonts
        try:
            self.title = pygame.font.Font('./fonts/GenBasB.ttf',70)
            self.header = pygame.font.Font('./fonts/Lobster.ttf',60)
            self.button = pygame.font.Font('./fonts/GenBasB.ttf',30)
            self.body = pygame.font.Font('./fonts/OpenSans-Light.ttf',20)
            self.instruction = pygame.font.Font('./fonts/OpenSans.ttf',30)
            self.choice_text = pygame.font.Font('./fonts/OpenSans-Light.ttf',30)
        except:
            self.title = pygame.font.SysFont("Calibri",40)
            self.header = pygame.font.SysFont("Calibri",25)
            self.body = pygame.font.SysFont("Calibri",15)
            self.button = pygame.font.SysFont("Calibri",25)


        self.background_color =  ( 232, 236, 237)
        self.text_color       =  (  50,  50,  50)
        self.highlight_teal   =  (  56, 146, 137)
        self.header_color     =  ( 205,  73,  57)
        self.highlight_red    =  ( 205,  73,  57)
        self.button_color     =  (  58, 138, 112)
        self.white            =  ( 255, 255, 255)


        self.press_sound = pygame.mixer.Sound('./sounds/buttonpress.wav')
        self.press_sound.set_volume(0.2)
        self.game_over_sound = pygame.mixer.Sound('./sounds/gameover.wav')

        self.RTB = True

        self.__dict__.update(kwds)

        self.screen.fill(self.background_color)
        self.screen.fill(self.background_color)

    # Truncates a written line for wrapped texts (in the final questionnaire)                                                                                       
    def truncline(self,text, font, maxwidth):
        real=len(text)
        stext=text
        l=font.size(text)[0]
        cut=0
        a=0
        done=1
        while l > maxwidth:
            a=a+1
            n=text.rsplit(None, a)[0]
            if stext == n:
                cut += 1
                stext= n[:-cut]
            else:
                stext = n
                l=font.size(stext)[0]
                real=len(stext)
                done=0
        return real, done, stext

    # Wraps a line to the width desired
    def wrapline(self, text='', font=None, maxwidth=int(screen_width*0.9)):
        done=0
        wrapped=[]

        while not done:
            nl, done, stext=self.truncline(text, font, maxwidth)
            wrapped.append(stext.strip())
            text=text[nl:]
        return wrapped
 
    def wait_fun(self,milliseconds):
        nowtime = pygame.time.get_ticks()
        while pygame.time.get_ticks()-nowtime < milliseconds:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

    def center_text(self,text=None,x_offset=0,y_offset=0, center_x=center_x, center_y=center_y):
        textpos = text.get_rect()
        textpos.centerx = center_x+x_offset
        textpos.centery = center_y+y_offset
        self.screen.blit(text,textpos)
        pygame.display.update()

    def surf_center_text(self, text, destsurf,destsurfposx,destsurfposy):
        textpos = text.get_rect()
        textpos.centerx = destsurf.centerx+destsurfposx
        textpos.centery = destsurf.centery+destsurfposy
        self.screen.blit(text,textpos)
  
    def text_screen(self,text,wait_time=0, font=None,font_color=None, valign='center', halign='center',x_displacement=0,y_displacement=100, maxwidth=int(screen_width*0.9)):
        # Text input should be raw text 
        if font is None:
            font = self.instruction 
        if font_color is None:
            font_color = self.text_color

        if len(text) != 0:
            yoffset = int(1.1*font.size(text)[1])
            formatted_text = self.wrapline(text=text,font=font,maxwidth=maxwidth)
            num_lines = int(len(formatted_text)/2)
            
            if valign == 'top':
                center_y = self.center_y-num_lines*2*yoffset + y_displacement
            elif valign == 'center':
                center_y = self.center_y + y_displacement
            elif valign == 'bottom':
                center_y = self.bottom_y-num_lines*yoffset + y_displacement

            if halign == 'center':
                center_x = self.center_x + x_displacement
            elif halign == 'right':
                center_x = self.right_center_x + x_displacement
            elif halign == 'left':
                center_x = self.left_center_x + x_displacement

            offset_array = numpy.array(range(-num_lines,num_lines+1))
            offset = yoffset*offset_array

            for j in range(len(formatted_text)):
                rendered_text = font.render(formatted_text[j],True,font_color)
                self.center_text(text=rendered_text,y_offset=offset[j],center_x=center_x, center_y=center_y)
        
        pygame.display.update()
        self.wait_fun(milliseconds=wait_time)

    def create_output_file(self, subject_name):
        # Make a folder with the patients name and the trial number in the output files dir
        filetochoose = 1
        dirmade = False
        foldernum = 0
        while not dirmade:
            dirname = './outputfiles/' + subject_name + '_' + repr(foldernum)
            subdirname = dirname + '/' + repr(filetochoose)
            if not os.path.isdir(dirname):
                os.mkdir('./outputfiles/' + subject_name + '_' + repr(foldernum))
                os.mkdir(subdirname)
                dirmade = True
            elif os.path.isdir(dirname) and not os.path.isdir(subdirname):
                os.mkdir(subdirname)
                dirmade = True
            else:
                foldernum += 1

        # Define output file
        nowstr = strftime("%Y%m%d%H%M%S", localtime()) 

        # Define the output file in the patient folder
        output_file = subdirname + '/output' + nowstr + '.txt'
        matlab_output_file = subdirname + '/output' + nowstr + '.mat'
        self.of = open(output_file, 'w')
        return matlab_output_file

    def text_input(self, message):
        w = 600
        h = 70
        csnamebox = pygame.draw.rect(self.screen,self.white,pygame.Rect((self.center_x-int(w/2), self.center_y-h-100, w, h)), 0)
        yoffset = 25
        if len(message) != 0:
            blitmessage = self.wrapline(text=message,font=self.body,maxwidth=330)
            for j in range(len(blitmessage)):
                self.screen.blit(self.body.render(blitmessage[j],True,self.text_color),\
                    (self.center_x-int(w/2)+10,\
                    self.center_y-h-100+yoffset*j))
            pygame.display.update()


    def subject_information_screen(self):

        self.make_banner(self.body.render("Please enter your information below",True,self.header_color))
        question = "Name"
        current_string = []
        self.text_input(question + ":| " + string.join(current_string,""))
        
        continue_button= TaskButton(rect=(self.center_x-120,self.center_y, 200,70),\
         caption="Continue",  bgcolor=self.button_color, fgcolor=self.background_color, font=self.button)

        continue_button.draw(self.screen)

        pygame.display.update()
        filling = True
        while filling:
            pygame.time.wait(20) 
            if pygame.event.peek(MOUSEBUTTONDOWN) or pygame.event.peek(MOUSEBUTTONUP) or pygame.event.peek(QUIT) or pygame.event.peek(KEYDOWN):
                for event in pygame.event.get():
                    if event.type==MOUSEBUTTONDOWN and len(current_string)>0:
                        continue_button.handleEvent(event)
                    elif event.type==MOUSEBUTTONUP and len(current_string)>0:
                        if 'click' in continue_button.handleEvent(event): 
                            self.press_sound.play()
                            filling=False
                    elif event.type == KEYDOWN:
                        if event.key == K_BACKSPACE:
                            current_string = current_string[0:-1]
                        elif event.key == K_MINUS:
                            current_string.append("_")
                        elif event.key != 13:
                            current_string.append(event.unicode)
                        elif event.key ==  K_RETURN:
                            filling = False
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    self.text_input(question + ": " + string.join(current_string,""))

                continue_button.draw(self.screen)
                pygame.display.update()
                # self.wait_fun(milliseconds=300)
            elif 0 < round(time.time()*1000) % 700 < 350 and len(current_string)==0:
                self.text_input(question + ": ")
            elif 350 < round(time.time()*1000) % 700 < 700 and len(current_string)==0:
                self.text_input(question + ":| ")
        return (string.join(current_string,""))

    def make_banner(self,text):
        textpos = text.get_rect()
        textpos.centerx = self.center_x
        textpos.centery = self.banner_y
        self.screen.blit(text,textpos)
        pygame.display.update()

    def subtitle(self,text):
        textpos = text.get_rect()
        textpos.centerx = self.center_x
        textpos.centery = self.banner_y+100
        self.screen.blit(text,textpos)
        pygame.display.update()


    def log(self,text):
        self.of.write(text + '\n')

    def game_music(self, onoff):
        if onoff == 'on':
            self.music.play(100,0)
        elif onoff == 'off':
            self.loopmusic.stop()

    # Main screen fixation point
    def attn_screen(self, attn=None,wait_time=3000):
        self.screen.fill(self.background_color)
        if attn is None:
            attn = pygame.image.load('./images/attn_cross.png').convert_alpha()
        self.screen.blit(attn,(self.screen_width/2 - attn.get_width()/2,self.screen_height/2 - attn.get_height()/2))
        pygame.display.update()
        self.of.write('Attention screen on ' + repr(time.time()) + '\n')
        self.wait_fun(milliseconds=wait_time)
        self.of.write('Attention screen off ' + repr(time.time()) + '\n')

    def blank_screen(self, time=0):
        self.screen.fill(self.background_color)
        pygame.display.update()
        self.wait_fun(milliseconds=time)
        
    def choice_screen(self,choice_image1=None, choice_text1=None, button_txt1="Choose", choice_image2=None, choice_text2=None, button_txt2=None):
       
        # This function sets up the canonical choice screen. Can be given on or two images.
        if choice_image1 is not None and choice_image2 is not None:
            self.screen.blit(choice_image1,(self.left_center_x,self.top_y))
            self.screen.blit(choice_image2,(self.right_center_x,self.top_y))
        elif choice_image1 is not None and choice_image2 is None:
            self.screen.blit(choice_image1,(self.center_x-choice_image1.get_width()/2,\
                self.top_y-choice_image1.get_height()/2))
        elif choice_image2 is not None and choice_image1 is None:
            self.screen.blit(choice_image1,(self.center_x-choice_image2.get_width()/2,\
                self.top_y-choice_image2.get_height()/2))

        # Write text (TODO: add condition for only one piece of text)
        if choice_text1 is not None:
            self.text_screen(text=choice_text1,font=self.choice_text,
             maxwidth=int(self.screen_width/3),valign='bottom',halign='left',wait_time=None)

        if choice_text2 is not None:
            self.text_screen(text=choice_text2,font=self.choice_text,
             maxwidth=int(self.screen_width/3),valign='bottom',halign='right',wait_time=None)

        # Make buttons
        if button_txt1 is not None and button_txt2 is not None:
            left_button = TaskButton(rect=(self.left_center_x-70,self.bottom_y+70, 140,70),\
             caption=button_txt2,  fgcolor=self.background_color, bgcolor=self.button_color, font=self.button)
            right_button = TaskButton(rect=(self.right_center_x-60,self.bottom_y+70, 140,70),\
             caption=button_txt1, fgcolor=self.background_color, bgcolor=self.button_color, font=self.button)
            left_button.draw(self.screen)
            right_button.draw(self.screen)
        elif button_txt1 is not None and button_txt2 is None:
            right_button = TaskButton(rect=(self.center_x-60,self.bottom_y+70, 140,70),\
             caption=button_txt1, fgcolor=self.background_color, bgcolor=self.button_color, font=self.button)
            right_button.draw(self.screen)
        elif button_txt2 is not None and button_txt1 is None:
            left_button = TaskButton(rect=(self.center_x-70,self.bottom_y+70, 140,70),\
             caption=button_txt2,  fgcolor=self.background_color, bgcolor=self.button_color, font=self.button)
            left_button.draw(self.screen)

        pygame.display.update()
        self.of.write('ChoiceScreen on ' + repr(time.time()) + '\n')
        
        # Choice phase
        playing = True
        while playing:
            pygame.time.wait(20)
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()

                if event.type in (MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN):
                    if button_txt2 is not None:
                        if 'click' in left_button.handleEvent(event):   
                            self.press_sound.play()               
                            self.log('Left button clicked \n')
                            button_clicked = ['left']
                            playing = False
                    if button_txt1 is not None:
                        if 'click' in right_button.handleEvent(event):
                            self.press_sound.play() 
                            button_clicked = ['right']
                            self.log('Right button clicked \n')
                            playing = False
                elif event.type == KEYDOWN:
                    pressedKey = pygame.key.name(event.key)
                    if pressedKey == 'left':
                        self.press_sound.play() 
                        left_button.buttonDown = True;
                        left_button.draw(self.screen)
                        pygame.display.update()
                        button_clicked = ['left']
                        self.wait_fun(200)
                        playing = False
                    elif pressedKey == 'right':
                        self.press_sound.play() 
                        right_button.buttonDown = True;
                        right_button.draw(self.screen)
                        pygame.display.update()
                        button_clicked = ['right']
                        self.wait_fun(200)
                        playing = False

            if button_txt1 is not None and button_txt2 is not None:           
                left_button.draw(self.screen)
                right_button.draw(self.screen)
            elif button_txt1 is not None and button_txt2 is None:
                right_button.draw(self.screen)
            elif button_txt2 is not None and button_txt1 is None:
                left_button.draw(self.screen)
            pygame.display.update()

        self.wait_fun(milliseconds=300)    
        return button_clicked

        
    def button_screen(self,choice_image=None, choice_text=None, button_txt=None, x_offset=0, y_offset=0):
        
        self.screen.blit(choice_image,(self.center_x-x_offset-choice_image.get_width()/2,\
        self.center_y+y_offset-choice_image.get_height()/2))

        if choice_text is not None:
            self.text_screen(text=choice_text,font=self.choice_text,
                 maxwidth=int(self.screen_width/3),valign='bottom',halign='left',wait_time=None)

        center_button = TaskButton(rect=(self.center_x-70,self.bottom_y+160, 140,70),\
             caption=button_txt,  fgcolor=self.button_color, bgcolor=self.background_color, font=self.button)

        center_button.draw(self.screen)
        pygame.display.update()
        self.of.write('ButtonScreen on ' + repr(time.time()) + '\n')
        
        # Choice phase
        playing = True
        while playing:
            pygame.time.wait(20)
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()

                if event.type in (MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN):
                    if button_txt is not None:
                        if 'click' in center_button.handleEvent(event):   
                            self.press_sound.play()              
                            self.log('Left button clicked \n')
                            button_clicked = ['left']
                            playing = False
                elif event.type == KEYDOWN:
                    pressedKey = pygame.key.name(event.key)
                    if pressedKey == 'left':
                        center_button.buttonDown = True;
                        center_button.draw(self.screen)
                        pygame.display.update()
                        button_clicked = ['left']
                        self.wait_fun(200)
                        playing = False
            center_button.draw(self.screen)
            pygame.display.update()

        self.wait_fun(milliseconds=300)    
        return button_clicked


    # Exit screen
    def exit_screen(self, exit_text="Exiting", font=None,font_color=None):
        self.blank_screen(time=10)
        
        if font is None:
            font = self.header

        if font_color is None:
            font_color = self.text_color

        # Text input should be raw text 
        self.text_screen(text=exit_text, font=self.header, font_color=font_color)
        pygame.display.update()
        self.game_over_sound.play()
        self.wait_fun(milliseconds=3000)
        self.log('Exiting game ' + repr(time.time()))
        exit()

