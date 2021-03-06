import pygame
import pygame_menu
import random
from os import path
from pygame.mixer import music

from debug import debug

game_folder = path.dirname(__file__)
img_dir = path.join(game_folder, 'img')

WIDTH = 1920
HEIGHT = 1080
FPS = 60

MAX_MOBS = 50
vol = 8

NEWMOB_TIME = 1000
# Задаем цветаМ
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

PARTICLE_LIVE = 1 * 1000
PARTICLE_DELAY = 10

ABOUT = ['Run away from big circles being a small circle!',
         'how to play:',
         "arrow controls, p to pause, don't touch space"]

# Создаем игру и окно
pygame.init()
pygame.mixer.init()

music_nya = "sounds/nya.mp3"
music_defolt = "sounds/electronic-senses-plastic-flowers.mp3"
sound_dead = pygame.mixer.Sound("sounds/minecraft-death-sound.mp3")
sound_start = pygame.mixer.Sound("sounds/supercell_start.mp3")

font_name = "arial"

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("circles")

sound_start.play()

clock = pygame.time.Clock()

music.load(music_defolt)

particle = None


def color_selector(selected_value, color, **kwargs):
    global player_img, mob_img, color_back, back_music, particle

    color_selector, index = selected_value

    if color_selector[1] == 1:
        player_img = "player.png"
        mob_img = "mob.png"
        particle = None
        color_back = (47, 113, 117)
        music.load(music_defolt)

    elif color_selector[1] == 2:
        player_img = "player_orange.png"
        mob_img = "mob_orange.png"
        particle = None
        color_back = (129, 52, 5)
        music.load(music_defolt)

    elif color_selector[1] == 3:
        player_img = "player_purple.png"
        mob_img = "mob_purple.png"
        particle = None
        color_back = (90, 24, 154)
        music.load(music_defolt)

    elif color_selector[1] == 4:
        player_img = "player_green.png"
        mob_img = "mob_green.png"
        particle = None
        color_back = (21, 93, 39)
        music.load(music_defolt)

    elif color_selector[1] == 5:
        player_img = "player_white.png"
        mob_img = "mob_white.png"
        particle = None
        color_back = (82, 97, 107)
        music.load(music_defolt)

    elif color_selector[1] == 6:
        player_img = "player_catnyan.png"
        mob_img = "mob_donut.png"
        particle = ParticleNyan(size=5)
        color_back = (1, 68, 121)
        music.load(music_nya)


def start_the_game():
    menu.disable()
    pygame.mouse.set_visible(False)


def new_mob(n=1):
    for _ in range(n):
        Mob()


def draw_text(surf, text, size, x, y, color=WHITE):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


class Character(pygame.sprite.Sprite):
    def __init__(self, filename, *groups):
        super(Character, self).__init__(all_sprites, *groups)
        self.image = pygame.image.load(path.join(img_dir, filename)).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


class Particle:
    def __init__(self, size):
        self.particles = []
        self.size = size

    def add_particles(self, position):
        pass

    def delete_particles(self):
        pass

    def draw(self):
        pass


class Player(Character):
    def __init__(self, particle):
        super(Player, self).__init__(player_img)
        self.speedx = 0
        self.speedy = 0
        self.speed = 5
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2
        self.input = None
        self.particle = particle
        self.particle_timer = pygame.time.get_ticks()
        self.direction = 'right'

    def flip_image(self, direction):
        if self.direction != direction:
            self.direction = direction
            self.image = pygame.transform.flip(self.image, True, False)

    def mouse_input(self):
        mouse_pos = pygame.mouse.get_pos()
        self.rect.center = mouse_pos
        rel_x = pygame.mouse.get_rel()[0]
        if rel_x > 0:
            self.flip_image('right')
        elif rel_x < 0:
            self.flip_image('left')

    def keyboard_input(self):
        self.speedx = 0
        self.speedy = 0

        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT]:
            self.speedx = -self.speed
            self.flip_image('left')
        if keystate[pygame.K_RIGHT]:
            self.speedx = self.speed
            self.flip_image('right')
        if keystate[pygame.K_UP]:       self.speedy = -self.speed
        if keystate[pygame.K_DOWN]:     self.speedy = self.speed

        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def define_input(self, input_mode):
        match input_mode:
            case 'keyboard':
                self.input = self.keyboard_input
            case 'mouse':
                self.input = self.mouse_input

    def draw(self):
        if self.particle:
            if pygame.time.get_ticks() - self.particle_timer >= PARTICLE_DELAY:
                self.particle.add_particles(self.rect.midleft if self.direction == 'right' else self.rect.midright)
                self.particle.draw()
                self.particle_timer = pygame.time.get_ticks()

    def update(self):
        self.input()
        if self.rect.right > WIDTH:     self.rect.right = WIDTH
        if self.rect.left < 0:          self.rect.left = 0
        if self.rect.top < 0:           self.rect.top = 0
        if self.rect.bottom > HEIGHT:   self.rect.bottom = HEIGHT


