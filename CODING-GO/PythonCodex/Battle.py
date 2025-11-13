import pygame, sys, random, time, subprocess, os

pygame.init()

# --- Window ---
WIDTH, HEIGHT = 1080, 585
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battle Mode")

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 60, 60)
GREEN = (60, 255, 60)
BLUE = (60, 60, 255)
GRAY = (25, 25, 25)
YELLOW = (255, 255, 120)

font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

# --- Weakness Table ---
weakness_chart = {
    "Fire": "Water",
    "Water": "Electric",
    "Electric": "Earth",
    "Earth": "Light",
    "Light": "Dark",
    "Dark": "Fire"
}

# --- Enemy Data ---
enemies = {
    "Asomalt": {"element": "Fire", "image": "PythonCodex/Enemies/Asomalt.png"},
    "Eyeduo": {"element": "Earth", "image": "PythonCodex/Enemies/Eyeduo.png"},
    "Lokpao": {"element": "Dark", "image": "PythonCodex/Enemies/Lokpao.png"},
    "Sunseko": {"element": "Light", "image": "PythonCodex/Enemies/Sunseko.png"},
    "Voidurgo": {"element": "Water", "image": "PythonCodex/Enemies/Voidurgo.png"},
    "Screamer": {"element": "Electric", "image": "PythonCodex/Enemies/Screamer.png"},
}

enemy_name = random.choice(list(enemies.keys()))
enemy = enemies[enemy_name]
enemy_hp = 100
player_hp = 100
player_stamina = 100
player_exp = 0
player_level = 1

enemy_img = pygame.image.load(enemy["image"])
enemy_img = pygame.transform.scale(enemy_img, (400, 400))
enemy_rect = enemy_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

player_input = ""
battle_message = f"A wild {enemy_name} appeared!"

defense_active = False
defense_timer = 0
defense_element = ""

state = "battle"
turn = "player"
last_attack_time = 0
enemy_delay = 10
clock = pygame.time.Clock()

current_world = 1  # Track world stage (1 to 3)

# --- Functions ---
def perform_attack(command):
    global enemy_hp, battle_message, defense_active, defense_timer, defense_element
    global player_stamina, player_exp, state

    if player_stamina <= 0:
        battle_message = "You're too tired to act!"
        return

    if command.startswith("Act.Attack."):
        try:
            parts = command.split(".")
            element = parts[3]
            move = parts[4].replace("()", "")
        except:
            battle_message = "Invalid attack syntax!"
            return

        player_stamina -= 15
        if weakness_chart[enemy["element"]] == element:
            damage = random.randint(80, 100)
            enemy_hp -= damage
            battle_message = f"Critical Hit! {enemy_name} took {damage} damage!"
        else:
            damage = random.randint(20, 50)
            enemy_hp -= damage
            battle_message = f"{enemy_name} took {damage} damage!"

    elif command.startswith("Act.Defend."):
        try:
            parts = command.split(".")
            element = parts[3].replace("()", "")
        except:
            battle_message = "Invalid defense syntax!"
            return

        player_stamina -= 10
        defense_active = True
        defense_element = element
        defense_timer = time.time() + 10
        battle_message = f"You created a {element} barrier!"

    else:
        battle_message = "Unknown command!"
        return

    if enemy_hp <= 0:
        enemy_defeated()


def enemy_defeated():
    global player_exp, player_level, battle_message, state, current_world
    gain_exp = random.randint(30, 60)
    player_exp += gain_exp
    battle_message = f"{enemy_name} was defeated! You gained {gain_exp} EXP!"

    if player_exp >= 100:
        player_exp -= 100
        player_level += 1
        player_hp = 100
        player_stamina = 100
        battle_message = f"You leveled up! LvL {player_level}!"

    pygame.time.delay(2000)
    go_to_next_world()


