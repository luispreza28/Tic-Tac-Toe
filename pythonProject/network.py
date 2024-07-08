import socket
import threading
import json

# Server configuration
SERVER = '127.0.1.1'  # Listen on all interfaces
PORT = 5555
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# Game state variables
board = [['' for _ in range(3)] for _ in range(3)]
current_player = 'X'
game_over = False
winner = None
players = {}


def handle_client(conn, player):
    global current_player, game_over
    conn.send(player.encode())
    while True:
        try:
            data = conn.recv(1024).decode()
            if data:
                move = json.loads(data)
                board[move['row']][move['col']] = move['symbol']
                check_win()
                current_player = 'O' if current_player == 'X' else 'X'

                update = {
                    'board': board,
                    'current_player': current_player,
                    'game_over': game_over,
                    'winner': winner
                }
                for p_conn in players.values():
                    p_conn.send(json.dumps(update).encode())
        except Exception as e:
            print(f"Error: {e}")
            break
    conn.close()


def check_win():
    global game_over, winner
    winning_combination = [
        [(0, 0), (0, 1), (0, 2)], # first row
        [(1, 0), (1, 1), (1, 2)], # second row
        [(2, 0), (2, 1), (2, 2)], # third row
        [(0, 0), (1, 0), (2, 0)], # first column
        [(0, 1), (1, 1), (2, 1)], # second column
        [(0, 2), (1, 2), (2, 2)], # third column
        [(0, 0), (1, 1), (2, 2)], # diagonal 1
        [(0, 2), (1, 1), (2, 0)]  # diagonal 2
    ]

    for combo in winning_combination:
        if board[combo[0][0]][combo[0][1]] != '' and board[combo[0][0]][combo[0][1]] == board[combo[1][0]][combo[1][1]] == board[combo[2][0]][combo[2][1]]:
            game_over = True
            winner = current_player
            return

    # Check for draw (all cells filled and no winner)
    if all(all(cell != '' for cell in row) for row in board):
        game_over = True



def start_server():
    server.listen(2)
    print(f"Server listening on {SERVER}:{PORT}")

    while True:
        conn, addr = server.accept()
        print(f"Connected to {addr}")

        player = 'X' if len(players) == 0 else 'O'
        players[player] = conn

        thread = threading.Thread(target=handle_client, args=(conn, player))
        thread.start()


if __name__ == '__main__':
    start_server()
