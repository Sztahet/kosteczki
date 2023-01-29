import math

def scoring_function(size):
    return round((size/5) * size)

def calculate_score(game_board, player_id):
    """Calculate the score for a player given the game board and their marker ID.
    
    Arguments:
        game_board (list of lists of ints): A 2D array representing the game board.
        player_id (int): The ID of the player whose score is being calculated.
        
    Returns:
        int: The calculated score for the player.
    """
    score = 0
    visited = set()
     # DFS function to traverse the game board
    def dfs(i, j):
        if (i, j) in visited:
            return
        visited.add((i, j))
        if game_board[i][j] != player_id:
            return

        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < len(game_board) and 0 <= nj < len(game_board[0]):
                dfs(ni, nj)
    # Loop through the game board
    for i in range(len(game_board)):
        for j in range(len(game_board[0])):
            if (i, j) not in visited and game_board[i][j] == player_id:
                island_size  = 0
                stack = [(i, j)]
                while stack:
                    x, y = stack.pop()
                    if (x, y) in visited:
                        continue
                    visited.add((x, y))
                    if game_board[x][y] == player_id:
                        island_size  += 1
                        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            ni, nj = x + di, y + dj
                            if (0 <= ni < len(game_board) and 0 <= nj < len(game_board[0])
                                and game_board[ni][nj] == player_id):
                                stack.append((ni, nj))
                score += scoring_function(island_size)

    return score