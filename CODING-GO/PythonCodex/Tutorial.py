import pygame, sys, time, random
from SaveFile import load_save, update_save  # ✅ Save system integration

pygame.init()

# --- Window ---
WIDTH, HEIGHT = 1080, 585
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tutorial")

# --- Colors ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 120, 255)

# --- Font ---
font = pygame.font.Font("PythonCodex/Fonts/Pixeled.ttf", 32)
dialogue_font = pygame.font.Font("PythonCodex/Fonts/Pixeled.ttf", 12)

# --- HP Bar Helper ---
def draw_hp_bar(surface, x, y, current_hp, max_hp, width=200, height=20):
    ratio = max(current_hp / max_hp, 0)
    outline_rect = pygame.Rect(x, y, width, height)
    fill_rect = pygame.Rect(x, y, width * ratio, height)
    pygame.draw.rect(surface, (255, 0, 0), fill_rect)
    pygame.draw.rect(surface, (255, 255, 255), outline_rect, 2)

# --- GUI flash helper ---
def flash_gui(path="PythonCodex/Images/GUI.png", duration=120):
    gui = pygame.image.load(path).convert_alpha()
    gui = pygame.transform.scale(gui, (WIDTH, HEIGHT))
    for alpha in list(range(0, 256, 25)) + list(range(255, -1, -25)):
        surf = gui.copy()
        surf.set_alpha(alpha)
        screen.blit(surf, (0, 0))
        pygame.display.flip()
        pygame.time.delay(int(duration / len(list(range(0, 256, 25)) + list(range(255, -1, -25)))))

# ==========================================
#  CUTSCENE: Get Player Name
# ==========================================
def show_text(text, delay=1.5):
    for alpha in range(0, 255, 10):
        screen.fill(BLACK)
        text_surface = font.render(text, True, (alpha, alpha, alpha))
        rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text_surface, rect)
        pygame.display.flip()
        pygame.time.delay(25)
    time.sleep(delay)

def get_player_name():
    clock = pygame.time.Clock()
    name = ""
    default = "Poko"
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
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    name = name.strip() or default
                    typing = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 12:
                        name += event.unicode
        clock.tick(30)
    show_text(f"Oh, {name} huh?... You're the one...")

    # Fade into next scene
    for alpha in range(255, -1, -15):
        fade_surface = pygame.Surface((WIDTH, HEIGHT))
        fade_surface.fill(BLACK)
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(30)

    # ✅ Save player name immediately after intro
    update_save(player_name=name, stage="tutorial_start")
    return name

