import argparse
import socket
import time
import uuid
import threading


class TaskQueue:

    def __init__(self, task_params):
        self._queue = task_params[0]
        self._length = task_params[1]
        self._data = task_params[2]
        self._id = str(uuid.uuid1())
        self._status = False
        self._timer: threading.Timer

    @property
    def id(self):
        return self._id

    @property
    def queue(self):
        return self._queue

    @property
    def length(self):
        return self._length

    @property
    def data(self):
        return self._data

    def show_status(self):
        print(f'{self.id} is over')
        self._status = False

    def ack(self):
        if self._status == True:
            self._timer.cancel()
            self._status = False
            return 'YES'
        return 'NO'

    def get(self):
        self._status = True
        self._timer = threading.Timer(10.0, self.show_status)
        self._timer.start()
        return f'{self.id} {self.length} {self.data}'

    @classmethod
    def check_in(cls, queue, id, dict_tasks):
        return 'YES' if dict_tasks.get(queue) is not None and dict_tasks[queue].id == id else 'NO'


class TaskQueueServer:

    def __init__(self, ip, port, path, timeout):
        self._path = path
        self._timeout = timeout
        self._ip = ip
        self._port = port
        self._dict_tasks = {}

    def get_task(self, task: TaskQueue):
        print(f'{task.id} is over')

    def _get_command(self, command_str):
        command_list = command_str.decode('utf-8').split()
        if command_list[0] == 'ADD':
            new_task = TaskQueue(command_list[1:])
            self._dict_tasks[new_task.queue] = new_task
            return new_task.id
        if command_list[0] == 'IN':
            return TaskQueue.check_in(command_list[1], command_list[2], self._dict_tasks)
        if command_list[0] == 'SAVE':
            return ' '.join(command_list[1:])
        task = self._dict_tasks.get(command_list[1], 'NONE')
        if command_list[0] == 'GET':
            return task.get() if task != 'NONE' else task
        if command_list[0] == 'ACK':
            return task.ack() if task != 'NONE' else task
        return 'ERROR\n'

    def run(self):
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # connection.bind((self._ip, self._port))
        connection.bind(('127.0.0.1', 1234))
        connection.listen(10)
        full_msg = b''
        while True:
            current_connection, address = connection.accept()
            current_connection.recv(21)
            while True:
                data = current_connection.recv(1000000)
                full_msg += data
                if full_msg.find(b'\xff\xf8') > -1:
                    current_connection.shutdown(1)
                    current_connection.close()
                    full_msg = b''
                    break
                elif full_msg.endswith(b'\r\n'):
                    print(len(full_msg))
                    print(full_msg)
                    current_connection.send(self._get_command(full_msg).encode())
                    current_connection.send('\n\r'.encode())
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
