# from display import Display
from inotify_simple import INotify, flags
import sys
import time


def main():

    # display = Display()
    filename = './.exchange'

    if len(sys.argv) > 1:
        filename = sys.argv[1]

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('')


    def watch_file_inotify(path, callback):
        inotify = INotify()
        wd = inotify.add_watch(path, flags.MODIFY | flags.MOVE_SELF | flags.DELETE_SELF)
        try:
            while True:
                for event in inotify.read(timeout=1000):
                    # display.update()
                    # event.mask contient les drapeaux
                    callback(event)
        except KeyboardInterrupt:
            inotify.rm_watch(wd)

    # usage basique
    def cb(ev):
        #print('inotify event', ev)
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
       
        #display.setText(content)
        print( ">", content, "<")


    watch_file_inotify(filename, cb)


if __name__ == '__main__':
    main()
