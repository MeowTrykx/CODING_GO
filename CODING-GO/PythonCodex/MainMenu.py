import pygame
import sys
import random
from Credits import show_credits
#from World0 import 
from SettingsTab import settings_menu

pygame.init()

# Fonts
font_button = pygame.font.Font("PythonCodex/Fonts/Pixeled.ttf", 36)

# Colors
CYAN = (0, 255, 255)
DARK_BLUE = (0, 80, 255)
BLACK = (0, 0, 0)

# Glitch
particles = [[random.randint(0, 1080), random.randint(0, 585)] for _ in range(100)]

# Assets
title_img = pygame.image.load("PythonCodex/Images/CodingGo.png").convert_alpha()
mc_image = pygame.image.load("PythonCodex/Player/MainMC.png").convert_alpha()
mc_image = pygame.transform.smoothscale(mc_image, (450, 450))  # static MC image

# --- Glitch transition (subtle) ---
def glitch_transition(screen):
    glitch_particles = [
        [random.randint(0, 1080), random.randint(0, 585), random.randint(20, 60),
         random.choice([(120, 220, 255), (0, 200, 255), (0, 255, 150), (255, 255, 255)])]
        for _ in range(8)  # subtle particle count
    ]
    clock = pygame.time.Clock()
    for _ in range(4):  # fewer iterations for subtle effect
        screen.fill(BLACK)
        for x, y, w, color in glitch_particles:
            pygame.draw.rect(screen, color, (x, y, w, 4))  # thin rectangles
        pygame.display.flip()
        clock.tick(60)
        pygame.time.delay(30)

# --- Matrix background ---
def draw_particles(screen, width=1080, height=585):
    for p in particles:
        pygame.draw.rect(screen, (0, random.randint(180, 255), random.randint(180, 255)), (p[0], p[1], 2, 4))
        p[1] += 2
        if p[1] > height:
            p[1] = 0
            p[0] = random.randint(0, width)

# --- Buttons ---
buttons = [
    {"text": "Start", "y_offset": title_img.get_rect(topleft=(100, 80)).bottom + 30, "action": "start"},
    {"text": "Info", "y_offset": title_img.get_rect(topleft=(100, 80)).bottom + 90, "action": "Info"},
    {"text": "Credits", "y_offset": title_img.get_rect(topleft=(100, 80)).bottom + 150, "action": "credits"},
    {"text": "Exit", "y_offset": title_img.get_rect(topleft=(100, 80)).bottom + 210, "action": "exit"},
]

# --- Main menu function ---
def main_menu(screen):
    clock = pygame.time.Clock()
    running = True
    width, height = screen.get_size()
    mc_rect = mc_image.get_rect(center=(width // 1.4, height // 1.8))
    title_rect = title_img.get_rect(topleft=(100, 80))

    while running:
        screen.fill(BLACK)
        draw_particles(screen, width, height)

        # Draw static MC and title
        screen.blit(mc_image, mc_rect)
        screen.blit(title_img, title_rect)

        mouse_pos = pygame.mouse.get_pos()

        # --- Draw buttons with hover effect ---
        for button in buttons:
            color = CYAN
            text_surface = font_button.render(button["text"], True, color)
            text_rect = text_surface.get_rect(topleft=(100, button["y_offset"]))

            if text_rect.collidepoint(mouse_pos):
                text_surface = font_button.render(button["text"], True, DARK_BLUE)

            screen.blit(text_surface, text_rect)

        # --- Event handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in buttons:
                    text_rect = font_button.render(button["text"], True, CYAN).get_rect(topleft=(100, button["y_offset"]))
                    if text_rect.collidepoint(event.pos):
                        glitch_transition(screen)
                        if button["action"] == "start":
                            pass # Replace with show_tutorial(screen) if available.
                        elif button["action"] == "Info":
                            settings_menu()
                        elif button["action"] == "credits":
                            show_credits(screen)
                        elif button["action"] == "exit":
                            pygame.quit()
                            sys.exit()

        pygame.display.flip()
        clock.tick(60)

# --- Run directly for testing ---
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1080, 585))
    pygame.display.set_caption("Main Menu")
    main_menu(screen)
