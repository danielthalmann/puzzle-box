from states.state import State
from deltatime import Deltatime

class RoomState(State):

    local_time = 0

    def enter(self):

        Deltatime.clear()
        self.machine.play_sound('sound/start-' + self.machine.languages[self.machine.lang] + '.mp3')
        self.machine.is_pressed(self.machine.IO_LID, True)
        self.machine.sound_volume(.2)
        self.local_time = 0

    def update(self):

        self.machine.displayCounter()

        self.local_time += Deltatime.tick()

        if not self.machine.is_pressed(self.machine.IO_LID, True):
            self.machine.transitionTo('PSYCHOLOGIST')
            return
            
        if self.machine.is_pressed(self.machine.IO_SELECT):
            self.machine.transitionTo('PSYCHOLOGIST')
            return

        if self.machine.isCronoFinish():
            self.machine.transitionTo('FINAL')
            return

        if self.machine.is_pressed(self.machine.IO_MENU):
            self.machine.transitionTo('MENU_INIT')
            return

        if (self.local_time > (15 * 60)):
            self.machine.sound_volume(1)
        else:
            if (self.local_time > (10 * 60)):
                self.machine.sound_volume(.8)
            else:
                if (self.local_time > (5 * 60)):
                    self.machine.sound_volume(.7)
                else:
                    if (self.local_time > (2 * 60)):
                        self.machine.sound_volume(.6)

    def leave(self):
        self.machine.resume_state = 'ROOM'

        