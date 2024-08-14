import tkinter as tk
import socket
import pickle
from card_game import Card, Player

# 初始化主视窗
root = tk.Tk()
root.title("扑克牌游戏")

# 变量
selected_cards = []
buttons = []

# 与服务器连接
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9999))

# 当点击牌时触发的事件
def on_card_click(button, card):
    if button["bg"] == "yellow":
        button.config(bg="SystemButtonFace")  # 恢复按钮原状
        selected_cards.remove(card)
    elif len(selected_cards) < 2:
        button.config(bg="yellow")  # 点击效果，改变按钮背景颜色
        selected_cards.append(card)
    
    # 隐藏服务器回应的标签
    result_label.config(text="")

# 当点击送出时触发的事件
def on_submit():
    if len(selected_cards) == 2:
        player_id = player_id_entry.get()
        if not player_id:
            result_label.config(text="请输入 Player ID。")
            return
        
        player = Player(player_id, selected_cards)

        # 将 Player 对象序列化并发送到服务器
        data = pickle.dumps(player)
        client.send(data)

        # 隐藏送出按钮
        submit_button.grid_remove()

        # 接收服务器的回应
        result = client.recv(1024).decode('utf-8')
        result_label.config(text=f"服务器回应: {result}")

        # 重置已选择的卡片
        for button in buttons:
            button.config(bg="SystemButtonFace")
        selected_cards.clear()

        # 显示送出按钮
        submit_button.grid(row=5, column=0, columnspan=13, pady=10)
    else:
        result_label.config(text="请选择两张卡片再送出。")

# 创建玩家ID输入框
tk.Label(root, text="Player ID:").grid(row=0, column=0, columnspan=2, pady=10)
player_id_entry = tk.Entry(root)
player_id_entry.grid(row=0, column=2, columnspan=11)

# 创建扑克牌按钮
def create_card_buttons():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = '23456789TJQKA'
    row = 1

    for suit in suits:
        for i, rank in enumerate(ranks):
            card = Card(suit, rank)
            button = tk.Button(root, text=f"{rank} of {suit}", width=10, height=3)
            button.config(command=lambda b=button, c=card: on_card_click(b, c))
            buttons.append(button)
            button.grid(row=row, column=i, padx=2, pady=2)  # 将按钮放置在指定的网格位置
        row += 1

# 创建扑克牌按钮
create_card_buttons()

# 创建送出按钮并放在第四列下方
submit_button = tk.Button(root, text="送出", command=on_submit)
submit_button.grid(row=5, column=0, columnspan=13, pady=10)  # 将送出按钮放置在第四列的下一列

# 显示服务器回应
result_label = tk.Label(root, text="")
result_label.grid(row=6, column=0, columnspan=13, pady=10)

# 启动主循环
root.mainloop()

# 关闭连接
client.close()
