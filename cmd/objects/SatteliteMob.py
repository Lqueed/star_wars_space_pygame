from cmd.helpers.ObjectHelper import rot_center
from BaseMob import BaseMob
import random
import math
import pygame
from cmd.config.config import (
    RES_X,
    RES_Y,
    AGGRESIVE_DISTANSE,
    MOB_SPEED,
    SATTELITE_SPEED
)


class SatteliteMob(BaseMob):
    """
    Базовый класс для всех мобов - хранит состояние, координаты и id
    Наследуется в т.ч. от фона - для расчета движения мобов вместе с фоном
    """
    def __init__(self,
                 screen,
                 img,
                 object_positions,
                 orientation,
                 mob_id=0,
                 spawn_coords=(),
                 aggressive=False,):
        super().__init__(screen=screen,
                         img=img,
                         object_positions=object_positions,
                         mob_id=mob_id,
                         spawn_coords=spawn_coords,
                         aggressive=aggressive)

        self.speed = SATTELITE_SPEED
        self.type = 'sattelite'
        self.orientation = orientation

    def is_player_near(self):
        return True
