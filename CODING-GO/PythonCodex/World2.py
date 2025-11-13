import os, pygame, sys

pygame.init()
pygame.font.init()
pygame.mixer.init()

#Window Tab
WIDTH, HEIGHT = 1080, 585
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("World 2")

#Fonts
font = pygame.font.Font("PythonCodex/Fonts/Pixeled.ttf", 32)
dialogue = pygame.font.Font("PythonCodex/Fonts/Pixeled.ttf", 18)
pause_font = pygame.font.Font("PythonCodex/Fonts/Pixeled.ttf", 32)
ui_font = pygame.font.Font("PythonCodex/Fonts/Pixeled.ttf", 18)

#BackGround and Platform
background = pygame.image.load("PythonCodex/BGandPLAT/W1night.png")
Platform = pygame.image.load("PythonCodex/BGandPLAT/W1nightPlatform.png")

WORLD_WIDTH = background.get_width()
GROUND_Y = 560  # y position of platform

#Assets - Player Expressions
grumpy = pygame.image.load("PythonCodex/Player/Grumpy.png")
contemp = pygame.image.load("PythonCodex/Player/Contemplating.png")
angry1 = pygame.image.load("PythonCodex/Player/AngryTalk.png")
angry2 = pygame.image.load("PythonCodex/Player/AngryTalk2.png")
smile = pygame.image.load("PythonCodex/Player/Smile.png")
talk1 = pygame.image.load("PythonCodex/Player/Talk1.png")
talk2 = pygame.image.load("PythonCodex/Player/Talk2.png")

# Scale setting (change this to resize character)
SCALE = 0.5
SIZE = 0.8

#Assets - Player model
walk1   = pygame.transform.scale_by(pygame.image.load("PythonCodex/Player/Walk1.png"), SCALE)
walk2   = pygame.transform.scale_by(pygame.image.load("PythonCodex/Player/Walk2.png"), SCALE)
idle    = pygame.transform.scale_by(pygame.image.load("PythonCodex/Player/IdleMC.png"), SCALE)
holdgui = pygame.transform.scale_by(pygame.image.load("PythonCodex/Player/HoldGui.png"), SIZE)

#Assets - Others
gui = pygame.image.load("PythonCodex/Images/GUI.png")
dummy = pygame.image.load("PythonCodex/Enemy/DummyOnGrr.png")
mew1 = pygame.image.load("PythonCodex/Images/Mewo1.png")
muwu = pygame.image.load("PythonCodex/Images/Mewo2.png")
mangry = pygame.image.load("PythonCodex/Images/Mewo3.png")

# Player Stats
max_hp = 100
hp = 100
max_mana = 50
mana = 50

def draw_bars(surface, hp, max_hp, mana, max_mana):
    # HP bar
    hp_bar_width = 200
    hp_ratio = hp / max_hp
    pygame.draw.rect(surface, (60, 60, 60), (20, 20, hp_bar_width, 25))
    pygame.draw.rect(surface, (255, 0, 0), (20, 20, hp_bar_width * hp_ratio, 25))

    hp_text = ui_font.render(f"{int(hp)}/{max_hp}", True, (255,255,255))
    surface.blit(hp_text, (230, 20))  # beside bar

    # Mana bar
    mana_bar_width = 200
    mana_ratio = mana / max_mana
    pygame.draw.rect(surface, (60, 60, 60), (20, 55, mana_bar_width, 20))
    pygame.draw.rect(surface, (0, 150, 255), (20, 55, mana_bar_width * mana_ratio, 20))

    mana_text = ui_font.render(f"{int(mana)}/{max_mana}", True, (255,255,255))
    surface.blit(mana_text, (230, 55))

# Player Setup
player_x = 100
player_y = 300
player_speed = 4
GRAVITY = 2
player_velocity_y = 0   # NEW: vertical speed

player_frame = 0
player_direction = "right"
hold_gui = False
current_sprite = idle

# Camera offset
camera_x = 0
camera_y = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                hold_gui = not hold_gui

    keys = pygame.key.get_pressed()

    # ✅ HP drains ONLY while paused
    if hold_gui:
        hp -= 0.1
        if hp < 0: hp = 0
        current_sprite = holdgui
        moving = False
    else:
        moving = False
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
            moving = True
            player_direction = "right"

        if keys[pygame.K_LEFT]:
            player_x -= player_speed
            moving = True
            player_direction = "left"

    # ✅ APPLY GRAVITY
    player_velocity_y += GRAVITY
    player_y += player_velocity_y

    # ✅ PLATFORM COLLISION
    player_height = idle.get_height()
    if player_y + player_height >= GROUND_Y:
        player_y = GROUND_Y - player_height
        player_velocity_y = 0  # stop falling

    # ✅ Boundaries so player stays inside map
    if player_x < 0:
        player_x = 0
    if player_x > WORLD_WIDTH - idle.get_width():
        player_x = WORLD_WIDTH - idle.get_width()

    # Animation
    if moving:
        player_frame += 0.15
        if player_frame >= 2:
            player_frame = 0
        current_sprite = walk1 if int(player_frame) == 0 else walk2
    else:
        if not hold_gui:
            current_sprite = idle

    # Flip sprite
    sprite_to_draw = pygame.transform.flip(current_sprite, True, False) if player_direction == "left" else current_sprite

    # ✅ Camera follows player but stops at edges
    camera_x = player_x - WIDTH // 2
    camera_x = max(0, min(camera_x, WORLD_WIDTH - WIDTH))
    camera_y = 0

    # DRAW
    screen.blit(background, (-camera_x, -camera_y))
    screen.blit(Platform, (0 - camera_x, 500 - camera_y))
    screen.blit(sprite_to_draw, (player_x - camera_x, player_y - camera_y))

    # Pause overlay
    if hold_gui:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        text = pause_font.render("PAUSED", True, (255, 255, 255))
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 40))

    draw_bars(screen, hp, max_hp, mana, max_mana)
    pygame.display.flip()

pygame.quit()