class Mob(Character):
    def __init__(self):
        super(Mob, self).__init__(mob_img, mobs)

        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + self.rect.height + 5 or self.rect.left < -(
                self.rect.width + 5) or self.rect.right > WIDTH + self.rect.width + 5:
            new_mob()
            self.kill()


class ParticleNyan(Particle):
    def add_particles(self, position):
        spawn_time = pygame.time.get_ticks()
        offset_x = -4

        particle_rect_1 = (pygame.rect.Rect(position[0] + offset_x, position[1] - self.size * 3, self.size, self.size), pygame.Color('Red'))
        particle_rect_2 = (pygame.rect.Rect(position[0] + offset_x, position[1] - self.size * 2, self.size, self.size), pygame.Color('Orange'))
        particle_rect_3 = (pygame.rect.Rect(position[0] + offset_x, position[1] - self.size, self.size, self.size), pygame.Color('Yellow'))
        particle_rect_4 = (pygame.rect.Rect(position[0] + offset_x, position[1], self.size, self.size), pygame.Color('Green'))
        particle_rect_5 = (pygame.rect.Rect(position[0] + offset_x, position[1] + self.size, self.size, self.size), pygame.Color('Lightblue'))
        particle_rect_6 = (pygame.rect.Rect(position[0] + offset_x, position[1] + self.size * 2, self.size, self.size), pygame.Color('Blue'))
        particle_rect_7 = (pygame.rect.Rect(position[0] + offset_x, position[1] + self.size * 3, self.size, self.size), pygame.Color('Purple'))

        particle = (spawn_time, particle_rect_1, particle_rect_2, particle_rect_3, particle_rect_4,
                    particle_rect_5, particle_rect_6, particle_rect_7)

        self.particles.append(particle)

    def delete_particles(self):
        particles_copy = [particle for particle in self.particles if pygame.time.get_ticks() - particle[0] < PARTICLE_LIVE]
        self.particles = particles_copy

    def draw(self):
        if self.particles:
            self.delete_particles()
            for particle in self.particles:
                for rect in particle[1:]:
                    pygame.draw.rect(screen, rect[1], rect[0])


sound = pygame_menu.sound.Sound()
sound.set_sound(pygame_menu.sound.SOUND_TYPE_KEY_ADDITION, "sounds/choose.mp3", volume=1)
sound.set_sound(pygame_menu.sound.SOUND_TYPE_WIDGET_SELECTION, "sounds/choose.mp3", volume=1)
sound.set_sound(pygame_menu.sound.SOUND_TYPE_CLICK_TOUCH, "sounds/choose.mp3", volume=1)


mytheme = pygame_menu.themes.Theme(background_color=(16, 0, 43, 255),
                                   title_background_color=(36, 0, 70),
                                   title_font_shadow=False,
                                   widget_padding=20,
                                   widget_font_color='#E0AAFF',
                                   widget_font=pygame.font.Font('./fonts/fortnitebattlefest.ttf', 50))
mytheme.title = False

menu = pygame_menu.Menu('', 1920, 1080, theme=mytheme)
settings_menu = pygame_menu.Menu('Settings', 1920, 1080, theme=mytheme)
about_menu = pygame_menu.Menu('About Game', 1920, 1080, theme=mytheme)

# Main Menu
menu.set_sound(sound, recursive=True)
menu.add.label(
    'ball game',
    background_color='#240046',
    background_inflate=(30, 0),
    float=False,
    font_size=80
).translate(0, -10)
menu.add.label('Your Score: 0 s', label_id='l_record').set_margin(x=0, y=50)
menu.add.button('Play', start_the_game)
menu.add.button('Settings', settings_menu)
menu.add.button('About', about_menu)
menu.add.button('Quit', pygame_menu.events.EXIT)