# ==========================================
#  BATTLE PROTOTYPE (typing based)
# ==========================================
def battle_scene(player_name, player_sprite, player_pos, player_hp, max_hp):
    # load enemy and GUI
    dummy = pygame.image.load("PythonCodex/Images/DummyOnGrr.png").convert_alpha()
    dummy = pygame.transform.scale(dummy, (300, 300))
    gui_panel = pygame.image.load("PythonCodex/Images/GUI.png").convert_alpha()
    gui_panel = pygame.transform.smoothscale(gui_panel, (520, 160))

    # battle variables
    clock = pygame.time.Clock()
    input_text = ""
    running = True
    enemy_hp = 100
    enemy_max = 100

    # attack spawn list
    elements = ["fire","water","earth","wind","light","ice","bolt"]
    attacks = []  # each attack dict: {text, x, y, speed, element}
    spawn_timer = 0
    spawn_interval = 120  # frames
    typed_success = 0

    # buttons
    button_w = 120; button_h = 36
    buttons = {
        "Attack": pygame.Rect(60, HEIGHT - 120, button_w, button_h),
        "Defend": pygame.Rect(200, HEIGHT - 120, button_w, button_h),
        "Items": pygame.Rect(340, HEIGHT - 120, button_w, button_h),
        "Run": pygame.Rect(480, HEIGHT - 120, button_w, button_h),
    }

    # simple typing UI: player needs to type the element that matches active attack to counter
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    # check input against any active attack (closest to bottom first)
                    if input_text.strip():
                        matched = False
                        for a in sorted(attacks, key=lambda x: -x["y"]):
                            if input_text.strip().lower() == a["element"]:
                                # success: remove attack, damage enemy
                                attacks.remove(a)
                                enemy_hp = max(0, enemy_hp - 25)
                                typed_success += 1
                                matched = True
                                break
                        input_text = ""
                        if enemy_hp <= 0:
                            # enemy defeated: exit battle (return to tutorial world)
                            return player_hp, True
                else:
                    # add typed char
                    if len(input_text) < 16 and event.unicode.isprintable():
                        input_text += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx,my = event.pos
                for name, rect in buttons.items():
                    if rect.collidepoint(mx,my):
                        # simple button feedback (no deep logic yet)
                        if name == "Attack":
                            enemy_hp = max(0, enemy_hp - 5)
                        elif name == "Run":
                            # attempt to run: small chance succeed
                            if random.random() < 0.3:
                                return player_hp, False

        # spawn attacks
        spawn_timer += 1
        if spawn_timer >= spawn_interval:
            spawn_timer = 0
            element = random.choice(elements)
            attacks.append({"text": element.upper(), "x": WIDTH - 200, "y": 120, "speed": 1.6, "element": element})

        # move attacks down
        for a in list(attacks):
            a["y"] += a["speed"]
            # if attack reaches player's area -> damage player
            if a["y"] > HEIGHT - 200:
                # hurt player
                player_hp = max(0, player_hp - 10)
                attacks.remove(a)
                if player_hp <= 0:
                    # player dies: end battle (you can change behavior)
                    return 0, True

        # draw battle scene
        screen.fill(BLACK)
        # background (darkened)
        # For simplicity reuse tutorial background scaled
        try:
            bg = pygame.image.load("PythonCodex/Images/TutorialBackground.png").convert()
            bg = pygame.transform.scale(bg, (WIDTH, bg.get_height()))
            screen.blit(bg, (0, HEIGHT - bg.get_height()))
        except:
            pass

        # player on left
        psurf = pygame.transform.scale(player_sprite, (int(player_sprite.get_width()*1.4), int(player_sprite.get_height()*1.4)))
        screen.blit(psurf, (80, HEIGHT - 320))

        # enemy on right
        screen.blit(dummy, (WIDTH - 400, HEIGHT - 360))

        # top-left player hp
        draw_hp_bar(screen, 40, 40, player_hp, max_hp)

        # enemy hp top-right
        draw_hp_bar(screen, WIDTH - 260, 40, enemy_hp, enemy_max)

        # GUI Panel bottom center (player's action panel)
        panel_x = WIDTH//2 - gui_panel.get_width()//2
        panel_y = HEIGHT - gui_panel.get_height() - 10
        screen.blit(gui_panel, (panel_x, panel_y))

        # Buttons overlay
        for name, rect in buttons.items():
            pygame.draw.rect(screen, GREY, rect)
            pygame.draw.rect(screen, WHITE, rect, 2)
            surf = dialogue_font.render(name, True, BLACK)
            screen.blit(surf, surf.get_rect(center=rect.center))

        # attacks display (descending) on right-mid
        for a in attacks:
            txt = dialogue_font.render(a["text"], True, BLUE)
            screen.blit(txt, (a["x"], a["y"]))

        # input box
        ibox = pygame.Rect(60, HEIGHT - 60, 420, 36)
        pygame.draw.rect(screen, (30,30,30), ibox)
        pygame.draw.rect(screen, WHITE, ibox, 2)
        itext = dialogue_font.render(input_text or "|", True, WHITE)
        screen.blit(itext, (ibox.x + 8, ibox.y + 6))

        # Hints
        hint = dialogue_font.render("Type element word then ENTER to counter an attack", True, (200,200,200))
        screen.blit(hint, (60, HEIGHT - 100))

        pygame.display.flip()
        clock.tick(60)

    return player_hp, True

