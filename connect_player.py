import socket
import threading
import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk
import pickle
from card_game import Player, Card

client_socket = None

def listen_for_server_messages(client_socket):
    try:
        enable_card_selection()
        while True:
            message = client_socket.recv(4096)
            if not message:
                break

            # 假设服务器发送的是字符串，直接显示
            display_message(message.decode('utf-8'))
            if message.decode('utf-8')=="disconnect":
                root.destroy()
            if message.decode('utf-8')=="all in" or message.decode('utf-8')=="fold":
                enable_card_selection()  # 重置并允许玩家再次选择手牌
    except Exception as e:
        display_message(f"Connection error: {e}")
    finally:
        client_socket.close()

def connect_to_server():
    global client_socket

    if client_socket is not None:
        display_message("Already connected to server.")
        return

    ip_address = simpledialog.askstring("Input", "Enter Server IP Address:", parent=root)
    if not ip_address:
        return

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip_address, 9999))

        listen_thread = threading.Thread(target=listen_for_server_messages, args=(client_socket,))
        listen_thread.daemon = True
        listen_thread.start()
    except Exception as e:
        display_message(f"Failed to connect to server: {e}")
        client_socket = None

def enable_card_selection():
    submit_button.config(state=tk.NORMAL)
    for button in card_buttons.values():
        button.config(state=tk.NORMAL)

def disable_card_selection():
    submit_button.config(state=tk.DISABLED)
    for button in card_buttons.values():
        button.config(state=tk.DISABLED)

def display_message(message):
    message_label.config(text=message)

def on_card_click(suit, rank, button):

    card = (suit, rank)
    if card in selected_cards:
        selected_cards.remove(card)
        button.config(bg="white")
        display_message(f"Deselected: {suit} {rank}")
    elif len(selected_cards) < 2:
        selected_cards.append(card)
        button.config(bg="blue")
        display_message(f"Selected: {suit} {rank}")
    else:
        display_message("Already selected two cards.")

def on_submit():
    if len(selected_cards) != 2:
        display_message("Please select exactly two cards.")
        return

    player_id = player_id_entry.get()
    if not player_id:
        display_message("Please enter a Player ID.")
        return

    hand = [Card(suit, rank) for suit, rank in selected_cards]
    player = Player(player_id, hand)
    
    data = pickle.dumps(player)
    try:
        client_socket.sendall(data)
        display_message(f"Player data sent: {player}")
        disable_card_selection()

        # 清除已选择的手牌并恢复背景颜色
        for suit, rank in selected_cards:
            card_buttons[(suit, rank)].config(bg="white")  # 恢复背景颜色
        selected_cards.clear()  # 清除选中的卡片列表

    except Exception as e:
        display_message(f"Failed to send player data: {e}")


def on_close():
    if client_socket:
        try:
            client_socket.close()
        except:
            pass
    root.destroy()

# 创建主窗口
root = tk.Tk()
root.title("Card Game Interface")
root.geometry("800x600")

root.protocol("WM_DELETE_WINDOW", on_close)  # 窗口关闭时执行

# 字典用来保存加载的图片对象以防止被垃圾回收
card_images = {}

# 列表保存用户选中的两张卡片
selected_cards = []

# 创建PlayerID的标签和输入框
player_id_label = tk.Label(root, text="Player ID:")
player_id_label.grid(row=0, column=0, columnspan=2)
player_id_entry = tk.Entry(root)
player_id_entry.grid(row=0, column=2, columnspan=2)

# 用于显示消息的标签
message_label = tk.Label(root, text="")
message_label.grid(row=1, column=0, columnspan=13, pady=10)

# 创建卡片按钮
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = '23456789TJQKA'
card_buttons = {}

# 创建卡片按钮
for i, suit in enumerate(suits):
    for j, rank in enumerate(ranks):
        image_path = f"images/{suit}_{rank}.png"
        try:
            image = Image.open(image_path)
            image = image.resize((80, 120), Image.LANCZOS)
            card_image = ImageTk.PhotoImage(image)
            card_images[(suit, rank)] = card_image
            
            # 创建按钮，初始没有加深的边框
            card_button = tk.Button(root, image=card_images[(suit, rank)],
                                    highlightbackground="black", highlightthickness=0)
            
            # 绑定事件时捕获card_button
            card_button.config(command=lambda s=suit, r=rank, b=card_button: on_card_click(s, r, b))
            
            card_button.grid(row=i + 2, column=j, padx=2, pady=2)
            card_buttons[(suit, rank)] = card_button  # 将按钮保存到字典中
        except Exception as e:
            display_message(f"Error loading image {image_path}: {e}")

# 创建送出按钮
submit_button = tk.Button(root, text="送出", command=on_submit)
submit_button.grid(row=len(suits) + 3, column=0, columnspan=len(ranks), pady=10)
disable_card_selection()  # 默认禁用手牌选择，直到游戏开始

# 启动主循环
connect_to_server()  # 启动时连接服务器
root.mainloop()