# Settings Menu
settings_menu.set_sound(sound, recursive=True)
movement_mode = settings_menu.add.toggle_switch('Game Control',
                                                True,
                                                toogleswitch_id='toogleswitch',
                                                state_text=('mouse', 'keyboard'),
                                                state_values=('mouse', 'keyboard'),
                                                width=250,
                                                slider_color=(255, 255, 255, 0),
                                                state_color=((255, 255, 255, 0), (255, 255, 255, 0)),
                                                switch_border_color=(255, 255, 255),
                                                state_text_font_color=('#E0AAFF', '#E0AAFF'))

settings_menu.add.selector('Style ', [('blue', 1),
                                      ('orange', 2),
                                      ('purple', 3),
                                      ('green', 4),
                                      ('white', 5),
                                      ('nyan cat', 6)],
                           onchange=color_selector,
                           onreturn=color_selector,
                           style=pygame_menu.widgets.SELECTOR_STYLE_FANCY,
                           style_fancy_bgcolor=(180, 180, 180, 0),
                           style_fancy_arrow_color=(255, 255, 255),
                           style_fancy_bordercolor=(255, 255, 255))

selector_mod = settings_menu.add.dropselect(
    title='Choose mod',
    items=[('Easy', 0),
           ('Normal', 1),
           ('Hard', 2),
           ('Unreal', 3)],
    font_size=30,
    selection_option_font_color='#E0AAFF',
    selection_option_selected_font_color='#E0AAFF',
    default=0,
    selection_option_font_size=25,
    selection_box_bgcolor=(255, 255, 255, 0),
    selection_box_arrow_color=(16, 0, 43, 255),
    selection_box_border_color=(255, 255, 255))

slider = settings_menu.add.range_slider('Mob Counter', MAX_MOBS, (1, 150), 1, rangeslider_id='range_slider',
                                        value_format=lambda x: str(int(x)))

volume_slider = settings_menu.add.range_slider('Volume', vol, (0, 10), 1, rangeslider_id='range_slider2',
                                               value_format=lambda x: str(int(x)))

settings_menu.add.button('Return to menu', pygame_menu.events.BACK)

# About Menu
about_menu.set_sound(sound, recursive=True)
about_menu.add.label(
    'About Game',
    background_color='#240046',
    background_inflate=(30, 0),
    float=False, font_size=80)

for elem in ABOUT:
    about_menu.add.label(elem, font_size=50)
    about_menu.add.vertical_margin(10)

about_menu.add.button('Return to menu', pygame_menu.events.BACK)

# Image init
player_img = "player.png"
mob_img = "mob.png"
color_back = (47, 113, 117)

# Цикл игры
game_over = True
running = True
paused = False
while running:
    if game_over:
        # if back_music:
        music.stop()

        if menu.is_enabled():
            menu.mainloop(screen)

        if slider.value_changed():
            MAX_MOBS = slider.get_value() - 1

        if volume_slider.value_changed():
            vol = volume_slider.get_value()
        pygame.mixer.music.set_volume(vol / 10)

        selected_value = selector_mod.get_value()[0][1]
        if selected_value == 0:
            NEWMOB_TIME = 1000
        elif selected_value == 1:
            NEWMOB_TIME = 500
        elif selected_value == 2:
            NEWMOB_TIME = 100
        elif selected_value == 3:
            NEWMOB_TIME = 5

        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()

        player = Player(particle=particle)

        player.define_input(movement_mode.get_value())

        time_in_game = 0

        start_time = pygame.time.get_ticks()

        mob_spawn_time = pygame.time.get_ticks()

        game_over = False

        # if music:
        music.play()

        clock.tick(FPS)

    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
                music.pause()
            if event.key == pygame.K_ESCAPE:
                running = False

    if not paused and not game_over:
        music.unpause()
        time_in_game += clock.get_time()
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            new_mob()

        if mob_spawn_time < pygame.time.get_ticks() - NEWMOB_TIME and len(mobs) <= MAX_MOBS:
            mob_spawn_time = pygame.time.get_ticks()
            new_mob()

        for hit in pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_mask):
            game_over = True
            menu.get_widget('l_record').set_title(f'Your Score: {round(time_in_game / 1000, 2)} s')
            menu.enable()
            sound_dead.play()

        # Обновление
        all_sprites.update()

        # Рендеринг
        screen.fill(color_back)
        all_sprites.draw(screen)
        player.draw()
        # draw_text(screen, str(len(mobs)), 20, WIDTH / 2, 10)
        # draw_text(screen, str(f'{time_in_game / 1000 :.2f}'), 20, WIDTH / 2, 30)

        # После отрисовки всего, переворачиваем экран
        pygame.display.flip()

pygame.quit()
