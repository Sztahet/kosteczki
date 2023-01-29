import pygame
import random
from mechanics.map_generator import generate_map
from mechanics.player import Player
from mechanics.marker import Marker
from mechanics.score import calculate_score

# Initialize pygame
pygame.init()
# Create a clock object to control the frame rate
clock = pygame.time.Clock()
# Set the size of the window, game always should be run in 4:3 window TODO SUPPORT for 16:9
game_width = 800
game_height = 600
window_size = (game_width, game_height)
screen = pygame.display.set_mode(window_size)
# Set the width of the player section
player_section_width = game_width-game_height
# Set the title of the window
pygame.display.set_caption("Kosteczki")
# Create a font
font_size = int(game_height/20)
font = pygame.font.Font(None, font_size)
small_font = pygame.font.Font(None, int(font_size*0.8))
# Create a variable to track the number of players
num_players = 8
# below is a number that is used to determinate how should we generate map etc. 15 by default
map_scale = 15
# Create how many markers should be in game - as well as how big the map should be default 20
map_size = 20
# set square_size for map
square_size = game_height/map_scale
# Create a list to store player names
player_names = ['' for _ in range(num_players)]
# Set constant player colors:
player_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
                 (0, 255, 255), (255, 0, 255), (255, 128, 0), (128, 0, 255)]
# Create a variable to track the current player
current_player = 0
# Create a delay between key presses
key_press_delay = 200
# Create a variable to track the last key press
last_key_press = pygame.time.get_ticks()
# Create a variable to track the last key press
last_key = None
# Create a button for selecting the number of players


def create_button(text, x, y, width, height, color):
    button_surface = font.render(text, True, (255, 255, 255))
    button_rect = button_surface.get_rect()
    button_rect.center = (x + width / 2, y + height / 2)
    pygame.draw.rect(screen, color, (x, y, width, height))
    screen.blit(button_surface, button_rect)
    return button_rect



# Create a function to handle player name input


