from socket import socket, SOL_SOCKET, SO_REUSEADDR
from .sslsocket import ServerSocket, UPiServerSocket


class ServerFactory:
    """
    A factory of asyncronous sockets.
    @loop: An event loop for handling sockets
    @context: An ssl context. If None, we do not use ssl
    @header_length: Message header length

    You need to call start_server to create these coroutine tasks
    Usage:

    from eclinicio import ServerFactory, EventLoop
    import ssl

    async def mycall_back(loop, ssl_client):
        with client:
            while True:
                data = await loop.sock_recv(ssl_client)
                ...
                reply = {
                    "name": "Dr. Abiira Nathan",
                    "age": "30",
                    "sex": "Male"
                }

                await loop.sock_sendall(reply)

    loop= EventLoop()
    ssl_context = ssl.create_default_context(purpuse=ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile=..., keyfile=...)

    factory = ServerFactory(loop, ssl_context)

    loop.create_task(factory.start_server(('0.0.0.0', 8000), mycall_back))
    loop.run_forever()

    """

    def __init__(self, loop, ssl_context=None, header_length=10):
        self.loop = loop
        self.context = ssl_context
        self.HL = header_length

    async def start_server(self, address, client_callback, addr_req=False,
                           pickle_data=True):

        """
        Create a server and pass it a coroutine to be called.

        Handle message sending and receiving yourself in th callback
        Run help(clinicio.ServerFactory) for details
        @param: address : socket addr to run the server on
        @param: client_callback: A coroutine call back function
                Should have three arguments(loop, client_socket, ipaddress)
                ipaddress is only passed to the callback if addr_req == True
        @param:
            pickle_data: If True, will pickle data before sending using ServerSocket
            else: Will use UPiServerSocket which does not unpickle data.
        """
        server_socket = socket()
        server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        server_socket.bind(address)
        server_socket.listen(5)

        while True:
            client_socket, client_address = await self.loop.sock_accept(server_socket)
            try:
                if pickle_data:
                    ssl_client = ServerSocket(client_socket, self.context, self.HL)
                else:
                    ssl_client = UPiServerSocket(client_socket, self.context, self.HL)
            except IOError:
                client_socket.close()
                continue

            if addr_req is True:
                self.loop.create_task(client_callback(self.loop, ssl_client, client_address))
            else:
                self.loop.create_task(client_callback(self.loop, ssl_client))
