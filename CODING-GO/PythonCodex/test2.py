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

# --- CUTSCENE FUNCTIONS ---
def glitch_screen(duration=250):
    glitch = pygame.Surface((WIDTH, HEIGHT))
    glitch.set_alpha(150)
    glitch.fill((random.randint(120,255), 0, 0))
    screen.blit(glitch, (0,0))
    pygame.display.update()
    pygame.time.delay(duration)

def type_text(text, y, delay=30):
    shown = ""
    for ch in text:
        shown += ch
        render = font.render(shown, True, WHITE)
        screen.fill(BLACK)
        screen.blit(render, (50, y))
        pygame.display.update()
        pygame.time.delay(delay)

def fade_to_white():
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.fill(WHITE)
    for a in range(0,255,5):
        fade.set_alpha(a)
        screen.blit(fade,(0,0))
        pygame.display.update()
        pygame.time.delay(30)

# --- INTRO CUTSCENE ---
screen.fill(BLACK)
pygame.display.update()
pygame.time.delay(500)

def type_centered(text, y_offset=0, delay=50):
    shown = ""
    while len(shown) < len(text):
        shown = text[:len(shown)+1]
        screen.fill(BLACK)
        draw_centered_text(screen, shown, font, WHITE, y_offset)
        pygame.display.update()
        pygame.time.delay(delay)

# Intro lines
type_centered("A.. Human?", 0)
pygame.time.delay(400)
type_centered("This isn't good...", 40)
pygame.time.delay(500)
glitch_screen()
screen.fill(BLACK)
pygame.display.update()
pygame.time.delay(500)
type_centered("What's your name?", 0)
pygame.time.delay(300)

# --- Centered Name Input ---
player_name = ""
typing = True

while typing:
    screen.fill(BLACK)
    draw_centered_text(screen, "What's your name?", font, WHITE, -40)
    draw_centered_text(screen, "> " + player_name + "_", font, WHITE, 10)
    draw_centered_text(screen, "Press Enter to Skip", ui_font, WHITE, 60)
    pygame.display.update()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RETURN:
                name_to_check = player_name.strip().lower()
                forbidden_names = ["abhel","theresa","lemar","raja","meowtrykx","aksel","rich","john lemar","maria theresa","marc abhel"]
                if name_to_check in forbidden_names:
                    while True:
                        screen.fill(BLACK)
                        draw_centered_text(screen, "Nope. You can't be named as one of us Admins.", font, WHITE, 0)
                        draw_centered_text(screen, "(Press SPACE to rename)", ui_font, WHITE, 50)
                        pygame.display.update()
                        for evt in pygame.event.get():
                            if evt.type == pygame.QUIT: pygame.quit(); sys.exit()
                            if evt.type == pygame.KEYDOWN and evt.key == pygame.K_SPACE:
                                player_name = ""
                                break
                        else:
                            continue
                        break
                    continue
                if player_name.strip() == "":
                    player_name = "Poko"
                typing = False
            elif e.key == pygame.K_BACKSPACE:
                player_name = player_name[:-1]
            else:
                player_name += e.unicode

# After name input
screen.fill(BLACK)
type_centered(f"Oh, {player_name} huh? Interesting..", 0)
pygame.time.delay(500)
type_centered("I'm...", 40)
pygame.time.delay(600)
fade_to_white()

# --- GAME ASSETS ---
background = pygame.image.load("PythonCodex/BGandPLAT/TutorialBackground.png")
Platform = pygame.image.load("PythonCodex/BGandPLAT/TutorialPlatform.png")
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
walk1 = pygame.transform.scale_by(pygame.image.load("PythonCodex/Player/Walk1.png"), SCALE)
walk2 = pygame.transform.scale_by(pygame.image.load("PythonCodex/Player/Walk2.png"), SCALE)
idle = pygame.transform.scale_by(pygame.image.load("PythonCodex/Player/IdleMC.png"), SCALE)
holdgui = pygame.transform.scale_by(pygame.image.load("PythonCodex/Player/HoldGui.png"), SIZE)

# Others
gui = pygame.image.load("PythonCodex/Images/GUI.png")
dummy = pygame.image.load("PythonCodex/Enemies/DummyOnGrr.png")
mew1 = pygame.image.load("PythonCodex/Images/Mewo1.png")
muwu = pygame.image.load("PythonCodex/Images/Mewo2.png")
mangry = pygame.image.load("PythonCodex/Images/Mewo3.png")
core = pygame.transform.scale_by(pygame.image.load("PythonCodex/Images/Core.png"), 0.15)

# Core spawn
core_positions = [[random.randint(100, WORLD_WIDTH-100), GROUND_Y-60] for _ in range(5)]
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

# Secret code variables
secret_active = False
secret_code = ""
SECRET_KEY = "S3CR3T_BOSS"

# --- UI Bars ---
def draw_bars(surface, hp, max_hp, mana, max_mana):
    hp_ratio = hp/max_hp
    pygame.draw.rect(surface,(255,0,0),(20,20,200,20))
    pygame.draw.rect(surface,(0,255,0),(20,20,200*hp_ratio,20))
    surface.blit(ui_font.render(f"HP: {int(hp)}/{max_hp}",True,WHITE),(225,18))
    mana_ratio = mana/max_mana
    pygame.draw.rect(surface,(50,50,255),(20,50,200,20))
    pygame.draw.rect(surface,(0,150,255),(20,50,200*mana_ratio,20))
    surface.blit(ui_font.render(f"MP: {int(mana)}/{max_mana}",True,WHITE),(225,48))

