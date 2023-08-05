from types import coroutine
from collections import deque
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE


@coroutine
def read_wait(sock):
    yield 'read_wait', sock


@coroutine
def write_wait(sock):
    yield 'write_wait', sock


class EventLoop:

    def __init__(self):
        self.ready = deque()
        self.selector = DefaultSelector()
        self.processes = []

    async def sock_recv(self, sock):
        await read_wait(sock)
        return sock.recv()

    async def sock_accept(self, sock):
        await read_wait(sock)
        return sock.accept()

    async def sock_sendall(self, sock, data):
        try:
            return sock.send_all(data)
        except BlockingIOError:
            await write_wait(sock)

    def read_wait(self, sock):
        self.selector.register(sock, EVENT_READ, self.current_task)

    def write_wait(self, sock):
        self.selector.register(sock, EVENT_WRITE, self.current_task)

    def create_task(self, coro):
        self.ready.append(coro)

    def run_forever(self):
        for p in self.processes:
            p.start()

        while True:
            while not self.ready:
                try:
                    events = self.selector.select()
                except OSError:
                    continue
                for key, _ in events:
                    self.ready.append(key.data)
                    self.selector.unregister(key.fileobj)

            while self.ready:
                self.current_task = self.ready.popleft()
                try:
                    # Run the generator to the yield
                    op, *args = self.current_task.send(None)

                    # Run the task -> e.g getattr(self, sock_recv)()
                    getattr(self, op)(*args)  # Sneaky method call
                except StopIteration:
                    continue


class GenericEventLoop(EventLoop):
    """Pluggable event loop for use with regular sockets
    Compatible with asyncio's event loop
    """
    async def sock_recv(self, sock, buflen):
        await read_wait(sock)
        return sock.recv(buflen)

    async def sock_accept(self, sock):
        await read_wait(sock)
        return sock.accept()

    async def sock_sendall(self, sock, data):
        try:
            return sock.send(data)
        except BlockingIOError:
            await write_wait(sock)
        except (ConnectionAbortedError, ConnectionResetError):
            pass
