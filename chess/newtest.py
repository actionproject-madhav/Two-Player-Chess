def check_valid_moves(piece, location, pieces, locations, enemy_pieces, enemy_locations):

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

# Initialize game wind

# Loading screen function



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





black_options = check_options(black_pieces, black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')
run = True
# Timer variables
player_1_time = 600  # 10 minutes for Player 1
player_2_time = 600  # 10 minutes for Player 2
current_player = 1  # Player 1 starts
turn_start_time = pygame.time.get_ticks()


loading_displayed = False
start_time = pygame.time.get_ticks()  # Initialize start_time here


selected_piece = None
selected_location = None
# Main game loop
# Ensure you reset selected_piece and selected_location after a move
selected_piece = None
selected_location = None
