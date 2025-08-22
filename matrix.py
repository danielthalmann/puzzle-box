import board
import neopixel
import time


# Exemple : matrice 8x8 sur GPIO18 (broche physique 12)
pixel_pin = board.D18
num_pixels = 256  # 8x8

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False)


def xy_to_index(x, y, width):
    return y * width + x

def clear(pixels):
    for x in range(32):
        for y in range(8):
            pixels[xy_to_index(x, y, 32)] = (0, 0, 0)

    pixels.show()


clear(pixels)


for x in range(256):

    pixels[x] = (0, 75, 65)
    time.sleep(0.1)
    pixels.show()


# for x in range(32):
#     for y in range(8):
#         pixels[xy_to_index(x, y, 32)] = (128, 0, 0)
#         time.sleep(0.1)
#         pixels.show()




