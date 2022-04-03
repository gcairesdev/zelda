from support import *

FPS = 60
TILE_SIZE = 64
TITLE = 'Zelda Pygame'

UI_BAR_HEIGHT = 20
UI_HEALTH_BAR_WIDTH = 200
UI_ENERGY_BAR_WIDTH = 140
UI_ITEM_BOX_SIZE = 80
UI_FONT = resourcePath('src/font/joystix.ttf')
UI_FONT_SIZE = 18
UI_TEXT_COLOR = '#EEEEEE'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
UI_BORDER_COLOR_ACTIVE = 'gold'
UI_HEALTH_COLOR = '#E0394C'
UI_ENERGY_COLOR = '#7180EE'

TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'

WATER_COLOR = '#71DDEE'

WEAPON_DATA = {
    'sword': {
        'cooldown': 100,
        'damage': 15,
        'graphic': resourcePath('src/img/weapons/sword/full.png')
    },
    'lance': {
        'cooldown': 400,
        'damage': 30,
        'graphic': resourcePath('src/img/weapons/lance/full.png')
    },
    'axe': {
        'cooldown': 300,
        'damage': 20,
        'graphic': resourcePath('src/img/weapons/axe/full.png')
    },
    'rapier': {
        'cooldown': 50,
        'damage': 8,
        'graphic': resourcePath('src/img/weapons/rapier/full.png')
    },
    'sai': {
        'cooldown': 80,
        'damage': 10,
        'graphic': resourcePath('src/img/weapons/sai/full.png')
    }
}

MAGIC_DATA = {
    'flame': {
        'strength': 5,
        'cost': 20,
        'graphic': resourcePath('src/img/particles/flame/fire.png')
    },
    'heal': {
        'strength': 20,
        'cost': 10,
        'graphic': resourcePath('src/img/particles/heal/heal.png')
    }
}

ENEMY_DATA = {
    'squid': {
        'health': 100,
        'exp': 100,
        'damage': 20,
        'attackType': 'slash',
        'attackSound': resourcePath('src/audio/attack/slash.wav'),
        'speed': 3,
        'resistance': 3,
        'attackRadius': 80,
        'noticeRadius': 360
    },
    'raccoon': {
        'health': 300,
        'exp': 250,
        'damage': 40,
        'attackType': 'claw',
        'attackSound': resourcePath('src/audio/attack/claw.wav'),
        'speed': 2,
        'resistance': 3,
        'attackRadius': 120,
        'noticeRadius': 400
    },
    'spirit': {
        'health': 100,
        'exp': 110,
        'damage': 8,
        'attackType': 'thunder',
        'attackSound': resourcePath('src/audio/attack/fireball.wav'),
        'speed': 4,
        'resistance': 3,
        'attackRadius': 60,
        'noticeRadius': 350
    },
    'bamboo': {
        'health': 70,
        'exp': 120,
        'damage': 6,
        'attackType': 'leaf_attack',
        'attackSound': resourcePath('src/audio/attack/slash.wav'),
        'speed': 3,
        'resistance': 3,
        'attackRadius': 50,
        'noticeRadius': 300
    }
}

HITBOX_OFFSET = {
    'player': -26,
    'object': -40,
    'grass': -10,
    'invisible': 0,
}
