import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

def id_Cliente(conn, text_area):
    try:
        data_type = conn.recv(1024).decode().strip()
        if data_type == 'TYPE text':
            data = conn.recv(1024).decode().strip()
            if data.startswith('DATA '):
                text = data[5:]
                with open('received_text.txt', 'w') as file:
                    file.write(text)
                conn.sendall(b'Valido\n')
                text_area.insert(tk.END, "Texto recebido e salvo.\n")
            else:
                conn.sendall(b'ERROR Formato Data Invalido\n')
                text_area.insert(tk.END, "Erro: Formato de texto inválido.\n")
        elif data_type == 'TYPE file':
            data = conn.recv(1024)
            if data.startswith(b'DATA '):
                contem = data[5:]
                with open('received_file', 'wb') as file:
                    file.write(contem)
                conn.sendall(b'Valido\n')
                text_area.insert(tk.END, "Arquivo recebido e salvo.\n")
            else:
                conn.sendall(b'ERROR Formato Data Invalido\n')
                text_area.insert(tk.END, "Erro: Formato de arquivo inválido.\n")
        else:
            conn.sendall(b'ERROR Tipo Invalido\n')
            text_area.insert(tk.END, "Erro: Tipo de dado inválido.\n")
    except Exception as e:
        conn.sendall(f'ERROR {str(e)}\n'.encode())
        text_area.insert(tk.END, f"Erro: {str(e)}\n")

class ServerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Servidor")
        
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
        self.text_area.pack(padx=10, pady=10)
        
        self.start_button = tk.Button(root, text="Iniciar Servidor", command=self.start_server)
        self.start_button.pack(pady=10)
        
        self.server_socket = None
        self.is_running = False

    def start_server(self):
        if not self.is_running:
            self.is_running = True
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind(('', 12345))
            self.server_socket.listen()
            self.text_area.insert(tk.END, "Servidor iniciado e aguardando conexões...\n")
            threading.Thread(target=self.accept_connections).start()

    def accept_connections(self):
        while self.is_running:
            conn, addr = self.server_socket.accept()
            self.text_area.insert(tk.END, f"Conectado por {addr}\n")
            threading.Thread(target=self.handle_client, args=(conn,)).start()

    def handle_client(self, conn):
        with conn:
            id_Cliente(conn, self.text_area)

if __name__ == "__main__":
    root = tk.Tk()
    app = ServerApp(root)
    root.mainloop()