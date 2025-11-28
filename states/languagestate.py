from states.state import State

class LanguageState(State):

    lang_select = 0

    def enter(self):
        self.lang_select = self.machine.lang

    def update(self):

        self.machine.setDisplayText("LA:" + self.machine.languages[self.lang_select])

        if self.machine.is_pressed(self.machine.IO_ENTER):
            self.machine.lang = self.lang_select
            self.machine.transitionTo('MENU')

        if self.machine.is_pressed(self.machine.IO_SELECT):
            self.lang_select += 1
            if (self.lang_select > len(self.machine.languages) - 1):
                self.lang_select = 0

        
