
import pygame
import sys
import time
import pygame
import sys
import time


def loading_screen():
    # Display the loading screen
    screen.fill((0, 0, 0))  # Fill the screen with black (loading screen)
    font = pygame.font.Font(None, 74)
    text = font.render("Loading...", True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(text, text_rect)
    pygame.display.update()


def check_valid_moves(piece, location, pieces, locations, enemy_pieces, enemy_locations):
    """
    Calculate valid moves for a given piece based on the game state.

    Args:
        piece (str): The type of the chess piece (e.g., 'king', 'queen', etc.).
        location (tuple): The current position of the piece (x, y).
        pieces (list): List of the current player's pieces.
        locations (list): List of the current positions of the player's pieces.
        enemy_pieces (list): List of the enemy's pieces.
        enemy_locations (list): List of the enemy's positions.

    Returns:
        list: List of valid moves as (x, y) tuples.
    """
    x, y = location
    valid_moves = []

    if piece == 'king':
        # King moves one step in all directions
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),          (0, 1),
                      (1, -1), (1, 0), (1, 1)]
        for dx, dy in directions:
            move = (x + dx, y + dy)
            if 0 <= move[0] < 8 and 0 <= move[1] < 8:  # Within board limits
                if move not in locations:  # Can't land on its own piece
                    valid_moves.append(move)

    elif piece == 'rook':
        # Rook moves in straight lines (horizontal and vertical)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in directions:
            for step in range(1, 8):
                move = (x + dx * step, y + dy * step)
                if 0 <= move[0] < 8 and 0 <= move[1] < 8:
                    if move in locations:  # Blocked by own piece
                        break
                    valid_moves.append(move)
                    if move in enemy_locations:  # Capture enemy piece, stop further
                        break
                else:
                    break

    # Add similar logic for other pieces: queen, bishop, knight, pawn.

    return valid_moves


def is_king_in_check(king_position, enemy_pieces, enemy_locations, current_pieces, current_locations):
    for i, piece in enumerate(enemy_pieces):
        # Ensure the arguments are passed correctly
        moves = check_valid_moves(
            piece,                 # piece type
            enemy_locations[i],    # location of the enemy piece
            enemy_pieces,          # list of enemy pieces
            enemy_locations,       # list of enemy locations
            current_pieces,        # list of current player's pieces
            current_locations      # list of current player's locations
        )
        if king_position in moves:
            return True
    return False



def is_checkmate(king_position, current_pieces, current_locations, enemy_pieces, enemy_locations):
    if not is_king_in_check(king_position, enemy_pieces, enemy_locations, current_pieces, current_locations):
        return False  # Not in check

    for i, piece in enumerate(current_pieces):
        moves = check_valid_moves(piece, current_locations[i], current_pieces, current_locations, enemy_pieces, enemy_locations)
        for move in moves:
            original_position = current_locations[i]
            current_locations[i] = move
            if not is_king_in_check(king_position, enemy_pieces, enemy_locations, current_pieces, current_locations):
                current_locations[i] = original_position
                return False
            current_locations[i] = original_position
    return True  # No moves escape the check



pygame.init()

# Initialize game window




# Loading screen function



WIDTH = 1000
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Chess')
font = pygame.font.Font('freesansbold.ttf', 20)
medium_font = pygame.font.Font('freesansbold.ttf', 40)
big_font = pygame.font.Font('freesansbold.ttf', 50)

start_ticks = pygame.time.get_ticks()  # Record the start time for the loading screen
loading_duration = 2000  # Duration of loading screen in milliseconds (2 seconds)


font = pygame.font.Font(None, 50)


def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02}:{seconds:02}"


