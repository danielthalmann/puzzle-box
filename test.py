from font import AsciiFont
import time
from datetime import datetime

asc = AsciiFont()


start = datetime.today()
counter = datetime(1, 1, 1) 
while(True) :
    delta = (datetime.today() - start)
    counter = datetime(1, 1, 1) + delta
    heure = counter.strftime("%M:%S")
    text = asc.getString(heure)
    asc.print(text)
    time.sleep(1)
    
    
#print(font.getChar("a"))