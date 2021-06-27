import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 1048


class UDPDataSender:

    def __init__(self, ip_address=UDP_IP, port=UDP_PORT):
        self.ip_address = ip_address
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_message(self, message):
        self.sock.sendto(message.encode('utf_8'), (UDP_IP, UDP_PORT))

