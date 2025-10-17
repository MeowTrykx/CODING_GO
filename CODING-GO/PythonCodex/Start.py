import os, pygame, sys

pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 1080, 585

# --- Paths relative to this file ---
base_path = os.path.dirname(os.path.abspath(__file__))
fonts_folder = os.path.join(base_path, "Fonts")
images_folder = os.path.join(base_path, "Images")
audio_folder = os.path.join(base_path, "Audio")

font_path = os.path.join(fonts_folder, "Pixeled.ttf")
bg_path = os.path.join(images_folder, "MainBackground.png")
title_path = os.path.join(images_folder, "CodingGo.png")

#Not Finished Yet.