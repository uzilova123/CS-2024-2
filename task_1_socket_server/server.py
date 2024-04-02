import socket
from datetime import datetime

HOST = "127.0.0.1"
PORT = 65421 # 1023 >


response_ok = """HTTP/1.1 200 OK
Date: {date}
Server: Apache/2.2.14 (Win32)
Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT
Content-Length: {length}
Content-Type: text/html
Connection: Closed

{body}"""


socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_server.bind((HOST, PORT))
socket_server.listen(1)

conn, addr = socket_server.accept()

data = b""
while True:
    data += conn.recv(1024)
    if data.endswith(b"\r\n\r\n"):
        break

request_data = data.decode("utf-8")

type_request, urn, _ = request_data.split("\r\n")[0].split(" ")
print(type_request, urn)

with open(urn.lstrip("//")) as file:
    response_body = file.read()

response = response_ok.format(
    date=datetime.now(),
    length=len(response_body.encode()),
    body=response_body
)
conn.sendall(response.encode())
conn.close()

socket_server.close()