# --- Death Sequence ---
def death_sequence(player_name):
    for _ in range(3):
        glitch_screen(200)
        pygame.time.delay(100)
    fade = pygame.Surface((WIDTH,HEIGHT))
    fade.fill(BLACK)
    for a in range(0,255,10):
        fade.set_alpha(a)
        screen.blit(fade,(0,0))
        pygame.display.update()
        pygame.time.delay(30)
    screen.fill(BLACK)
    draw_centered_text(screen,"You Died.",font,WHITE,-20)
    draw_centered_text(screen,f"{player_name}, LvL 1",font,WHITE,20)
    pygame.display.update()
    pygame.time.delay(2000)
    glitch_screen(300)
    reborn_rect = pygame.Rect(WIDTH//2-150, HEIGHT//2+40, 120,40)
    quit_rect = pygame.Rect(WIDTH//2+30, HEIGHT//2+40,120,40)
    while True:
        screen.fill(BLACK)
        draw_centered_text(screen,"You Died.",font,WHITE,-40)
        draw_centered_text(screen,f"{player_name}, LvL 1",font,WHITE,0)
        pygame.draw.rect(screen,(100,255,100),reborn_rect,border_radius=8)
        pygame.draw.rect(screen,(255,100,100),quit_rect,border_radius=8)
        screen.blit(ui_font.render("Reborn",True,BLACK),(reborn_rect.x+15,reborn_rect.y+10))
        screen.blit(ui_font.render("Quit",True,BLACK),(quit_rect.x+40,quit_rect.y+10))
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                mx,my = e.pos
                if reborn_rect.collidepoint(mx,my):
                    return "reborn"
                if quit_rect.collidepoint(mx,my):
                    return "quit"

# --- GAME LOOP ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                hold_gui = not hold_gui

            if event.key == pygame.K_k:  # Activate secret input
                secret_active = True
                secret_code = ""

            # --- SECRET CODE INPUT HANDLER ---
            if secret_active:
                if event.key == pygame.K_RETURN:
                    if secret_code.upper() == SECRET_KEY:
                        pygame.quit()
                        os.system("python PythonCodex/BossLevel.py")
                        sys.exit()
                    else:
                        secret_active = False  # Wrong code closes input
                elif event.key == pygame.K_BACKSPACE:
                    secret_code = secret_code[:-1]
                else:
                    secret_code += event.unicode

    keys = pygame.key.get_pressed()

    # --- If secret input is active, draw overlay and skip rest of game loop ---
    if secret_active:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        draw_centered_text(screen, "Enter Secret Code:", font, WHITE, -20)
        draw_centered_text(screen, secret_code + "_", font, WHITE, 20)
        pygame.display.update()
        continue  # Skip normal gameplay updates while typing secret code

    # --- PLAYER MOVEMENT ---
    if hold_gui:
        hp -= 0.1 if hp>0 else 0
        current_sprite = holdgui
        moving = False
    else:
        moving = False
        if keys[pygame.K_RIGHT]: player_x += player_speed; moving=True; player_direction="right"
        if keys[pygame.K_LEFT]: player_x -= player_speed; moving=True; player_direction="left"

    # --- Death Check ---
    if hp <= 0:
        choice = death_sequence(player_name)
        if choice=="reborn":
            hp = max_hp
            mana = max_mana
            player_x,player_y=100,400
            continue
        elif choice=="quit":
            pygame.quit()
            os.system("python PythonCodex/MainMenu.py")
            sys.exit()

    # --- Platform Collision ---
    platform_rect = Platform.get_rect(topleft=(0,GROUND_Y))
    player_rect = current_sprite.get_rect(topleft=(player_x,player_y))
    if player_rect.bottom >= platform_rect.top:
        player_y = platform_rect.top - current_sprite.get_height()

    player_x = max(0,min(player_x,WORLD_WIDTH-idle.get_width()))

    if moving:
        player_frame += 0.15
        if player_frame >=2: player_frame=0
        current_sprite = walk1 if int(player_frame)==0 else walk2
    else:
        if not hold_gui: current_sprite = idle

    sprite_to_draw = pygame.transform.flip(current_sprite,True,False) if player_direction=="left" else current_sprite
    camera_x = max(0,min(player_x-WIDTH//2,WORLD_WIDTH-WIDTH))
    float_offset += float_direction*0.5
    if float_offset>10 or float_offset<-10: float_direction*=-1

    screen.blit(background,(-camera_x,0))
    screen.blit(Platform,(0-camera_x,500))

    for core_data in core_positions[:]:
        cx,cy = core_data
        core_rect = core.get_rect(topleft=(cx,cy+float_offset))
        if player_rect.colliderect(core_rect):
            hp = min(max_hp,hp+15)
            mana = min(max_mana,mana+10)
            core_positions.remove(core_data)

    for cx,cy in core_positions:
        screen.blit(core,(cx-camera_x,cy+float_offset))

    screen.blit(sprite_to_draw,(player_x-camera_x,player_y))

    if hold_gui:
        overlay = pygame.Surface((WIDTH,HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0,0,0))
        screen.blit(overlay,(0,0))
        screen.blit(pause_font.render("PAUSED",True,WHITE),(WIDTH//2-70,HEIGHT//2-20))

    draw_bars(screen,hp,max_hp,mana,max_mana)
    pygame.display.flip()

pygame.quit()
