import pygame, sys, time
from SettingsComp import (
    get_player_name, set_player_name,
    get_player_level, set_player_level,
    reset_settings
)

pygame.init()
WIDTH, HEIGHT = 1080, 585
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Settings")

# --- Font ---
try:
    font = pygame.font.Font("PythonCodex/Fonts/Pixeled.ttf", 24)
except:
    font = pygame.font.SysFont("consolas", 24)

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHTGREY = (180, 180, 180)
RED = (200, 60, 60)

# --- Fade text animation ---
def fade_message(text, color=WHITE, duration=1.2):
    for alpha in range(0, 256, 25):
        screen.fill(BLACK)
        msg = font.render(text, True, color)
        rect = msg.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(msg, rect)
        pygame.display.flip()
        pygame.time.delay(30)
    time.sleep(duration)
    for alpha in range(255, -1, -25):
        screen.fill(BLACK)
        msg = font.render(text, True, color)
        rect = msg.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(msg, rect)
        pygame.display.flip()
        pygame.time.delay(30)

# --- Return to main menu ---
def return_to_main(screen):
    import MainMenu
    MainMenu.main_menu(screen)

# --- Settings Menu ---
def settings_menu():
    clock = pygame.time.Clock()
    player_name = get_player_name()
    player_level = get_player_level()

    title_y = 100
    player_y = 220
    level_y = 280
    buttons_y = 420

    running = True
    while running:
        screen.fill(BLACK)

        # --- Title ---
        title = font.render("SETTINGS", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, title_y)))

        # --- Player Info ---
        player_label = font.render(f"Player: {player_name}", True, LIGHTGREY)
        level_label = font.render(f"Level: {player_level}", True, LIGHTGREY)
        screen.blit(player_label, player_label.get_rect(center=(WIDTH // 2, player_y)))
        screen.blit(level_label, level_label.get_rect(center=(WIDTH // 2, level_y)))

        # --- Buttons ---
        exit_text = font.render("Exit", True, WHITE)
        delete_text = font.render("Delete Progress", True, RED)
        exit_rect = exit_text.get_rect(center=(WIDTH // 2 - 200, buttons_y))
        delete_rect = delete_text.get_rect(center=(WIDTH // 2 + 200, buttons_y))
        screen.blit(exit_text, exit_rect)
        screen.blit(delete_text, delete_rect)

        pygame.display.flip()

        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos

                # Exit button
                if exit_rect.collidepoint(mx, my):
                    return_to_main(screen)
                    running = False

                # Delete Progress
                elif delete_rect.collidepoint(mx, my):
                    reset_settings()
                    set_player_name("????")
                    set_player_level(1)
                    player_name = "????"
                    player_level = 1
                    fade_message("Progress Reset!", RED)

        clock.tick(60)

# --- Run directly for testing ---
if __name__ == "__main__":
    settings_menu()
