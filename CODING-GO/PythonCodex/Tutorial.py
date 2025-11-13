import pygame, sys, time

pygame.init()

# --- Window ---
WIDTH, HEIGHT = 1080, 585
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tutorial Scene")

# --- Colors ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# --- Font ---
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 32)

# --- Helper: Fade In Text ---
def show_text(text, delay=1.5):
    """Fade-in text effect."""
    for alpha in range(0, 255, 10):
        screen.fill(BLACK)
        text_surface = font.render(text, True, (alpha, alpha, alpha))
        rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text_surface, rect)
        pygame.display.flip()
        pygame.time.delay(30)
    time.sleep(delay)

# --- Get Player Name ---
def get_player_name():
    clock = pygame.time.Clock()
    name = ""
    default = "Poko"

    # Intro dialogue
    for line in ["Oh, it's you...", "You finally arrived...", "Say... What's your name?"]:
        show_text(line)

    typing = True
    while typing:
        screen.fill(BLACK)
        prompt = font.render("Enter your name:", True, WHITE)
        name_surface = font.render(name or "|", True, WHITE)
        screen.blit(prompt, prompt.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))
        screen.blit(name_surface, name_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20)))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    name = name.strip() or default
                    typing = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.unicode.isprintable() and len(name) < 12:
                    name += event.unicode

        clock.tick(30)

    # Outro dialogue
    show_text(f"Oh, {name} huh?... You're the one...")
    return name

# --- Camera Offset Helper ---
def get_camera_offset(px, py, bg_width, bg_height):
    camera_x = px - WIDTH // 2
    camera_y = py - HEIGHT // 2
    camera_x = max(0, min(camera_x, bg_width - WIDTH))
    camera_y = max(0, min(camera_y, bg_height - HEIGHT))
    return camera_x, camera_y

# --- Main Tutorial Scene ---
def tutorial_scene(player_name):
    # Try to load images; fallback if missing
    try:
        background = pygame.image.load("PythonCodex/Images/TutorialBackground.png").convert()
        platform = pygame.image.load("PythonCodex/Images/TutorialPlatform.png").convert_alpha()
        mc_idle = pygame.image.load("PythonCodex/Images/IdleMC.png").convert_alpha()
    except:
        background = pygame.Surface((3000, 1000))
        background.fill((100, 200, 255))
        platform = pygame.Surface((3000, 200))
        platform.fill((60, 40, 20))
        mc_idle = pygame.Surface((100, 100))
        mc_idle.fill((255, 200, 0))

    # --- World setup ---
    player = pygame.transform.scale(mc_idle, (100, 100))
    player_x, player_y = 200, 350
    player_speed = 6

    bg_width, bg_height = background.get_size()
    pf_width, pf_height = platform.get_size()

    # --- Main loop ---
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player_x -= player_speed
        if keys[pygame.K_d]:
            player_x += player_speed
        if keys[pygame.K_w]:
            player_y -= player_speed
        if keys[pygame.K_s]:
            player_y += player_speed

        # Keep player in bounds
        player_x = max(0, min(player_x, bg_width - player.get_width()))
        player_y = max(0, min(player_y, bg_height - pf_height - player.get_height()))

        # Camera
        camera_x, camera_y = get_camera_offset(player_x, player_y, bg_width, bg_height)

        # Draw
        screen.fill((0, 0, 0))
        screen.blit(background, (-camera_x, -camera_y))
        screen.blit(platform, (-camera_x, bg_height - pf_height - camera_y))
        screen.blit(player, (player_x - camera_x, player_y - camera_y))

        # Display name tag (top left corner)
        name_tag = small_font.render(f"Player: {player_name}", True, WHITE)
        screen.blit(name_tag, (20, 20))

        pygame.display.flip()
        clock.tick(60)

# --- Game Start ---
if __name__ == "__main__":
    player_name = get_player_name()
    tutorial_scene(player_name)