white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
captured_pieces_white = []
captured_pieces_black = []
turn_step = 0
selection = 100
valid_moves = []
black_queen = pygame.image.load('black queen.png')
black_queen = pygame.transform.scale(black_queen, (80, 80))
black_queen_small = pygame.transform.scale(black_queen, (45, 45))
black_king = pygame.image.load('black king.png')
black_king = pygame.transform.scale(black_king, (80, 80))
black_king_small = pygame.transform.scale(black_king, (45, 45))
black_rook = pygame.image.load('black rook.png')
black_rook = pygame.transform.scale(black_rook, (80, 80))
black_rook_small = pygame.transform.scale(black_rook, (45, 45))
black_bishop = pygame.image.load('black bishop.png')
black_bishop = pygame.transform.scale(black_bishop, (80, 80))
black_bishop_small = pygame.transform.scale(black_bishop, (45, 45))
black_knight = pygame.image.load('black knight.png')
black_knight = pygame.transform.scale(black_knight, (80, 80))
black_knight_small = pygame.transform.scale(black_knight, (45, 45))
black_pawn = pygame.image.load('black pawn.png')
black_pawn = pygame.transform.scale(black_pawn, (65, 65))
black_pawn_small = pygame.transform.scale(black_pawn, (45, 45))
white_queen = pygame.image.load('white queen.png')
white_queen = pygame.transform.scale(white_queen, (80, 80))
white_queen_small = pygame.transform.scale(white_queen, (45, 45))
white_king = pygame.image.load('white king.png')
white_king = pygame.transform.scale(white_king, (80, 80))
white_king_small = pygame.transform.scale(white_king, (45, 45))
white_rook = pygame.image.load('white rook.png')
white_rook = pygame.transform.scale(white_rook, (80, 80))
white_rook_small = pygame.transform.scale(white_rook, (45, 45))
white_bishop = pygame.image.load('white bishop.png')
white_bishop = pygame.transform.scale(white_bishop, (80, 80))
white_bishop_small = pygame.transform.scale(white_bishop, (45, 45))
white_knight = pygame.image.load('white knight.png')
white_knight = pygame.transform.scale(white_knight, (80, 80))
white_knight_small = pygame.transform.scale(white_knight, (45, 45))
white_pawn = pygame.image.load('white pawn.png')
white_pawn = pygame.transform.scale(white_pawn, (65, 65))
white_pawn_small = pygame.transform.scale(white_pawn, (45, 45))
white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
small_white_images = [white_pawn_small, white_queen_small, white_king_small, white_knight_small,
                      white_rook_small, white_bishop_small]
black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
small_black_images = [black_pawn_small, black_queen_small, black_king_small, black_knight_small,
                      black_rook_small, black_bishop_small]
piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']
counter = 0
winner = ''
game_over = False


def draw_board():
    for i in range(32):
        column = i % 4
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(screen, 'light gray', [600 - (column * 200), row * 100, 100, 100])
        else:
            pygame.draw.rect(screen, 'light gray', [700 - (column * 200), row * 100, 100, 100])
        pygame.draw.rect(screen, 'gray', [0, 800, WIDTH, 100])
        pygame.draw.rect(screen, 'gold', [0, 800, WIDTH, 100], 5)
        pygame.draw.rect(screen, 'gold', [800, 0, 200, HEIGHT], 5)
        status_text = ['White!', 'Move',
                       'Black', 'Move']
        if turn_step == 0 or turn_step == 1:  # White's turn
            text_color = 'white'
        else:  # Black's turn
            text_color = 'black'
        screen.blit(big_font.render(status_text[turn_step], True, text_color), (810, 400))
        for i in range(9):
            pygame.draw.line(screen, 'black', (0, 100 * i), (800, 100 * i), 2)
            pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i, 800), 2)
        screen.blit(medium_font.render('FORFEIT', True, 'black'), (810, 830))


def draw_pieces():
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        if white_pieces[i] == 'pawn':
            screen.blit(white_pawn, (white_locations[i][0] * 100 + 22, white_locations[i][1] * 100 + 30))
        else:
            screen.blit(white_images[index], (white_locations[i][0] * 100 + 10, white_locations[i][1] * 100 + 10))
        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(screen, 'red', [white_locations[i][0] * 100 + 1, white_locations[i][1] * 100 + 1,
                                                 100, 100], 2)

    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == 'pawn':
            screen.blit(black_pawn, (black_locations[i][0] * 100 + 22, black_locations[i][1] * 100 + 30))
        else:
            screen.blit(black_images[index], (black_locations[i][0] * 100 + 10, black_locations[i][1] * 100 + 10))
        if turn_step >= 2:
            if selection == i:
                pygame.draw.rect(screen, 'blue', [black_locations[i][0] * 100 + 1, black_locations[i][1] * 100 + 1,
                                                  100, 100], 2)


