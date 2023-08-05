import socket
import struct

from .commands import Commands


class RemoteI2CClient:
    def __init__(self, remote_host, remote_port=5446):
        self._remote_host = remote_host
        self._remote_port = remote_port
        self._server = None
    
    def connect(self):
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.connect((self._remote_host, self._remote_port))
    
    def disconnect(self):
        self._server.close()
        
    def read_byte(self, i2c_addr: int, force:bool=None) -> int:
        """
        Read a single byte from a device.

        :param i2c_addr: i2c address
        :param force: Unused - here for compatibility with other libraries
        :return: Read byte value
        """
        self._server.sendall(bytes([Commands.ReadByte, i2c_addr]))
        value, = self._server.recv(1)
        return value
    
    def write_byte(self, i2c_addr: int, value: int, force:bool=None) -> None:
        """
        Write a single byte to a device.

        :param i2c_addr: i2c address
        :param value: Byte value to transmit
        :param force: Unused - here for compatibility with other libraries
        """
        self._server.sendall(bytes([Commands.WriteByte, i2c_addr, value]))
    
    def read_byte_data(self, i2c_addr: int, register: int, force:bool=None) -> int:
        """
        Read a single byte from a designated register.

        :param i2c_addr: i2c address
        :param register: Register to read
        :param force: Unused - here for compatibility with other libraries
        :return: Read byte value
        """
        self._server.sendall(bytes([Commands.ReadByteData, i2c_addr, register]))
        value, = self._server.recv(1)
        return value
    
    def write_byte_data(self, i2c_addr: int, register: int, value: int, force:bool=None) -> None:
        """
        Write a byte to a given register.

        :param i2c_addr: i2c address
        :param register: Register to read
        :param value: Byte value to transmit
        :param force: Unused - here for compatibility with other libraries
        """
        self._server.sendall(bytes([Commands.WriteByteData, i2c_addr, register, value]))
    
    
    def read_word_data(self, i2c_addr: int, register: int, force:bool=None) -> int:
        """
        Read a single word (2 bytes) from a given register.

        :param i2c_addr: i2c address
        :param register: Register to read
        :param force: Unused - here for compatibility with other libraries
        :return: Read byte value
        """
        self._server.sendall(bytes([Commands.ReadWordData, i2c_addr, register]))
        value = self._server.recv(2)
        return struct.unpack('>H', value)[0]
    
    def write_word_data(self, i2c_addr: int, register: int, value: int, force:bool=None) -> None:
        """
        Write a single word (2 bytes) to a given register.

        :param i2c_addr: i2c address
        :param register: Register to read
        :param value: Word value to transmit
        :param force: Unused - here for compatibility with other libraries
        """
        self._server.sendall(bytes([Commands.WriteWordData, i2c_addr, register]))
        self._server.sendall(struct.pack('>H', value))
    
    def read_i2c_block_data(self, i2c_addr: int, register: int, length: int, force:bool=None) -> int:
        """
        Read a block of byte data from a given register.

        :param i2c_addr: i2c address
        :param register: Start register
        :param length: Desired block length
        :param force: Unused - here for compatibility with other libraries
        :return: List of bytes
        """
        self._server.sendall(bytes([Commands.ReadI2CBlockData, i2c_addr, register, length]))
        value = self._server.recv(length)
        return value
    
    def write_i2c_block_data(self, i2c_addr: int, register: int, data: list, force:bool=None) -> None:
        """
        Write a block of byte data to a given register.

        :param i2c_addr: i2c address
        :param register: Start register
        :param data: List of bytes
        :param force: Unused - here for compatibility with other libraries
        """
        self._server.sendall(bytes([Commands.WriteI2CBlockData, i2c_addr, register, len(data)]))
        self._server.sendall(bytes(data))
    