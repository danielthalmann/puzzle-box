from font import AsciiFont

asc = AsciiFont()
l = asc.getChar('B')

text = asc.getString(" START ")
asc.print(text)
asc.print(l)
#print(font.getChar("a"))