def check_options(pieces, locations, turn):
    moves_list = []
    all_moves_list = []
    for i in range((len(pieces))):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves_list = check_pawn(location, turn)
        elif piece == 'rook':
            moves_list = check_rook(location, turn)
        elif piece == 'knight':
            moves_list = check_knight(location, turn)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn)
        elif piece == 'queen':
            moves_list = check_queen(location, turn)
        elif piece == 'king':
            moves_list = check_king(location, turn)
        all_moves_list.append(moves_list)
    return all_moves_list


def check_king(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list


def check_queen(position, color):
    moves_list = check_bishop(position, color)
    second_list = check_rook(position, color)
    for i in range(len(second_list)):
        moves_list.append(second_list[i])
    return moves_list


def check_bishop(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  # up-right, up-left, down-right, down-left
        path = True
        chain = 1
        if i == 0:
            x = 1
            y = -1
        elif i == 1:
            x = -1
            y = -1
        elif i == 2:
            x = 1
            y = 1
        else:
            x = -1
            y = 1
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list


def check_rook(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  # down, up, right, left
        path = True
        chain = 1
        if i == 0:
            x = 0
            y = 1
        elif i == 1:
            x = 0
            y = -1
        elif i == 2:
            x = 1
            y = 0
        else:
            x = -1
            y = 0
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list


def check_pawn(position, color):
    moves_list = []
    if color == 'white':
        if (position[0], position[1] + 1) not in white_locations and \
                (position[0], position[1] + 1) not in black_locations and position[1] < 7:
            moves_list.append((position[0], position[1] + 1))
        if (position[0], position[1] + 2) not in white_locations and \
                (position[0], position[1] + 2) not in black_locations and position[1] == 1:
            moves_list.append((position[0], position[1] + 2))
        if (position[0] + 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] - 1, position[1] + 1))
    else:
        if (position[0], position[1] - 1) not in white_locations and \
                (position[0], position[1] - 1) not in black_locations and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))
        if (position[0], position[1] - 2) not in white_locations and \
                (position[0], position[1] - 2) not in black_locations and position[1] == 6:
            moves_list.append((position[0], position[1] - 2))
        if (position[0] + 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] - 1, position[1] - 1))
    return moves_list


def check_knight(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    # 8 squares to check for knights, they can go two squares in one direction and one in another
    targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list



def draw_valid(moves):
    if turn_step < 2:
        color = 'red'
    else:
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50), 5)


def draw_captured():
    for i in range(len(captured_pieces_white)):
        captured_piece = captured_pieces_white[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_black_images[index], (825, 5 + 50 * i))
    for i in range(len(captured_pieces_black)):
        captured_piece = captured_pieces_black[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_white_images[index], (925, 5 + 50 * i))


def draw_check():
    if turn_step < 2:
        if 'king' in white_pieces:
            king_index = white_pieces.index('king')
            king_location = white_locations[king_index]
            for i in range(len(black_options)):
                if king_location in black_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark red', [white_locations[king_index][0] * 100 + 1,
                                                              white_locations[king_index][1] * 100 + 1, 100, 100], 5)
    else:
        if 'king' in black_pieces:
            king_index = black_pieces.index('king')
            king_location = black_locations[king_index]
            for i in range(len(white_options)):
                if king_location in white_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark blue', [black_locations[king_index][0] * 100 + 1,
                                                               black_locations[king_index][1] * 100 + 1, 100, 100], 5)


def draw_game_over():
    pygame.draw.rect(screen, 'black', [200, 200, 400, 70])
    screen.blit(font.render(f'{winner} won the game!', True, 'white'), (210, 210))
    screen.blit(font.render(f'Press ENTER to Restart!', True, 'white'), (210, 240))


