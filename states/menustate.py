from states.state import State

class MenuState(State):

    state_menu = ['LANGUAGE', 'RESET', 'RESUME']
    state_menu_index = 0

    def enter(self):
        self.state_menu_index = 0

    def update(self):

        if self.machine.is_pressed(self.machine.IO_SELECT):
            self.state_menu_index += 1

        if self.state_menu_index > (len(self.state_menu) - 1):
            self.state_menu_index = 0

        match self.state_menu[self.state_menu_index]:
            case 'LANGUAGE':
                self.displayLang()
            case 'RESET':
                self.displayReset()
            case'RESUME':
                self.displayResume()

        if self.machine.is_pressed(self.machine.IO_ENTER):
            self.machine.transitionTo(self.state_menu[self.state_menu_index])
    
    def displayLang(self):

        self.machine.setDisplayText('LANG')

    def displayReset(self):

        self.machine.setDisplayText('RESET')

    def displayResume(self):

        self.machine.setDisplayText('RESUM')
