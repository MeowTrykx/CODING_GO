# Intro.py
import pygame, sys, random, time
from MainMenu import main_menu

pygame.init()

# --- Window ---
WIDTH, HEIGHT = 1080, 585
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Intro")

# --- Colors ---
BLACK = (0, 0, 0)
RED = (255, 60, 60)
TEAL = (0, 255, 255)
GREEN = (0, 255, 150)
BLUE_GLITCH = (120, 220, 255)
WHITE = (255, 255, 255)
CYAN = (0, 200, 255)
GLITCH_COLORS = [BLUE_GLITCH, CYAN, TEAL, WHITE]

GLITCH_SYMBOLS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&?!*><~")

# --- Font ---
try:
    font = pygame.font.Font("PythonCodex/Fonts/Pixeled.ttf", 64)
except:
    font = pygame.font.SysFont("consolas", 64)

clock = pygame.time.Clock()

# --- Draw Centered Text with Optional Shake ---
def draw_centered_text(text, color, shake=0):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(WIDTH // 2 + random.randint(-shake, shake),
                                 HEIGHT // 2 + random.randint(-shake, shake)))
    screen.blit(surf, rect)

# --- Unified Glitch Animation ---
def unified_glitch_text(final_text, color, delay_per_letter=0.09, flicker_intensity=0.35, shake_intensity=3):
    display_text = [" "] * len(final_text)

    for i in range(len(final_text)):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        # Randomize letters for glitch flicker
        for j in range(i + 1):
            if random.random() < flicker_intensity:
                display_text[j] = random.choice(GLITCH_SYMBOLS)
            else:
                display_text[j] = final_text[j]

        # Flicker unrevealed letters
        for k in range(i + 1, len(final_text)):
            display_text[k] = random.choice(GLITCH_SYMBOLS) if random.random() < 0.15 else " "

        screen.fill(BLACK)
        draw_centered_text("".join(display_text), color, shake=shake_intensity)
        pygame.display.flip()
        clock.tick(60)
        time.sleep(delay_per_letter)

    # Final stable frame
    screen.fill(BLACK)
    draw_centered_text(final_text, color)
    pygame.display.flip()
    time.sleep(0.6)

# --- Enhanced Multi-Color Glitch Transition ---
def multi_color_glitch_transition(duration=1.8, density=140):
    """Blue/teal/cyan glitch static with screen shake and flicker."""
    start = time.time()
    shake_intensity = 5
    while time.time() - start < duration:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        screen.fill(BLACK)

        # Flicker overlay intensity
        for _ in range(density):
            color = random.choice(GLITCH_COLORS)
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            w = random.randint(8, 60)
            h = random.randint(2, 16)
            pygame.draw.rect(screen, color, (x, y, w, h))

        # Random shake overlay flicker
        offset_x = random.randint(-shake_intensity, shake_intensity)
        offset_y = random.randint(-shake_intensity, shake_intensity)
        pygame.display.get_surface().scroll(offset_x, offset_y)

        pygame.display.flip()
        clock.tick(75)
        time.sleep(0.02)

# --- Main Sequence ---
def intro_sequence():
    unified_glitch_text("PowerRangers", TEAL, delay_per_letter=0.08, flicker_intensity=0.4, shake_intensity=4)
    pygame.time.wait(250)

    unified_glitch_text("Presents...", RED, delay_per_letter=0.07, flicker_intensity=0.4, shake_intensity=3)
    pygame.time.wait(200)

    unified_glitch_text("Coding Go", GREEN, delay_per_letter=0.09, flicker_intensity=0.4, shake_intensity=5)
    pygame.time.wait(300)

    multi_color_glitch_transition(duration=2.0, density=180)
    main_menu(screen)

if __name__ == "__main__":
    intro_sequence()
