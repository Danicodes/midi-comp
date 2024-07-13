import pygame
import pygame.midi


if __name__ == "__main__":
    pygame.mixer.init(44100, -16, 2, 1024)
    pygame.mixer.music.set_volume(1.0)
    pygame.midi.init()
    clock = pygame.time.Clock()

    print(pygame.mixer.get_init())
    while True:
        a = input("1. Load File. 2. Play, 3. Stop, 4. Soundeffect, 5. Quit\n").strip()
        if a == "1":
            midifile = input("Midi filename to play: ")
            midifile = midifile.strip()
        elif a == "2": 
            print(f"Playing track: {midifile}")
            pygame.mixer.music.load(midifile)
            pygame.mixer.music.play(loops=0)
        elif a == "3":
            pygame.mixer.music.stop()
        elif a == "5":
            pygame.quit()
            break
        elif a == "4":
            dundundun = pygame.mixer.Sound('dundundun.wav')
            dundundun.play()
        else:
            break