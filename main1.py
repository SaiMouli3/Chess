import chess
import chess.engine
import pygame
import threading
from flask import Flask, render_template, request

app = Flask(__name__)
pygame.init()

# Constants
tile_size = 80
board_size = tile_size * 8
white = (255, 255, 255)
black = (0, 0, 0)

screen = pygame.display.set_mode((board_size, board_size))
pygame.display.set_caption("Chess Game")
piece_images = {}

# Load stockfish
engine = chess.engine.SimpleEngine.popen_uci(r"C:\Users\ADMIN\Downloads\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe")

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

def draw_board():
    for row in range(8):
        for col in range(8):
            color = white if (row + col) % 2 == 0 else black
            pygame.draw.rect(screen, color, pygame.Rect(col * tile_size, row * tile_size, tile_size, tile_size))

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

def run_pygame(game_mode):
    board = chess.Board()
    selected = None
    running = True

    while running and not board.is_game_over():
        draw_board()
        render_pieces(board)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN and board.turn == chess.WHITE:
                x, y = pygame.mouse.get_pos()
                col, row = x // tile_size, 7 - (y // tile_size)
                square = chess.square(col, row)

                if selected is not None:
                    move = chess.Move(selected, square)
                    if move in board.legal_moves:
                        board.push(move)
                        selected = None
                    else:
                        selected = square
                else:
                    if board.piece_at(square) and board.piece_at(square).color == chess.WHITE:
                        selected = square

        if game_mode == "human_vs_ai" and board.turn == chess.BLACK:
            result = engine.play(board, chess.engine.Limit(time=1.0))
            board.push(result.move)

    pygame.quit()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/play", methods=["POST"])
def play():
    mode = request.form.get("mode")
    t = threading.Thread(target=run_pygame, args=(mode,))
    t.start()
    return "Game Started! Check Pygame Window."

if __name__ == "__main__":
    load_pieces()
    app.run(debug=True)
