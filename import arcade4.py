import arcade
import random
import os

# Параметры экрана
SCREEN_WIDTH = 1060
SCREEN_HEIGHT = 580
SCREEN_TITLE = "Egg Thrower"

# Пути к изображениям
NEST_IMAGE = "nest.png"
EGG_IMAGE = "egg.png"
EAGLE_IMAGE_PREFIX = "eagle"
EAGLE_LEFT_IMAGE_PREFIX = "eagle_L"
BACKGROUND_IMAGE = "fon_1.png"
LOGO_IMAGE = "logo.png"
MUSIC_FILE = "music.mp3"
LEVEL_IMAGE = "level_select.png"
LEVEL1_IMAGE = "level1.png"
LEVEL2_IMAGE = "level2.png"
LEVEL3_IMAGE = "level3.png"
HOME_IMAGE = "home.png"

class StartView(arcade.View):

    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.WHITE)

        self.level_sprite = None

        self.settings = None

    def setup(self):

        self.level_sprite = arcade.Sprite(LEVEL_IMAGE)
        self.level_sprite.center_x = SCREEN_WIDTH // 2
        self.level_sprite.center_y = SCREEN_HEIGHT // 2


    def on_draw(self):
        self.clear()

        arcade.draw_sprite(self.level_sprite)
        

    def on_mouse_press(self, x, y, button, modifiers):
        """Начало игры при нажатии клавиши"""
        if self.level_sprite.left <= x <= self.level_sprite.right and self.level_sprite.bottom <= y <= self.level_sprite.top:
            game_view = SelectLevel()
            game_view.setup()
            self.window.show_view(game_view)


class EndView(arcade.View):

    def __init__(self, rec):
        super().__init__()
        arcade.set_background_color(arcade.color.WHITE)

        self.home_sprite = None

        self.rec = rec

        self.settings = None

    def setup(self):

        self.home_sprite = arcade.Sprite(HOME_IMAGE, 0.8)
        self.home_sprite.center_x = SCREEN_WIDTH // 2
        self.home_sprite.center_y = SCREEN_HEIGHT // 2


    def on_draw(self):
        self.clear()

        arcade.draw_sprite(self.home_sprite)

        arcade.draw_text(f"Рекорд - {self.rec}", SCREEN_WIDTH - 300, 530, arcade.color.BLACK, 35)

        

    def on_mouse_press(self, x, y, button, modifiers):
        """Начало игры при нажатии клавиши"""
        if self.home_sprite.left <= x <= self.home_sprite.right and self.home_sprite.bottom <= y <= self.home_sprite.top:
            game_view = StartView()
            game_view.setup()
            self.window.show_view(game_view)

class SelectLevel(arcade.View):
    def __init__(self):
        super().__init__()

        self.level1_sprite = None
        self.level2_sprite = None
        self.level3_sprite = None
        self.menu_sprite = None

    def setup(self):

        self.level1_sprite = arcade.Sprite(LEVEL1_IMAGE, 0.4)
        self.level1_sprite.center_x = SCREEN_WIDTH // 2
        self.level1_sprite.center_y = SCREEN_HEIGHT // 9 * 8

        self.level2_sprite = arcade.Sprite(LEVEL2_IMAGE, 0.4)
        self.level2_sprite.center_x = SCREEN_WIDTH // 2
        self.level2_sprite.center_y = SCREEN_HEIGHT // 9 * 6

        self.level3_sprite = arcade.Sprite(LEVEL3_IMAGE, 0.4)
        self.level3_sprite.center_x = SCREEN_WIDTH // 2
        self.level3_sprite.center_y = SCREEN_HEIGHT // 9 * 4

        self.menu_sprite = arcade.Sprite(HOME_IMAGE, 0.4)
        self.menu_sprite.center_x = SCREEN_WIDTH // 2
        self.menu_sprite.center_y = SCREEN_HEIGHT // 9 * 2

    def on_draw(self):

        self.clear()
        
        arcade.draw_sprite(self.level1_sprite)
        arcade.draw_sprite(self.level2_sprite)
        arcade.draw_sprite(self.level3_sprite)
        arcade.draw_sprite(self.menu_sprite)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.level1_sprite.left <= x <= self.level1_sprite.right and self.level1_sprite.bottom <= y <= self.level1_sprite.top:
            game_view = EggThrower(4)
            game_view.setup()
            self.window.show_view(game_view)
        elif self.level2_sprite.left <= x <= self.level2_sprite.right and self.level2_sprite.bottom <= y <= self.level2_sprite.top:
            game_view = EggThrower(5)
            game_view.setup()
            self.window.show_view(game_view)
        elif self.level3_sprite.left <= x <= self.level3_sprite.right and self.level3_sprite.bottom <= y <= self.level3_sprite.top:
            game_view = EggThrower(6)
            game_view.setup()
            self.window.show_view(game_view)
        elif self.menu_sprite.left <= x <= self.menu_sprite.right and self.menu_sprite.bottom <= y <= self.menu_sprite.top:
            game_view = StartView()
            game_view.setup()
            self.window.show_view(game_view)
        

