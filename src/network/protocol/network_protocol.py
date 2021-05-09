import struct


class NetworkProtocol:
    def __init__(self, sock):
        self.sock = sock

    def send_message(self, message):
        # Prefix each message with a 4-byte length (network byte order)
        message = struct.pack('>I', len(message)) + message
        return self.sock.sendall(message)

    def recv_msg(self):
        # Read message length and unpack it into an integer
        raw_msg_len = self.recvall(4)
        if not raw_msg_len:
            return None
        msg_len = struct.unpack('>I', raw_msg_len)[0]
        # Read the message data
        return self.recvall(msg_len)

    def recvall(self, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = bytearray()
        while len(data) < n:
            packet = self.sock.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data
