import socket

class Connection:
    STMT_SIZE_MASK = 0x0F
    MAX_DATA_RECV = 0x0400

    sock = None

    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    def close(self):
        self.sock.sendall(b'e')
        self.sock.recv(1)
        self.sock.close()
    
    def query(self, stmt):
        barr = bytearray('q', 'ascii')
        barr.append(len(stmt) & self.STMT_SIZE_MASK)
        barr.extend(stmt.encode('ascii'))
        self.sock.sendall(barr)
        data = self.sock.recv(self.MAX_DATA_RECV)
        results = data.decode().split(':')
        return results[0], results[1:]

    def prepare(self, stmt, binds):
        barr = bytearray('p', 'ascii')
        barr.append(len(stmt) & self.STMT_SIZE_MASK)
        barr.extend(stmt.encode('ascii'))

        for i in binds:
            barr.extend('b'.encode('ascii'))
            barr.append(len(i) & self.STMT_SIZE_MASK)
            barr.extend(i.encode('ascii'))

        barr.extend('x'.encode('ascii'))
        barr.append(0x00)
        self.sock.sendall(barr)

        data = self.sock.recv(self.MAX_DATA_RECV)
        results = data.decode().split(':')
        return results[0], results[1:]
