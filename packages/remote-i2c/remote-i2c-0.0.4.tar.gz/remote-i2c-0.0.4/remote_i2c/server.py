import socket
import struct
from smbus2 import SMBus
from .commands import Commands


class RemoteI2CServer:

    def __init__(self, i2c_bus_number=1, host='', port=5446):
        self._i2c_bus_number = i2c_bus_number
        self._host = host
        self._port = port
        self._on_client = None
    
    def __str__(self):
        return f"<RemoteI2CServer i2cbus={self._i2c_bus_number} host='{self._host}' port={self._port}>"

    def on_client(self, func):
        self._on_client = func
    
    def serve(self):
        bus = SMBus(1)
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self._host, self._port))
        server.listen(1)
        while True:
            client, remote_address = server.accept()
            if self._on_client:
                self._on_client(client, remote_address)
            while True:
                data = client.recv(1)
                if not data:
                    break
                command = data[0]
                response = self.CommandMap[command](self, bus, client)
                if response is not None:
                    client.sendall(response)
    
    def _read_byte(self, bus, client):
        addr, = client.recv(1)
        value = bus.read_byte(addr)
        return bytes([value])

    def _write_byte(self, bus, client):
        addr, value = client.recv(2)
        bus.write_byte(addr, data)
    
    def _read_byte_data(self, bus, client):
        addr, register = client.recv(2)
        value = bus.read_byte_data(addr, register)
        return bytes([value])
    
    def _write_byte_data(self, bus, client):
        addr, register, value = client.recv(3)
        bus.write_byte_data(addr, register, value)
    
    def _read_word_data(self, bus, client):
        addr, register = client.recv(2)
        value = bus.read_word_data(addr, register)
        return struct.pack('>h', value)

    def _write_word_data(self, bus, client):
        addr, register = client.recv(2)
        value = struct.unpack('>h', *client.recv(2))[0]
        bus.write_word_data(addr, register, value)
    
    def _read_i2c_block_data(self, bus, client):
        addr, register, count = client.recv(3)
        block = bus.read_i2c_block_data(addr, register, count)
        return bytes(block)

    def _write_i2c_block_data(self, bus, client):
        addr, register, count = client.recv(3)
        block = client.recv(count)
        bus.write_i2c_block_data(addr, register, block)

    CommandMap = {
        Commands.ReadByte: _read_byte,
        Commands.WriteByte: _write_byte,
        Commands.ReadByteData: _read_byte_data,
        Commands.WriteByteData: _write_byte_data,
        Commands.ReadWordData: _read_word_data,
        Commands.WriteWordData: _write_word_data,
        Commands.ReadI2CBlockData: _read_i2c_block_data,
        Commands.WriteI2CBlockData: _write_i2c_block_data,
    }