# ==========================================
#  TUTORIAL SCENE (main)
# ==========================================
def tutorial_scene(player_name):
    # load images
    background = pygame.image.load("PythonCodex/Images/TutorialBackground.png").convert()
    platform = pygame.image.load("PythonCodex/Images/TutorialPlatform.png").convert_alpha()
    mc_idle = pygame.image.load("PythonCodex/Images/IdleMC.png").convert_alpha()
    mc_walk1 = pygame.image.load("PythonCodex/Images/Walk1.png").convert_alpha()
    mc_walk2 = pygame.image.load("PythonCodex/Images/Walk2.png").convert_alpha()
    angry1 = pygame.image.load("PythonCodex/Images/AngryTalk.png").convert_alpha()
    angry2 = pygame.image.load("PythonCodex/Images/AngryTalk2.png").convert_alpha()
    contemplating_image = pygame.image.load("PythonCodex/Images/Contemplating.png").convert_alpha()
    mewo1 = pygame.image.load("PythonCodex/Images/Mewo1.png").convert_alpha()
    mewo2 = pygame.image.load("PythonCodex/Images/Mewo2.png").convert_alpha()
    mewo3 = pygame.image.load("PythonCodex/Images/Mewo3.png").convert_alpha()
    # new assets
    gui_full = pygame.image.load("PythonCodex/Images/GUI.png").convert_alpha()
    dummy_on_grr = pygame.image.load("PythonCodex/Images/DummyOnGrr.png").convert_alpha()

    # --- Scale background & platform only by width ---
    bg_height = background.get_height()
    pf_height = platform.get_height()
    background = pygame.transform.scale(background, (WIDTH, bg_height))
    platform = pygame.transform.scale(platform, (WIDTH, pf_height))

    # --- Resize portraits ---
    def resize(img): return pygame.transform.smoothscale(img, (100, 100))
    angry1, angry2, contemplating_image = map(resize, [angry1, angry2, contemplating_image])
    mewo1, mewo2, mewo3 = map(resize, [mewo1, mewo2, mewo3])

    # --- Scale MC ---
    mc_idle = pygame.transform.scale_by(mc_idle, 0.5)
    mc_walk1 = pygame.transform.scale_by(mc_walk1, 0.5)
    mc_walk2 = pygame.transform.scale_by(mc_walk2, 0.5)

    # --- Player Setup ---
    player_x = 50
    player_y = 250
    player_speed = 6
    walk_frame = 0
    facing_right = True
    frozen = False

    # --- Camera ---
    camera_x = 0

    # --- Dialogue ---
    dialogues = [
        ("Where the F#@K am I?", contemplating_image, "Player"),
        ("This place... doesn't look normal.", contemplating_image, "Player"),
    ]
    dialogue_index = 0
    dialogue_text, current_portrait, speaker = dialogues[dialogue_index]
    show_dialogue = True

    # --- Flags ---
    void_triggered = False
    mewo_sequence = False
    hp_sequence = False
    after_hp_reaction = False
    gui_flashing = False
    pre_battle_dialogues_done = False

    # --- Dialogue sets ---
    post_void_dialogues = [
        ("WHAT THE F#@K!", angry2, "Player"),
        ("Why and How did I go back?!", angry1, "Player"),
        ("I CAN'T MOVE!", angry2, "Player"),
    ]
    mewo_dialogues = [
        ("You should definitely work on your Language..", mewo3, "???"),
        ("Ah— I'm MeowTrykx. Nice to meet you.", mewo2, "MeowTrykx"),
    ]
    mewo_index, post_index = 0, 0

    # --- HP ---
    max_hp = 100
    current_hp = max_hp
    target_hp = max_hp

    # main loop
    clock = pygame.time.Clock()
    running = True
    while running:
        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    # advance normal dialogues
                    if show_dialogue and not void_triggered:
                        if dialogue_index < len(dialogues) - 1:
                            dialogue_index += 1
                            dialogue_text, current_portrait, speaker = dialogues[dialogue_index]
                        else:
                            show_dialogue = False

                    # post-void reaction dialogues
                    elif void_triggered and post_index < len(post_void_dialogues) - 1:
                        post_index += 1
                        dialogue_text, current_portrait, speaker = post_void_dialogues[post_index]
                        if post_index == 2:
                            frozen = True

                    # mewo dialogues
                    elif mewo_sequence:
                        if mewo_index < len(mewo_dialogues) - 1:
                            mewo_index += 1
                            dialogue_text, current_portrait, speaker = mewo_dialogues[mewo_index]
                        else:
                            # MeowTrykx finished intro -> trigger player reaction line then HP drop
                            mewo_sequence = False
                            hp_sequence = True
                            dialogue_text = "Uh.. A Floating—"
                            current_portrait = contemplating_image
                            speaker = "Player"

                    # after HP drops (we'll use this to advance through the new scripted sequence)
                    elif after_hp_reaction:
                        # Step through scripted post-HP sequence
                        if not pre_battle_dialogues_done:
                            # sequence order:
                            # 1) MC: "MY HP! WHAT HAPPENED?!" (we will set this immediately after hp ends)
                            # 2) MeowTrykx line 1
                            # 3) MeowTrykx line 2 (GUI transfer) -> GUI flash -> MC "WAIT- ENEMIES?!" -> MeowTrykx "Yes, Enemies." -> spawn Dummy -> start battle
                            after_hp_reaction = False  # consume the trigger, next logic below will handle
                            # set first MC reaction
                            dialogue_text = "MY HP! WHAT HAPPENED?!"
                            current_portrait = angry2
                            speaker = "Player"
                            # mark that next press will go to mewo reply 1 by setting a small state
                            after_step = 1
                            # store step in a temporary variable attached to function scope via closure:
                            tutorial_scene.after_step = 1
                        else:
                            pass

        # HP animation (when mewo triggered hp_sequence earlier)
        if hp_sequence:
            target_hp = 1
            if current_hp > target_hp:
                current_hp -= 8  # drain faster
                if current_hp < target_hp: current_hp = target_hp
            else:
                current_hp = target_hp
                hp_sequence = False
                # after HP finished, queue the MC reaction sequence
                after_hp_reaction = True

        # handle after_hp steps (since we used a little state on the function)
        if hasattr(tutorial_scene, "after_step"):
            step = tutorial_scene.after_step
            # Wait for player pressing Z to continue through these steps.
            # We'll detect press in events earlier, but since we cleared after_hp_reaction there, now rely on z presses
            # to move sequence forward. To do that, we check if dialogue_text equals specific lines and on Z we advance.
            # To keep things simple, we use a small keyboard state: check pygame.key.get_pressed on Z and detect edge.
            keys = pygame.key.get_pressed()
            # to avoid detecting held key across frames, we will poll events: (we already consumed keydown events earlier)
            # so we'll just rely on the next K_z press in events loop — to implement this reliably, let's watch for KEYDOWN in events.
            # But because we consumed that code, we need a different approach: create a small local variable to track presses
            pass

        # Movement allowed only when not frozen and no dialogue showing
        keys = pygame.key.get_pressed()
        moving = False
        if not frozen and not show_dialogue and not mewo_sequence and not hp_sequence and not hasattr(tutorial_scene, "in_script_step"):
            if keys[pygame.K_LEFT]:
                player_x -= player_speed
                facing_right = False
                moving = True
            elif keys[pygame.K_RIGHT]:
                player_x += player_speed
                facing_right = True
                moving = True

        # Animation
        current_sprite = mc_idle
        if moving:
            walk_frame += 1
            current_sprite = mc_walk1 if walk_frame // 10 % 2 == 0 else mc_walk2
        if not facing_right:
            current_sprite = pygame.transform.flip(current_sprite, True, False)

        # Void trigger
        if player_x > 900 and not void_triggered:
            player_x = 50
            void_triggered = True
            frozen = True
            dialogue_text, current_portrait, speaker = post_void_dialogues[0]

        # Fade to black then mewo sequence
        if void_triggered and post_index == len(post_void_dialogues) - 1 and dialogue_text == "I CAN'T MOVE!":
            pygame.time.delay(1000)
            fade = pygame.Surface((WIDTH, HEIGHT))
            for alpha in range(0, 255, 10):
                fade.fill(BLACK)
                fade.set_alpha(alpha)
                screen.blit(fade, (0, 0))
                pygame.display.flip()
                pygame.time.delay(30)
            mewo_sequence = True
            frozen = True
            mewo_index = 0
            dialogue_text, current_portrait, speaker = mewo_dialogues[0]

        # camera
        camera_x = max(0, player_x - WIDTH // 2)

        # draw world
        screen.fill(BLACK)
        screen.blit(background, (-camera_x, HEIGHT - bg_height))
        screen.blit(platform, (-camera_x, HEIGHT - pf_height))
        screen.blit(current_sprite, (player_x - camera_x, player_y))

        # mewo placeholder on right when sequence present
        if mewo_sequence:
            screen.blit(mewo1, (WIDTH - 200, player_y - 50))

        # Dialogue box logic: we need to handle the scripted sequence after HP drop
        # We'll implement a small state machine using tutorial_scene.script_step
        if not hasattr(tutorial_scene, "script_step"):
            tutorial_scene.script_step = 0  # 0 = normal, 1..n steps for after HP

        # If after_hp_reaction was just queued, set script_step = 1 and set initial dialogue to MC reaction
        if after_hp_reaction and tutorial_scene.script_step == 0:
            tutorial_scene.script_step = 1
            dialogue_text = "MY HP! WHAT HAPPENED?!"
            current_portrait = angry2
            speaker = "Player"
            frozen = True
            # ensure we wait for Z to move forward; we'll track with script_step increments

        # Handle player pressing Z to move script steps (we need to capture KEYDOWN Z reliably)
        # We'll re-check events here (safe because main event loop above didn't handle all cases)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                if tutorial_scene.script_step == 1:
                    # MeowTrykx line 1
                    tutorial_scene.script_step = 2
                    dialogue_text, current_portrait, speaker = ("Ah. You don't belong in this world as I remembered... Oh well!", mewo2, "MeowTrykx")
                elif tutorial_scene.script_step == 2:
                    tutorial_scene.script_step = 3
                    dialogue_text, current_portrait, speaker = ("Take this GUI! Now It's connected to your life. Don't use it when you're not in Battle.", mewo2, "MeowTrykx")
                elif tutorial_scene.script_step == 3:
                    # Do GUI flash, then MC "WAIT- ENEMIES?!"
                    tutorial_scene.script_step = 4
                    # flash GUI fullscreen
                    flash_gui("PythonCodex/Images/GUI.png", duration=900)
                    dialogue_text, current_portrait, speaker = ("WAIT- ENEMIES?!", angry2, "Player")
                elif tutorial_scene.script_step == 4:
                    tutorial_scene.script_step = 5
                    dialogue_text, current_portrait, speaker = ("Yes, Enemies.", mewo2, "MeowTrykx")
                elif tutorial_scene.script_step == 5:
                    # summon dummy and go to battle
                    # spawn dummy on right, small delay, then move to battle_scene
                    tutorial_scene.script_step = 6
                    # draw final frame then transition
                    screen.fill(BLACK)
                    screen.blit(background, (-camera_x, HEIGHT - bg_height))
                    screen.blit(platform, (-camera_x, HEIGHT - pf_height))
                    screen.blit(current_sprite, (player_x - camera_x, player_y))
                    # draw mewo on right
                    screen.blit(mewo3, (WIDTH - 200, player_y - 50))
                    # show dialogue briefly
                    dialogue_surface = pygame.Surface((WIDTH, 140), pygame.SRCALPHA)
                    dialogue_surface.fill((0,0,0,128))
                    screen.blit(dialogue_surface, (0, HEIGHT - 140))
                    screen.blit(current_portrait, (WIDTH - 140, HEIGHT - 120))
                    name_surface = dialogue_font.render("MeowTrykx:", True, (255,220,220))
                    screen.blit(name_surface, (WIDTH - 280, HEIGHT - 110))
                    text_surface = dialogue_font.render("Yes, Enemies.", True, WHITE)
                    screen.blit(text_surface, (WIDTH - 260, HEIGHT - 80))
                    pygame.display.flip()
                    pygame.time.delay(900)
                    # transition to battle. use current_hp (which is 1)
                    # call battle scene (returns player_hp, victory_flag)
                    player_hp_after, battle_result = battle_scene(player_name, mc_idle, (player_x, player_y), current_hp, max_hp)
                    # after battle returns, place values back and resume or end
                    current_hp = player_hp_after
                    # for now, after battle we simply return to tutorial (could branch)
                    # clear script state and continue
                    tutorial_scene.script_step = 0
                    frozen = False
                    mewo_sequence = False

        # Dialogue box displayed while in normal dialogs, void etc or during script steps up to 5
        if show_dialogue or void_triggered or mewo_sequence or hp_sequence or tutorial_scene.script_step in (1,2,3,4,5):
            dialogue_surface = pygame.Surface((WIDTH, 140), pygame.SRCALPHA)
            dialogue_surface.fill((0,0,0,128))
            screen.blit(dialogue_surface, (0, HEIGHT - 140))

            # choose portrait placement
            if mewo_sequence or tutorial_scene.script_step in (2,3,5):
                # mewo on right
                screen.blit(current_portrait, (WIDTH - 140, HEIGHT - 120))
            else:
                screen.blit(current_portrait, (40, HEIGHT - 120))

            # speaker name
            current_speaker = speaker.replace("Player", player_name) if speaker else ""
            name_surface = dialogue_font.render(f"{current_speaker}:", True, (255,220,220)) if current_speaker else None
            if name_surface:
                screen.blit(name_surface, (160, HEIGHT - 110))

            # text
            text_surface = dialogue_font.render(dialogue_text, True, WHITE)
            screen.blit(text_surface, (170, HEIGHT - 80))

            # continue prompt
            continue_surface = dialogue_font.render("Press Z to Continue", True, (200,200,200))
            screen.blit(continue_surface, continue_surface.get_rect(bottomright=(WIDTH - 20, HEIGHT - 10)))

        # draw HP
        draw_hp_bar(screen, 40, 40, current_hp, max_hp)

        pygame.display.flip()
        clock.tick(60)

# ==========================================
#  GAME START
# ==========================================
if __name__ == "__main__":
    player_name = get_player_name()
    tutorial_scene(player_name)
