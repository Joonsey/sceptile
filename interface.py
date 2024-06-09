from enum import StrEnum, auto

import threading
import zmq

SEPERATOR = "^:!"

class ComTypes(StrEnum):
    PREDICT = auto()
    HEALTH = auto()
    RESULT = auto()
    ERROR = auto()


class SceptileInterface:
    """
    This interface is supposed to be used by external programs

    all features intended to be public to other programs should go through this interface
    """
    def __init__(self, server_address: str = "localhost"):
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect(f"tcp://{server_address}:5555")

    def _send(self, prefix: ComTypes, message: str) -> None:
        self.socket.send(f"{prefix}{SEPERATOR}{message}".encode())

    def _recv(self) -> tuple[str, str]:
        message = self.socket.recv()
        print(f'got message: {message}')
        sign, message = message.decode().split(SEPERATOR)
        return sign, message

    def predict(self, image: str) -> tuple[str, str]:
        self._send(ComTypes.PREDICT, image)
        return self._recv()

    def health_check(self) -> bool:
        self._send(ComTypes.HEALTH, "")
        sign, _ = self._recv()
        return sign == ComTypes.HEALTH

if __name__ == "__main__":
    client = SceptileInterface()
    r = client.predict("https://www.researchgate.net/publication/348605076/figure/fig1/AS:1022470203117574@1620787301403/The-three-Sample-leaves-of-potato-are-a-leaf-affected-by-Light-Blight-b-leaf.jpg")
    print(r)
