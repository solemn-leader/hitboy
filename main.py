import pygame
from consts import *

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)

from helpers import *
from entities import entities
timer = pygame.time.Clock()
# pygame.mixer.init()
# pygame.mixer.music.load("audio/monster.mp3")
# pygame.mixer.music.play()
game_status = GameStatuses.PLAYING

while True:
    events = pygame.event.get()
    if check_exit(events):
        pygame.quit()
        exit()
    clean_screen(screen, GameStatuses.PLAYING)
    time_passed_in_secs = timer.tick(60) / 1000
    for entity in entities:
        if entity.is_movable:
            entity.move(
                time_passed_in_secs,
                up_button_clicked=up_button_clicked(events)
            )
        entity.draw(screen)
    pygame.display.flip()