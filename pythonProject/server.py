import socket
import threading
import json
import time

SERVER = "127.0.1.1"  # Replace with your server IP
PORT = 5555

clients = []
symbols = ['X', 'O']
board = [['' for _ in range(3)] for _ in range(3)]
player_turn = 'X'
game_over = False
winner = None
connection_check_interval = 1  # seconds


def broadcast(message):
    message['num_clients'] = len(clients)
    for client in clients:
        try:
            client.send((json.dumps(message) + '\n').encode())
        except socket.error as e:
            print(f"Error sending message to a client: {e}")
            clients.remove(client)


def handle_client(client, symbol):
    global player_turn, game_over, winner

    try:
        client.send((json.dumps({'symbol': symbol, 'num_clients': len(clients)}) + '\n').encode())

        while True:
            data = client.recv(2048).decode()
            if data:
                move = json.loads(data)
                print(f"Received move: {move}")

                if not game_over and board[move['row']][move['col']] == '':
                    board[move['row']][move['col']] = move['symbol']
                    player_turn = 'O' if player_turn == 'X' else 'X'
                    game_over, winner = check_game_over()

                update = {
                    'board': board,
                    'current_player': player_turn,
                    'game_over': game_over,
                    'winner': winner,
                }
                broadcast(update)

                if game_over:
                    time.sleep(3)
                    reset_game()
                    broadcast({
                        'board': board,
                        'current_player': player_turn,
                        'game_over': game_over,
                        'winner': winner
                    })
    except socket.error as e:
        print(f"Client disconnected: {e}")
    finally:
        if client in clients:
            clients.remove(client)
        client.close()


def reset_game():
    global board, player_turn, game_over, winner
    board = [['' for _ in range(3)] for _ in range(3)]
    player_turn = 'X'
    game_over = False
    winner = None


def check_game_over():
    for row in board:
        if row[0] == row[1] == row[2] != '':
            return True, row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != '':
            return True, board[0][col]
    if board[0][0] == board[1][1] == board[2][2] != '':
        return True, board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != '':
        return True, board[0][2]
    if all(board[row][col] != '' for row in range(3) for col in range(3)):
        return True, 'Draw'
    return False, None


def check_connections():
    while True:
        if len(clients) < 2:
            for client in clients:
                try:
                    client.send((json.dumps(
                        {'message': 'Waiting for another player...', 'num_clients': len(clients)}) + '\n').encode())
                except socket.error as e:
                    print(f"Error sending waiting message to client: {e}")
                    clients.remove(client)
        time.sleep(connection_check_interval)


def accept_connections(server):
    while True:
        client, addr = server.accept()
        clients.append(client)
        print(f"Connected to {addr}")

        if len(clients) == 2:
            broadcast({'message': 'Both players are connected. Game starting...'})
            print("Both players are connected. Game starting...")

            for i, client in enumerate(clients):
                threading.Thread(target=handle_client, args=(client, symbols[i]), daemon=True).start()
        else:
            client.send((json.dumps({'message': 'Waiting for another player...', 'num_clients': len(clients)}) + '\n').encode())


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER, PORT))
    server.listen(2)
    print("Server started, waiting for connections...")

    # Start the connection checking thread
    threading.Thread(target=check_connections, daemon=True).start()
    accept_connections(server)


if __name__ == "__main__":
    main()
