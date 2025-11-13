import pygame, sys, random, os

pygame.init()

# --- WINDOW SETUP ---
WIDTH, HEIGHT = 1080, 585
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battle System")

# --- COLORS ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 80, 80)
YELLOW = (255, 255, 100)
GREEN = (100, 255, 100)
BLUE = (120, 120, 255)

# --- FONTS ---
font = pygame.font.Font("PythonCodex/Fonts/Pixeled.ttf", 32)
title_font = pygame.font.Font("PythonCodex/Fonts/Pixeled.ttf", 48)

# --- PLAYER INFO ---
player_name = "Player"
player_input = ""
battle_log = []
input_active = True

# --- ENEMY DATABASE ---
enemies = {
    "Asomalt": {"element": "fire", "hp": 100, "max_hp": 100, "img": "Asomalt.png"},
    "Eyeduo": {"element": "earth", "hp": 120, "max_hp": 120, "img": "Eyeduo.png"},
    "Lokpao": {"element": "dark", "hp": 90, "max_hp": 90, "img": "Lokpao.png"},
    "Sunseko": {"element": "light", "hp": 110, "max_hp": 110, "img": "Sunseko.png"},
    "Voidurgo": {"element": "water", "hp": 130, "max_hp": 130, "img": "Voidurgo.png"},
    "Screamer": {"element": "electric", "hp": 80, "max_hp": 80, "img": "Screamer.png"},
    "Aksel": {"element": "light", "hp": 200, "max_hp": 200, "img": "Aksel.png"},
    "BossAbhel": {"element": "dark", "element": "light", "element": "water", "element": "fire", "element": "electric", "element": "earth", "hp": "????", "max_hp": 999999, "img": "BossAbhel.png"},
}

# --- ELEMENT WEAKNESS CHART ---
weakness_chart = {
    "fire": "water",
    "water": "electric",
    "electric": "earth",
    "earth": "wind",
    "wind": "fire",
    "dark": "light",
    "light": "dark"
}

# --- PICK ENEMY ---
def select_enemy(name=None):
    if name:
        return name, enemies[name].copy()
    else:
        pick = random.choice(list(enemies.keys())[:-2])  # exclude bosses by default
        return pick, enemies[pick].copy()

enemy_name, enemy_data = select_enemy()
enemy_hp = enemy_data["hp"]
enemy_element = enemy_data["element"]

# --- LOAD ENEMY IMAGE ---
enemy_img_path = os.path.join("Enemies", enemy_data["img"])
if os.path.exists(enemy_img_path):
    enemy_image = pygame.image.load(enemy_img_path).convert_alpha()
    # Scale down if image is too big
    img_rect = enemy_image.get_rect()
    scale_factor = 400 / max(img_rect.width, img_rect.height)
    enemy_image = pygame.transform.scale(enemy_image, (int(img_rect.width * scale_factor), int(img_rect.height * scale_factor)))
else:
    enemy_image = None

# --- FUNCTIONS ---
def draw_text_center(text, y, color=WHITE, size=32):
    f = pygame.font.Font(None, size)
    render = f.render(text, True, color)
    rect = render.get_rect(center=(WIDTH // 2, y))
    screen.blit(render, rect)

def add_log(text, color=WHITE):
    battle_log.append((text, color))
    if len(battle_log) > 6:
        battle_log.pop(0)

def calculate_damage(command):
    global enemy_hp, input_active

    if not command.startswith("Act.Attack.Element."):
        add_log("Invalid syntax!", RED)
        return

    try:
        # Parse structure: Act.Attack.Element.Fire.FireBall():
        parts = command.split(".")
        element = parts[3].lower()
        skill = parts[4].split("(")[0].lower()

        # Base damage values
        base_damage = {
            "fireball": 35,
            "watersplash": 40,
            "earthcrash": 35,
            "windslash": 30,
            "lightburst": 45,
            "shadowbite": 45,
            "electroshock": 38,
        }.get(skill, 0)

        if base_damage == 0:
            add_log(f"Unknown skill: {skill}", RED)
            return

        # Apply weakness logic
        multiplier = 1.0
        if weakness_chart.get(enemy_element) == element:
            multiplier = 2.5
            add_log("CRITICAL HIT!", YELLOW)

        damage = int(base_damage * multiplier)
        enemy_hp = max(0, enemy_hp - damage)

        add_log(f"You used {skill.capitalize()} ({element.title()})!")
        add_log(f"{enemy_name} took {damage} damage!", GREEN)

        if enemy_hp <= 0:
            add_log(f"{enemy_name} has been defeated!", YELLOW)
            input_active = False

    except Exception as e:
        add_log("Command Error!", RED)
        print(e)

def draw_battle_screen():
    screen.fill(BLACK)

    # Enemy image (center top)
    if enemy_image:
        img_rect = enemy_image.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
        screen.blit(enemy_image, img_rect)

    # Enemy name + HP
    draw_text_center(f"{enemy_name} - Element: {enemy_element.title()}", 80, YELLOW, 40)

    # HP bar
    hp_ratio = enemy_hp / enemy_data["max_hp"]
    pygame.draw.rect(screen, (60, 0, 0), (340, 120, 400, 25))
    pygame.draw.rect(screen, (255, 0, 0), (340, 120, 400 * hp_ratio, 25))
    draw_text_center(f"HP: {enemy_hp}/{enemy_data['max_hp']}", 150, WHITE, 28)

    # Player input bar
    pygame.draw.rect(screen, (40, 40, 40), (100, 500, 880, 40))
    txt_surface = font.render("> " + player_input, True, WHITE)
    screen.blit(txt_surface, (110, 510))

    # Log (bottom left)
    y = 350
    for text, color in battle_log:
        t = font.render(text, True, color)
        screen.blit(t, (100, y))
        y += 30

    pygame.display.flip()

# --- SECRET BOSS ACCESS ---
def secret_boss_code():
    global enemy_name, enemy_data, enemy_hp, enemy_element, enemy_image
    enemy_name, enemy_data = select_enemy("BossAbhel")
    enemy_hp = enemy_data["hp"]
    enemy_element = enemy_data["element"]

    # Load image
    path = os.path.join("Enemies", enemy_data["img"])
    if os.path.exists(path):
        img = pygame.image.load(path).convert_alpha()
        scale_factor = 400 / max(img.get_width(), img.get_height())
        enemy_image = pygame.transform.scale(img, (int(img.get_width() * scale_factor), int(img.get_height() * scale_factor)))

    add_log("⚠️ Secret Boss Abhel has appeared!", RED)

# --- MAIN LOOP ---
running = True
while running:
    draw_battle_screen()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and input_active:
            if event.key == pygame.K_RETURN:
                command = player_input.strip()
                if command:
                    calculate_damage(command)
                    player_input = ""

            elif event.key == pygame.K_BACKSPACE:
                player_input = player_input[:-1]

            elif event.key == pygame.K_k:  # Hidden boss trigger
                player_input = ""
                add_log("Enter Secret Code:", YELLOW)
                input_active = False
                secret_code = ""
                waiting = True
                while waiting:
                    for e in pygame.event.get():
                        if e.type == pygame.KEYDOWN:
                            if e.key == pygame.K_RETURN:
                                if secret_code == "S3CR3T_B055":
                                    secret_boss_code()
                                else:
                                    add_log("Invalid Code.", RED)
                                input_active = True
                                waiting = False
                            elif e.key == pygame.K_BACKSPACE:
                                secret_code = secret_code[:-1]
                            else:
                                secret_code += e.unicode

            else:
                player_input += event.unicode

    pygame.time.delay(30)
