import RPi.GPIO as GPIO
import time
import sys
import select
import termios
import tty
import pygame
from datetime import datetime
from display import Display
from deltatime import Deltatime

class Puzzlebox:

    state = 'START'
    last_state = 'START'
    menu_activated = False
    state_menu = ['LANGUAGE', 'RESET', 'RESUME']
    state_menu_index = 0
    resume_state = ''

    
    lang = 0
    lang_select = 0
    languages = ['French', 'German']

    display = None
    crono = 0

    # GPIO const
    IO_MENU = 13
    IO_SELECT = 7
    IO_ENTER = 17

    IO_LED_RED_JACK = 8
    IO_LED_GREEN_JACK = 11

    IO_LED_RED_SWITCH = 12
    IO_LED_GREEN_SWITCH = 6

    IO_BUTTON_1 = 10
    IO_BUTTON_2 = 25
    IO_BUTTON_3 = 26
    IO_BUTTON_4 = 19

    IO_LID = 20

    IO_OUT_JACK_1 = 24
    IO_OUT_JACK_2 = 22
    IO_OUT_JACK_3 = 23
    IO_OUT_JACK_4 = 27    
    IO_OUT_JACK_5 = 9

    IO_IN_JACK_1 = 15
    IO_IN_JACK_2 = 4
    IO_IN_JACK_3 = 14
    IO_IN_JACK_4 = 3    
    IO_IN_JACK_5 = 2

    def start(self):

        self.state = 'START'
        self.display = Display()
        self.initHardware()
        self.gameLoop()
        curses.wrapper()


    def initGame(self):

        GPIO.output(self.IO_LED_RED_JACK, GPIO.HIGH)  # Met le GPIO 17 à l’état haut (3.3V)
        GPIO.output(self.IO_LED_GREEN_JACK, GPIO.LOW)   # Met le GPIO 17 à l’état bas (0V)

        GPIO.output(self.IO_LED_RED_SWITCH, GPIO.HIGH)  # Met le GPIO 17 à l’état haut (3.3V)
        GPIO.output(self.IO_LED_GREEN_SWITCH, GPIO.LOW)   # Met le GPIO 17 à l’état bas (0V)

        self.crono = 0

        self.state = 'ROOM'
        self.play_sound('sound/relaxing.mp3')

    def roomGame(self):

        self.displayCounter()

        if self.is_pressed(self.IO_SELECT):
            self.play_sound('sound/inspiring-emotional.mp3')
            self.state = 'PSYCHOLOGIST'

    def psychologistGame(self):

        self.displayCounter()

        GPIO.output(self.IO_LED_RED_JACK, GPIO.LOW)  # Met le GPIO 17 à l’état haut (3.3V)
        GPIO.output(self.IO_LED_GREEN_JACK, GPIO.HIGH)   # Met le GPIO 17 à l’état bas (0V)

        GPIO.output(self.IO_LED_RED_SWITCH, GPIO.LOW)  # Met le GPIO 17 à l’état haut (3.3V)
        GPIO.output(self.IO_LED_GREEN_SWITCH, GPIO.HIGH)   # Met le GPIO 17 à l’état bas (0V)


        if self.is_pressed(self.IO_SELECT):
            self.crono = 0
            self.state = 'FINAL'


    def displayCounter(self):

        self.crono += Deltatime.tick()
        counter = datetime(1, 1, 1) + Deltatime.delta(seconds=self.crono)
        heure = counter.strftime("%M:%S")
        self.display.setText(heure)

    def finalGame(self):

        self.crono += Deltatime.tick()
        self.display.setText(" Bravo c'est fini ")
        if (self.crono > 10):
            self.crono = 0
            self.state = 'INIT'

    def checkIfMenu(self):

        if self.is_pressed(self.IO_MENU):
            self.resume_state = self.state
            self.state = 'MENU_INIT'

    def menuInit(self):

        self.display.setText("MENU")
        time.sleep(3)


        self.state_menu_index = 0
        self.state = self.state_menu[self.state_menu_index]

        
    def menuLanguage(self):

        if self.menu_activated:

            self.display.setText(self.languages[self.lang_select])

            if self.is_pressed(self.IO_ENTER):
               self.lang = self.lang_select
               self.menu_activated = False

            if self.is_pressed(self.IO_SELECT):
                self.lang_select += 1
                if (self.lang_select > len(self.languages) - 1):
                    self.lang_select = 0

            
        else:
            self.display.setText("LANGUAGE")

            self.switchMenu()

            if self.is_pressed(self.IO_ENTER):
                self.lang_select = self.lang
                self.menu_activated = True



    def menuReset(self):
        self.display.setText("RESET")
        if self.is_pressed(self.IO_ENTER):
            self.state = 'INIT'
        else:
            self.switchMenu()


    def menuResume(self):

        self.display.setText("RESUME")

        if self.is_pressed(self.IO_ENTER):
            self.state = self.resume_state
        else:
            self.switchMenu()


    def switchMenu(self):

        if self.is_pressed(self.IO_SELECT):
            self.state_menu_index += 1

        if self.state_menu_index > (len(self.state_menu) - 1):
            self.state_menu_index = 0

        if self.state != self.state_menu[self.state_menu_index]:
            self.state = self.state_menu[self.state_menu_index]
            self.menu_activated = False

            
    def gameLoop(self):

        while(True):

            if (self.state == 'START'):
                self.state = 'INIT'
                
            elif (self.state == 'INIT'):
                self.initGame()

            elif (self.state == 'ROOM'):
                self.roomGame()
                self.checkIfMenu()

            elif (self.state == 'PSYCHOLOGIST'):
                self.psychologistGame()
                self.checkIfMenu()

            elif (self.state == 'FINAL'):
                self.finalGame()
                self.checkIfMenu()

            elif (self.state == 'MENU_INIT'):
                self.menuInit()

            elif (self.state == 'MENU'):
                self.menu()

            elif (self.state == 'LANGUAGE'):
                self.menuLanguage()

            elif (self.state == 'RESET'):
                self.menuReset()

            elif (self.state == 'RESUME'):
                self.menuResume()
                
            if self.state != self.last_state:
                print(self.state)
                self.last_state = self.state
  
            self.display.update()
            Deltatime.update()
            time.sleep(.4)  # pour éviter de saturer le CPU


    def initHardware(self):

        GPIO.setmode(GPIO.BCM)      # Numérotation BCM
        # GPIO en entrée
        GPIO.setup(self.IO_MENU, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.IO_SELECT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.IO_ENTER, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.setup(self.IO_IN_JACK_1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.IO_IN_JACK_2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.IO_IN_JACK_3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.IO_IN_JACK_4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.IO_IN_JACK_5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.setup(self.IO_BUTTON_1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.IO_BUTTON_2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.IO_BUTTON_3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.IO_BUTTON_4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.setup(self.IO_LID, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # GPIO en sortie
        GPIO.setup(self.IO_LED_RED_JACK, GPIO.OUT)
        GPIO.setup(self.IO_LED_GREEN_JACK, GPIO.OUT)
        GPIO.setup(self.IO_LED_RED_SWITCH, GPIO.OUT)
        GPIO.setup(self.IO_LED_GREEN_SWITCH, GPIO.OUT)
    
        GPIO.setup(self.IO_OUT_JACK_1, GPIO.OUT)
        GPIO.setup(self.IO_OUT_JACK_2, GPIO.OUT)
        GPIO.setup(self.IO_OUT_JACK_3, GPIO.OUT)
        GPIO.setup(self.IO_OUT_JACK_4, GPIO.OUT)
        GPIO.setup(self.IO_OUT_JACK_5, GPIO.OUT)

        pygame.mixer.init()

        
    def get_key_nonblocking(self, timeout=0.0):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            r, _, _ = select.select([sys.stdin], [], [], timeout)
            if r:
                return sys.stdin.read(1)
            return None
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    

    def is_pressed(self, io):

        if GPIO.input(io):
            return True

        keytest = 'none'
        if (io == self.IO_SELECT):
            keytest = 'n'
        if (io == self.IO_MENU):
            keytest = 'm'
        if (io == self.IO_ENTER):
            keytest = 'b'

        key = self.get_key_nonblocking(0.01)  # 100 ms timeout
        if key:
            return (key == keytest)
        else:
            return False
        

    def play_sound(self, path):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

        pygame.mixer.music.load(path)
        pygame.mixer.music.play(loops=-1)



        