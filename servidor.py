import socket

def id_Cliente(conn):
    try:
        data_type = conn.recv(1024).decode().strip()
        if data_type == 'TYPE text':
            data = conn.recv(1024).decode().strip()
            if data.startswith('DATA '):
                text = data[5:]
                with open('received_text.txt', 'w') as file:
                    file.write(text)
                conn.sendall(b'Valido\n')
            else:
                conn.sendall(b'ERROR Formato Data Invalido\n')
        elif data_type == 'TYPE file':
            data = conn.recv(1024)
            if data.startswith(b'DATA '):
                contem = data[5:]
                with open('received_file', 'wb') as file:
                    file.write(contem)
                conn.sendall(b'Valido\n')
            else:
                conn.sendall(b'ERROR Formato Data Invalido\n')
        else:
            conn.sendall(b'ERROR Tipo Invalido\n')
    except Exception as e:
        conn.sendall(f'ERROR {str(e)}\n'.encode())

def main():
    host = '172.50.4.13'
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((host, port))
        server.listen()
        print("Servidor aguardando conexões...")
        while True:
            conn, addr = server.accept()
            with conn:
                print(f"Conectado por {addr}")
                id_Cliente(conn)

if __name__ == "__main__":
    main()