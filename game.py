from puzzlebox import Puzzlebox

try:
    game = Puzzlebox()
    game.start()
except KeyboardInterrupt:
    game.cleanup()
