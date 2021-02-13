import socketserver
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Tuple, Callable


class Server(HTTPServer):

    def __init__(self, server_address: Tuple[str, int], RequestHandlerClass: Callable[..., BaseHTTPRequestHandler]):
        super().__init__(server_address, RequestHandlerClass)
        print(f"Сервер запущен по адресу: {self.server_address}")
        self.serve_forever()

    def __del__(self):
        self.shutdown()
        print(f"Сервер остановлен")

class RequestHandler(BaseHTTPRequestHandler):

    def __init__(self, request: bytes, client_address: Tuple[str, int], server: socketserver.BaseServer):
        super().__init__(request, client_address, server)

    def do_POST(self):
        print("Вызван метод: POST")
        headers = [{item[0]: item[1]} for item in self.headers.items()]

        print(f"Клиенту: {self.client_address} отправлены заголовки {headers}")
        self.send_response(201, headers)
        self.end_headers()


if __name__ == '__main__':
    server = Server(("0.0.0.0", 7777), RequestHandler)