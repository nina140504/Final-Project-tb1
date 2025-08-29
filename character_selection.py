import pygame
import sys
import os
import subprocess
import time

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Choose your charakter.")
clock = pygame.time.Clock()

background_path = os.path.join("Images", "main_menu_title.png")
arrow_path = os.path.join("Images", "arrow_button.png")

background = pygame.image.load(background_path)
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
arrow_img = pygame.image.load(arrow_path)
arrow_img = pygame.transform.scale(arrow_img, (120, 120))
arrow_rect = arrow_img.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))

# Character Images
char_files = [
    os.path.join("Images", "Character", "png", "Finja.png"),
    os.path.join("Images", "Character", "png", "Jan.png"),
    os.path.join("Images", "Character", "png", "Nina.png"),
    os.path.join("Images", "Character", "png", "Qianxun.png"),
    os.path.join("Images", "Character", "png", "racoon.png")
]
char_icons = []
for path in char_files:
    try:
        img = pygame.image.load(path)
        char_icons.append(pygame.transform.scale(img, (100, 100)))
    except Exception as e:
        surf = pygame.Surface((100, 100))
        surf.fill((125, 125, 125))
        char_icons.append(surf)

font_big = pygame.font.SysFont("Courier New", 28, bold=True)
font_small = pygame.font.SysFont("Courier New", 22)
input_font = pygame.font.SysFont(None, 38)

# State variables -- this part was created with AI
STATE_PLAYERNUM = 0
STATE_SELECT = 1
STATE_DONE = 2
state = STATE_PLAYERNUM

num_players = None
current_player = 0
player_names = []
player_choices = []
typed_name = ""

# buttons for number of players -- this was created with AI
button_width, button_height = 60, 60
button_gap = 40
buttons = []
for i in range(1, 6):
    x = SCREEN_WIDTH // 2 - ((5 * button_width + 4 * button_gap)//2) + (i-1)*(button_width+button_gap)
    y = SCREEN_HEIGHT // 2 + 70 - button_height//2
    rect = pygame.Rect(x, y, button_width, button_height)
    buttons.append((rect, str(i)))

box_width, box_height = 760, 260
box_rect = pygame.Rect((SCREEN_WIDTH-box_width)//2, 280, box_width, box_height)

def draw_playernum():
    screen.blit(background, (0, 0))
    overlay = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 170))
    screen.blit(overlay, box_rect.topleft)
    t1 = font_big.render("How many players?", True, (255,215,90))
    screen.blit(t1, (SCREEN_WIDTH//2-t1.get_width()//2, box_rect.y+40))
    for rect, txt in buttons:
        pygame.draw.rect(screen, (255, 255, 255), rect, 2)
        pygame.draw.rect(screen, (225,225,225), rect, 3)
        lab = font_big.render(txt, True, (255, 255, 255))
        screen.blit(lab, (rect.x + (rect.width-lab.get_width())//2, rect.y+8))

def draw_selection():
    screen.blit(background, (0, 0))
    # Overlay-Box
    overlay = pygame.Surface((box_width, box_height+50), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 0))
    screen.blit(overlay, box_rect.topleft)
    # text
    t1 = font_big.render(f"Player {current_player+1}: Click your character", True, (255,220,80))
    t2 = font_small.render("Enter your name and press ENTER.", True, (255,255,255))
    screen.blit(t1, (SCREEN_WIDTH//2-t1.get_width()//2, box_rect.y+30))
    screen.blit(t2, (SCREEN_WIDTH//2-t2.get_width()//2, box_rect.y+76))
    # character icons
    icon_y = box_rect.y+120
    icon_rects = []
    for i, icon in enumerate(char_icons):
        x = box_rect.x+40+i*140
        rect = pygame.Rect(x, icon_y, 100, 100)
        # selection mark
        outline_color = (255, 225, 0) if (len(player_choices) > current_player and player_choices[current_player] == i) else (120,120,120)
        pygame.draw.rect(screen, outline_color, rect, 5)
        screen.blit(icon, (x, icon_y))
        icon_rects.append(rect)
    # entering name
    name_label = font_small.render("Name:", True, (255,255,255))
    screen.blit(name_label, (SCREEN_WIDTH//2-210, icon_y+115))
    name_box = pygame.Rect(SCREEN_WIDTH//2-130, icon_y+110, 250, 48)
    pygame.draw.rect(screen, (220,220,220), name_box)
    text_surf = input_font.render(typed_name, True, (55,55,55))
    screen.blit(text_surf, (name_box.x+10, name_box.y+5))
    return icon_rects, name_box

def draw_done():
    screen.blit(background, (0, 0))
    overlay = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 170))
    screen.blit(overlay, box_rect.topleft)
    t = font_big.render("All done!", True, (60,255,120))
    t2 = font_small.render("Click arrow to start the game.", True, (255,255,255))
    screen.blit(t, (SCREEN_WIDTH//2-t.get_width()//2, box_rect.y+80))
    screen.blit(t2, (SCREEN_WIDTH//2-t2.get_width()//2, box_rect.y+140))
    screen.blit(arrow_img, arrow_rect)


# --- Main Loop ---
running = True
while running:
    if state == STATE_PLAYERNUM:
        draw_playernum()
    elif state == STATE_SELECT:
        icon_rects, name_box = draw_selection()
    elif state == STATE_DONE:
        draw_done()
    pygame.display.flip()
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if state == STATE_PLAYERNUM:
                for idx, (rect, txt) in enumerate(buttons):
                    if rect.collidepoint(event.pos):
                        num_players = int(txt)
                        state = STATE_SELECT
            elif state == STATE_SELECT:
                # Char-Icons Klick -- thi was created with ai
                for i, rect in enumerate(icon_rects):
                    if rect.collidepoint(event.pos):
                        if len(player_choices)<=current_player:
                            player_choices.append(i)
                        else:
                            player_choices[current_player] = i
            elif state == STATE_DONE and arrow_rect.collidepoint(event.pos):
                with open("player_selection.txt", "w") as f:
                    for pname, pchar in zip(player_names, player_choices):
                        f.write(f"{pname};{char_files[pchar]}\n")
                base_path = os.path.dirname(os.path.abspath(__file__))
                main_game_path = os.path.join(base_path, "main_game_loop.py")
                proc = subprocess.Popen([sys.executable, main_game_path])
                time.sleep(1.5)
                pygame.quit()
                sys.exit()
        elif event.type == pygame.KEYDOWN:
            if state == STATE_SELECT and name_box.collidepoint(pygame.mouse.get_pos()):
                # name input
                if event.key == pygame.K_RETURN:
                    if typed_name and len(player_choices)>current_player:
                        player_names.append(typed_name)
                        typed_name = ""
                        current_player += 1
                        if current_player == num_players:
                            state = STATE_DONE
                elif event.key == pygame.K_BACKSPACE:
                    typed_name = typed_name[:-1]
                elif len(typed_name) < 12 and event.unicode.isprintable():
                    typed_name += event.unicode
