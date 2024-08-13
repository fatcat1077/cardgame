import socket
import threading
import pickle  # 用于反序列化对象
from card_game import Player  # 导入 Player 类
from expect_value_calculator import evaluate_players  # 导入您提供的计算函数 evaluate_players

# 用来存储所有玩家的 Player 对象
players = []
player_sockets = {}

# 用来同步四个玩家的手牌
lock = threading.Lock()

def handle_client(client_socket, addr):
    try:
        while True:
            # 接收数据
            data = client_socket.recv(4096)  # 调整缓冲区大小以适应较大的对象
            if not data:
                break

            # 反序列化 Player 对象
            try:
                player = pickle.loads(data)
                print(f"Received {player} from {addr}")
            except pickle.PickleError as e:
                print(f"Failed to deserialize data from {addr}: {e}")
                continue

            with lock:
                players.append(player)
                player_sockets[player.player_id] = client_socket

                # 如果已经接收到四个玩家
                if len(players) == 4:
                    # 评估所有玩家
                    results = evaluate_players(players)
                    
                    # 根据评估结果发送响应
                    for player in players:
                        response = "all in" if results[player.player_id] else "fold"
                        player_sockets[player.player_id].send(response.encode('utf-8'))

                    # 清空玩家列表和连接，以便进行下一轮
                    players.clear()
                    player_sockets.clear()

    except Exception as e:
        print(f"Player {addr} disconnected. Error: {e}")
    finally:
        client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 设置 SO_REUSEADDR 选项
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server.bind(('0.0.0.0', 9999))
    server.listen(4)
    print("Server listening on port 9999")

    try:
        while True:
            try:
                server.settimeout(1)  # 设置超时时间为1秒，定期检查中断
                client_socket, addr = server.accept()
            except socket.timeout:
                continue  # 如果超时，继续检查中断信号
            except KeyboardInterrupt:
                print("Keyboard interrupt received, stopping server...")
                break

            print(f"Accepted connection from {addr}")
            client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_handler.daemon = True  # 设置为守护线程
            client_handler.start()

    except KeyboardInterrupt:
        print("Keyboard interrupt received, shutting down server...")
    finally:
        server.close()
        print("Server closed.")

if __name__ == "__main__":
    main()
