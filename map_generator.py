import random

def generate_map(num_players, num_cols, num_rows,map_size):
    # Create an empty 2D array of squares
    game_board = [['B' for _ in range(num_cols)] for _ in range(num_rows)]
    desired_playable_area = map_size * num_players

    # Helper function to check if a square is within the boundaries of the map
    def is_valid(row, col):
        return 0 <= row < num_rows and 0 <= col < num_cols

    # Start at the middle of the map
    curr_row = int(num_rows/2)
    curr_col = int(num_cols/2)
    game_board[curr_row][curr_col] = 'Y'
    playable_area = 1
    # Use neverending loop var in case if stack in for loop
    neverending_loop = 0
    # Use a random walk to fill connected squares
    while playable_area < desired_playable_area:
        # Generate a random direction
        if neverending_loop >50:
            curr_row = int(num_rows/2)
            curr_col = int(num_cols/2)
            neverending_loop = 0
        direction = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        next_row = curr_row + direction[0]
        next_col = curr_col + direction[1]
        # Check if the next square is within the boundaries and not filled yet
        if is_valid(next_row, next_col) and game_board[next_row][next_col] == 'B':
            curr_row = next_row
            curr_col = next_col
            game_board[curr_row][curr_col] = 'X'
            playable_area += 1
        else: 
            if is_valid(next_row, next_col):
                curr_row = next_row
                curr_col = next_col
            neverending_loop +=1
    return game_board