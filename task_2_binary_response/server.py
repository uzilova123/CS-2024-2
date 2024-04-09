import socket
import base64
from datetime import datetime

HOST = "127.0.0.1"
PORT = 65432  # 1023 >


response_404 = """HTTP/1.1 404 NOT FOUND
 Date: {date}
 Server: Apache/2.2.14 (Win32)
 Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT
 Content-Length: {length}
 Content-Type: text/html
 Connection: Closed

 {body}"""


response_ok = """HTTP/1.1 200 OK
Date: {date}
Server: Apache/2.2.14 (Win32)
Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT
Content-Length: {length}
Content-Type: text/html
Connection: Closed

{body}"""


response_binary = """HTTP/1.1 200 OK
Date: {date}
Server: Apache/2.2.14 (Win32)
Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT
Content-Length: {length}
Content-Type: image/jpg
Connection: Closed

{body}"""


def get_request(conn: socket.socket) -> str:
    data = b""
    while True:
        data += conn.recv(1024)
        if data.endswith(b"\r\n\r\n"):
            break
    return data.decode("utf-8")


def return_html_response(urn: str):
    with open(urn.lstrip("//")) as file:
        response_body = file.read()

    return response_ok.format(
        date=datetime.now(),
        length=len(response_body.encode()),
        body=response_body,
    )

def return_binary_response(urn: str):
    with open(urn.lstrip("//"), 'rb') as file:
        response_body = base64.encodebytes(file.read())

    return response_binary.format(
        date=datetime.now(),
        length=len(response_body),
        body=response_body,
    )

def return_404_response(exc: Exception):
    response_body = f"<html><h1>Catch Exception</h1><p>{exc}</p><p>{exc.__traceback__}</p></html>"

    return response_404.format(
        date=datetime.now(),
        length=len(response_body),
        body=response_body,
    )

socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_server.bind((HOST, PORT))
socket_server.listen(1)

try:
    while True:
        conn, addr = socket_server.accept()
        with conn:
            request_data = get_request(conn)
            type_request, urn, _ = request_data.split("\r\n")[0].split(" ")
            print(type_request, urn)

            try:
                if urn.endswith(".ico") or urn.endswith(".jpg"):
                    response = return_binary_response(urn)
                else:
                    response = return_html_response(urn)
            except Exception as e:
                response = return_404_response(e)
            conn.sendall(response.encode())

except KeyboardInterrupt:
    socket_server.close()
