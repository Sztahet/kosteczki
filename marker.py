class Marker:
    def __init__(self, player_marker, color, x, y, size):
        self.player_marker = player_marker
        self.color = color
        self.x = x
        self.y = y
        self.size = size
        self.default_size = size
        self.is_selected = False

    def select(self, mouse_x, mouse_y):
        if self.x <= mouse_x <= self.x + self.size and self.y <= mouse_y <= self.y + self.size:
            self.is_selected = not self.is_selected
        else:
            self.is_selected = False
        if self.is_selected:
            self.size *= 1.25
        else:
            self.size = self.default_size
    def marker_to_map(self, game_board, board_y, board_x):
        print (board_y,board_x)
        # TODO range of valid board_y,board_x
        game_board[board_y][board_x] = self.player_marker
        if board_y+1 < len(game_board):
            if game_board[board_y+1][board_x] == 'X':
                game_board[board_y+1][board_x] = 'Y'
        if game_board[board_y-1][board_x] == 'X' and board_y > 0:
            game_board[board_y-1][board_x] = 'Y'
        if board_x+1 < len(game_board):
            if game_board[board_y][board_x+1] == 'X':
                game_board[board_y][board_x+1] = 'Y'
        if game_board[board_y][board_x-1] == 'X' and board_x > 0:
            game_board[board_y][board_x-1] = 'Y'
        return game_board