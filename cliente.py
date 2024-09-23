import socket  # Importa a biblioteca socket para comunicação via rede
import tkinter as tk  # Importa o tkinter para criação da interface gráfica
from tkinter import filedialog, scrolledtext, simpledialog  # Importa funcionalidades específicas do tkinter

# Função para enviar texto ao servidor
def EnvioDeTexto(soquete, area_resposta):
    # Solicita ao usuário que insira o texto a ser enviado
    texto = simpledialog.askstring("Entrada de Texto", "Digite o texto a ser enviado:")
    if texto:  # Se o texto foi inserido
        try:
            # Envia o tipo de dado sendo enviado (texto) ao servidor
            soquete.sendall(b'TYPE text\n')
            # Envia o conteúdo do texto
            soquete.sendall(f'DATA {texto}\n'.encode())
            # Recebe a resposta do servidor
            resposta = soquete.recv(1024).decode()
            # Exibe a resposta na área de resposta da interface gráfica
            area_resposta.insert(tk.END, f"Resposta do servidor: {resposta}\n")
        except Exception as e:  # Em caso de erro
            area_resposta.insert(tk.END, f"Erro ao enviar texto: {str(e)}\n")

# Função para enviar um arquivo ao servidor
def EnvioDeArquivo(soquete, area_resposta):
    # Abre um diálogo para o usuário selecionar o arquivo
    caminho_arquivo = filedialog.askopenfilename()
    if caminho_arquivo:  # Se o arquivo foi selecionado
        try:
            # Abre o arquivo no modo de leitura binária
            with open(caminho_arquivo, 'rb') as arquivo:
                conteudo = arquivo.read()  # Lê o conteúdo do arquivo
            # Envia o tipo de dado sendo enviado (arquivo) ao servidor
            soquete.sendall(b'TYPE file\n')
            # Envia o conteúdo do arquivo
            soquete.sendall(b'DATA ' + conteudo + b'\n')
            # Recebe a resposta do servidor
            resposta = soquete.recv(1024).decode()
            # Exibe a resposta na área de resposta da interface gráfica
            area_resposta.insert(tk.END, f"Resposta do servidor: {resposta}\n")
        except FileNotFoundError:  # Se o arquivo não foi encontrado
            area_resposta.insert(tk.END, "Arquivo não foi encontrado.\n")
        except Exception as e:  # Em caso de erro
            area_resposta.insert(tk.END, f"Erro ao enviar arquivo: {str(e)}\n")

# Classe que representa a aplicação cliente
class AppCliente:
    def __init__(self, janela_raiz):
        self.janela_raiz = janela_raiz
        self.janela_raiz.title("Cliente")  # Define o título da janela
        
        # Rótulo para o campo de entrada do host
        self.rotulo_host = tk.Label(janela_raiz, text="Host:")
        self.rotulo_host.pack(padx=10, pady=5)
        
        # Campo de entrada para o host
        self.entrada_host = tk.Entry(janela_raiz, width=50)
        self.entrada_host.pack(padx=10, pady=5)
        
        # Rótulo para o campo de entrada da porta
        self.rotulo_porta = tk.Label(janela_raiz, text="Porta:")
        self.rotulo_porta.pack(padx=10, pady=5)
        
        # Campo de entrada para a porta
        self.entrada_porta = tk.Entry(janela_raiz, width=50)
        self.entrada_porta.pack(padx=10, pady=5)
        
        # Botão para conectar ao servidor
        self.botao_conectar = tk.Button(janela_raiz, text="Conectar", command=self.conectar_ao_servidor)
        self.botao_conectar.pack(padx=10, pady=5)
        
        # Botão para enviar texto ao servidor
        self.botao_texto = tk.Button(janela_raiz, text="Enviar Texto", command=self.enviar_texto)
        self.botao_texto.pack(padx=10, pady=5)
        
        # Botão para enviar arquivo ao servidor
        self.botao_arquivo = tk.Button(janela_raiz, text="Enviar Arquivo", command=self.enviar_arquivo)
        self.botao_arquivo.pack(padx=10, pady=5)
        
        # Área para exibir as respostas do servidor
        self.area_resposta = scrolledtext.ScrolledText(janela_raiz, wrap=tk.WORD, width=50, height=10)
        self.area_resposta.pack(padx=10, pady=10)
        
        self.soquete = None  # Inicialmente, o socket é None, indicando que não está conectado

    # Função para conectar ao servidor
    def conectar_ao_servidor(self):
        host = self.entrada_host.get()  # Obtém o host inserido pelo usuário
        porta = int(self.entrada_porta.get())  # Obtém a porta inserida pelo usuário
        try:
            # Cria um socket e conecta ao servidor
            self.soquete = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.soquete.connect((host, porta))
            self.area_resposta.insert(tk.END, "Conectado ao servidor.\n")  # Exibe mensagem de sucesso
        except Exception as e:  # Em caso de erro ao conectar
            self.area_resposta.insert(tk.END, f"Erro ao conectar ao servidor: {str(e)}\n")

    # Função para enviar texto ao servidor
    def enviar_texto(self):
        if self.soquete:  # Verifica se está conectado ao servidor
            EnvioDeTexto(self.soquete, self.area_resposta)  # Chama a função para enviar o texto
        else:
            self.area_resposta.insert(tk.END, "Erro: Não conectado ao servidor.\n")

    # Função para enviar arquivo ao servidor
    def enviar_arquivo(self):
        if self.soquete:  # Verifica se está conectado ao servidor
            EnvioDeArquivo(self.soquete, self.area_resposta)  # Chama a função para enviar o arquivo
        else:
            self.area_resposta.insert(tk.END, "Erro: Não conectado ao servidor.\n")

# Função principal para iniciar a interface gráfica
if __name__ == "__main__":
    janela_raiz = tk.Tk()  # Cria a janela principal
    app = AppCliente(janela_raiz)  # Inicializa a aplicação cliente
    janela_raiz.mainloop()  # Inicia o loop da interface gráfica
