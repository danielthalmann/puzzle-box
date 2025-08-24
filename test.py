from font import AsciiFont

asc = AsciiFont()
l = asc.getLetter('B')

for y in range(len(l)):
    print(l[y])

#print(font.getLetter("a"))