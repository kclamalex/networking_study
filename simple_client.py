import socket


class SimpleClient:
    def call(self, host: str, port: int):
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
        client_sock.connect((host, port))
        client_sock.sendall(b"hello, world")
        client_sock.shutdown(socket.SHUT_WR)

        chunks = []
        while True:
            try:
                data = client_sock.recv(2048)
                if not data:
                    break
                chunks.append(data)
                print("Received", repr(b"".join(chunks)))
            except KeyboardInterrupt:
                break
        client_sock.close()


if __name__ == "__main__":
    server = SimpleClient()
    server.call("127.0.0.1", 34560)
