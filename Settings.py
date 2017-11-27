#Settings
TITLE = "Lunar  Jump!"
WIDTH = 500
HEIGHT = 650
FPS = 60
FONT_NAME = 'sailor moon 2010'
HS_FILE = "highscore.txt"

#player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 1
PLAYER_JUMP = 28

#Game Properties
BOOST_POWER = 60
POW_SPAWN_PCT = 7
BOW_SPAWN_PCT = 4
LIFE_SPAWN_PCT = 2
ENEMY_FREQ = 2000
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
POWER_LAYER = 1
ENEMY_LAYER = 2
STAR_LAYER = 0
BOW_LAYER = 1
LIFE_LAYER = 1

#starting platforms
PLATFORM_LIST = [(0, HEIGHT - 60),
                (WIDTH / 2 - 50, HEIGHT * 3 / 4),
                (125, HEIGHT - 350),
                (350, 200),
                (175, 100)]

#define colors
MIDNIGHT = (25, 25, 112)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 153)
BLACK = (0, 0, 0)
HPINK = (255, 0, 128)
PINK = (255, 192, 203)
BLUE = (173, 216, 230)
