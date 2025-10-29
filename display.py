from font import AsciiFont
import board
import neopixel
from deltatime import Deltatime
import sys
from inotify_simple import INotify, flags

class Display:

    text = ''
    matrixText = None
    color = (20, 20, 20)
    bgColor = (0, 0, 0)

    font = None
    matrix = None
    pixels = None
    scrolltime = 0
    start_x = 0
    scroll = False
    crono = 0

    MATRIX_WIDTH = 32
    MATRIX_HEIGHT = 8

    pixel_pin = board.D18
    num_pixels = 256

    def __init__(self):

        self.font = AsciiFont()
        self.matrix = self.getMatrix(self.MATRIX_WIDTH, self.MATRIX_HEIGHT)
        self.pixels = neopixel.NeoPixel(self.pixel_pin, self.num_pixels, auto_write=False)

    def setText(self, text):

        if (self.text != text):
            self.crono = 0
            self.start_x = 0
            self.text = text
            self.matrixText = self.font.getString(text)
            if(len(self.matrixText) > 0):
                if(len(self.matrixText[0]) > self.MATRIX_WIDTH):
                    self.scroll = True
                else:
                    self.scroll = False

    def update(self):

        self.clear()
        if (self.scroll):

            self.crono += Deltatime.tick()
            if (self.crono > .1 ):
                self.crono = 0
                self.start_x += 1
                start = -20

        try:
            self.draw(1, 0, self.matrixText)
        except:
            None
       # self.font.print(self.matrixText)

    def xy_to_index(self, x, y):

        return self.matrix[7 - y][x]

    def clear(self):

        for x in range(256):
            self.pixels[x] = (0, 0, 0)

    def draw(self, offset_x, offset_y, ch):


        max_y = len(ch)

        if (max_y > self.MATRIX_HEIGHT):
            max_y = self.MATRIX_HEIGHT

        for y in range(max_y):

            max_x = len(ch[y])

            if (max_x > self.MATRIX_WIDTH):
                max_x = self.MATRIX_WIDTH            

            for x in range(max_x):

                if ch[y][x + self.start_x] == 1:
                    color = self.color
                else:
                    color = self.bgColor
                    
                try:
                    self.pixels[self.xy_to_index(x + offset_x, y + offset_y)] = color
                except:
                    None                    

        self.pixels.show()
            

    def getMatrix(self, width, height):

        matrix = [[0 for _ in range(width)] for _ in range(height)]

        last = (width * height) - 1

        for x in range(width - 2, -1, -2):
            for y in range(height - 1, -1, -1):
                
                matrix[y][x] = (last - ((width  - x) * height)) + (height - y)

        for x in range(width - 1, -1, -2):
            for y in range(height - 1, -1, -1):
                
                matrix[y][x] = (last - ((width - 1 - x) * height)) - (height - 1 - y)

        return matrix


def main():

    path = './.exchange'
    display = Display()

    if len(sys.argv) > 1:
        path = sys.argv[1]

    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        with open(path, 'w', encoding='utf-8') as f:
            f.write('')

    refresh(display)
    watch_file_inotify(path, cb, display)


def watch_file_inotify(path, callback, display):
    inotify = INotify()
    wd = inotify.add_watch(path, flags.MODIFY | flags.MOVE_SELF | flags.DELETE_SELF)
    try:
        while True:
            for event in inotify.read(timeout=100):
                # event.mask contient les drapeaux
                callback(event, path, display)
            refresh(display)
    except KeyboardInterrupt:
        display.setText("")
        refresh(display)
        inotify.rm_watch(wd)
    except Exception as ex:
        inotify.rm_watch(wd)
        with open('.dispay.log', 'w', encoding='utf-8') as f:
            f.write(ex.with_traceback)

    

# usage basique
def cb(ev, filename, display):
    #print('inotify event', ev)
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    display.setText(content)
    #print( ">", content, "<")
    
def refresh(display):
    display.update()


if __name__ == '__main__':
    main()