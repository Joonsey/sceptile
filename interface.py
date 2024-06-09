import zmq


class SceptileInterface:
    """
    This interface is supposed to be used by external programs

    all features intended to be public to other programs should go through this interface
    """
    def __init__(self, server_address: str = "localhost"):
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect(f"tcp://{server_address}:5555")

    def predict(self, image: str) -> str:
        self.socket.send(image.encode())
        messsage = self.socket.recv()
        return messsage.decode()

if __name__ == "__main__":
    client = SceptileInterface()
    r = client.predict("https://cdn.discordapp.com/attachments/399649647116812308/1249112578391543819/large-leaved-lime-leaves-npl-01128259-philippe-clement-og.png?ex=6666c6fe&is=6665757e&hm=e8d30cbcc03ad27f7cbbce9450480860606b872147c1801aeea29485ad9a0677&")
    print(r)
