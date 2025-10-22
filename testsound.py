#!/usr/bin/env python3
"""testsound.py

Script de diagnostic pour la lecture audio.
Usage: ./testsound.py chemin/vers/fichier.mp3

Il tente :
- pygame.mixer (normal)
- pygame.mixer en forçant SDL_AUDIODRIVER=dummy (no sound, mais pas d'erreur)
- lecteurs externes (mpg123, omxplayer, aplay, cvlc)

Affiche des messages d'erreur/diagnostic pour aider à comprendre pourquoi l'audio ne fonctionne pas.
"""
import os
import sys
import time
import subprocess


def try_pygame(path):
    try:
        import pygame
        # Initialisation avec buffer un peu grand pour Raspberry Pi
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
        print("pygame.mixer initialisé:", pygame.mixer.get_init())
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        start = time.time()
        # Attendre jusqu'à 10s ou jusqu'à la fin de la piste
        while pygame.mixer.music.get_busy() and time.time() - start < 10:
            time.sleep(0.1)
        if pygame.mixer.music.get_busy():
            print("La piste est toujours en lecture (ou la durée > 10s).")
        else:
            print("Lecture terminée ou piste très courte.")
        return True
    except Exception as e:
        print("Erreur pygame:", repr(e))
        return False


def try_subprocess(path):
    # Liste de commandes candidates (vérifier présence sur le système)
    candidates = [
        ["mpg123", "-q", path],
        ["omxplayer", path],
        ["aplay", path],
        ["cvlc", "--play-and-exit", path],
    ]
    for cmd in candidates:
        try:
            print("Essai avec :", cmd[0])
            p = subprocess.Popen(cmd)
            try:
                p.wait(timeout=5)
                print(f"Le lecteur externe {cmd[0]} a démarré (ret code {p.returncode}).")
            except subprocess.TimeoutExpired:
                print(f"{cmd[0]} joue (timeout d'attente atteint), on termine le test.")
                p.terminate()
            return True
        except FileNotFoundError:
            # Le binaire n'existe pas, passer au suivant
            print(cmd[0], "non installé")
            continue
        except Exception as e:
            print("Erreur en lançant", cmd, ":", repr(e))
    return False


def main():
    if len(sys.argv) < 2:
        print("Usage: testsound.py <file>")
        sys.exit(1)

    path = sys.argv[1]
    if not os.path.exists(path):
        print("Fichier introuvable:", path)
        sys.exit(1)

    print("Fichier:", path)

    print("--- Tentative avec pygame ---")
    ok = try_pygame(path)
    if ok:
        print("pygame a été utilisé (ou tenté). Vérifie si tu entends le son.")
        return

    print("pygame a échoué. On retente en forçant SDL_AUDIODRIVER=dummy (aucun son mais sans erreur).")
    os.environ["SDL_AUDIODRIVER"] = "dummy"
    try:
        # Recharger l'état si pygame est déjà importé : on force re-import
        import importlib
        importlib.reload(__import__("pygame"))
    except Exception:
        # si pygame n'est pas importé, ce n'est pas grave
        pass

    ok = try_pygame(path)
    if ok:
        print("Lecture (mode dummy) effectuée — ceci montre que pygame fonctionne mais qu'aucune carte audio n'est disponible.")
        return

    print("--- Tentative avec des lecteurs externes ---")
    if try_subprocess(path):
        print("Lecture lancée avec un lecteur externe.")
        return

    print("Aucun moyen de lecture réussi. Diagnostics utiles:")
    print(" - Si vous êtes sous WSL, configurez un serveur PulseAudio ou utilisez WSLg (Windows 11)")
    print(" - Vérifiez les périphériques ALSA sur la machine : 'aplay -l'")
    print(" - Installez un lecteur: sudo apt install mpg123 alsa-utils")


if __name__ == '__main__':
    main()

