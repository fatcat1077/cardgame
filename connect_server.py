import socketserver
import threading
import pickle  # 用于反序列化对象
from card_game import Player  # 导入 Player 类
from expect_value_calculator import evaluate_players  # 导入计算函数 evaluate_players

# 用来存储所有玩家的 Player 对象
players = []
player_sockets = {}
lock = threading.Lock()
connected_players = 0  # 计数连接的玩家数量

class PlayerHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global players, player_sockets, connected_players

        try:
            with lock:
                connected_players += 1  # 增加连接玩家计数
                player_sockets[self.request] = None  # 记录当前连接的socket

                # 通知玩家等待其他玩家加入
                self.request.sendall(f"已连接到服务器，等待其他玩家加入...".encode('utf-8'))

                # 如果已经有四个玩家连接，通知所有玩家开始游戏
                if connected_players == 4:
                    print(player_sockets.keys())
                    for sock in player_sockets.keys():
                        sock.sendall("所有玩家已连接，开始游戏！".encode('utf-8'))

            while True:
                # 接收数据
                data = self.request.recv(4096)  # 调整缓冲区大小以适应较大的对象
                if not data:
                    raise ConnectionResetError("玩家断开连接")

                # 反序列化 Player 对象
                try:
                    player = pickle.loads(data)
                    print(f"Received {player} from {self.client_address}")

                    # 验证玩家数据是否符合预期
                    if not isinstance(player, Player) or not player.hand:
                        raise ValueError("Invalid player data")

                except (pickle.PickleError, ValueError) as e:
                    print(f"Data error from {self.client_address}: {e}")
                    # 发送错误消息并要求玩家重新输入
                    self.request.sendall("数据错误，请重新发送。".encode('utf-8'))
                    continue

                with lock:
                    players.append(player)
                    player_sockets[self.request] = player

                    # 如果已经接收到四个玩家的卡牌
                    if len(players) == 4:
                        # 评估所有玩家
                        results = evaluate_players(players)
                        
                        # 根据评估结果发送响应
                        for sock, player in player_sockets.items():
                            if player is not None:
                                response = "all in" if results[player.player_id] else "fold"
                                sock.sendall(response.encode('utf-8'))

                        # 清空玩家列表和连接，以便进行下一轮
                        players.clear()
                        for sock in player_sockets.keys():
                            player_sockets[sock] = None

        except ConnectionResetError as e:
            print(f"Player {self.client_address} disconnected. Error: {e}")
            self.handle_player_disconnect()

        except Exception as e:
            print(f"Player {self.client_address} disconnected. Error: {e}")
            self.handle_player_disconnect()

        finally:
            with lock:
                if self.request in player_sockets:
                    del player_sockets[self.request]

    def handle_player_disconnect(self):
        """
        处理玩家断线的情况，通知其他玩家并重置游戏状态。
        """
        global players, player_sockets, connected_players
        with lock:
            print(self.request in player_sockets and player_sockets[self.request])
            if self.request in player_sockets and player_sockets[self.request]:
                disconnected_player_id = player_sockets[self.request].player_id
                # 通知其他玩家有玩家断线
                for sock in player_sockets.keys():
                    #現在跑不進來
                    if sock != self.request and player_sockets[sock] is not None:
                        try:
                            #現在跑不進來
                            sock.sendall(f"Player ID {disconnected_player_id} disconnected just now. Please reconnect again".encode('utf-8'))
                        except Exception as e:
                            print(f"Failed to send disconnect message: {e}")

            # 断开所有连接并重置状态
            for sock in list(player_sockets.keys()):
                try:
                    sock.close()
                except Exception as e:
                    print(f"Failed to close socket: {e}")

            # 重置所有变量
            players.clear()
            player_sockets.clear()
            connected_players = 0  # 确保玩家计数被正确重置

class PlayerServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 9999

    with PlayerServer((HOST, PORT), PlayerHandler) as server:
        print(f"Server listening on port {PORT}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("Keyboard interrupt received, shutting down server...")
        finally:
            server.server_close()
            print("Server closed.")

