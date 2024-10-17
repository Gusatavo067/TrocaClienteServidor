import socket  # Importa a biblioteca socket para comunicação via rede
import threading  # Importa threading para suportar múltiplas conexões simultâneas
import tkinter as tk  # Importa o tkinter para a criação da interface gráfica
from tkinter import scrolledtext  # Importa a funcionalidade de texto com barra de rolagem

# Função que lida com o cliente conectado
def id_Cliente(conexao, area_texto):
    try:
        # Recebe o tipo de dado enviado pelo cliente (texto ou arquivo)
        tipo_dado = conexao.recv(1024).decode().strip()
        
        if tipo_dado == 'TYPE text':  # Se o dado for do tipo texto
            dado = conexao.recv(1024).decode().strip()  # Recebe o dado
            if dado.startswith('DATA '):  # Verifica se o dado começa com "DATA"
                texto = dado[5:]  # Extrai o texto após "DATA"
                # Salva o texto recebido em um arquivo
                with open('texto_recebido.txt', 'w') as arquivo:
                    arquivo.write(texto)
                conexao.sendall(b'Valido\n')  # Envia uma confirmação ao cliente
                area_texto.insert(tk.END, "Texto recebido e salvo.\n")  # Mostra uma mensagem na interface
            else:
                # Envia uma mensagem de erro ao cliente caso o formato seja inválido
                conexao.sendall(b'ERROR Formato Data Invalido\n')
                area_texto.insert(tk.END, "Erro: Formato de texto inválido.\n")
        
        elif tipo_dado == 'TYPE file':  # Se o dado for do tipo arquivo
            dado = conexao.recv(1024)  # Recebe o arquivo em formato binário
            if dado.startswith(b'DATA '):  # Verifica se o dado começa com "DATA"
                conteudo = dado[5:]  # Extrai o conteúdo do arquivo após "DATA"
                # Salva o arquivo recebido
                with open('arquivo_recebido', 'wb') as arquivo:
                    arquivo.write(conteudo)
                conexao.sendall(b'Valido\n')  # Envia uma confirmação ao cliente
                area_texto.insert(tk.END, "Arquivo recebido e salvo.\n")  # Mostra uma mensagem na interface
            else:
                # Envia uma mensagem de erro ao cliente caso o formato seja inválido
                conexao.sendall(b'ERROR Formato Data Invalido\n')
                area_texto.insert(tk.END, "Erro: Formato de arquivo inválido.\n")
        
        else:  # Se o tipo de dado não for reconhecido
            conexao.sendall(b'ERROR Tipo Invalido\n')  # Envia uma mensagem de erro ao cliente
            area_texto.insert(tk.END, "Erro: Tipo de dado inválido.\n")
    
    except Exception as e:  # Em caso de exceção
        # Envia o erro ao cliente e exibe na interface
        conexao.sendall(f'ERROR {str(e)}\n'.encode())
        area_texto.insert(tk.END, f"Erro: {str(e)}\n")

# Classe que representa a aplicação do servidor
class AppServidor:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Servidor")  # Define o título da janela
        
        # Área de texto com rolagem para mostrar informações e logs do servidor
        self.area_texto = scrolledtext.ScrolledText(raiz, wrap=tk.WORD, width=50, height=20)
        self.area_texto.pack(padx=10, pady=10)
        
        # Botão para iniciar o servidor
        self.botao_iniciar = tk.Button(raiz, text="Iniciar Servidor", command=self.iniciar_servidor)
        self.botao_iniciar.pack(pady=10)
        
        # Botão para encerrar o servidor
        self.botao_encerrar = tk.Button(raiz, text="Encerrar Servidor", command=self.encerrar_servidor)
        self.botao_encerrar.pack(pady=10)
        
        self.socket_servidor = None  # Inicialmente, o socket do servidor é None
        self.servidor_ativo = False  # Variável para indicar se o servidor está em execução

    # Função para iniciar o servidor
    def iniciar_servidor(self):
        if not self.servidor_ativo:  # Verifica se o servidor já está em execução
            self.servidor_ativo = True
            # Cria um socket de servidor
            self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_servidor.bind(('', 12345))  # Associa o socket à porta 12345
            self.socket_servidor.listen()  # O servidor começa a escutar conexões
            self.area_texto.insert(tk.END, "Servidor iniciado e aguardando conexões...\n")
            # Cria uma nova thread para aceitar conexões simultaneamente
            threading.Thread(target=self.aceitar_conexoes).start()

    # Função para aceitar conexões de clientes
    def aceitar_conexoes(self):
        while self.servidor_ativo:  # Enquanto o servidor estiver ativo
            try:
                conexao, endereco = self.socket_servidor.accept()  # Aceita uma conexão
                self.area_texto.insert(tk.END, f"Conectado por {endereco}\n")  # Mostra quem conectou
                # Cria uma nova thread para lidar com o cliente conectado
                threading.Thread(target=self.tratar_cliente, args=(conexao,)).start()
            except OSError:
                break  # Sai do loop se o socket for fechado

    # Função que trata as requisições de um cliente
    def tratar_cliente(self, conexao):
        with conexao:  # Garante que a conexão será fechada corretamente
            id_Cliente(conexao, self.area_texto)  # Chama a função que processa o cliente

    # Função para encerrar o servidor
    def encerrar_servidor(self):
        if self.servidor_ativo:
            self.servidor_ativo = False
            self.socket_servidor.close()  # Fecha o socket do servidor
            self.area_texto.insert(tk.END, "Servidor encerrado.\n")

# Função principal para iniciar a interface gráfica
if __name__ == "__main__":
    raiz = tk.Tk()  # Cria a janela principal
    app = AppServidor(raiz)  # Inicializa a aplicação do servidor
    raiz.mainloop()  # Inicia o loop da interface gráfica