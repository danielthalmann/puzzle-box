import board
import neopixel
import time


# Exemple : matrice 8x8 sur GPIO18 (broche physique 12)
pixel_pin = board.D18
num_pixels = 256  # 32x8
matrix = [[0 for _ in range(8)] for _ in range(32)]



for y in range(8):
    i = 0
    for x in range(255 - y, 0, -16):
        matrix[i][y] = x
        i += 2

for y in range(8):
    i = 1
    for x in range(255 -15 + y, 0, -16):
        matrix[i][y] = x
        i += 2

# 
print (matrix)
#exit()


pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False)


def xy_to_index(x, y):
    return matrix[x][y]

def clear(pixels):
    for x in range(256):
        pixels[x] = (0, 0, 0)

    pixels.show()


clear(pixels)

#pixels[xy_to_index(0, 0)] = (15, 13, 4)
#pixels[xy_to_index(0, 31)] = (15, 13, 4)
#pixels.show()


for x in range(32):
    for y in range(8):
        pixels[xy_to_index(x, y)] = (15, 13, 4)
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






