import socket
import tkinter as tk
from tkinter import filedialog, scrolledtext, simpledialog

def EnvioDeTexto(sock, response_area):
    texto = simpledialog.askstring("Entrada de Texto", "Digite o texto a ser enviado:")
    if texto:
        try:
            sock.sendall(b'TYPE text\n')
            sock.sendall(f'DATA {texto}\n'.encode())
            resposta = sock.recv(1024).decode()
            response_area.insert(tk.END, f"Resposta do servidor: {resposta}\n")
        except Exception as e:
            response_area.insert(tk.END, f"Erro ao enviar texto: {str(e)}\n")

def EnvioDeFile(sock, response_area):
    file_caminho = filedialog.askopenfilename()
    if file_caminho:
        try:
            with open(file_caminho, 'rb') as file:
                contem = file.read()
            sock.sendall(b'TYPE file\n')
            sock.sendall(b'DATA ' + contem + b'\n')
            resposta = sock.recv(1024).decode()
            response_area.insert(tk.END, f"Resposta do servidor: {resposta}\n")
        except FileNotFoundError:
            response_area.insert(tk.END, "Arquivo não foi encontrado.\n")
        except Exception as e:
            response_area.insert(tk.END, f"Erro ao enviar arquivo: {str(e)}\n")

class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cliente")
        
        self.host_label = tk.Label(root, text="Host:")
        self.host_label.pack(padx=10, pady=5)
        
        self.host_entry = tk.Entry(root, width=50)
        self.host_entry.pack(padx=10, pady=5)
        
        self.port_label = tk.Label(root, text="Porta:")
        self.port_label.pack(padx=10, pady=5)
        
        self.port_entry = tk.Entry(root, width=50)
        self.port_entry.pack(padx=10, pady=5)
        
        self.connect_button = tk.Button(root, text="Conectar", command=self.connect_to_server)
        self.connect_button.pack(padx=10, pady=5)
        
        self.text_button = tk.Button(root, text="Enviar Texto", command=self.enviar_text)
        self.text_button.pack(padx=10, pady=5)
        
        self.file_button = tk.Button(root, text="Enviar Arquivo", command=self.enviar_file)
        self.file_button.pack(padx=10, pady=5)
        
        self.response_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10)
        self.response_area.pack(padx=10, pady=10)
        
        self.sock = None

    def connect_to_server(self):
        host = self.host_entry.get()
        port = int(self.port_entry.get())
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, port))
            self.response_area.insert(tk.END, "Conectado ao servidor.\n")
        except Exception as e:
            self.response_area.insert(tk.END, f"Erro ao conectar ao servidor: {str(e)}\n")

    def enviar_text(self):
        if self.sock:
            EnvioDeTexto(self.sock, self.response_area)
        else:
            self.response_area.insert(tk.END, "Erro: Não conectado ao servidor.\n")

    def enviar_file(self):
        if self.sock:
            EnvioDeFile(self.sock, self.response_area)
        else:
            self.response_area.insert(tk.END, "Erro: Não conectado ao servidor.\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = ClientApp(root)
    root.mainloop()