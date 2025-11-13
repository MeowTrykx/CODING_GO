import os, pygame, sys, random

pygame.init()
pygame.font.init()
pygame.mixer.init()

#Window Tab
WIDTH, HEIGHT = 1080, 585
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("World 0")

#Colors
BLACK = (0,0,0)
WHITE = (255,255,255)

#Fonts
font = pygame.font.Font("PythonCodex/Fonts/Pixeled.ttf", 18)
dialogue = pygame.font.Font("PythonCodex/Fonts/Pixeled.ttf", 18)
pause_font = pygame.font.Font("PythonCodex/Fonts/Pixeled.ttf", 32)
ui_font = pygame.font.Font("PythonCodex/Fonts/Pixeled.ttf", 18)

def draw_centered_text(surface, text, font, color=(255,255,255), y_offset=0):
    render = font.render(text, True, color)
    rect = render.get_rect(center=(WIDTH//2, HEIGHT//2 + y_offset))
    surface.blit(render, rect)

# --- GAME ASSETS BELOW THIS LINE ---

#Background and Platform
background = pygame.image.load("PythonCodex/BGandPLAT/W1.png")
Platform = pygame.image.load("PythonCodex/BGandPLAT/W1Platform.png")

WORLD_WIDTH = background.get_width()
GROUND_Y = 560

# Expressions
grumpy = pygame.image.load("PythonCodex/Player/Grumpy.png")
contemp = pygame.image.load("PythonCodex/Player/Contemplating.png")
angry1 = pygame.image.load("PythonCodex/Player/AngryTalk.png")
angry2 = pygame.image.load("PythonCodex/Player/AngryTalk2.png")
smile = pygame.image.load("PythonCodex/Player/Smile.png")
talk1 = pygame.image.load("PythonCodex/Player/Talk1.png")
talk2 = pygame.image.load("PythonCodex/Player/Talk2.png")

# Scale setting 
SCALE = 0.5
SIZE = 0.8

# Player sprites
walk1   = pygame.transform.scale_by(pygame.image.load("PythonCodex/Player/Walk1.png"), SCALE)
walk2   = pygame.transform.scale_by(pygame.image.load("PythonCodex/Player/Walk2.png"), SCALE)
idle    = pygame.transform.scale_by(pygame.image.load("PythonCodex/Player/IdleMC.png"), SCALE)
holdgui = pygame.transform.scale_by(pygame.image.load("PythonCodex/Player/HoldGui.png"), SIZE)

# Others
gui = pygame.image.load("PythonCodex/Images/GUI.png")
dummy = pygame.image.load("PythonCodex/Enemies/DummyOnGrr.png")
mew1 = pygame.image.load("PythonCodex/Images/Mewo1.png")
muwu = pygame.image.load("PythonCodex/Images/Mewo2.png")
mangry = pygame.image.load("PythonCodex/Images/Mewo3.png")
core = pygame.transform.scale_by(pygame.image.load("PythonCodex/Images/Core.png"), 0.15)

# Core spawn
core_positions = []
for i in range(5):
    core_positions.append([random.randint(100, WORLD_WIDTH-100), GROUND_Y - 60])

float_offset = 0
float_direction = 1

# Player Stats
max_hp = 100; hp = 100
max_mana = 50; mana = 50

player_x = 100; player_y = 400
player_speed = 4
player_frame = 0
player_direction = "right"
hold_gui = False
current_sprite = idle

camera_x = 0

# UI Bars
def draw_bars(surface, hp, max_hp, mana, max_mana):
    hp_ratio = hp / max_hp
    pygame.draw.rect(surface, (255,0,0),(20,20,200,20))
    pygame.draw.rect(surface,(0,255,0),(20,20,200*hp_ratio,20))
    surface.blit(ui_font.render(f"HP: {int(hp)}/{max_hp}",True,(255,255,255)),(225,18))

    mana_ratio = mana / max_mana
    pygame.draw.rect(surface,(50,50,255),(20,50,200,20))
    pygame.draw.rect(surface,(0,150,255),(20,50,200*mana_ratio,20))
    surface.blit(ui_font.render(f"MP: {int(mana)}/{max_mana}",True,(255,255,255)),(225,48))

# GAME LOOP
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_g:
            hold_gui = not hold_gui

    keys = pygame.key.get_pressed()

    if hold_gui:
        hp -= 0.1 if hp > 0 else 0
        current_sprite = holdgui
        moving = False
    else:
        moving = False
        if keys[pygame.K_RIGHT]: player_x += player_speed; moving = True; player_direction="right"
        if keys[pygame.K_LEFT]:  player_x -= player_speed; moving = True; player_direction="left"

    platform_rect = Platform.get_rect(topleft=(0,GROUND_Y))
    player_rect = current_sprite.get_rect(topleft=(player_x, player_y))
    if player_rect.bottom >= platform_rect.top:
        player_y = platform_rect.top - current_sprite.get_height()

    player_x = max(0, min(player_x, WORLD_WIDTH - idle.get_width()))

    if moving:
        player_frame += 0.15
        if player_frame >= 2: player_frame = 0
        current_sprite = walk1 if int(player_frame) == 0 else walk2
    else:
        if not hold_gui: current_sprite = idle

    sprite_to_draw = pygame.transform.flip(current_sprite, True, False) if player_direction=="left" else current_sprite

    camera_x = max(0, min(player_x - WIDTH//2, WORLD_WIDTH - WIDTH))

    float_offset += float_direction * 0.5
    if float_offset > 10 or float_offset < -10: float_direction *= -1

    screen.blit(background, (-camera_x,0))
    screen.blit(Platform,(0-camera_x,500))

    for core_data in core_positions[:]:
        cx, cy = core_data
        core_rect = core.get_rect(topleft=(cx, cy + float_offset))
        if player_rect.colliderect(core_rect):
            hp = min(max_hp, hp+15)
            mana = min(max_mana, mana+10)
            core_positions.remove(core_data)

    for cx, cy in core_positions:
        screen.blit(core,(cx-camera_x, cy + float_offset))

    screen.blit(sprite_to_draw, (player_x-camera_x, player_y))

    if hold_gui:
        overlay = pygame.Surface((WIDTH,HEIGHT)); overlay.set_alpha(150); overlay.fill((0,0,0))
        screen.blit(overlay,(0,0))
        screen.blit(pause_font.render("PAUSED", True, WHITE),(WIDTH//2-70, HEIGHT//2-20))

    draw_bars(screen, hp, max_hp, mana, max_mana)
    pygame.display.flip()

pygame.quit()