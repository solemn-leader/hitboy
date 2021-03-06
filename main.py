import pygame
from consts import *

pygame.init()
pygame.font.init()
pygame.mixer.init()
screen = pygame.display.set_mode(SCREEN_SIZE)


def main():
    from entities import (
        entities,
        obstacles,
        planes,
        rockets,
        menu,
        score,
        pause_menu,
        start_new_game,
        object_adder
    )
    from helpers import (
        get_max_score,
        load_image,
        clean_screen,
        check_exit,
        check_pause,
        up_button_clicked,
        where_to_shoot,
        get_angle_by_three_points,
        get_point_on_same_line,
        finish_game
    )
    import webbrowser
    timer = pygame.time.Clock()
    # pygame.mixer.music.load("audio/monster.mp3")
    # pygame.mixer.music.play()
    game_status = GameStatuses.MENU
    max_score = get_max_score()
    pygame.display.set_caption('Hitboy.')
    pygame.display.set_icon(load_image('favicon.png'))
    pointer = pygame.transform.scale(load_image('pointer.png'), POINTER_SIZE)

    while True:
        time_passed_in_secs = timer.tick(60) / 1000
        if game_status == GameStatuses.GAME_OVER:
            menu.draw(screen)
            events = pygame.event.get()
            if check_exit(events):
                pygame.quit()
                exit(0)
            user_choice = menu.get_user_choice(events)
            if user_choice is not None:
                if user_choice == UserChoicesMenu.PLAY:
                    game_status = GameStatuses.PLAYING
                    pygame.mouse.set_visible(False)
                    entities, obstacles = start_new_game(
                        entities, obstacles, object_adder, score)
                elif user_choice == UserChoicesMenu.EXIT:
                    pygame.quit()
                    exit(0)
                elif user_choice == UserChoicesMenu.ABOUT:
                    webbrowser.open(ABOUT_URL)

        elif game_status == GameStatuses.PAUSE:
            pause_menu.draw(screen)
            events = pygame.event.get()
            if check_exit(events):
                pygame.quit()
                exit(0)
            user_choice = pause_menu.get_user_choice(events)
            if user_choice is not None:
                if user_choice == UserChoicesMenu.PLAY:
                    object_adder.reset_timers()
                    game_status = GameStatuses.PLAYING
                    pygame.mouse.set_visible(False)
                elif user_choice == UserChoicesMenu.EXIT:
                    pygame.quit()
                    exit(0)
                elif user_choice == UserChoicesMenu.RESTART:
                    game_status = GameStatuses.PLAYING
                    entities, obstacles = start_new_game(
                        entities, obstacles, object_adder, score)
                    pygame.mouse.set_visible(False)

        elif game_status == GameStatuses.MENU:
            clean_screen(screen, game_status)
            menu.draw(screen)
            events = pygame.event.get()
            if check_exit(events):
                pygame.quit()
                exit(0)
            user_choice = menu.get_user_choice(events)
            if user_choice is not None:
                if user_choice == UserChoicesMenu.PLAY:
                    game_status = GameStatuses.PLAYING
                    pygame.mouse.set_visible(False)
                    entities, obstacles = start_new_game(
                        entities, obstacles, object_adder, score)
                elif user_choice == UserChoicesMenu.EXIT:
                    pygame.quit()
                    exit(0)
                elif user_choice == UserChoicesMenu.ABOUT:
                    webbrowser.open(ABOUT_URL)

        elif game_status == GameStatuses.PLAYING:
            # entities[1] is main charecter
            events = pygame.event.get()
            if check_pause(events):
                game_status = GameStatuses.PAUSE
                pygame.mouse.set_visible(True)
                continue
            if check_exit(events):
                pygame.quit()
                exit(0)
            clean_screen(screen, GameStatuses.PLAYING)
            score.increase()
            score.draw(screen)
            object_adder.add_planes_and_obstacles_if_necessary(
                entities, obstacles, planes)
            # object_adder.add_plane_if_necessary(entities, planes)  # then
            # delete it
            object_adder.add_rockets_if_necessary(
                entities,
                rockets,
                entities[1].weapon.get_rocket_initial_point(),
                where_to_shoot(events))
            entities[1].weapon.rotate(
                get_angle_by_three_points(
                    get_point_on_same_line(entities[1].weapon.coords()),
                    entities[1].weapon.coords(),
                    pygame.mouse.get_pos(),
                )
            )
            for entity in entities:
                if entity.is_movable:
                    entity.move(
                        time_passed_in_secs,
                        up_button_clicked=up_button_clicked(events)
                    )
                if entity.can_die:
                    dead = entity.try_to_die(obstacles)
                    if dead:
                        entity.draw(screen)
                        pygame.display.flip()
                        game_status = finish_game(score)
                        break
                if entity.can_finish_game:
                    game_over = entity.try_to_finish_game()
                    if game_over:
                        game_status = finish_game(score)
                        break
                if entity.can_interact_with_rockets:
                    entity.interact_with_rockets(
                        entities, obstacles, planes, rockets)
                if entity.must_die:
                    entity.die(entities, obstacles, planes, rockets)
                entity.draw(screen)
            screen.blit(pointer, pygame.mouse.get_pos())
        pygame.display.flip()


if __name__ == "__main__":
    main()
