"""from flask import Flask, request, Response
import requests
import socket
import threading

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS', 'TRACE', 'CONNECT'])
def proxy():
    if request.method == 'CONNECT':
        return handle_connect()
    
    url = request.args.get('url')
    if not url:
        return "URL parameter is required", 400

    try:
        req_method = request.method
        resp = requests.request(req_method, url, json=request.get_json(), headers=request.headers)
        return Response(resp.content, status=resp.status_code, headers=dict(resp.headers))
    except requests.exceptions.RequestException as e:
        return str(e), 500

def handle_connect():
    target = request.path  # Espera-se que a URL seja no formato "host:porta"
    
    try:
        # Cria um socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target.split(':')[0], int(target.split(':')[1])))
        
        # Responde ao cliente que a conexão foi estabelecida
        response = 'HTTP/1.1 200 Connection Established\r\n\r\n'
        request.environ.get('wsgi.input').sendall(response.encode())
        
        # Redireciona o socket em uma thread
        threading.Thread(target=handle_tunnel, args=(sock,)).start()
        
        return Response(status=200)
    except Exception as e:
        return f"Failed to connect: {str(e)}", 500

def handle_tunnel(sock):
    # Aqui você deve implementar a lógica para gerenciar a comunicação entre cliente e servidor
    pass

if __name__ == '__mai__'


import socket

def start_proxy(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    ip_address = socket.gethostbyname(socket.gethostname())
    print(f"Proxy rodando em http://{ip_address}:{port}...")


    while True:
        client_socket, addr = server_socket.accept()
        print(f"Conexão de {addr}")
        handle_client(client_socket)

def handle_client(client_socket):
    request = client_socket.recv(4096).decode()
    print(f"Solicitação recebida:\n{request}")

    # Extrair URL da solicitação
    lines = request.splitlines()
    if len(lines) > 0:
        first_line = lines[0].split()
        method = first_line[0]
        url = first_line[1]

        # Extrair host e porta
        if "://" in url:
            url = url.split("://")[1]
        host, path = url.split('/', 1) if '/' in url else (url, '')

        # Conectar ao servidor de destino
        target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        target_socket.connect((host, 80))
        target_socket.send(f"{method} /{path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n".encode())

        # Receber resposta do servidor de destino
        response = target_socket.recv(4096)
        target_socket.close()

        # Enviar resposta de volta ao cliente
        client_socket.send(response)
    
    client_socket.close()

if __name__ == "__main__":
    start_proxy(8888)
"""

import socket
import ssl

def start_proxy(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"Proxy rodando em http://0.0.0.0:{port}...")
nt(client_socket):
    request = client_socket.recv(4096).decode()
    print(f"Solicitação recebida:\n{request}")

    lines = request.splitlines()
    if len(lines) > 0:
        first_line = lines[0].split()
        method = first_line[0]
        url = first_line[1]

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
            # Conectar ao servidor de destino
            target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if port == 443:
                target_socket = ssl.wrap_socket(target_socket)
            target_socket.connect((host, port))
            target_socket.send(f"{method} /{path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n".encode())

            # Receber resposta do servidor de destino
            response = target_socket.recv(4096)
            target_socket.close()

            # Enviar resposta de volta ao cliente
            client_socket.send(response)
        except socket.gaierror:
            print(f"Erro ao conectar com o host: {host}")
            client_socket.send(b"HTTP/1.1 502 Bad Gateway\r\n\r\n")
    
    client_socket.close()

if __name__ == "__main__":
    start_proxy(8888)