def handle_name_input():
    global current_player, last_key_press, last_key
    keys = pygame.key.get_pressed()
    shift = pygame.key.get_mods() & pygame.KMOD_SHIFT
    if keys[pygame.K_BACKSPACE] and pygame.time.get_ticks() - last_key_press > key_press_delay:
        player_names[current_player] = ''
        last_key_press = pygame.time.get_ticks()
    elif keys[pygame.K_RETURN] and pygame.time.get_ticks() - last_key_press > key_press_delay:
        next_player()
        last_key_press = pygame.time.get_ticks()
    else:
        for i in range(97, 123):
            if keys[i]:
                if pygame.time.get_ticks() - last_key_press > (key_press_delay // ((i != last_key) + 1)):
                    if shift:
                        player_names[current_player] += chr(i-32)
                    else:
                        player_names[current_player] += chr(i)
                    last_key = i
                    last_key_press = pygame.time.get_ticks()
# Create a function to handle button clicks


def handle_button_clicks():
    global game_state, game_board, markers, players, swap_buttons, current_player
    if start_button_rect.collidepoint(pygame.mouse.get_pos()):
        game_board = generate_map(num_players, map_scale, map_scale, map_size)
        # handling markers
        markers = []
        for i in range(num_players):
            for j in range(map_size):
                markers.append(Marker(
                    i, player_colors[i], None, None, square_size/2))
        # handle players
        for i in range(num_players):
            random.shuffle(markers)
            players.append(
                Player(player_names[i], player_colors[i], markers))
            markers = markers[3:]
            swap_buttons.append(i)
        current_player = random.randint(0,num_players -1) # selecting random player who will do the first move in game
        game_state = "running"

# Create a function to handle clicks on the button


def handle_button_num_players_change(button_rect):
    global num_players, player_names
    if button_rect.collidepoint(pygame.mouse.get_pos()):
        num_players += 1
        if num_players > 8:
            num_players = 5
        player_names = ["Player " + str(i+1) for i in range(num_players)]


# Create a function to display the player section

def display_player_section():
    # Draw a rectangle for the player section
    pygame.draw.rect(screen, (0, 0, 0), (game_width -
                     player_section_width, 0, player_section_width, game_height))
    # Set the starting y position for the player names
    y = game_height/20
    # Iterate through the player names and display them and thier score and markers
    for i, name in enumerate(player_names):
        player_name_surface = font.render(f"{name}  ({players[i].score})", True, player_colors[i])
        screen.blit(player_name_surface, (game_width -
                    player_section_width+(player_section_width/5), y))
        if i == current_player:
            pygame.draw.rect(screen, (255, 255, 255), (game_width-player_section_width+(player_section_width/5) - 5,
                             y - 5, player_name_surface.get_width() + 10, player_name_surface.get_height() + 10), 2)
        x = game_width-player_section_width+(player_section_width/5)
        y += font_size

        for marker in players[i].markers:
            marker.x = x
            marker.y = y
            pygame.draw.rect(screen, marker.color, pygame.Rect(
                marker.x, marker.y, marker.size, marker.size))
            x += player_section_width/5

    # Create a swap button for this player
        swap_button = SwapButton(i, x, y, square_size/2)
        swap_button.rect.center = (x+square_size/2, y+square_size/4)
        if current_player != i and len(markers) > 0:
            swap_button.draw(screen)
        swap_buttons[i] = swap_button
        y += font_size
    markers_left = font.render(
        f'markers left:{len(markers)}', True, (255, 255, 255))
    screen.blit(markers_left, (game_width-player_section_width +
                (player_section_width/5), game_height - font_size))
# function to swap markers


class SwapButton():
    def __init__(self, player_id, x, y, size):
        self.player_id = player_id
        self.rect = pygame.Rect(x, y, size, size)
        self.text = "<->"
        self.color = (0, 0, 0)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        button_surface = small_font.render(self.text, True, self.color)
        screen.blit(button_surface, self.rect)


def swap_markers(player1, player2):
    player1_markers = player1.markers
    player2_markers = player2.markers
    player1.markers = player2_markers
    player2.markers = player1_markers

def next_player():
    global current_player,players
    current_player += 1
    if current_player >= num_players:
        current_player = 0
    if game_state != 'menu':
        if len(players[current_player].markers) > 0:
            players[current_player].markers[0].is_selected = True
            players[current_player].markers[0].size *= 1.25

# swap buttons array
swap_buttons = []
# players empty array to be filled when game start to run
players = []

# Create a variable to track the game state
game_state = "menu"
frame_counter = 0 #used only for displaying position of current player in menu (to easy spot where you typing)
# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            # sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and game_state == 'menu':
            handle_button_num_players_change(button_rect)
            handle_button_clicks()
        elif event.type == pygame.MOUSEBUTTONDOWN and game_state == 'running':

            # Get the mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for button in swap_buttons:
                if button.rect.collidepoint(mouse_x, mouse_y) and button.player_id != current_player and len(markers) > 0:
                    swap_markers(players[current_player],
                                 players[button.player_id])
                    next_player()
            # Check if the mouse position is within the marker's rectangle
            for marker in players[current_player].markers:
                if mouse_x >= game_width - player_section_width:
                    marker.select(mouse_x, mouse_y)
                elif game_board[int(mouse_y/square_size)][int(mouse_x/square_size)] == 'Y' and marker.is_selected:
                    game_board = marker.marker_to_map(game_board, int(
                        mouse_y/square_size), int(mouse_x/square_size))
                    players[marker.player_marker].score = calculate_score(game_board,marker.player_marker)
                    players[current_player].remove_marker(marker)
                    if len(markers):
                        new_marker = markers[0]
                        players[current_player].add_marker(new_marker)
                        markers.remove(new_marker)
                    next_player()
    if game_state == "menu":
        frame_counter = (frame_counter + 1) % 20
        screen.fill((0, 0, 0))
        handle_name_input()
        # Create a button for selecting the number of players
        button_rect = create_button(
            f"{num_players} Players", 100, 100, 200, 50, (0, 255, 0))
        # Create a list to store player colors
        player_colors = [player_colors[i %
                                       len(player_colors)] for i in range(len(player_colors))]

        for i, (name, color) in enumerate(zip(player_names, player_colors)):
            if frame_counter >= 10 and i == current_player:
                pacer = "|"
            else:
                pacer = ""
            player_name_text = font.render(
                f"{i+1}. {name}{pacer}", True, color)
            player_name_rect = player_name_text.get_rect()
            player_name_rect.center = (400, 100 + (i * 30))
            screen.blit(player_name_text, player_name_rect)
        start_button_surface = font.render("Start Game", True, (255, 255, 255))
        start_button_rect = start_button_surface.get_rect()
        start_button_rect.center = (400, 500)
        screen.blit(start_button_surface, start_button_rect)
    elif game_state == "running":
        # Draw the game here
        screen.fill((0, 0, 0))
        if len(markers) == 0 and len(players[current_player].markers) == 0:
            end_game = True
            for  i in range(0,num_players):
                if len(players[i].markers) > 0: end_game = False
            if end_game:
                print('move to result screen')
            
        display_player_section()
        for row in range(len(game_board)):
            for col in range(len(game_board[row])):
                if game_board[row][col] == 'X':
                    square_rect = pygame.Rect(
                        (col * square_size)+1, (row * square_size)+1, square_size-1, square_size-1)
                    pygame.draw.rect(screen, (128, 128, 128), square_rect)
                elif game_board[row][col] == 'Y':
                    square_rect = pygame.Rect(
                        (col * square_size)+1, (row * square_size)+1, square_size-1, square_size-1)
                    pygame.draw.rect(screen, (255, 255, 255), square_rect)
                elif game_board[row][col] in (0, 1, 2, 3, 4, 5, 6, 7):
                    square_rect = pygame.Rect(
                        (col * square_size)+1, (row * square_size)+1, square_size-1, square_size-1)
                    pygame.draw.rect(
                        screen, player_colors[game_board[row][col]], square_rect)
    pygame.display.update()
    # Limit the frame rate to 10 FPS
    clock.tick(10)
