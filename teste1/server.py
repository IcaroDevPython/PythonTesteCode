import socket
import ssl
from printcolor import *
import select

SERVER_HOST = ""
SERVER_PORT = 8080

def start_proxy_server():
    global SERVER_HOST, SERVER_PORT
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)

    info(f"Proxy rodando em {socket.gethostbyname(socket.gethostname())}:{SERVER_PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        success(f">>> Conexão de {addr}")
        client_handle(client_socket)

def client_handle(client_socket):
    request = client_socket.recv(4096).decode()
    info(f"\t> Solicitação recebida:\n{request}".replace("\n", "\n\t"))
    
    requestlist = request.splitlines()
    method, url, _ = requestlist[0].split()

    if method == "CONNECT":
        host, port = url.split(":")
        handler_connect(client_socket, host, int(port))
    else:
        handler_method(client_socket, method, url)

def handler_connect(client_socket, hostname, port):
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname, do_handshake_on_connect=False) as ssock:
                print("S_SOCK VERSION:", ssock.version())
                client_socket.send(b"HTTP/1.1 200 Connection Established\r\n\r\n")

                while True:
                    read_sockets = [client_socket, ssock]
                    readable, _, _ = select.select(read_sockets, [], [])

                    for r in readable:
                        data = r.recv(4096)
                        print(r, "->" , data)
                        if not data:
                            return
                        
                        if r is client_socket:
                            ssock.send(data)
                        else:
                            client_socket.send(data)

    except Exception as e:
        print(f"Erro ao processar a conexão: {e}")
    finally:
        client_socket.close()
        print("Conexão fechada.")

def handler_method(client_socket, method, url):
    if url.startswith("http://"):
        url = url[7:]
        port = 80
    elif url.startswith("https://"):
        url = url[8:]
        port = 443
    else:
        client_socket.close()
        return

    host, path = (url.split('/', 1) + [''])[:2]
    try:
        target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        target_socket.connect((host, port))
        if port == 443:
            target_socket = ssl.wrap_socket(target_socket)

        # Formatar a solicitação corretamente
        request_line = f"{method} /{path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        target_socket.send(request_line.encode())

        response = b""
        while True:
            chunk = target_socket.recv(4096)
            if not chunk:
                break
            response += chunk
        target_socket.close()
        client_socket.send(response)
    except socket.gaierror:
        error(f"Erro ao conectar com o host: {host}")
        client_socket.send(b"HTTP/1.1 502 Bad Gateway\r\n\r\n")
    finally:
        client_socket.close()

start_proxy_server()