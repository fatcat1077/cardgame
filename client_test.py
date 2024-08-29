import socket

# 建立客戶端 Socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

# 發送訊息並接收回應
while True:
    message = input("請輸入要發送的訊息（輸入 'exit' 結束連線）: ")
    if message == 'exit':
        break
    client_socket.send(message.encode('utf-8'))
    response = client_socket.recv(1024).decode('utf-8')
    print(f"收到伺服器的回應: {response}")

# 關閉連接
client_socket.close()
