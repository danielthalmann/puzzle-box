from states.state import State
from deltatime import Deltatime
import RPi.GPIO as GPIO

class RoomState(State):


    def enter(self):

        self.machine.play_sound('sound/start-' + self.machine.languages[self.machine.lang] + '.mp3')
        self.machine.is_pressed(self.machine.IO_LID, True)

    def update(self):

        self.machine.displayCounter()

        if not self.machine.is_pressed(self.machine.IO_LID, True):
            self.machine.transitionTo('PSYCHOLOGIST')
            
        if self.machine.is_pressed(self.machine.IO_SELECT):
            self.machine.transitionTo('PSYCHOLOGIST')

        if self.machine.is_pressed(self.machine.IO_MENU):
            self.machine.transitionTo('MENU_INIT')

    def leave(self):
        self.machine.resume_state = 'ROOM'

        