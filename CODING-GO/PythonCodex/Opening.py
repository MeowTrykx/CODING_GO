import pygame, sys, json, os, time

pygame.init()

# --- Window ---
WIDTH, HEIGHT = 1080, 585
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Prototype 2.3")

clock = pygame.time.Clock()
FPS = 30

# --- Colors ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# --- Font ---
font_path = "PythonCodex/Fonts/Pixeled.ttf"  # Path to your Pixeled.ttf
font = pygame.font.Font(font_path, 32)

# --- Save system ---
SAVE_FILE = "savefile.json"

def load_save():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

# --- Fade text function ---
def fade_text(text, delay=0.02, hold=1.0):
    """Fade a line of text in, hold, then fade out."""
    for alpha in range(0, 256, 10):
        screen.fill(BLACK)
        text_surface = font.render(text, True, (alpha, alpha, alpha))
        rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text_surface, rect)
        pygame.display.flip()
        pygame.time.delay(int(delay * 1000))

    time.sleep(hold)

    for alpha in range(255, -1, -10):
        screen.fill(BLACK)
        text_surface = font.render(text, True, (alpha, alpha, alpha))
        rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text_surface, rect)
        pygame.display.flip()
        pygame.time.delay(int(delay * 1000))

# --- Name input ---
def get_player_name():
    save = load_save()
    if "player_name" in save:
        return save["player_name"]

    # --- Intro lines with fade ---
    fade_text("Oh, it's you...")
    fade_text("You finally arrived...")
    fade_text("Say... What's your name?")

    name = ""
    default_name = "Poko"
    clock = pygame.time.Clock()
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
                    name = name.strip() or default_name
                    typing = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.unicode.isprintable() and len(name) < 12:
                    name += event.unicode

        clock.tick(30)

    fade_text(f"Oh, {name} huh?... You're the one...")

    save["player_name"] = name
    save_data(save)
    return name

# --- Main ---
def main():
    player_name = get_player_name()
    screen.fill(BLACK)
    fade_text(f"Adventure awaits, {player_name}!", delay=0.015, hold=1.5)
    time.sleep(1)
    pygame.quit()

# --- Load images ---
background = pygame.image.load("PythonCodex/BGandPLAT/TutorialBackground.png").convert()
platform_img = pygame.image.load("PythonCodex/BGandPLAT/TutorialPlatform.png").convert_alpha()
idle_img = pygame.image.load("PythonCodex/Player/IdleMC.png").convert_alpha()
walk_imgs = [
    pygame.image.load("PythonCodex/Player/Walk1.png").convert_alpha(),
    pygame.image.load("PythonCodex/Player/Walk2.png").convert_alpha()
]

# --- Resize player images (kid-sized) ---
scale = 0.4
idle_img = pygame.transform.scale_by(idle_img, scale)
walk_imgs = [pygame.transform.scale_by(img, scale) for img in walk_imgs]

# --- Set platform position ---
# Platform stays at the very bottom of the window
platform_rect = platform_img.get_rect(midbottom=(WIDTH // 2, HEIGHT))

# --- MC position ---
# Keep MC above black line (adjust if needed)
black_line_y = HEIGHT - 80  # adjust this if feet don't align perfectly
player_rect = idle_img.get_rect(midbottom=(WIDTH // 2, black_line_y))

# --- Movement / Animation settings ---
player_speed = 6
current_frame = 0
frame_timer = 0
frame_delay = 10
facing_right = True

# --- Game Loop ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # --- Input ---
    keys = pygame.key.get_pressed()
    moving = False

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_rect.x -= player_speed
        facing_right = False
        moving = True
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_rect.x += player_speed
        facing_right = True
        moving = True

    # --- Animation ---
    frame_timer += 1
    if moving:
        if frame_timer >= frame_delay:
            current_frame = (current_frame + 1) % len(walk_imgs)
            frame_timer = 0
        image = walk_imgs[current_frame]
    else:
        image = idle_img

    if not facing_right:
        image = pygame.transform.flip(image, True, False)

    # --- Draw Everything ---
    screen.blit(background, (0, 0))
    screen.blit(platform_img, platform_rect)
    screen.blit(image, player_rect)

    pygame.display.flip()
    clock.tick(FPS)

if __name__ == "__main__":
    main()
