import socket

# 建立伺服器 Socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(1)
print("伺服器已啟動，等待客戶端連接...")

# 接受客戶端連接
client_socket, client_address = server_socket.accept()
print(f"客戶端 {client_address} 已連接")

# 接收並回傳資料
while True:
    data = client_socket.recv(1024).decode('utf-8')
    if not data:
        break
    print(f"收到客戶端的訊息: {data}")
    response = f"伺服器回應: {data}"
    client_socket.send(response.encode('utf-8'))

# 關閉連接
client_socket.close()
server_socket.close()
