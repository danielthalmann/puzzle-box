from display import Display
from inotify_simple import INotify, flags
import sys
import time
import asyncio


display = Display()
filename = './.exchange'

async def main():

    if len(sys.argv) > 1:
        filename = sys.argv[1]

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('')

    await watch_file_inotify(filename, cb)
    await refresh()


async def watch_file_inotify(path, callback):
    inotify = INotify()
    wd = inotify.add_watch(path, flags.MODIFY | flags.MOVE_SELF | flags.DELETE_SELF)
    try:
        while True:
            for event in inotify.read(timeout=1000):
                display.update()
                print( ">wait<")
                # event.mask contient les drapeaux
                callback(event)
    except KeyboardInterrupt:
        inotify.rm_watch(wd)

# usage basique
async def cb(ev):
    #print('inotify event', ev)
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    display.setText(content)
    print( ">", content, "<")
    
async def refresh():
    while True: 
        await asyncio.sleep(.4)
        display.update()


if __name__ == '__main__':
    asyncio.run(main())