def go_to_next_world():
    """After victory, automatically start the next world script"""
    global current_world

    fade_out()
    pygame.display.flip()
    pygame.time.delay(1000)

    if current_world == 1:
        os.system("python World1.py")
    elif current_world == 2:
        os.system("python World2.py")
    elif current_world == 3:
        os.system("python World3.py")
    else:
        pygame.quit()
        sys.exit()

    current_world += 1  # Next time we enter battle, it’ll continue


def fade_out():
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.fill(BLACK)
    for alpha in range(0, 255, 5):
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(30)


def enemy_attack():
    global player_hp, battle_message, defense_active, defense_element, state
    elements = ["Fire", "Water", "Earth", "Light", "Dark", "Electric"]
    element = random.choice(elements)
    move = random.choice(["Blast", "Wave", "Bolt"])
    command = f"Act.Attack.Element.{element}.{move}()"
    damage = random.randint(30, 70)

    if defense_active:
        damage = int(damage * 0.3)
        battle_message = f"{enemy_name} used {command}, but your {defense_element} barrier softened the hit!"
    else:
        battle_message = f"{enemy_name} used {command}! {damage} damage dealt!"

    player_hp -= damage
    if player_hp <= 0:
        state = "death"


def draw_bar(x, y, value, max_value, color, label):
    ratio = max(value / max_value, 0)
    pygame.draw.rect(screen, (80, 80, 80), (x, y, 200, 20))
    pygame.draw.rect(screen, color, (x, y, 200 * ratio, 20))
    text = font.render(f"{label}: {int(value)}/{max_value}", True, WHITE)
    screen.blit(text, (x + 210, y - 2))


def death_screen():
    screen.fill(BLACK)
    draw_centered(big_font, "You Died.", YELLOW, -60)
    draw_centered(font, f"LvL {player_level}", WHITE, 0)
    draw_centered(font, "Press R to Reborn or Q to Quit", WHITE, 80)
    pygame.display.update()


def draw_centered(font_type, text, color, y_offset=0):
    txt = font_type.render(text, True, color)
    rect = txt.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(txt, rect)


# --- Game Loop ---
while True:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        if state == "battle":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if player_input.strip() != "":
                        perform_attack(player_input)
                        player_input = ""
                        last_attack_time = time.time()
                        turn = "waiting"
                elif event.key == pygame.K_BACKSPACE:
                    player_input = player_input[:-1]
                else:
                    player_input += event.unicode

        elif state == "death":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    player_hp = 100
                    player_stamina = 100
                    state = "battle"
                    battle_message = "You were reborn..."
                elif event.key == pygame.K_q:
                    pygame.quit(); sys.exit()

    if defense_active and time.time() > defense_timer:
        defense_active = False
        defense_element = ""
        battle_message = "Your barrier faded."

    if state == "battle" and turn == "waiting" and time.time() - last_attack_time >= enemy_delay and enemy_hp > 0:
        enemy_attack()
        turn = "player"

    if state == "battle":
        screen.blit(enemy_img, enemy_rect)
        draw_bar(150, 470, player_hp, 100, GREEN, "HP")
        draw_bar(150, 500, player_stamina, 100, YELLOW, "STAMINA")
        draw_bar(700, 70, enemy_hp, 100, BLUE, enemy_name)

        # EXP Bar
        pygame.draw.rect(screen, (50, 50, 50), (400, 550, 300, 15))
        pygame.draw.rect(screen, (120, 200, 255), (400, 550, 300 * (player_exp / 100), 15))
        exp_text = font.render(f"EXP: {player_exp}/100 (LvL {player_level})", True, WHITE)
        screen.blit(exp_text, (400, 520))

        msg_surface = font.render(battle_message, True, WHITE)
        input_surface = font.render(">>> " + player_input, True, WHITE)
        screen.blit(msg_surface, (50, 50))
        screen.blit(input_surface, (50, 540))

    elif state == "death":
        death_screen()

    pygame.display.flip()
    clock.tick(30)
