import tkinter as tk
from PIL import Image, ImageTk
import itertools
from card_game import Player, Card

# 创建主窗口
root = tk.Tk()
root.title("Card Game Interface")
root.geometry("800x600")

# 字典用来保存加载的图片对象以防止被垃圾回收
card_images = {}
selected_images = {}  # 用于保存选中效果的图片

# 列表保存用户选中的两张卡片
selected_cards = []

# 函数：在 GUI 上显示信息
def display_message(message):
    message_label.config(text=message)

# 函数：当用户点击卡片按钮时执行
def on_card_click(suit, rank, button):
    card = (suit, rank)
    
    if card in selected_cards:
        # 如果卡片已经选中，再次点击取消选中
        selected_cards.remove(card)
        button.config(bg="white")  # 恢复原始背景颜色
        display_message(f"Deselected: {suit} {rank}")
    elif len(selected_cards) < 2:
        # 如果卡片未选中且已选中少于两张，添加到选中列表
        selected_cards.append(card)
        button.config(bg="blue")  # 设置选中背景颜色
        display_message(f"Selected: {suit} {rank}")
    else:
        display_message("Already selected two cards.")


# 函数：当用户点击“送出”按钮时执行
def on_submit():
    if len(selected_cards) != 2:
        display_message("Please select exactly two cards.")
        return
    
    player_id = player_id_entry.get()
    if not player_id:
        display_message("Please enter a Player ID.")
        return

    # 将选中的卡片转为Card对象
    hand = [Card(suit, rank) for suit, rank in selected_cards]
    player = Player(player_id, hand)
    print(player)
    display_message(f"Player created: {player}")
    
    # 重置选择
    selected_cards.clear()
    # 重置卡片按钮的图片
    for (suit, rank), button in card_buttons.items():
        button.config(image=card_images[(suit, rank)])

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


# 创建送出按钮
submit_button = tk.Button(root, text="送出", command=on_submit)
submit_button.grid(row=len(suits) + 3, column=0, columnspan=len(ranks), pady=10)

# 启动主循环
root.mainloop()
