import socket
import threading
import select
import signal
import sys
from card_game import Player
import pickle
from expect_value_calculator import evaluate_players

# 全局变量
players = []
player_data = []
lock = threading.Lock()

def handle_client(client_socket, address):
    global players, player_data
    print(f"Player connected from {address}")

    with lock:
        if len(players) >= 4:
            client_socket.sendall("Game already started. Connection refused.".encode('utf-8'))
            client_socket.close()
            return

        players.append(client_socket)
        if len(players) < 4:
            client_socket.sendall("Waiting for other players to connect.".encode('utf-8'))
        else:
            for player_socket in players:
                player_socket.sendall("Game starting!".encode('utf-8'))

    while True:
        try:
            data = client_socket.recv(4096)
            if not data:
                break

            player = pickle.loads(data)
            print(f"Received player data: {player}")

            with lock:
                player_data.append(player)

                if len(player_data) < 4:
                    client_socket.sendall("Waiting for other players to choose cards.".encode('utf-8'))
                else:
                    results = evaluate_players(player_data)

                    # 根据评估结果，将对应的字符串消息发送给每个玩家
                    for p in player_data:
                        player_id = p.player_id
                        decision = results.get(player_id, False)  # 获取该玩家的布尔结果
                        
                        # 根据布尔值发送 "all in" 或 "fold"
                        message = "all in" if decision == True else "fold"
                        player_socket = players[player_data.index(p)]
                        player_socket.sendall(message.encode('utf-8'))

                    # 重置状态准备下一轮
                    player_data.clear()

        except Exception as e:
            print(f"Error: {e}")
            break

    with lock:
        if client_socket in players:
            players.remove(client_socket)
        
        print(f"Player disconnected from {address}")

        #測試用
        #print(players)
        #print(client_socket)

        
        for player in players:
            player.sendall("disconnect".encode('utf-8'))


    client_socket.close()

def signal_handler(sig, frame):
    print("Server is shutting down...")
    with lock:
        for client_socket in players:
            client_socket.close()
    sys.exit(0)

def start_server():
    signal.signal(signal.SIGINT, signal_handler)  # 注册信号处理程序

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9999))
    server.listen(4)
    print("Server started, waiting for players...")

    while True:
        try:
            # 使用 select 等待 server 套接字或 sys.stdin 的输入
            readable, _, _ = select.select([server], [], [], 1)

            if server in readable:
                client_socket, addr = server.accept()
                client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
                client_thread.start()

        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    start_server()
