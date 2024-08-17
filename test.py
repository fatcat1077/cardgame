import tkinter as tk
import socket
import pickle
from threading import Thread
from card_game import Card, Player
from tkinter import simpledialog, messagebox

# 初始化主视窗
root = tk.Tk()
root.title("期望值計算機_4人AOF")

# 提示用户输入IP地址
ip_address = simpledialog.askstring("输入IP地址", "请输入要连接的服务器IP地址：")

# 如果用户取消输入对话框，直接退出程序
if not ip_address:
    messagebox.showwarning("操作取消", "未输入IP地址，程序将退出。")
    root.destroy()
    exit()

# 与服务器连接
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((ip_address, 9999))
except Exception as e:
    messagebox.showerror("连接失败", f"无法连接到服务器: {e}")
    root.destroy()
    exit()

# 变量
selected_cards = []
buttons = []
connection_active = True  # 新增布尔变量，用于追踪连接状态

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

# 向服务器发送手牌的函数，放在一个单独的线程中
def send_hand_to_server(player):
    try:
        # 将 Player 对象序列化并发送到服务器
        data = pickle.dumps(player)
        client.send(data)

        # 显示等待消息（通过主线程执行）
        root.after(0, lambda: result_label.config(text="正在等待其他玩家..."))

        # 接收服务器的最终回应
        result = client.recv(1024).decode('utf-8')
        root.after(0, lambda: result_label.config(text=f"伺服器回應: {result}"))

        # 允许再次输入（通过主线程执行）
        root.after(0, reset_interface)

    except Exception as e:
        root.after(0, lambda: result_label.config(text=f"错误: {e}"))
    finally:
        # 重置送出按钮（通过主线程执行）
        root.after(0, lambda: submit_button.grid(row=5, column=0, columnspan=13, pady=10))

# 当点击送出时触发的事件
def on_submit():
    if len(selected_cards) == 2:
        player_id = player_id_entry.get()
        if not player_id:
            result_label.config(text="請輸入 Player ID。")
            return
        
        player = Player(player_id, selected_cards)

        # 隐藏送出按钮
        submit_button.grid_remove()

        # 启动一个线程来发送手牌并接收服务器的回应
        Thread(target=send_hand_to_server, args=(player,)).start()

        # 重置已选择的卡片
        for button in buttons:
            button.config(bg="SystemButtonFace")
        selected_cards.clear()
    else:
        result_label.config(text="請點選兩張手牌再送出。")

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

# 隐藏的手牌选择控件和提交按钮
def hide_card_controls():
    for button in buttons:
        button.grid_remove()
    submit_button.grid_remove()

# 初始化时隐藏手牌选择控件
hide_card_controls()

# 显示手牌选择控件和提交按钮
def show_card_controls():
    for button in buttons:
        button.grid()
    submit_button.grid()

# 重置界面以允许玩家继续输入
def reset_interface():
    for button in buttons:
        button.config(bg="SystemButtonFace", state=tk.NORMAL)  # 重置按钮状态
    selected_cards.clear()  # 清空已选择的卡片
    submit_button.grid(row=5, column=0, columnspan=13, pady=10)  # 显示送出按钮
    result_label.config(text="")

# 处理断线信息并显示新的窗口
def handle_disconnect(message):
    global connection_active
    connection_active = False  # 更新连接状态为断开
    # 关闭当前窗口
    root.destroy()
    
    # 创建一个新的窗口，显示断线信息
    reconnect_window = tk.Tk()
    reconnect_window.title("断线通知")
    tk.Label(reconnect_window, text=message, padx=20, pady=20).pack()
    tk.Button(reconnect_window, text="确定", command=reconnect_window.destroy).pack(pady=10)
    reconnect_window.mainloop()

# 检查是否所有玩家已连接
def check_player_ready():
    try:
        while connection_active:  # 检查连接状态
            message = client.recv(1024).decode('utf-8')
            if not connection_active:  # 如果连接已经断开，退出循环
                break
            if "Player disconnected" in message:  # 改为检测断线消息的触发条件
                root.after(0, lambda: handle_disconnect(message))
                break
            elif message == "所有玩家已连接，开始游戏！":
                root.after(0, lambda: result_label.config(text="所有玩家已连接，您可以选择手牌并提交。"))
                root.after(0, show_card_controls)  # 显示手牌选择控件
            else:
                root.after(0, lambda: result_label.config(text=message))
    except Exception as e:
        root.after(0, lambda: result_label.config(text=f"错误: {e}"))

# 启动一个线程来等待所有玩家连接
Thread(target=check_player_ready).start()

# 启动主循环
root.mainloop()

# 关闭连接
client.close()
