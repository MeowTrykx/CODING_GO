import pygame
import os
import sys

pygame.init()

# --- Window setup ---
WIDTH, HEIGHT = 1080, 585
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Credits")

# --- Colors ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 60, 60)
BLUE = (100, 180, 255)
GREEN = (80, 255, 100)
ORANGE = (255, 170, 70)

# --- Paths ---
base_path = os.path.dirname(os.path.abspath(__file__))
font_path = os.path.join(base_path, "Fonts", "Pixeled.ttf")
images_path = os.path.join(base_path, "Images")

# --- Fonts ---
try:
    name_font = pygame.font.Font(font_path, 22)
    role_font = pygame.font.Font(font_path, 16)
    print("✅ Font loaded successfully")
except:
    name_font = pygame.font.SysFont("consolas", 22)
    role_font = pygame.font.SysFont("consolas", 16)
    print("⚠️ Font fallback used")

# --- Member list (Order & Colors) ---
credits_data = [
    ("Marc.png", "Marc Abhel", "Project Manager", RED),
    ("JohnLemar.png", "John Lemar", "Documentation", BLUE),
    ("Theresa.png", "Theresa", "Documentation", GREEN),
    ("Raja.png", "Raja Sameer", "Game Tester", BLUE),
    ("MeowTrykx.png", "MeowTrykx", "All-Arounder", ORANGE)
]

# --- Load Images ---
credits = []
for filename, name, role, color in credits_data:
    path = os.path.join(images_path, filename)
    if os.path.exists(path):
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.scale(img, (220, 220))
        credits.append((img, name, role, color))
        print(f"✅ Loaded {filename}")
    else:
        print(f"⚠️ Missing image: {path}")

# --- Music ---
try:
    audio_path = os.path.join(base_path, "Audio", "Slowed1.mp3")
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play(-1)
    print("🎵 Music playing...")
except Exception as e:
    print("⚠️ Music not found:", e)

# --- Show Credits ---
def show_credits(screen):
    clock = pygame.time.Clock()
    scroll_y = 0
    scroll_speed = 40

    spacing = 350  # space between each credit
    total_height = len(credits) * spacing + 300
    max_scroll = max(0, total_height - HEIGHT)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.fadeout(600)
                    return_to_main(screen)

            elif event.type == pygame.MOUSEWHEEL:
                scroll_y += event.y * scroll_speed
                scroll_y = max(-max_scroll, min(0, scroll_y))

        screen.fill(BLACK)

        y = 150 + scroll_y  # starting offset

        # --- Draw each credit ---
        for img, name, role, color in credits:
            center_x = WIDTH // 2

            # Draw box border
            rect = img.get_rect(center=(center_x, y))
            border_rect = pygame.Rect(rect.x - 10, rect.y - 10, rect.width + 20, rect.height + 20)
            pygame.draw.rect(screen, color, border_rect, 4)

            # Draw image
            screen.blit(img, rect)

            # Draw name
            name_surface = name_font.render(name, True, color)
            name_rect = name_surface.get_rect(center=(center_x, rect.bottom + 25))
            screen.blit(name_surface, name_rect)

            # Draw role
            role_surface = role_font.render(role, True, WHITE)
            role_rect = role_surface.get_rect(center=(center_x, name_rect.bottom + 20))
            screen.blit(role_surface, role_rect)

            y += spacing

        # Footer text
        footer = role_font.render("Use Mouse Wheel to Scroll | Press ESC to Return", True, WHITE)
        footer_rect = footer.get_rect(center=(WIDTH // 2, HEIGHT - 30))
        screen.blit(footer, footer_rect)

        pygame.display.flip()
        clock.tick(60)

# --- Return to Main Menu ---
def return_to_main(screen):
    import MainMenu
    MainMenu.main_menu(screen)

# --- Run standalone test ---
if __name__ == "__main__":
    show_credits(screen)
