import socket
import selectors
import types

class MultiServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.selector = selectors.DefaultSelector()

    def build_non_blocking_websocket(self, host, port):
        server_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
            proto=0,
        )
        server_socket.bind((host,port))
        server_socket.listen(10)
        server_socket.setblocking(False)
        return server_socket

    def accept(self, server_socket):
        client_socket, client_addr = server_socket.accept()
        client_socket.setblocking(False)
        data = types.SimpleNamespace(addr=client_addr, inb=b"", outb=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.selector.register(client_socket, events, data=data)
        print(f"New connection from {client_addr}")

    def recv(self, key: selectors.SelectorKey , mask):
        server_socket: socket.socket = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = server_socket.recv(1024)
            if recv_data:
                data.inb += recv_data
                data.outb += recv_data
                print(recv_data)
            else:
                print(f"Closing connection to {data.addr}")
                self.selector.unregister(server_socket)
                server_socket.close()
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                sent = server_socket.send(data.outb)  # Should be ready to write
                data.outb = data.outb[sent:]

    def run(self):
        server_socket = self.build_non_blocking_websocket(self.host, self.port)
        self.selector.register(server_socket, selectors.EVENT_READ, data=None)
        try:
            while True:
                events = self.selector.select(timeout=30)
                for key, mask in events:
                    if key.data is None:
                        self.accept(key.fileobj)
                    else:
                        self.recv(key, mask)
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")
        finally:
            self.selector.close()


if __name__ == "__main__":
    server = MultiServer("127.0.0.1",34560)
    server.run()