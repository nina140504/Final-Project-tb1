import numpy as np
import pygame
import sys
import random
import os
import subprocess
import time

#initializing the game frame
pygame.init()
pygame.mixer.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Madeira-Party!")

# paths
board_image = pygame.image.load(os.path.join("Images", "board_map.png")).convert_alpha()
board_image = pygame.transform.scale(board_image, (screen_width, screen_height))
current_folder = os.path.dirname(os.path.abspath(__file__))
sound_folder = os.path.join(current_folder, "sounds")

# load sounds
whoosh_sound = pygame.mixer.Sound(os.path.join(sound_folder, "whoosh.wav"))
score_sound = pygame.mixer.Sound(os.path.join(sound_folder, "score.wav"))
wrong_sound = pygame.mixer.Sound(os.path.join(sound_folder, "wrong.wav"))

# helper function for the sounds
def play_field_sound(field):
    if field == "blue":
        wrong_sound.play()
    elif field == "pink" or field == "yellow":
        score_sound.play()
    elif field == "white":
        whoosh_sound.play()


# background music
music_path = os.path.join(sound_folder, "music", "GameLoop_music_zapsplat_game_music_fun_tropical_caribean_steel_drums_percussion_008.mp3")
pygame.mixer.music.load(music_path)
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

#loading player images
def scale_img(img, size=(50, 50)):
    return pygame.transform.scale(img, size)

player_names = []
player_images = []
with open("player_selection.txt", "r") as f:
    for line in f:
        name, img_path = line.strip().split(";")
        player_names.append(name)
        img = pygame.image.load(img_path)
        player_images.append(pygame.transform.scale(img, (70, 70)))


#dice image
dice_image = pygame.image.load(os.path.join("Images", "dices.png")).convert_alpha()
dice_image = pygame.transform.scale(dice_image, (80, 80))
dice_rect = dice_image.get_rect()
dice_rect.topleft = (screen_width - dice_rect.width - 20, 20)

# defining the board fields
board_positions = [
    "white",   # -3 points
    "yellow",  # neutral
    "blue", # minigame
    "blue",   # +2 points
    "white",
    "pink",
    "yellow",
    "white",
    "white",
    "yellow",
    "white",
    "blue",
    "yellow",
    "white",
    "pink",
    "yellow",
    "white",
    "blue",
    "yellow",
    "white",
    "pink"
]

#defining the field positions
original_board_coords = [
    (1779,167),  #field 1
    (1257,203),  #field 2
    (808,287),  #field 3
    (505,509),  #field 4
    (272,764),  #field 5
    (199,1160),  #field 6
    (272,1483),  #field 7
    (507,1783),  #field 8
    (785,2091),  #field 9
    (1189,2175),  #field 10
    (1624,2225),  #field 11
    (2085,2225),  #field 12
    (2480,2077),  #field 13
    (2814,1953),  #field 14
    (3154,1824),  #field 15
    (3258,1552),  #field 16
    (3373,1274),  #field 17
    (3258,878),  #field 18
    (3050,499),  #field 19
    (2708,317),  #field 20
    (2318,207)  #field 21
]

board_coords = [
    (int(x / 3508 * screen_width), int(y / 2339 * screen_height))
    for (x, y) in original_board_coords
]
#this part was created with ai
assert len(board_positions) == len(board_coords)
#

#classes for the game logic

class Player:
    def __init__(self, name, image, start_pos=0):
        self.name = name
        self.position = start_pos
        self.score = 0
        self.minigames_played = 0
        self.image = image
        self.active = True

#updating board position
    def move(self, steps, board_size):
        self.position = (self.position + steps) % board_size

    def get_coords(self, board_coords):
        return board_coords[self.position]

