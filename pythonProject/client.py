import pygame
import socket
import json
import sys
import select
import time
from enum import Enum

# Constants
SERVER = "127.0.1.1"  # Replace with your server IP
PORT = 5555
WIDTH, HEIGHT = 600, 600
WHITE = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
END_GAME_COLOR = (0, 0, 255)
DELAY_BEFORE_RESET = 3
GRID_SIZE = 3
GRID_LINE_WIDTH = 10
CELL_PADDING = 50
SYMBOL_SIZE = WIDTH // 6 - 30

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')

# Global variables
board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
player_turn = 'X'
game_over = False
winner = None
waiting_for_player = True
my_symbol = None
num_clients = 0
recv_buffer = ''

# Add music
pygame.mixer.init()

pygame.mixer.music.load('goofy_main_menu_music.mp3')
pygame.mixer.music.play(loops=-1)

# Game state
class GameState(Enum):
    MAIN_MENU = 1
    SINGLE_PLAYER = 2
    MULTIPLAYER = 3


game_state = GameState.MAIN_MENU


def draw_lines():
    for i in range(1, GRID_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT // GRID_SIZE * i), (WIDTH, HEIGHT // GRID_SIZE * i), GRID_LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH // GRID_SIZE * i, 0), (WIDTH // GRID_SIZE * i, HEIGHT), GRID_LINE_WIDTH)


def draw_symbols():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            symbol = board[row][col]
            if symbol == 'X':
                pygame.draw.line(screen, LINE_COLOR, (col * WIDTH // GRID_SIZE + CELL_PADDING, row * HEIGHT // GRID_SIZE + CELL_PADDING),
                                 (col * WIDTH // GRID_SIZE + WIDTH // GRID_SIZE - CELL_PADDING, row * HEIGHT // GRID_SIZE + HEIGHT // GRID_SIZE - CELL_PADDING), GRID_LINE_WIDTH)
                pygame.draw.line(screen, LINE_COLOR, (col * WIDTH // GRID_SIZE + WIDTH // GRID_SIZE - CELL_PADDING, row * HEIGHT // GRID_SIZE + CELL_PADDING),
                                 (col * WIDTH // GRID_SIZE + CELL_PADDING, row * HEIGHT // GRID_SIZE + HEIGHT // GRID_SIZE - CELL_PADDING), GRID_LINE_WIDTH)
            elif symbol == 'O':
                pygame.draw.circle(screen, LINE_COLOR, (col * WIDTH // GRID_SIZE + WIDTH // 6, row * HEIGHT // GRID_SIZE + HEIGHT // 6), SYMBOL_SIZE, GRID_LINE_WIDTH)


def draw_board():
    screen.fill(WHITE)
    draw_lines()
    draw_symbols()


def draw_waiting_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 50)
    text = font.render("Waiting for another player...", True, LINE_COLOR)
    screen.blit(text, (WIDTH // 10, HEIGHT // 2))


def send_move(row, col, symbol):
    move = {'row': row, 'col': col, 'symbol': symbol}
    try:
        client_socket.send(json.dumps(move).encode())
    except socket.error as e:
        print(f"Error sending move: {e}")


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and not waiting_for_player and not game_over and player_turn == my_symbol:
            x, y = pygame.mouse.get_pos()
            row, col = y // (HEIGHT // GRID_SIZE), x // (WIDTH // GRID_SIZE)
            if board[row][col] == '':
                send_move(row, col, player_turn)


def receive_update():
    global board, player_turn, game_over, winner, waiting_for_player, my_symbol, recv_buffer, num_clients
    try:
        ready = select.select([client_socket], [], [], 0.1)
        if ready[0]:
            data = client_socket.recv(2048).decode()
            recv_buffer += data
            while '\n' in recv_buffer:
                message, recv_buffer = recv_buffer.split('\n', 1)
                if message:
                    process_data(message)
    except socket.error as e:
        print(f"Error receiving update: {e}")


def process_data(message):
    global board, player_turn, game_over, winner, waiting_for_player, my_symbol, num_clients
    try:
        update = json.loads(message)
        if 'symbol' in update:
            my_symbol = update['symbol']
        if 'num_clients' in update:
            num_clients = update['num_clients']
            waiting_for_player = num_clients < 2
        if 'message' in update:
            handle_message(update['message'])
        if 'board' in update:
            board = update['board']
            player_turn = update['current_player']
            game_over = update['game_over']
            winner = update['winner']
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")


def handle_message(message):
    global waiting_for_player
    if 'Waiting for another player...' in message:
        waiting_for_player = True
    elif 'Both players are connected. Game starting...' in message:
        waiting_for_player = False


def reset_game():
    global board, player_turn, game_over, winner
    board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    player_turn = 'X'
    game_over = False
    winner = None


def handle_game_over():
    font = pygame.font.Font(None, 50)
    screen.fill(WHITE)
    if winner == 'Draw':
        text = font.render("No contest!", True, END_GAME_COLOR)
    elif my_symbol == winner:
        text = font.render(f"YOU WON!", True, END_GAME_COLOR)
    else:
        text = font.render(f"YOU LOST!", True, END_GAME_COLOR)
    screen.blit(text, (WIDTH // 4, HEIGHT // 2))
    pygame.display.update()
    time.sleep(DELAY_BEFORE_RESET)
    reset_game()
    waiting_for_player = num_clients < 2


def draw_main_menu():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 50)
    text = font.render("Tic-Tac-Toe", True, LINE_COLOR)
    screen.blit(text, (WIDTH // 4, HEIGHT // 4))
    single_player_text = font.render("1. Single Player", True, LINE_COLOR)
    screen.blit(single_player_text, (WIDTH // 4, HEIGHT // 2))
    multiplayer_text = font.render("2. Multiplayer", True, LINE_COLOR)
    screen.blit(multiplayer_text, (WIDTH // 4, HEIGHT // 2 + 60))


def handle_main_menu_events():
    global game_state
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                game_state = GameState.SINGLE_PLAYER
            elif event.key == pygame.K_2:
                game_state = GameState.MULTIPLAYER


def handle_single_player_events():
    pass


def main():
    global waiting_for_player, game_over, game_state
    draw_board()

    while True:
        if game_state == GameState.MAIN_MENU:
            draw_main_menu()
            handle_main_menu_events()
        elif game_state == GameState.SINGLE_PLAYER:
            draw_board()
            handle_single_player_events()
        elif game_state == GameState.MULTIPLAYER:
            handle_events()
            if waiting_for_player:
                draw_waiting_screen()
            else:
                draw_board()
            receive_update()
            if game_over:
                handle_game_over()
        pygame.display.update()

if __name__ == '__main__':
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER, PORT))
        initial_data = client_socket.recv(2048).decode()
        initial_json = json.loads(initial_data)
        my_symbol = initial_json.get('symbol', None)
        num_clients = initial_json.get('num_clients', 0)
        print(f"Connected to server, assigned symbol: {my_symbol}, number of clients: {num_clients}")
    except socket.error as e:
        print(f"Error connecting to server: {e}")
        sys.exit()
    main()
