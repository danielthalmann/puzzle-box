from puzzlebox import Puzzlebox
import signal


def exit_gracefully(signum, frame):
    game.stop()


try:
    game = Puzzlebox()
    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGTERM, exit_gracefully)
    game.start()
except KeyboardInterrupt:
    game.cleanup()