black_options = check_options(black_pieces, black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')
# Main game loop
run = True
player_1_time = 600  # 10 minutes for Player 1
player_2_time = 600  # 10 minutes for Player 2
current_player = 1  # Player 1 starts
turn_start_time = pygame.time.get_ticks()
timer = pygame.time.Clock()
fps = 60
timer_x = 850

timer_y_player1 = 20
start_time = pygame.time.get_ticks()  # Initialize start_time here


timer_y_player2 = HEIGHT - 140

turn_step = 0

loading_duration = 2000
start_ticks = pygame.time.get_ticks()
loading_displayed = False


selected_piece = None
selected_location = None
valid_moves = []

# Main game loop
run = True
player_1_time = 600  # 10 minutes for Player 1
player_2_time = 600  # 10 minutes for Player 2
current_player = 1  # Player 1 starts
turn_start_time = pygame.time.get_ticks()

selected_piece = None
selected_location = None
valid_moves = []

while run:
    timer.tick(fps)
    if not loading_displayed:
        loading_screen()
        if pygame.time.get_ticks() - start_time >= loading_duration:
            loading_displayed = True

    # Update elapsed time
    elapsed_ticks = (pygame.time.get_ticks() - turn_start_time) // 1000
    if current_player == 1:
        time_left = max(player_1_time - elapsed_ticks, 0)
    else:
        time_left = max(player_2_time - elapsed_ticks, 0)

    # Check for time out
    if time_left == 0:
        winner = "Black" if current_player == 1 else "White"
        game_over = True

    # Draw the game board and pieces
    screen.fill('dark gray')
    draw_board()
    draw_pieces()
    draw_check()

    # Display the timer
    if current_player == 1:
        text_color = "White"
    else:
        text_color = "Black"
    player_1_timer = font.render(f" {player_1_time // 60}:{player_1_time % 60:02}", True, text_color)
    player_2_timer = font.render(f" {player_2_time // 60}:{player_2_time % 60:02}", True, text_color)

    # Blit the timer texts to the right side of the screen
    screen.blit(player_1_timer, (timer_x, timer_y_player1))  # White timer at top right
    screen.blit(player_2_timer, (timer_x, timer_y_player2))  # Black timer at bottom right

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            x_coord = event.pos[0] // 100
            y_coord = event.pos[1] // 100
            click_coords = (x_coord, y_coord)

            print(f"Clicked on: {click_coords}")

            # Handle piece selection and move
            if current_player == 1:  # White player's turn
                if click_coords in white_locations and selected_piece is None:
                    selection = white_locations.index(click_coords)
                    selected_piece = white_pieces[selection]
                    selected_location = click_coords
                    print(f"Selected White piece: {selected_piece} at {selected_location}")
                    valid_moves = check_valid_moves(selected_piece, selected_location, white_pieces, white_locations, black_pieces, black_locations)
                    print(f"Valid moves: {valid_moves}")
                    turn_step = 1  # White player's turn in progress
                elif click_coords in valid_moves and selected_piece is not None:
                    # Move the selected white piece
                    print(f"Moving White piece to {click_coords}")
                    white_locations[selection] = click_coords
                    # Handle capture
                    if click_coords in black_locations:
                        captured_index = black_locations.index(click_coords)
                        captured_pieces_white.append(black_pieces[captured_index])
                        black_pieces.pop(captured_index)
                        black_locations.pop(captured_index)
                    # Reset for the next move
                    selected_piece = None
                    selected_location = None
                    valid_moves = []
                    current_player = 2  # Switch to black player's turn
                    turn_start_time = pygame.time.get_ticks()

            elif current_player == 2:  # Black player's turn
                if click_coords in black_locations and selected_piece is None:
                    selection = black_locations.index(click_coords)
                    selected_piece = black_pieces[selection]
                    selected_location = click_coords
                    print(f"Selected Black piece: {selected_piece} at {selected_location}")
                    valid_moves = check_valid_moves(selected_piece, selected_location, black_pieces, black_locations, white_pieces, white_locations)
                    print(f"Valid moves: {valid_moves}")
                    turn_step = 2  # Black player's turn in progress
                elif click_coords in valid_moves and selected_piece is not None:
                    # Move the selected black piece
                    print(f"Moving Black piece to {click_coords}")
                    black_locations[selection] = click_coords
                    # Handle capture
                    if click_coords in white_locations:
                        captured_index = white_locations.index(click_coords)
                        captured_pieces_black.append(white_pieces[captured_index])
                        white_pieces.pop(captured_index)
                        white_locations.pop(captured_index)
                    # Reset for the next move
                    selected_piece = None
                    selected_location = None
                    valid_moves = []
                    current_player = 1  # Switch to white player's turn
                    turn_start_time = pygame.time.get_ticks()

        if winner != '':
            game_over = True
            draw_game_over()

    pygame.display.flip()



pygame.quit()



