import pygame
from cmd.objects.Player import Player
from cmd.objects.ObjectPositions import ObjectPositions
from cmd.background.TileBackground import TileBackground
from cmd.helpers.KeyHelper import (
    detect_player_rotate,
    detect_shoot,
    detect_free_flight,
)
from cmd.config.config import (
    GAME_TITLE,
    RES_X,
    RES_Y,
    speed,
    SHOT_IMG,
    BACKGOUND_TILE_IMG,
    BASE_MOB_IMG,
    BASE_PLAYER_IMG,
)

"""
Все методы содержащие в названии draw - отрисовывают объекты на экране
Все методы содержащие в названии move - просчитывают передвижение объектов
"""


# константы и объект игры
display_size = (RES_X, RES_Y)

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode(display_size)
pygame.display.set_caption(GAME_TITLE)

shoot_delay = 0
shot_img = pygame.image.load(SHOT_IMG)

# основной класс-синглтон, который хранит координаты всех объектов и через который считаем взаимодействия
object_positions = ObjectPositions(screen=screen)

# синглтон игрока - будет один
# player = Player(img="png/x-wing-small.png",
#                 screen=screen,
#                 object_positions=object_positions)

# объект фона - один
bg = TileBackground(img=BACKGOUND_TILE_IMG,
                    screen=screen)

# спавним мобов сколько нужно
for _ in range(3):
    object_positions.add_mob(img=BASE_MOB_IMG,
                             screen=screen,
                             object_positions=object_positions)

object_positions.add_player(
    Player(img=BASE_PLAYER_IMG,
           screen=screen,
           object_positions=object_positions)
)

clock = pygame.time.Clock()
run = True
while run:
    # 60 фпс
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # спавн мобов если кончились
    object_positions.spawn_more_mobs_random()

    # считываем нажатия клавиш
    keys = pygame.key.get_pressed()

    # передвижение поворот + вперед-назад - определяем по кнопкам
    move_speed, left, right = detect_player_rotate(keys, speed)

    # полет по инерции
    free_flight = detect_free_flight(keys)

    # определяем направление полета
    if free_flight:
        left, right, up, down = object_positions.player_obj.get_set_rotation_free_flight(left, right)
    else:
        left, right, up, down = object_positions.player_obj.get_set_rotation(
            move_speed,
            left,
            right,
            object_positions.player_obj.destroyed
        )

    shoot = detect_shoot(keys)
    if shoot:
        # стрельба - спавним новый выстрел раз в 20 фреймов (3 раза в секунду). Выстрел тоже объект
        if shoot_delay <= 0:
            object_positions.add_shot(shot_img, object_positions.player_obj.orientation)
            shoot_delay = 20

    # обратный отсчет фреймов до след выстрела
    if shoot_delay > 0:
        shoot_delay -= 1

    # двигаем фон
    bg.move(left, right, up, down)

    # сначала всегда отрисовываем фон, потом сверху все остальное
    bg.draw()

    # двигаем мобов и выстрелы
    object_positions.move_mobs(left, right, up, down)
    object_positions.move_shots()

    # ищем пересечения хитбоксов мобов с игроком и выстрелами
    object_positions.find_collisions()

    # отрисовываем игрока и мобов
    object_positions.draw_all()

    if object_positions.player_obj.destroyed:
        myfont = pygame.font.SysFont('Arial Bold', int(RES_Y / 5))
        textsurface = myfont.render('YOU FUCKED UP', False, (255, 255, 255))
        screen.blit(textsurface, (RES_X / 2 - int(RES_X / 3.2), RES_Y / 2 - int(RES_Y / 20)))

    pygame.display.update()

pygame.quit()