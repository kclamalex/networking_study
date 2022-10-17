import socket
class SimpleServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def run(self):
        server_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
            proto=0,
        )
        server_socket.bind((self.host,self.port))
        server_socket.listen(10)
        while True:
            try:
                client_socket, client_addr = server_socket.accept()
                print(f"New connection from {client_addr}")
                chunks = []
                while True:
                    data = client_socket.recv(2048)
                    if not data:
                        break
                    chunks.append(data)
                client_socket.sendall(b''.join(chunks))
                client_socket.close()
            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    server = SimpleServer("127.0.0.1",34560)
    server.run()