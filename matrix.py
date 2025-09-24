import board
import neopixel
import time
from font import AsciiFont


# Exemple : matrice 8x8 sur GPIO18 (broche physique 12)
pixel_pin = board.D18
num_pixels = 256  # 32x8

def getMatrix(width, height):

    matrix = [[0 for _ in range(width)] for _ in range(height)]

    last = (width * height) - 1

    for x in range(width - 2, -1, -2):
        for y in range(height - 1, -1, -1):
            
            matrix[y][x] = (last - ((width  - x) * height)) + (height - y)

    for x in range(width - 1, -1, -2):
        for y in range(height - 1, -1, -1):
            
            matrix[y][x] = (last - ((width - 1 - x) * height)) - (height - 1 - y)

    return matrix
            
            
matrix = getMatrix(32, 8)
# ###
#for y in range(8):
   ## print (matrix[y])#



#exit()


pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False)

def draw(offset_x, offset_y, ch):
    for y in range(len(ch)):
        for x in range(len(ch[y])):
            if ch[y][x] == 1:
                pixels[xy_to_index(x + offset_x, y + offset_y)] = (15, 113, 40)

    pixels.show()


def xy_to_index(x, y):
    return matrix[7 - y][x]

def clear(pixels):
    for x in range(256):
        pixels[x] = (0, 0, 0)

    pixels.show()


clear(pixels)

#pixels[xy_to_index(0, 0)] = (15, 13, 4)
#pixels[xy_to_index(0, 31)] = (15, 13, 4)
#pixels.show()
asc = AsciiFont()
text = asc.getString("03:64")

draw(1, 0, text)

exit()


for y in range(8):
    for x in range(32):
        pixels[xy_to_index(x, y)] = (115, 113, 4)
        time.sleep(0.1)
        pixels.show()







# for x in range(256):
#     pixels[x] = (15, 13, 4)
#     time.sleep(0.1)
#     pixels.show()


# for x in range(32):
#     for y in range(8):
#         pixels[xy_to_index(x, y, 32)] = (128, 0, 0)
#         time.sleep(0.1)
#         pixels.show()






