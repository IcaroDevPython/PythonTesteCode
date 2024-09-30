import socket
import ssl

def start_proxy(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(5)
    print(f"\033[33mProxy rodando em http://0.0.0.0:{port}\033[m")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"\033[32m>>> Conexão de {addr}\033[m")
        handle_client(client_socket)

def handle_client(client_socket):
    request = client_socket.recv(4096).decode()
    print(f"\033[34m\t> Solicitação recebida:\n{request}\033[m".replace("\n","\n\t"))

    lines = request.splitlines()
    if len(lines) > 0:
        first_line = lines[0].split()
        method = first_line[0]
        url = first_line[1]

        # Determinar se é HTTP ou HTTPS
        if url.startswith("http://"):
            url = url[7:]  # Remove 'http://'
            port = 80
        elif url.startswith("https://"):
            url = url[8:]  # Remove 'https://'
            port = 443
        else:
            client_socket.close()
            return

        host, path = (url.split('/', 1) + [''])[:2]

        try:
            # Conectar ao servidor de destino
            target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            target_socket.connect((host, port))
            if port == 443:  # Para HTTPS, envolva em SSL
                target_socket = ssl.wrap_socket(target_socket)
                
            # Enviar a requisição ao servidor de destino
            target_socket.send(f"{method} /{path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n".encode())

            # Receber a resposta do servidor de destino
            response = target_socket.recv(4096)
            target_socket.close()

            # Enviar a resposta de volta ao cliente
            client_socket.send(response)
        except socket.gaierror:
            print(f"Erro ao conectar com o host: {host}")
            client_socket.send(b"HTTP/1.1 502 Bad Gateway\r\n\r\n")
    
    client_socket.close()

if __name__ == "__main__":
    start_proxy(8888)
