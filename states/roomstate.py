from states.state import State
from deltatime import Deltatime
import RPi.GPIO as GPIO

class RoomState(State):

    time = 0

    def enter(self):

        self.machine.play_sound('sound/start-' + self.machine.languages[self.machine.lang] + '.mp3')
        self.machine.is_pressed(self.machine.IO_LID, True)
        self.machine.sound_volume(.2)
        self.time = 0

    def update(self):

        self.machine.displayCounter()

        self.time += Deltatime.tick()

        if not self.machine.is_pressed(self.machine.IO_LID, True):
            self.machine.transitionTo('PSYCHOLOGIST')
            
        if self.machine.is_pressed(self.machine.IO_SELECT):
            self.machine.transitionTo('PSYCHOLOGIST')

        if self.machine.is_pressed(self.machine.IO_MENU):
            self.machine.transitionTo('MENU_INIT')

        if (self.time > (15 * 60)):
            self.machine.sound_volume(1)
        else:
            if (self.time > (10 * 60)):
                self.machine.sound_volume(.8)
            else:
                if (self.time > (5 * 60)):
                    self.machine.sound_volume(.6)
                else:
                    if (self.time > (2 * 60)):
                        self.machine.sound_volume(.4)

    def leave(self):
        self.machine.resume_state = 'ROOM'

        