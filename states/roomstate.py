from state import State
from ..deltatime import Deltatime

class RoomState(State):

    def enter(self):
        Deltatime.clear()
        # self.machine.play_sound('sound/relaxing.mp3')
        self.machine.play_sound('sound/start-' + self.machine.languages[self.machine.lang_select] + '.mp3')

    def update(self):

        self.machine.displayCounter()

        if self.is_jack_resolved():
            self.machine.transitionTo('PSYCHOLOGIST')

        if not self.machine.is_pressed(self.machine.IO_LID):
            self.machine.transitionTo('PSYCHOLOGIST')
            print("boucle")

        if self.machine.is_pressed(self.machine.IO_SELECT):
            self.machine.transitionTo('PSYCHOLOGIST')

        if self.machine.is_pressed(self.machine.IO_MENU):
            self.machine.transitionTo('MENU_INIT')

    def is_jack_resolved(self):

        line1 = self.machine.check_jack(self.machine.IO_IN_JACK_1, self.machine.IO_OUT_JACK_1)
        line2 = self.machine.check_jack(self.machine.IO_IN_JACK_2, self.machine.IO_OUT_JACK_2)
        line3 = self.machine.check_jack(self.machine.IO_IN_JACK_3, self.machine.IO_OUT_JACK_3)
        line4 = self.machine.check_jack(self.machine.IO_IN_JACK_4, self.machine.IO_OUT_JACK_4)
        line5 = self.machine.check_jack(self.machine.IO_IN_JACK_5, self.machine.IO_OUT_JACK_5)

        if line1 and line2 and line3 and line4 and line5:
            return True
        else:
            return False

    def leave(self):
        self.machine.resume_state = 'ROOM'

        