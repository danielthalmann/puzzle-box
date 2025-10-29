import RPi.GPIO as GPIO
import time
import sys
import select
import termios
import tty
import pygame
import subprocess
from datetime import datetime
from deltatime import Deltatime

class Puzzlebox:

    state = 'START'
    last_state = 'START'
    menu_activated = False
    state_menu = ['LANGUAGE', 'RESET', 'RESUME']
    state_menu_index = 0
    resume_state = ''

    last_display_text = ''
    
    lang = 0
    lang_select = 0
    languages = ['FR', 'DE']

    crono = 0

    process = None

    # GPIO const
    IO_MENU = 13
    IO_SELECT = 7
    IO_ENTER = 17

    IO_LED_RED_JACK = 3 # legacy 8
    IO_LED_GREEN_JACK = 2 # legacy 11

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
    IO_IN_JACK_4 = 8 # legacy 3    
    IO_IN_JACK_5 = 11 # legacy 2

    IO_OUT_LED = 5

    def start(self):

        self.state = 'START'
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

        self.is_jack_resolved()

        self.is_button_pressed()

        if self.is_pressed(self.IO_LID):
            print("boucle")

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
        self.setDisplayText(heure)

    def finalGame(self):

        self.crono += Deltatime.tick()
        self.setDisplayText(" Bravo c'est fini ")
        if (self.crono > 10):
            self.crono = 0
            self.state = 'INIT'

    def checkIfMenu(self):

        if self.is_pressed(self.IO_MENU):
            self.resume_state = self.state
            self.state = 'MENU_INIT'

    def menuInit(self):

        self.setDisplayText("MENU")
        time.sleep(3)


        self.state_menu_index = 0
        self.state = self.state_menu[self.state_menu_index]

        
    def menuLanguage(self):

        if self.menu_activated:

            self.setDisplayText(self.languages[self.lang_select])

            if self.is_pressed(self.IO_ENTER):
               self.lang = self.lang_select
               self.menu_activated = False

            if self.is_pressed(self.IO_SELECT):
                self.lang_select += 1
                if (self.lang_select > len(self.languages) - 1):
                    self.lang_select = 0

            
        else:
            self.setDisplayText("LA:" + self.languages[self.lang_select])

            self.switchMenu()

            if self.is_pressed(self.IO_ENTER):
                self.lang_select = self.lang
                self.menu_activated = True



    def menuReset(self):
        self.setDisplayText("RESET")
        if self.is_pressed(self.IO_ENTER):
            self.state = 'INIT'
        else:
            self.switchMenu()


    def menuResume(self):

        self.setDisplayText("RES.")

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
  
            Deltatime.update()
            time.sleep(.1)  # pour éviter de saturer le CPU


    def initHardware(self, bounce_ms=50):

        # bounce_ms: debounce time in milliseconds for inputs
        self.bounce_ms = bounce_ms
        # dict to store last pressed timestamp per IO pin (seconds since epoch)
        self.last_pressed_times = {}
        self.last_state_pressed = {}

        GPIO.setmode(GPIO.BCM)      # Numérotation BCM
        # GPIO en entrée
        GPIO.setup(self.IO_MENU, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.IO_SELECT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.IO_ENTER, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.setup(self.IO_IN_JACK_1, GPIO.IN)
        GPIO.setup(self.IO_IN_JACK_2, GPIO.IN)
        GPIO.setup(self.IO_IN_JACK_3, GPIO.IN)
        # GPIO 2 and 3 include 1,8kohm pull UP
        GPIO.setup(self.IO_IN_JACK_4, GPIO.IN)
        GPIO.setup(self.IO_IN_JACK_5, GPIO.IN)

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

        GPIO.setup(self.IO_OUT_LED, GPIO.OUT)
        GPIO.output(self.IO_OUT_LED, GPIO.HIGH)

        self.initJackOutput()
        self.initSwitch()

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
    
    def is_button_pressed(self):
        self.check_button(self.IO_BUTTON_1)
        self.check_button(self.IO_BUTTON_2)
        self.check_button(self.IO_BUTTON_3)
        self.check_button(self.IO_BUTTON_4)

    def check_button(self, in_switch):

        pressed = False
        if self.is_pressed(in_switch, True):
            pressed = True

        if self.switchs.get(in_switch, False) != pressed:
            self.switchs[in_switch] = pressed
            print(self.switchs)

    def is_jack_resolved(self):

        self.check_jack(self.IO_IN_JACK_1, self.IO_OUT_JACK_1)
        self.check_jack(self.IO_IN_JACK_2, self.IO_OUT_JACK_2)
        self.check_jack(self.IO_IN_JACK_3, self.IO_OUT_JACK_3)
        self.check_jack(self.IO_IN_JACK_4, self.IO_OUT_JACK_4)
        self.check_jack(self.IO_IN_JACK_5, self.IO_OUT_JACK_5)


    def check_jack(self, in_jack, out_jack):
        
        #if self.jacks.get(in_jack, None) == None:
        #   self.jacks[in_jack] = False

        ok = False
        GPIO.output(out_jack, GPIO.HIGH)
        time.sleep(.001)
        if GPIO.input(in_jack):
            ok = True
        else:
            ok = False

        GPIO.output(out_jack, GPIO.LOW)

        if self.jacks.get(in_jack, False) != ok:
            self.jacks[in_jack] = ok
            print(self.jacks)

        return ok

    def initJackOutput(self):
        self.jacks = {self.IO_IN_JACK_1: False, self.IO_IN_JACK_2: False, self.IO_IN_JACK_3: False, self.IO_IN_JACK_4: False, self.IO_IN_JACK_5: False}
        GPIO.output(self.IO_OUT_JACK_1, GPIO.LOW)
        GPIO.output(self.IO_OUT_JACK_2, GPIO.LOW)
        GPIO.output(self.IO_OUT_JACK_3, GPIO.LOW)
        GPIO.output(self.IO_OUT_JACK_4, GPIO.LOW)
        GPIO.output(self.IO_OUT_JACK_5, GPIO.LOW)

    def initSwitch(self):
        self.switchs = {self.IO_BUTTON_1: False, self.IO_BUTTON_2: False, self.IO_BUTTON_3: False, self.IO_BUTTON_4: False}

    def is_pressed(self, io, maintain = False):
        now = time.time()

        if self.last_state_pressed.get(io, False):
            if not (GPIO.input(io)):
                self.last_pressed_times[io] = 0
                self.last_state_pressed[io] = False
            return maintain
        else:
            if GPIO.input(io):
                print(io)
                last = self.last_pressed_times.get(io, 0)
                if (last == 0):
                    self.last_pressed_times[io] = now
                else:
                    # if last press too recent, ignore
                    if (now - last) * 1000 < self.bounce_ms:
                        return False
                    self.last_pressed_times[io] = 0
                    self.last_state_pressed[io] = True
                    return True
            else:
                self.last_pressed_times[io] = 0


        return False

    def play_sound(self, path):
        
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

        pygame.mixer.music.load(path)
        pygame.mixer.music.play(loops=-1)


    def setDisplayText(self, text):
        filename = './.exchange'
        if (self.last_display_text != text):
            self.last_display_text = text
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(text)

    def cleanup(self):
        self.setDisplayText('')
        GPIO.cleanup()
