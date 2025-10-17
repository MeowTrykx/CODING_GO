import pygame, sys

# --- Initialize ---
pygame.init()

# --- Window setup ---
WIDTH, HEIGHT = 1080, 585
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tutorial Scene")

clock = pygame.time.Clock()
FPS = 60

# --- Load images ---
background = pygame.image.load("PythonCodex/Images/TutorialBackground.png").convert()
platform_img = pygame.image.load("PythonCodex/Images/TutorialPlatform.png").convert_alpha()
idle_img = pygame.image.load("PythonCodex/Images/IdleMC.png").convert_alpha()
walk_imgs = [
    pygame.image.load("PythonCodex/Images/Walk1.png").convert_alpha(),
    pygame.image.load("PythonCodex/Images/Walk2.png").convert_alpha()
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
player_speed = 3
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