class Game:
    def __init__(self, player_names, player_images, board_positions, board_coords):
        self.players = [
            Player(name, image)
            for name, image in zip(player_names, player_images)
            ]
        self.board_positions = board_positions
        self.board_coords = board_coords
        self.turn_index = 0
        self.finished_players = set()
        self.total_minigames = 5
        self.rules_files = {
            "boozypairs_game.py": os.path.join("Mini Games", "boozypairs", "boozypairs_rules.py"),
            "catfish_game.py": os.path.join("Mini Games", "catfishfever", "catfish_rules.py"),
            "coconutcatch_game.py": os.path.join("Mini Games", "coconutcatch", "coconutcatch_rules.py"),
            "suitcase_game.py": os.path.join("Mini Games", "suitcasesort", "suitcase_rules.py"),
            "ananas_game.py": os.path.join("Mini Games", "ananaspong", "ananas_rules.py")
        }

    def roll_dice(self):
        return np.random.randint(1, 7)


    def apply_field(self, player):
        field = self.board_positions[player.position]
        if field == "blue":
            player.score -= 3
        elif field == "pink":
            player.score += 2
        elif field == "yellow":
            # --- starting minigame overlay  ---
            self.show_minigame_overlay()
            player.minigames_played += 1
            minigame_score = self.play_minigame(player)
            player.score += minigame_score
            # --- this part was created with ai
            if player.minigames_played >= self.total_minigames:
                player.active = False
                self.finished_players.add(player.name)
                print (f"{player.name} is done.", self.finished_players)
        # white has no action


    def show_minigame_overlay(self):
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.set_alpha(180)
        overlay.fill((40, 40, 40))
        screen.blit(overlay, (0, 0))
        notice = pygame.font.SysFont(None,48).render(
            "minigame is running...", True, (255,255,0))
        screen.blit(notice, (screen_width//2 - notice.get_width()//2, screen_height//2 - notice.get_height()//2))
        pygame.display.flip()

#integrating the minigames
    def play_minigame(self, player):
        print(f"{player.name} plays a minigame.")
        minigames = [
            os.path.join("Mini Games", "boozypairs", "boozypairs_rules.py"),
            os.path.join("Mini Games", "catfishfever", "catfish_rules.py"),
            os.path.join("Mini Games", "coconutcatch", "coconutcatch_rules.py"),
            os.path.join("Mini Games", "suitcasesort", "suitcase_rules.py"),
            os.path.join("Mini Games", "ananaspong", "ananas_rules.py")
        ]
        chosen_game = random.choice(minigames)
        basename = os.path.basename(chosen_game)
        rules_file = self.rules_files.get(basename)
        print(f"{player.name} starts {chosen_game}.")

        result = subprocess.run([sys.executable, chosen_game], capture_output = True, text = True)
        try:
            score = int(result.stdout.strip().splitlines()[-1])
        except Exception:
            score = 0
        return score

    def play_turn(self):
        player = self.players[self.turn_index]
        if player.minigames_played >= self.total_minigames:
            player.active = False
            self.finished_players.add(player.name)
            print(f"{player.name} is done and skips this turn.")
            self.next_turn()
            return

        dice = self.roll_dice()
        print(f"{player.name} rolls {dice}.")
        player.move(dice, len(self.board_positions))
        print(f"{player.name} lands on the field {player.position} ({self.board_positions[player.position]}).")
        self.apply_field(player)
        print(f"{player.name} has now {player.score} points and played {player.minigames_played} minigames.")

        if len(self.finished_players) == len(self.players):
            print("All players are done. The Game is over!")
            self.show_results()
            return True

        self.next_turn()
        return False

    def next_turn(self):
        # identify the next active player
        orig_index = self.turn_index
        while True:
            self.turn_index = (self.turn_index + 1) % len(self.players)
            if self.players[self.turn_index].active:
                break
            # endless security
            if self.turn_index == orig_index:
                break

    def show_results(self):
        print("FINAL SCORE:")
        for player in self.players:
            print(f"{player.name}: {player.score} points")

# main game
def main():
    game = Game(player_names, player_images, board_positions, board_coords)
    font = pygame.font.SysFont(None, 33)
    score_font = pygame.font.SysFont(None, 28)
    clock = pygame.time.Clock()
    finished = False
    waiting_for_roll = True

    message = ""
    show_message_ticks = 0
    pending_move = None
    pending_field_action = None
    field_wait_ticks = 0

    margin_top = 20
    margin_left = 20
    icon_size = 35
    spacing = 10

    while not finished:
        while not game.players[game.turn_index].active:
            game.next_turn()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                while not game.players[game.turn_index].active:
                    game.next_turn()
                current_player = game.players[game.turn_index]
                if current_player.minigames_played >= game.total_minigames:
                    current_player.active = False
                    game.finished_players.add(current_player.name)
                    game.next_turn()
                    continue

                #this part was created with ai ---
                if (dice_rect.collidepoint(mouse_pos) and
                        waiting_for_roll and
                        pending_move is None and
                        pending_field_action is None and
                        game.players[game.turn_index].active):
                    dice_value = game.roll_dice()
                    message = f"Player {game.turn_index + 1} rolled a {dice_value}."
                    show_message_ticks = pygame.time.get_ticks()
                    pending_move = (game.turn_index, dice_value)
                    waiting_for_roll = False
                # ---

        if pending_move is not None:
        # showing message for 1 sec then screen blend
            if pygame.time.get_ticks() - show_message_ticks < 1000:
                pass
            else:
                current_idx, dice_value = pending_move
                player = game.players[current_idx]
                player.move(dice_value, len(game.board_positions))
                field = game.board_positions[player.position]
                play_field_sound(field)
                field_wait_ticks = pygame.time.get_ticks()
                pending_field_action = player
                pending_move = None
                message = ""

        if pending_field_action is not None:
            if pygame.time.get_ticks() - field_wait_ticks < 1500:
                pass
            else:
                game.apply_field(pending_field_action)
                player = pending_field_action
                if player.minigames_played >= game.total_minigames and player.active:
                    player.active = False
                    game.finished_players.add(player.name)
                finished = len(game.finished_players) == len(game.players)
                if finished:
                    final_scores = sorted(
                        [(p.name, p.score) for p in game.players],
                        key=lambda x: x[1], reverse=True
                    )
                    pygame.quit()
                    from end_screen import run_end_screen
                    run_end_screen(final_scores)
                    sys.exit()
                else:
                    pending_field_action = None
                    message = ""
                    waiting_for_roll = True
                    game.next_turn()
                    while not game.players[game.turn_index].active:
                        game.next_turn()

        screen.fill((0,0,0))
        screen.blit(board_image, (0,0))

        # --- Mini-Icons + Score top left ---
        for idx, player in enumerate(game.players):
            small_icon = pygame.transform.scale(player.image, (icon_size, icon_size))
            y_pos = margin_top + idx * (icon_size + spacing)
            if game.turn_index == idx and player.active:
                border_color = (220, 220, 0)
                border_thickness = 4
            else:
                border_color = (150, 150, 150)
                border_thickness = 2
            icon_rect = pygame.Rect(margin_left, y_pos, icon_size, icon_size)
            pygame.draw.rect(screen, border_color, icon_rect, border_thickness)
            screen.blit(small_icon, (margin_left, y_pos))
            score_text = score_font.render(str(player.score), True, (255,255,255))
            screen.blit(score_text, (margin_left + icon_size + 10, y_pos + icon_size//4))

        # --- figures on the board ---
        for idx, player in enumerate(game.players):
            x, y = board_coords[player.position]
            icon = player.image
            screen.blit(icon, (x-20+idx*6, y-40+idx*6))
            name_img = font.render(player.name, True, (235, 220, 235))
            screen.blit(name_img, (x-20+idx*6, y-60+idx*6))

        # --- message ---
        if message:
            message_img = font.render(message, True, (255,255,80))
            screen.blit(message_img, (screen_width//2 - message_img.get_width()//2, screen_height//2 - 100))

        # --- Dice top right ---
        screen.blit(dice_image, dice_rect.topleft)

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    # --- this was created with ai
    final_scores = main()
    from end_screen import run_end_screen
    run_end_screen(final_scores)

