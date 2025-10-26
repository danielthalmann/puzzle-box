import subprocess
import time


cmd = ["mpg123", "-q", "--loop", "-1", "sound/relaxing.mp3"]

print("Essai avec :", cmd)
process = subprocess.Popen(cmd)

while True:
    time.sleep(10)

# Vérifier si le processus est encore en cours
if process.poll() is None:
    print("Le script tourne encore, on l'arrête.")
    process.terminate()   # envoie SIGTERM
    process.wait()        # attend qu'il se termine
else:
    print("Le script a fini naturellement.")





