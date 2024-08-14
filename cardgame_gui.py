import tkinter as tk

# 初始化主視窗
root = tk.Tk()
root.title("撲克牌遊戲")

# 變數
selected_cards = []
buttons = []

# 當點擊牌時觸發的事件
def on_card_click(button):
    if button["bg"] == "yellow":
        button.config(bg="SystemButtonFace")  # 恢復按鈕原狀
        selected_cards.remove(button)
    elif len(selected_cards) < 2:
        button.config(bg="yellow")  # 點擊效果，改變按鈕背景顏色
        selected_cards.append(button)

# 當點擊送出時觸發的事件
def on_submit():
    if len(selected_cards) == 2:
        for button in selected_cards:
            button.config(bg="SystemButtonFace")  # 恢復按鈕原狀
        selected_cards.clear()

        # 隱藏送出按鈕5秒鐘
        submit_button.grid_remove()
        root.after(5000, lambda: submit_button.grid(row=4, column=0, columnspan=13, pady=10))

# 創建撲克牌按鈕
def create_card_buttons():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = '23456789TJQKA'
    row = 0

    for suit in suits:
        for i, rank in enumerate(ranks):
            card = f"{rank} of {suit}"
            button = tk.Button(root, text=card, width=10, height=3)
            button.config(command=lambda b=button: on_card_click(b))
            buttons.append(button)
            button.grid(row=row, column=i, padx=2, pady=2)  # 將按鈕放置在指定的網格位置
        row += 1

# 創建撲克牌按鈕
create_card_buttons()

# 創建送出按鈕並放在第四列下方
submit_button = tk.Button(root, text="送出", command=on_submit)
submit_button.grid(row=4, column=0, columnspan=13, pady=10)  # 將送出按鈕放置在第四列的下一列

# 啟動主迴圈
root.mainloop()
