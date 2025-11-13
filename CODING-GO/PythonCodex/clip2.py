import pygame, sys, time, random, json
from MainMenu import main_menu

pygame.init()

# --- Window setup ---
WIDTH, HEIGHT = 1080, 585
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tutorial")

# --- Colors ---
BLACK = (0, 0, 0)
RED = (255, 40, 40)
WHITE = (255, 255, 255)

# --- Font ---
try:
    font = pygame.font.Font("PythonCodex/Fonts/Pixeled.ttf", 20)
except:
    font = pygame.font.SysFont("consolas", 28)

clock = pygame.time.Clock()

# --- Load saved name if exists ---
def get_player_name():
    try:
        with open("PythonCodex/player_data.json", "r") as f:
            data = json.load(f)
            return data.get("name", "Poko")
    except:
        return "Poko"

player_name = get_player_name()

# --- Fade text function ---
def fade_text(text, color=RED, stay=1.5, fade_speed=5):
    """Fade in and out a single line of text."""
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    # Fade in
    for alpha in range(0, 256, fade_speed):
        screen.fill(BLACK)
        temp = text_surface.copy()
        temp.set_alpha(alpha)
        screen.blit(temp, rect)
        pygame.display.flip()
        clock.tick(60)

    # Pause
    start_time = time.time()
    while time.time() - start_time < stay:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(BLACK)
        screen.blit(text_surface, rect)
        pygame.display.flip()
        clock.tick(60)

    # Fade out
    for alpha in range(255, -1, -fade_speed):
        screen.fill(BLACK)
        temp = text_surface.copy()
        temp.set_alpha(alpha)
        screen.blit(temp, rect)
        pygame.display.flip()
        clock.tick(60)

# --- Glitch effect ---
def glitch_effect(duration=1.2):
    """Simple static glitch effect."""
    start_time = time.time()
    while time.time() - start_time < duration:
        screen.fill(BLACK)
        for _ in range(50):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            w = random.randint(20, 100)
            h = random.randint(2, 8)
            color = random.choice([(255, 0, 0), (200, 0, 0), (255, 80, 80), (255, 255, 255)])
            pygame.draw.rect(screen, color, (x, y, w, h))
        pygame.display.flip()
        clock.tick(60)

# --- Dialogue Sequence ---
def play_opening_cutscene():
    fade_text("Too Bad..")
    fade_text("But you can Improve I assure you.")
    fade_text("Just keep going buddy.")
    fade_text("As you venture here,")
    fade_text("You'd understand why you're really here in the first place.")
    fade_text(f"See you soon, {player_name}.")
    fade_text("Don't Forget Me, Please..")
    glitch_effect()

# --- Run the cutscene ---

if __name__ == "__main__":
    play_opening_cutscene()
    pygame.quit()
