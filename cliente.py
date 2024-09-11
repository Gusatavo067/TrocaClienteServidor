import socket

def EnvioDeTexto(sock):
    texto = input("Digite o texto a ser enviado: ")
    sock.sendall(b'TYPE text\n')
    sock.sendall(f'DATA {texto}\n'.encode())

def EnvioDeFile(sock):
    file_caminho = input("Digite o caminho do arquivo a ser enviado: ")
    try:
        with open(file_caminho, 'rb') as file:
            contem = file.read()
        sock.sendall(b'TYPE file\n')
        sock.sendall(b'DATA ' + contem + b'\n')
    except FileNotFoundError:
        print("Arquivo não foi encontrado.")

def main():
    host = '172.50.4.52'
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        while True:
            opcao = input("Digite '1' para enviar um texto ou '2' para enviar arquivo: ")
            if opcao == '1':
                EnvioDeTexto(sock)
            elif opcao == '2':
                EnvioDeFile(sock)
            else:
                print("Escolha inválida.")
                continue

            resposta = sock.recv(1024).decode()
            print("Resposta do servidor:", resposta)
            if resposta.startswith("Valido"):
                break

if __name__ == "__main__":
    main()