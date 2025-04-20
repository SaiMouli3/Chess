import sys
import pygame
import chess
import chess.engine

# Initialize Pygame
pygame.init()

# Constants
tile_size = 80
board_size = tile_size * 8
white = (255, 255, 255)
black = (0, 0, 0)
screen = pygame.display.set_mode((board_size, board_size))
pygame.display.set_caption("Chess Game")

# Dictionary to store piece images
piece_images = {}

# Load images of chess pieces
def load_pieces():
    pieces = ["p", "r", "n", "b", "q", "k"]
    colors = ["w", "b"]
    for color in colors:
        for piece in pieces:
            name = f"{color}{piece}.png"
            path = f"images/{name}"
            piece_images[f"{color}{piece}"] = pygame.transform.scale(
                pygame.image.load(path), (tile_size, tile_size)
            )

# Draw the chessboard
def draw_board():
    for row in range(8):
        for col in range(8):
            color = white if (row + col) % 2 == 0 else black
            pygame.draw.rect(screen, color, pygame.Rect(col * tile_size, row * tile_size, tile_size, tile_size))

# Render pieces on the board
def render_pieces(board):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            row = 7 - chess.square_rank(square)
            col = chess.square_file(square)
            color = 'w' if piece.color == chess.WHITE else 'b'
            symbol = piece.symbol().lower()
            img = piece_images.get(f"{color}{symbol}")
            if img:
                screen.blit(img, (col * tile_size, row * tile_size))

# Run the game (Human vs Human or Human vs AI)
def run_game(mode):
    board = chess.Board()
    selected = None
    load_pieces()
    engine = None

    if mode == "human_vs_ai":
        engine = chess.engine.SimpleEngine.popen_uci(
            r"C:\Users\ADMIN\Downloads\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe"
        )

    running = True
    while running and not board.is_game_over():
        draw_board()
        render_pieces(board)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // tile_size
                row = 7 - (y // tile_size)
                square = chess.square(col, row)

                if selected is not None:
                    move = chess.Move(selected, square)
                    if move in board.legal_moves:
                        board.push(move)
                        selected = None
                    else:
                        selected = None  # Deselect if invalid
                else:
                    piece = board.piece_at(square)
                    if piece and piece.color == board.turn:
                        selected = square

        # AI move
        if mode == "human_vs_ai" and board.turn == chess.BLACK:
            result = engine.play(board, chess.engine.Limit(time=1.0))
            board.push(result.move)

    if engine:
        engine.quit()

    pygame.quit()

# Run main
if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "human_vs_human"
    run_game(mode)
