from Serialization import Tag
from Serialization.json_io import encodeJSON, decodeJSON
import sys, struct

def sendNetworkData(connection, tag):
    if isinstance(tag, Tag):
        data = encodeJSON(tag)
        connection.sendall(struct.pack('>i', len(data))+data.encode('ascii'))
    else:
        raise TypeError('Value tag, needs to be of Tag object.')

def receiveNetworkData(connection):
    #data length is packed into 4 bytes
    total_len=0;total_data=bytearray();size=sys.maxsize
    sock_data=bytearray();recv_size=8192
    while total_len<size:
        sock_data=connection.recv(recv_size)
        if not sock_data:
            return None
        if not total_data:
            if len(sock_data)>4:
                size=struct.unpack('>i', sock_data[:4])[0]
                for b in sock_data[4:]:
                    total_data.append(b)
            elif len(sock_data) == 4:
                size=struct.unpack('>i', sock_data[:4])[0]
        else:
            total_data.append(sock_data)
        total_len=len(total_data)
    return decodeJSON(bytes(total_data).decode('ascii'))