class EggThrower(arcade.View):
    def __init__(self, speed):
        super().__init__()
        arcade.set_background_color(arcade.color.WHITE)

        # Спрайты
        self.eagle_list = None
        self.eagle_left_list = None
        self.bg = self.texture = arcade.load_texture(BACKGROUND_IMAGE)


        # Игрок и яйцо
        self.eagle_sprite = None
        self.eagle_x = 400
        self.egg_sprite = None

        # Другие переменные
        self.count_shoots = 3
        self.count_goals = 0
        self.egg_falling = False
        self.egg_ready = True
        self.move_x = 0
        self.current_direction = 1
        self.num_iter = 0
        self.num_frame = 0
        self.egg_y = None
        self.egg_x = None
        self.nest_speed = speed

        self.cont = None
        self.num = None

        # Загрузка звука
        self.music = None  # Добавлено инициализацию

    def setup(self):
        # Создание списков спрайтов
        self.eagle_list = arcade.SpriteList()
        self.eagle_left_list = arcade.SpriteList()

        # Загрузка изображений орла
        for i in range(10):
            img = arcade.Sprite(f"{EAGLE_IMAGE_PREFIX}{i}.png")
            self.eagle_list.append(img)
            img_left = arcade.Sprite(f"{EAGLE_LEFT_IMAGE_PREFIX}{i}.png")
            self.eagle_left_list.append(img_left)

        # Загрузка изображения гнезда и яйца
        self.nest_sprite = arcade.Sprite(NEST_IMAGE)
        self.nest_sprite.center_x = SCREEN_WIDTH // 2
        self.nest_sprite.center_y = 50

        self.egg_sprite = arcade.Sprite(EGG_IMAGE)


        # Проверка, существует ли файл музыки, и загрузка его
        if os.path.exists(MUSIC_FILE):
            self.music = arcade.Sound(MUSIC_FILE)
            self.music.play(-1)

    def on_draw(self):
        self.clear()

        # Отрисовка фона
        arcade.draw_texture_rect(self.bg, arcade.rect.XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT))


        # Отрисовка гнезда
        arcade.draw_sprite(self.nest_sprite)



        # Отрисовка орла
        if self.move_x == -1:
            arcade.draw_sprite(self.eagle_left_list[self.num_frame])
        else:
            arcade.draw_sprite(self.eagle_list[self.num_frame])

        # Отрисовка яйца
        if self.egg_falling:
            self.egg_sprite.center_x = self.egg_x
            self.egg_sprite.center_y = self.egg_y
            arcade.draw_sprite(self.egg_sprite)
        

        # Отрисовка счета
        arcade.draw_text(f"Попадания - {self.count_goals}", SCREEN_WIDTH - 300, 530, arcade.color.BLACK, 35)
        arcade.draw_text(f"Попытки - {self.count_shoots}", SCREEN_WIDTH - 300, 480, arcade.color.BLACK, 35)

    def on_update(self, delta_time):
        self.num_iter += 1
        self.num_frame = self.num_iter // 3 % 9

        # Случайное изменение направления
        if random.random() < 0.05:
            self.current_direction *= -1

        # Движение гнезда
        self.nest_sprite.center_x += self.nest_speed * self.current_direction

        # Ограничение движения гнезда
        if self.nest_sprite.left < 0:
            self.nest_sprite.left = 0
            self.current_direction = 1
        elif self.nest_sprite.right > SCREEN_WIDTH:
            self.nest_sprite.right = SCREEN_WIDTH
            self.current_direction = -1


        #Экран окончания


        if self.count_shoots == 0:
            game_view = EndView(self.num)
            game_view.setup()
            self.window.show_view(game_view)

        # Движение яйца


        
        if self.egg_falling:
            self.egg_y -= 15

            is_collision = arcade.check_for_collision(self.egg_sprite, self.nest_sprite)

            if is_collision:
                self.egg_falling = False
                self.egg_ready = True
                self.count_goals += 1
                self.egg_sprite.center_y = 500

            elif self.egg_y < 0:
                self.egg_falling = False
                self.egg_ready = True
                self.count_shoots -= 1
                self.egg_sprite.center_y = 500

        # Движение орла
        self.eagle_x += self.move_x * 5
        self.eagle_left_list[self.num_frame].center_x = self.eagle_x
        self.eagle_list[self.num_frame].center_x = self.eagle_x
        self.eagle_list[self.num_frame].center_y = 500
        self.eagle_left_list[self.num_frame].center_y = 500

        # Ограничение движения орла
        if self.eagle_left_list[self.num_frame].left < 0:
            self.eagle_x = self.eagle_left_list[self.num_frame].width // 2
        elif self.eagle_list[self.num_frame].right > SCREEN_WIDTH:
            self.eagle_x = SCREEN_WIDTH - self.eagle_list[self.num_frame].width // 2

        if self.nest_speed == 4:
    # Читаем рекорд
            try:
                with open('lvl1.txt', 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        self.num = int(content)
                    else:
                        self.num = 0
            except FileNotFoundError:
                self.num = 0

            # Если текущий счёт больше или равен рекорду — обновляем
            if self.count_goals > self.num:
                with open('lvl1.txt', 'w', encoding='utf-8') as f:
                    f.write(str(self.count_goals))
                self.num = self.count_goals  # обновляем рекорд в памяти

        elif self.nest_speed == 5:
            try:
                with open('lvl2.txt', 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        self.num = int(content)
                    else:
                        self.num = 0
            except FileNotFoundError:
                self.num = 0

            if self.count_goals > self.num:
                with open('lvl2.txt', 'w', encoding='utf-8') as f:
                    f.write(str(self.count_goals))
                self.num = self.count_goals

        elif self.nest_speed == 6:
            try:
                with open('lvl3.txt', 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        self.num = int(content)
                    else:
                        self.num = 0
            except FileNotFoundError:
                self.num = 0

            if self.count_goals > self.num:
                with open('lvl3.txt', 'w', encoding='utf-8') as f:
                    f.write(str(self.count_goals))
                self.num = self.count_goals


    def on_key_press(self, key, modifiers):
        # Движение орла
        if key == arcade.key.D:
            self.move_x = 1
        elif key == arcade.key.A:
            self.move_x = -1
        # Прыжок
        elif key == arcade.key.SPACE and self.egg_ready:
            self.egg_falling = True
            self.egg_ready = False
            self.egg_x = self.eagle_list[self.num_frame].center_x
            self.egg_y = self.eagle_list[self.num_frame].center_y

    def on_key_release(self, key, modifiers):
        if key == arcade.key.D:
            if self.move_x == 1:
                self.move_x = 0
        elif key == arcade.key.A:
            if self.move_x == -1:
                self.move_x = 0

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start = StartView()
    window.show_view(start)
    start.setup()
    arcade.run()
    
if __name__ == "__main__":
    main()
