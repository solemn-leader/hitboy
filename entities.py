from helpers import load_image
import pygame
from datetime import datetime
from consts import *
from random import choice


class GameObject(object):
    '''base object for all base objects'''
    is_movable = False

    def __init__(self, x: int, y: int):
        self.x, self.y = x, y

    def draw(self, screen):
        pass

    def move(
        self,
        time_passed_in_secs: int,
        **kwargs
    ):
        pass

    def update_rect(self):
        pass


class Floor(GameObject):
    '''element hitboy runs on'''
    is_movable = False
    can_kill_hitboy = False

    def __init__(self, x, y):
        super().__init__(x, y)
        self.rect = pygame.Rect(
            *FLOOR_RECT_POSITION
        )

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)


class Hitboy(GameObject):
    '''represents our character'''
    dead = False
    is_movable = True  # character moves upside down
    dead_image = load_image('hitboy_dead.png')
    y_speed, jump_speed = 0, -400  # pix per second
    can_kill_hitboy = False

    images = [
        pygame.transform.scale(image, HITBOY_SIZE) for image in (
            load_image('hitboy0.png'),
            load_image('hitboy1.png')
        )
    ]

    def __init__(self, x: int, y: int, floor: Floor):
        super().__init__(x, y)
        self.update_rect()
        self.current_image_index = 0
        self.floor = floor

    def update_rect(self):
        self.rect = pygame.Rect(
            self.x,
            self.y,
            HITBOY_SIZE[0],
            HITBOY_SIZE[1]
        )

    def move(
        self,
        time_passed_in_secs: int,
        **kwargs
    ):
        if not (datetime.now().microsecond % CHANGE_IMAGE_PERIOD):
            self.change_image()
        if self.stands_on_floor():
            if kwargs.get('up_button_clicked', False):
                self.y_speed = self.jump_speed  # self.jump
            else:
                self.put_hero_on_the_ground()
                self.y_speed = 0
        else:
            self.y_speed += G * time_passed_in_secs
        self.y += int(self.y_speed * time_passed_in_secs)
        self.update_rect()

    def put_hero_on_the_ground(self):
        self.x, self.y = HITBOY_START_POSITION
        self.update_rect()

    def stands_on_floor(self) -> bool:
        return self.rect.colliderect(self.floor.rect)

    def draw(self, screen):
        screen.blit(self.images[self.current_image_index], self.rect)

    def __str__(self):
        return "Hitboy! x: {}, y: {}, current_image: {}, y_speed: {}".format(
            self.x,
            self.y,
            self.current_image_index,
            self.y_speed
        )

    def change_image(self):
        self.current_image_index = (
            self.current_image_index + 1) % len(self.images)


class Obstacle(GameObject):
    is_movable = True
    speed = -300  # moving towards player

    def __init__(self, x, y, image_name):
        super().__init__(x, y)
        self.image = pygame.transform.scale(
            load_image(image_name), OBSTACLE_SIZE
        )
        self.update_rect()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, time_passed_in_secs, **kwargs):
        self.x += self.speed * time_passed_in_secs
        self.update_rect()

    def update_rect(self):
        self.rect = pygame.Rect(
            self.x,
            self.y,
            OBSTACLE_SIZE[0],
            OBSTACLE_SIZE[1]
        )


entities = []  # all game objects
entities.append(
    Floor(*FLOOR_RECT_POSITION[:2])
)
entities.append(
    Hitboy(*HITBOY_START_POSITION, entities[0])
)
entities.append(
    Obstacle(*OBSTACLE_START_POSITION, choice(OBSTACLE_IMAGES_NAMES))
)