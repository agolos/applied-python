import argparse
import socket
import time


class TaskQueueServer:

    def __init__(self, ip, port, path, timeout):
        self._path = path
        self._timeout = timeout
        self._ip = ip
        self._port = port

    @property
    def ip(self):
        return self._ip

    @property
    def port(self):
        return self._port

    @property
    def path(self):
        return self._path

    @property
    def timeout(self):
        return self._timeout

    @ip.setter
    def ip(self, value):
        self._ip = value

    @port.setter
    def port(self, value):
        self._port = value

    @path.setter
    def path(self, value):
        self._path = value

    @timeout.setter
    def timeout(self, value):
        self._timeout

    @classmethod
    def _get_command(csl, command_str):
        try:
            command_list = command_str.decode('utf-8').split()
        except UnicodeDecodeError:
            return ''
        if command_list[0] == 'ADD':
            return ' '.join(command_list[1:])
        if command_list[0] == 'GET':
            return ' '.join(command_list[1:])
        if command_list[0] == 'ACK':
            return ' '.join(command_list[1:])
        if command_list[0] == 'IN':
            return ' '.join(command_list[1:])
        if command_list[0] == 'SAVE':
            return ' '.join(command_list[1:])
        return 'invalid command\n'

    def run(self):
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        connection.bind(('127.0.0.1', 1234))
        connection.listen(10)
        full_msg = b''
        while True:
            current_connection, address = connection.accept()
            while True:
                data = current_connection.recv(2048)
                full_msg += data
                if full_msg.find(b'\xff\xf8') > -1:
                    current_connection.shutdown(1)
                    current_connection.close()
                    full_msg = b''
                    break
                elif full_msg.endswith(b'\r\n'):
                    current_connection.send(TaskQueueServer._get_command(full_msg).encode())
                    full_msg = b''



def parse_args():
    parser = argparse.ArgumentParser(description='This is a simple task queue server with custom protocol')
    parser.add_argument(
        '-p',
        action="store",
        dest="port",
        type=int,
        default=5555,
        help='Server port')
    parser.add_argument(
        '-i',
        action="store",
        dest="ip",
        type=str,
        default='0.0.0.0',
        help='Server ip adress')
    parser.add_argument(
        '-c',
        action="store",
        dest="path",
        type=str,
        default='./',
        help='Server checkpoints dir')
    parser.add_argument(
        '-t',
        action="store",
        dest="timeout",
        type=int,
        default=300,
        help='Task maximum GET timeout in seconds')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    server = TaskQueueServer(**args.__dict__)
    server.run()
