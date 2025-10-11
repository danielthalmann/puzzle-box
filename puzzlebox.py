import RPi.GPIO as GPIO
import time
from datetime import datetime
from display import Display
from deltatime import Deltatime

class Puzzlebox:

    state = 'START'

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


    def initGame(self):

        GPIO.output(self.IO_LED_RED_JACK, GPIO.HIGH)  # Met le GPIO 17 à l’état haut (3.3V)
        GPIO.output(self.IO_LED_GREEN_JACK, GPIO.LOW)   # Met le GPIO 17 à l’état bas (0V)

        GPIO.output(self.IO_LED_RED_SWITCH, GPIO.HIGH)  # Met le GPIO 17 à l’état haut (3.3V)
        GPIO.output(self.IO_LED_GREEN_SWITCH, GPIO.LOW)   # Met le GPIO 17 à l’état bas (0V)

        self.crono = 0

        self.state = 'ROOM'

    def roomGame(self):

        self.crono += Deltatime.tick()

        counter = datetime(1, 1, 1) + Deltatime.delta(seconds=self.crono)

        heure = counter.strftime("%M:%S")

        self.display.setText(heure)

        if (self.crono > 5):
            self.crono = 0
            self.state = 'FINAL'

    def finalGame(self):

        self.crono += Deltatime.tick()
        self.display.setText("Bravo c'est fini")
        if (self.crono > 10):
            self.crono = 0
            self.state = 'INIT'


    def gameLoop(self):

        while(True):

            if (self.state == 'START'):
                self.state = 'INIT'
                
            elif (self.state == 'INIT'):
                self.initGame()

            elif (self.state == 'ROOM'):
                self.roomGame()

            elif (self.state == 'FINAL'):
                self.finalGame()

            print(self.state)
  
            self.display.update()
            Deltatime.update()
            time.sleep(.1)  # pour éviter de saturer le CPU


    def initHardware(self):

        GPIO.setmode(GPIO.BCM)      # Numérotation BCM
        # GPIO en entrée
        GPIO.setup(self.IO_MENU, GPIO.IN)
        GPIO.setup(self.IO_SELECT, GPIO.IN)
        GPIO.setup(self.IO_ENTER, GPIO.IN)

        GPIO.setup(self.IO_IN_JACK_1, GPIO.IN)
        GPIO.setup(self.IO_IN_JACK_2, GPIO.IN)
        GPIO.setup(self.IO_IN_JACK_3, GPIO.IN)
        GPIO.setup(self.IO_IN_JACK_4, GPIO.IN)
        GPIO.setup(self.IO_IN_JACK_5, GPIO.IN)

        GPIO.setup(self.IO_BUTTON_1, GPIO.IN)
        GPIO.setup(self.IO_BUTTON_2, GPIO.IN)
        GPIO.setup(self.IO_BUTTON_3, GPIO.IN)
        GPIO.setup(self.IO_BUTTON_4, GPIO.IN)

        GPIO.setup(self.IO_LID, GPIO.IN)  

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

        
    





        