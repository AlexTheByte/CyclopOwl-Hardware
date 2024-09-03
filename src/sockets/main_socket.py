from socket_handlers.socket_client_handler_interface import SocketClientHandlerInterface
import logging
import socket

logger = logging.getLogger('MainSocket')


class MainSocket:
    def __init__(self, host: str, port: int, client_handler: SocketClientHandlerInterface) -> None:
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind((host, port))
        self._socket.listen()
        self._socket_client_handler = client_handler
        self._is_running = True

    def listen(self) -> None:
        while self._is_running:
            try:
                conn, addr = self._socket.accept()
                logger.info("Client connected : %s", addr)

                with conn:
                    self._socket_client_handler.handle(conn, addr)

            except (BrokenPipeError, ConnectionResetError):
                logger.info("Client disconnected : %s", addr)

    def stop(self) -> None:
        # self._socket.shutdown(socket.SHUT_RDWR)
        self._is_running = False
        self._socket.close()
        self._socket.detach()
