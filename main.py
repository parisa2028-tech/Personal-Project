import pygame, sys, asyncio
from sys import exit
import random
import sys
from settings import (WIN_WIDTH, WIN_HEIGHT, CLOUD_SPEED, key_positions, bg_image, scaled_bird_image, moving_cloud_image,
                      scaled_moving_cloud_image, scaled_top_pillar_image, scaled_bg_image, GAP_SIZE, SPAWN_DELAY,
                      BASE_PILLAR_SPEED, scaled_game_over, scaled_string_image, heading, solfege_text, thai_solfege_text,
                      info1_text, info2_text, info3_text, info4_text, info5_text, info6_text, info7_text, info8_text,
                      info9_text, info10_text, scaled_keybinds, scaled_thai_keybinds, scaled_tutorial_example, key_sounds,
                      BASE_PILLAR_SPEED, SPEED_INCREASE_AMOUNT, SPEED_INCREASE_INTERVAL, MAX_PILLAR_SPEED, pillar_speed,
                      info52_text, info53_text, sub_heading)

# Initialize pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()
# Allow for control of frame rate of game
clock = pygame.time.Clock()

# Set up main window
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

# Buttons for main menu
class Button:
    def __init__(self, pos, text_input, font, base_color, hovering_color='dark blue', rect_color='dark grey'):
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input = text_input
        self.rect_color = rect_color

        # Render text surface
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.text_rect = self.text.get_rect(center=pos)

        # Button rectangle (for padding around text, hello padding nice to see you again after the music player)
        self.rect = pygame.Rect(0, 0, self.text_rect.width + 40, self.text_rect.height + 20)
        self.rect.center = pos

    def update(self, screen):
        # Draw rectangle background
        pygame.draw.rect(screen, self.rect_color, self.rect, border_radius=8)
        # Draw text
        screen.blit(self.text, self.text_rect)

    def check_for_input(self, position):
        # Return True if mouse clicked inside button rect
        return self.rect.collidepoint(position)

    def change_color(self, position):
        # Change text color when hovering over
        if self.rect.collidepoint(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

# Intro & Tutorial
async def tutorial():
    pygame.display.set_caption("Tutorial (press the key 'x' to exit)")

    # Set keybinds image as rectangle
    scaled_keybinds_rect = scaled_keybinds.get_rect(center=(135, 170))

    # Set thai keybinds image as rectangle
    scaled_thai_keybinds_rect = scaled_thai_keybinds.get_rect(center=(135, 290))

    # Set tutorial example image as rectangle
    scaled_tutorial_example_rect = scaled_tutorial_example.get_rect(center=(450, 290))


    # --- Game loop ---
    run = True
    while run:
        # Draw background onto screen
        window.blit(scaled_bg_image, (0, 0))

        # Draw text onto screen
        window.blit(heading, (10, 30))
        window.blit(sub_heading, (10, 70))
        window.blit(solfege_text, (10, 100))
        window.blit(thai_solfege_text, (10, 220))
        window.blit(info1_text, (10, 360))
        window.blit(info2_text, (10, 385))
        window.blit(info3_text, (10, 400))
        window.blit(info52_text, (10, 415))
        window.blit(info53_text, (10, 430))

        window.blit(info4_text, (10, 460))
        window.blit(info5_text, (10, 475))
        window.blit(info6_text, (10, 490))
        window.blit(info7_text, (10, 520))
        window.blit(info8_text, (10, 545))
        window.blit(info9_text, (10, 560))
        window.blit(info10_text, (10, 575))

        # Draw image onto screen
        window.blit(scaled_keybinds, scaled_keybinds_rect)
        window.blit(scaled_thai_keybinds, scaled_thai_keybinds_rect)
        window.blit(scaled_tutorial_example, scaled_tutorial_example_rect)

        # Draw border around tutorial_example_rect (light gray)
        pygame.draw.rect(window, (255, 255, 255), scaled_tutorial_example_rect, 4)

        # If pressed key 'x' get transported back to main menu (changed from pygame quit bc itch.io has no red x button)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    await main()


        pygame.display.update()
        await asyncio.sleep(0)

# Main Game
async def play():
    pygame.display.set_caption("Main Game (press the key 'x' to exit)")

    # Cloud sprites (my beloved, you are the only one that was relatively easy to code)
    class Cloud(pygame.sprite.Sprite):
        # __init__ defines sprite position using xy coordinates
        def __init__(self, x, y, scale=1.0):
            # Initialize base class
            super().__init__()
            # Set sprite as image (original, not scaled version)
            # Convert alpha makes images transparent
            base = moving_cloud_image.convert_alpha()
            # w is width, h is height
            w, h = base.get_size()
            # Scale proportionally
            self.image = pygame.transform.smoothscale(base, (int(w * scale), int(h * scale)))
            self.image.set_alpha(120)  # Transparency (invi-solid): 0-255
            self.rect = self.image.get_rect(topleft=(x, y))

        def update(self):
            # Move the cloud
            # Subtract scroll speed from x position of rectangle
            self.rect.x -= CLOUD_SPEED
            # Delete part of rectangle that is offscreen
            if self.rect.right < 0:
                self.kill()

    # String C
    class StringC(pygame.sprite.Sprite):
        def __init__(self, x, y):
            # Initialize base class
            super().__init__()
            # Set sprite as image (original, not scaled version)
            # Convert alpha makes images transparent
            self.image = scaled_string_image.convert_alpha()
            self.image.set_alpha(180)  # Transparency (invi-solid): 0-255
            self.rect = self.image.get_rect(topleft=(x, y))

    # String G
    class StringG(pygame.sprite.Sprite):
        def __init__(self, x, y):
            # Initialize base class
            super().__init__()
            # Set sprite as image (original, not scaled version)
            # Convert alpha makes images transparent
            self.image = scaled_string_image.convert_alpha()
            self.image.set_alpha(180)  # Transparency (invi-solid): 0-255
            self.rect = self.image.get_rect(topleft=(x, y))

    # Bird sprite
    class Bird(pygame.sprite.Sprite):
        # __init__ defines sprite position using xy coordinates
        def __init__(self, x, y):
            # Initialize base class
            super().__init__()
            # Set sprite as bird image
            self.image = scaled_bird_image
            # Set sprite image as rectangle for movement (topleft)
            self.rect = scaled_bird_image.get_rect(topleft=(x, y))

            # Bird movement state
            self.target_pos = self.rect.topleft
            # Pixels per frame (5)
            self.speed = 5

            # Start as being "at target"
            self.at_target = True

        def update(self):
            # Current position
            x, y = self.rect.topleft
            # Target position
            tx, ty = self.target_pos

            # bird movement on x-axis (# snap directly to target x)
            x = tx

            # bird movement on y-axis (smooooth glide)
            # Only for y bc I want instant movement between K.1-K.4 and K.5-K.9 (between strings)
            if y < ty:
                y += min(self.speed, ty - y)
            if y > ty:
                y -= min(self.speed, y - ty)

            # Apply the new xy cooridnate/position back to sprite rect (Basically update sprite rectangle)
            self.rect.topleft = (x, y)

            # Check if bird has reached its target
            self.at_target = (x == tx and y == ty)

    # Pillar Sprites
    class Pillar(pygame.sprite.Sprite):
        def __init__(self, x, y, height, flipped=False):
            super().__init__()
            base_image = scaled_top_pillar_image
            # Scale image to needed height
            self.image = pygame.transform.scale(base_image, (base_image.get_width(), height))
            if flipped:
                self.image = pygame.transform.flip(self.image, False, True)
                self.rect = self.image.get_rect(bottomleft=(x, y))
            else:
                self.rect = self.image.get_rect(topleft=(x, y))

        def update(self):
            # Move the pillar
            # Subtract scroll speed from x position of rectangle
            global pillar_speed
            self.rect.x -= pillar_speed
            # Delete part of rectangle that is offscreen
            if self.rect.right < 0:
                self.kill()

    # The all sprites group consists of...ba dam ba dam...the bird and the clouds, and the strings
    # The add cloud is below in the events portion bc code doesn't run properly if I put it here (order of events)
    all_sprites = pygame.sprite.Group()
    bird = Bird(50, 200)
    stringc = StringC(70, 0)
    stringg = StringG(200, 0)
    all_sprites.add(stringc, stringg, bird)

    # Seperate from all_sprites group (bird and clouds group)
    all_pillars = pygame.sprite.Group()
    last_spawn_time = pygame.time.get_ticks()

    # Cloud spawn event (every 2 seconds)
    SPAWN_CLOUD = pygame.USEREVENT + 1
    # 1000 ms = 1 second
    pygame.time.set_timer(SPAWN_CLOUD, 5000)


    # ----------***Main Loop Starts Here***-----------
    # When pygame is running, main window will appear and stay
    run = True
    while run:
        # Make access universal (global instead of local)
        global pillar_speed, scroll_speed, last_speed_increase_time

        # Draw background (blit displays image and image position)
        window.blit(scaled_bg_image, (0, 0))

        # Events
        # If pressed key 'x' get transported back to main menu (changed from pygame quit bc itch.io has no red x button)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    await main()
            if event.type == SPAWN_CLOUD:
                # Spawn cloud only on timer (so they don't get squished)
                # Clouds start offscreen (right side) with random position and scale
                random_cloud_x = random.randint(WIN_WIDTH, WIN_WIDTH + 200)
                # We shall get ~floaty~ clouds, because they are not always at same height
                random_cloud_y = random.randint(50, 300)
                # Clouds vary in size but keep proportions (finally, they are not squished)
                random_scale = random.uniform(0.5, 1.2)
                cloud = Cloud(random_cloud_x, random_cloud_y, scale=random_scale)
                all_sprites.add(cloud)
            # If key gets pressed, player moves to specific x y coordinate
            elif event.type == pygame.KEYDOWN:
                # Looks up whether that key is pressed (from dictionary ([key] in previous line), if it is the loop is run (handle once-per-press)
                if event.key in key_positions:
                    # Moves rectangle with bird sprite using the topleft coordinates of the rectangle to target position
                    bird.target_pos = key_positions[event.key]
                    # play sound if exists
                    if event.key in key_sounds:
                        key_sounds[event.key].play()

        # Spawn pillars
        current_time = pygame.time.get_ticks()
        if current_time - last_spawn_time > SPAWN_DELAY:
            # 20% chance to spawn a full pillar
            if random.random() < 0.2:
                full_pillar = Pillar(WIN_WIDTH, 0, WIN_HEIGHT, flipped=False)
                all_pillars.add(full_pillar)
            else:
                # 80% chance to spawn a normal gap pair pillars
                # Random position for gap
                gap_y = random.randint(150, WIN_HEIGHT - 150 - GAP_SIZE)

                # Dynamically resizes image (thank you pygame.transform.scale)
                # Top pillar stretches from top of screen to gap_y (so it doesn't look wonky)
                # For top pillar, flip it vertically and anchor it to the bottom of the gap.
                top_height = gap_y
                top_pillar = Pillar(WIN_WIDTH, gap_y, top_height, flipped=True)

                # Bottom pillar stretches from bottom of gap to bottom of screen (same here)
                # For bottom pillar, anchor it to the top of the gap. (0----- kind of like wraaaamp)
                bottom_height = WIN_HEIGHT - (gap_y + GAP_SIZE)
                bottom_pillar = Pillar(WIN_WIDTH, gap_y + GAP_SIZE, bottom_height, flipped=False)

                all_pillars.add(top_pillar, bottom_pillar)
            last_spawn_time = current_time

        # Gradually increase pillar speed (pillars speed up)
        current_time = pygame.time.get_ticks()
        # Keep track of when the speed last increased
        last_speed_increase_time = pygame.time.get_ticks()
        if current_time - last_speed_increase_time >= SPEED_INCREASE_INTERVAL:
            if pillar_speed < MAX_PILLAR_SPEED:
                pillar_speed += SPEED_INCREASE_AMOUNT
            last_speed_increase_time = current_time

        # Update Assets - Clouds, Pipes, Bird (may need to switch)
        all_sprites.update()
        all_pillars.update()

        # Displays game over image when bird collides with pillar
        if bird.at_target and pygame.sprite.spritecollide(bird, all_pillars, False,
                                                          collided=pygame.sprite.collide_rect_ratio(0.5)):
            window.blit(scaled_game_over, (20, 70))
            pygame.display.update()  # refresh screen so it's visible
            # Waits for 0.5 seconds
            await asyncio.sleep(1)  # don't use pygame.time.delay bc it doesn't work well with pygbag
            # Illusion of game over (go back to main menu)
            await main()

        # Draw Assets - Clouds, Pipes, Bird
        # Current draw order:
        # 1. Clouds + Bird (from all_sprites)
        # 2. Pillars
        all_sprites.draw(window)
        all_pillars.draw(window)

        clock.tick(60)
        # Update the display
        pygame.display.update()
        await asyncio.sleep(0)

# Sandbox
async def sandbox():
    pygame.display.set_caption("Sandbox (press the key 'x' to exit)")

    # Cloud sprites (my beloved, you are the only one that was relatively easy to code)
    class Cloud(pygame.sprite.Sprite):
        # __init__ defines sprite position using xy coordinates
        def __init__(self, x, y, scale=1.0):
            # Initialize base class
            super().__init__()
            # Set sprite as image (original, not scaled version)
            # Convert alpha makes images transparent
            base = moving_cloud_image.convert_alpha()
            # w is width, h is height
            w, h = base.get_size()
            # Scale proportionally
            self.image = pygame.transform.smoothscale(base, (int(w * scale), int(h * scale)))
            self.image.set_alpha(180)  # Transparency (invi-solid): 0-255
            self.rect = self.image.get_rect(topleft=(x, y))

        def update(self):
            # Move the cloud
            # Subtract scroll speed from x position of rectangle
            self.rect.x -= CLOUD_SPEED
            # Delete part of rectangle that is offscreen
            if self.rect.right < 0:
                self.kill()

    # String C
    class StringC(pygame.sprite.Sprite):
        def __init__(self, x, y):
            # Initialize base class
            super().__init__()
            # Set sprite as image (original, not scaled version)
            # Convert alpha makes images transparent
            self.image = scaled_string_image.convert_alpha()
            self.image.set_alpha(180)  # Transparency (invi-solid): 0-255
            self.rect = self.image.get_rect(topleft=(x, y))

    # String G
    class StringG(pygame.sprite.Sprite):
        def __init__(self, x, y):
            # Initialize base class
            super().__init__()
            # Set sprite as image (original, not scaled version)
            # Convert alpha makes images transparent
            self.image = scaled_string_image.convert_alpha()
            self.image.set_alpha(200)  # Transparency (invi-solid): 0-255
            self.rect = self.image.get_rect(topleft=(x, y))

    # Bird sprite
    class Bird(pygame.sprite.Sprite):
        # __init__ defines sprite position using xy coordinates
        def __init__(self, x, y):
            # Initialize base class
            super().__init__()
            # Set sprite as bird image
            self.image = scaled_bird_image
            # Set sprite image as rectangle for movement (topleft)
            self.rect = scaled_bird_image.get_rect(topleft=(x, y))

            # Bird movement state
            self.target_pos = self.rect.topleft
            # Pixels per frame (5)
            self.speed = 5

            # Start as being "at target"
            self.at_target = True

        def update(self):
            # Current position
            x, y = self.rect.topleft
            # Target position
            tx, ty = self.target_pos

            # bird movement on x-axis (# snap directly to target x)
            x = tx

            # bird movement on y-axis (smooooth glide)
            # Only for y bc I want instant movement between K.1-K.4 and K.5-K.9 (between strings)
            if y < ty:
                y += min(self.speed, ty - y)
            if y > ty:
                y -= min(self.speed, y - ty)

            # Apply the new xy cooridnate/position back to sprite rect (Basically update sprite rectangle)
            self.rect.topleft = (x, y)

            # Check if bird has reached its target
            self.at_target = (x == tx and y == ty)

    # The all sprites group consists of...ba dam ba dam...the bird and the clouds, and the strings
    # The add cloud is below in the events portion bc code doesn't run properly if I put it here (order of events)
    all_sprites = pygame.sprite.Group()
    bird = Bird(50, 200)
    stringc = StringC(70, 0)
    stringg = StringG(200, 0)
    all_sprites.add(stringc, stringg, bird)

    # Cloud spawn event (every 2 seconds)
    SPAWN_CLOUD = pygame.USEREVENT + 1
    # 1000 ms = 1 second
    pygame.time.set_timer(SPAWN_CLOUD, 5000)

    # Pause the music ONCE
    pygame.mixer.music.pause()

    # ----------***Main Loop Starts Here***-----------
    # When pygame is running, main window will appear and stay
    run = True
    while run:
        # Draw background (blit displays image and image position)
        window.blit(scaled_bg_image, (0, 0))

        # Events
        # If pressed key 'x' get transported back to main menu (changed from pygame quit bc itch.io has no red x button)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    pygame.mixer.music.unpause()
                    await main()
                    # Unpause the music
            if event.type == SPAWN_CLOUD:
                # Spawn cloud only on timer (so they don't get squished)
                # Clouds start offscreen (right side) with random position and scale
                random_cloud_x = random.randint(WIN_WIDTH, WIN_WIDTH + 200)
                # We shall get ~floaty~ clouds, because they are not always at same height
                random_cloud_y = random.randint(50, 300)
                # Clouds vary in size but keep proportions (finally, they are not squished)
                random_scale = random.uniform(0.5, 1.2)
                cloud = Cloud(random_cloud_x, random_cloud_y, scale=random_scale)
                all_sprites.add(cloud)
            # If key gets pressed, player moves to specific x y coordinate
            elif event.type == pygame.KEYDOWN:
                # Looks up whether that key is pressed (from dictionary ([key] in previous line), if it is the loop is run (handle once-per-press)
                if event.key in key_positions:
                    # Moves rectangle with bird sprite using the topleft coordinates of the rectangle to target position
                    bird.target_pos = key_positions[event.key]
                    # play sound iif exists
                    if event.key in key_sounds:
                        key_sounds[event.key].play()

        # Update Assets - Clouds, Pipes, Bird (may need to switch)
        all_sprites.update()

        # Draw Assets - Clouds, Pipes, Bird
        # Current draw order:
        # 1. Clouds + Bird (from all_sprites)
        all_sprites.draw(window)

        clock.tick(60)
        # Update the display
        pygame.display.update()
        await asyncio.sleep(0)

# Main menu screen

# Initialize mixer (for bg music)
pygame.mixer.init()
pygame.mixer.music.load("bgm/chillbgm.mp3")
pygame.mixer.music.play(-1, 0.0)

# Set music volume to 15%
volume_level = 0.15
pygame.mixer.music.set_volume(volume_level)

font = pygame.font.SysFont("Alice", 75)

tutorial_button = Button((WIN_WIDTH / 2, 250), "TUTORIAL", font, "white")
play_button = Button((WIN_WIDTH / 2, 350), "PLAY", font, "white")
sandbox_button = Button((WIN_WIDTH / 2, 450), "SANDBOX", font, "white")

async def main():
    #-----Main Menu Starts Here----
    while True:
        pygame.display.set_caption("Menu (press red 'x' in the top left to exit)")

        window.blit(scaled_bg_image, (0, 0))
        menu_mouse_pos = pygame.mouse.get_pos()

        # Main menu title
        menu_text = pygame.font.SysFont("Alice", 80).render("PILLAR DODGE!", True, 'white')
        menu_rect = menu_text.get_rect(center=(WIN_WIDTH/2, 100))
        window.blit(menu_text, menu_rect)

        # Subtitle
        subtitle_text = pygame.font.SysFont("Alice", 20).render("Help the bird dodge the pillars. If you can it will sing for you!", True, 'white')
        subtitle_rect = menu_text.get_rect(center=(270, 175))
        window.blit(subtitle_text, subtitle_rect)

        # Extra text
        extra_text = pygame.font.SysFont("Alice", 20).render("Listen to the sounds of the Thai fiddle (Saw U)", True, 'white')
        extra_rect = menu_text.get_rect(center=(310, 200))
        window.blit(extra_text, extra_rect)

        # Update button colors + draw them
        for button in [tutorial_button, play_button, sandbox_button]:
            button.change_color(menu_mouse_pos)
            button.update(window)

        # Event loop (1. Quitting pygame/closing the window, 2. Mouse clicks on button (tutorial, main game, sandbox)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if tutorial_button.check_for_input(menu_mouse_pos):
                    await tutorial()
                if play_button.check_for_input(menu_mouse_pos):
                    await play()
                if sandbox_button.check_for_input(menu_mouse_pos):
                    await sandbox()

        pygame.display.update()
        await asyncio.sleep(0)

asyncio.run(main())