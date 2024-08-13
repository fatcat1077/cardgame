import socket
import pickle  # 用于序列化对象
from card_game import Card, Player  # 导入 Card 和 Player 类

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 9999))

    player_id = input("Enter your player ID: ")

    while True:
        hand_input = input("Enter your hand (two cards, e.g., H2 D3): ")
        # 将输入的手牌转换为 Card 对象列表
        hand = []
        for card_str in hand_input.split():
            suit_char = card_str[0]  # 获取花色字符，例如 'H'
            rank = card_str[1:]  # 获取牌面数字，例如 '2'

            # 将花色字符映射到花色名称
            suits = {'H': 'Hearts', 'D': 'Diamonds', 'C': 'Clubs', 'S': 'Spades'}
            suit = suits.get(suit_char.upper())
            if not suit or rank not in Card.VALID_RANKS:
                print(f"Invalid card: {card_str}. Please enter again.")
                continue

            # 创建 Card 对象并添加到手牌列表中
            hand.append(Card(suit, rank))

        if len(hand) != 2:
            print("You must enter exactly two valid cards.")
            continue

        # 创建 Player 对象
        player = Player(player_id, hand)

        # 将 Player 对象序列化并发送到服务器
        data = pickle.dumps(player)
        client.send(data)

        # 接收服务器的响应
        result = client.recv(1024).decode('utf-8')
        print(f"Server response: {result}")

    # 关闭客户端连接
    client.close()

if __name__ == "__main__":
    main()
