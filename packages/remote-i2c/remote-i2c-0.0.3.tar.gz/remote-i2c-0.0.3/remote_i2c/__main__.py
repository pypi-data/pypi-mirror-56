import argparse
from .server import RemoteI2CServer

server = RemoteI2CServer()
server.on_client(lambda client, remote_address: print('Accepting connection from', remote_address))
print('Starting Remote I2C Server', server)
server.serve()
