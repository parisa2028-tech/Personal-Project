import pygame
pygame.init()
pygame.mixer.init()

# All constants
WIN_WIDTH = 500
WIN_HEIGHT = 600
scroll_speed = 1
BASE_PILLAR_SPEED = 1
pillar_speed = BASE_PILLAR_SPEED
CLOUD_SPEED = 1   # So the clouds always drift slowly (don't get speed up with the pillars)

SPEED_INCREASE_INTERVAL = 10000  # every 10 seconds (1000 = 1 sec)
SPEED_INCREASE_AMOUNT = 1 # pixels per frame
MAX_PILLAR_SPEED = 15 # cap so the game doesn't become impossible to play

# Gap size between top and bottom pillars
GAP_SIZE = 100
SPAWN_DELAY = 4000  # in milliseconds (1000 ms = 1 sec)


# Key pressed to sprite position dictionary (much cleaner than before)
key_positions = {
    pygame.K_1: (50,100),
    pygame.K_2: (50,200),
    pygame.K_3: (50, 300),
    pygame.K_4: (50, 400),
    pygame.K_5: (180, 100),
    pygame.K_6: (180, 200),
    pygame.K_7: (180, 300),
    pygame.K_8: (180, 400),
    pygame.K_9: (180, 500),
}

# Key pressed to make sound
key_sounds = {
    pygame.K_1: pygame.mixer.Sound("sfx/SFX Do.wav"),
    pygame.K_2: pygame.mixer.Sound("sfx/SFX Re.wav"),
    pygame.K_3: pygame.mixer.Sound("sfx/SFX Mi v2.wav"),
    pygame.K_4: pygame.mixer.Sound("sfx/SFX Fa v2.wav"),
    pygame.K_5: pygame.mixer.Sound("sfx/SFX So v2.wav"),
    pygame.K_6: pygame.mixer.Sound("sfx/SFX La v2.wav"),
    pygame.K_7: pygame.mixer.Sound("sfx/SFX Ti v2.wav"),
    pygame.K_8: pygame.mixer.Sound("sfx/SFX High Do.wav"),
    pygame.K_9: pygame.mixer.Sound("sfx/SFX High Re.wav")
}

# Images for main game and sandbox
bg_image = pygame.image.load("images/sky.png")
moving_cloud_image = pygame.image.load("images/clouds.png")
bird_image = pygame.image.load("images/bird.png")
scaled_bird_image = pygame.transform.smoothscale(bird_image, (50, 50))
top_pillar_image = pygame.image.load("images/top_pillar.png")
game_over_image = pygame.image.load("images/game_over_bird.png")
scaled_game_over = pygame.transform.scale(game_over_image, (500, 500))

string_image = pygame.image.load("images/string.png")
scaled_string_image = pygame.transform.scale(string_image, (5, WIN_HEIGHT))


scaled_top_pillar_image = pygame.transform.smoothscale(top_pillar_image,(100, 200))

scaled_bg_image = pygame.transform.smoothscale(bg_image, (WIN_WIDTH, WIN_HEIGHT))
scaled_moving_cloud_image = pygame.transform.smoothscale(moving_cloud_image, (100, WIN_HEIGHT/2))

# Text for intro & tutorial
# Heading text
heading = pygame.font.SysFont("Alice", 50).render("How to play PILLAR DODGE!", True, 'white')

# Solfege text
solfege_text = pygame.font.SysFont("Alice", 25).render("Keybinds: Solfege (Do Re Mi)", True, 'white')

# Thai solfege text
thai_solfege_text = pygame.font.SysFont("Alice", 25).render("Keybinds: Thai Solfege", True, 'white')

# More information text
info1_text = pygame.font.SysFont("Alice", 30).render("Game Information: ", True, 'white')
info2_text = pygame.font.SysFont("Alice", 20).render("Each keybind corresponds with a note.", True, 'white')
info3_text = pygame.font.SysFont("Alice", 20).render("Ex. (press 1 for C)", True, 'white')
info4_text = pygame.font.SysFont("Alice", 25).render("Main Game:", True, 'white')
info5_text = pygame.font.SysFont("Alice", 20).render("Press numbers 1-9 to dodge the pillars.", True, 'white')
info52_text = pygame.font.SysFont("Alice", 20).render("Switch strings by pressing",True,'white')
info53_text = pygame.font.SysFont("Alice", 20).render("1st string: keys 1-4, 2nd string: keys 5-9",True,'white')
info6_text = pygame.font.SysFont("Alice", 20).render("If the bird crashes into the pillar, you LOSE!", True, 'white')
info7_text = pygame.font.SysFont("Alice", 25).render("Sandbox:", True, 'white')
info8_text = pygame.font.SysFont("Alice", 20).render("Experiment with notes, play new songs and have FUN!", True,'white')
info9_text = pygame.font.SysFont("Alice", 20).render("Fun Fact: Dodge the Pillars is inspired by the thai instrument Saw U.", True, 'white')
info10_text = pygame.font.SysFont("Alice", 20).render("All sound effects are made with Saw U", True, 'white')

# Keybinds
keybinds = pygame.image.load("images/keybinds.png")
# Scale image
scaled_keybinds = pygame.transform.scale(keybinds, (250, 75))

# Thai keybinds
thai_keybinds = pygame.image.load("images/thai_keybinds.png")
# Scale image
scaled_thai_keybinds = pygame.transform.scale(thai_keybinds, (250, 75))

# Tutorial example image
tutorial_example = pygame.image.load("images/tutorial_ex.png")
# Scale image
scaled_tutorial_example = pygame.transform.scale(tutorial_example, (320, 400))
