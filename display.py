from font import AsciiFont
import board
import neopixel

class Display:

    text = ''
    matrixText = None
    color = (155, 20, 40)

    font = None
    matrix = None
    pixels = None


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

            self.text = text
            self.matrixText = self.font.getString(text)

    def update(self):

        self.clear()
        self.draw(1, 0, self.matrixText)
       # self.font.print(self.matrixText)

    def xy_to_index(self, x, y):

        return self.matrix[7 - y][x]

    def clear(self):

        for x in range(256):
            self.pixels[x] = (0, 0, 0)

    def draw(self, offset_x, offset_y, ch):

        for y in range(len(ch)):
            for x in range(len(ch[y])):
                if ch[y][x] == 1:
                    self.pixels[self.xy_to_index(x + offset_x, y + offset_y)] = self.color

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
            
            
