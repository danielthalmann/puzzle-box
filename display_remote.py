from display import Display
from inotify_simple import INotify, flags
import sys
import time
import asyncio


display = Display()
filename = './.exchange'

def main():

    path = filename
    if len(sys.argv) > 1:
        path = sys.argv[1]

    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        with open(path, 'w', encoding='utf-8') as f:
            f.write('')

    refresh()
    watch_file_inotify(path, cb)


def watch_file_inotify(path, callback):
    inotify = INotify()
    wd = inotify.add_watch(path, flags.MODIFY | flags.MOVE_SELF | flags.DELETE_SELF)
    try:
        while True:
            for event in inotify.read(timeout=100):
                # event.mask contient les drapeaux
                callback(event)
            refresh()
    except KeyboardInterrupt:
        display.setText("")
        refresh()
        inotify.rm_watch(wd)

# usage basique
def cb(ev):
    #print('inotify event', ev)
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    display.setText(content)
    #print( ">", content, "<")
    
def refresh():
    display.update()


if __name__ == '__main__':
    main()

