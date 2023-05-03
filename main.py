import tkinter as tk
from tkinter import font
import matplotlib.pyplot as plt
import networkx as nx
from graphviz import Digraph


class Grafo:
    def __init__(self, vertices):
        self.vertices = vertices
        self.grafo = {}
        self.antecessor = {}

    def add(self, vert_inicial, vert_final, peso):
        if vert_inicial not in self.grafo:
            self.grafo[vert_inicial] = []
            self.antecessor[vert_inicial] = None
        if vert_final not in self.grafo:
            self.grafo[vert_final] = []
            self.antecessor[vert_final] = None
        self.grafo[vert_inicial].append((vert_final, peso))

    def bellman_ford(self, janela_resposta, origem, destino):
        infinito = float("inf")
        custo = {vertice: infinito for vertice in self.grafo}
        custo[origem] = 0

        for c in range(self.vertices - 1):
            atualizados = False
            for vert_inicial in self.grafo:
                for vert_final, peso in self.grafo[vert_inicial]:
                    if custo[vert_inicial] != infinito and custo[vert_final] > custo[vert_inicial] + peso:
                        self.antecessor[vert_final] = vert_inicial
                        custo[vert_final] = custo[vert_inicial] + peso
                        atualizados = True
            if atualizados == False:
                break

        ciclo_negativo = False
        for vert_inicial in self.grafo:
            for vert_final, peso in self.grafo[vert_inicial]:
                if custo[vert_inicial] != infinito and custo[vert_inicial] + peso < custo[vert_final]:
                    ciclo_negativo = True
                    break
            if ciclo_negativo:
                break

        if ciclo_negativo:
            texto = tk.Label(janela_resposta, text="Ciclo negativo!")
            texto.pack()
            return False

        caminho = []
        conexao = True
        vert_atual = destino
        while vert_atual != None:
            caminho.append(vert_atual)
            vert_atual = self.antecessor[vert_atual]
            if vert_atual == None and vert_atual != origem:
                conexao = False
                break
        caminho.reverse()

        contador = 0
        tamanho = len(caminho)
        for i in caminho:
            visualizador_menor.add_node(vertices_aeroportos[int(i)-1])
            if contador != tamanho-1:
                visualizador_menor.add_edge(vertices_aeroportos[int(
                    caminho[contador])-1], vertices_aeroportos[int(caminho[contador+1])-1])
            contador += 1

        trajetos = []
        for i in range(tamanho - 1):
            vert_inicial = caminho[i]
            vert_final = caminho[i + 1]
            for vert_destino, peso in self.grafo[vert_inicial]:
                if vert_destino == vert_final:
                    trajetos.append(
                        f"{vert_inicial} --> {vert_final}: {peso} ({vertices_aeroportos[vert_inicial-1].strip()} --> {vertices_aeroportos[vert_final-1].strip()})")

        if custo[destino] != infinito:
            for trajeto in trajetos:
                texto = tk.Label(janela_resposta, text=trajeto)
                texto.pack()
            conexao = True
        custo_total = f"O tempo mínimo para ir de {vertices_aeroportos[int(origem)-1].strip()} a {vertices_aeroportos[int(destino)-1].strip()} é {custo[destino]:.{4}f} dias ({(custo[destino])*24:.{4}f} horas)"
        return conexao, custo_total


vertices = 332
ligacoes = open("ligacoes.txt")
vertices_txt = open("vertices.txt")
aeroportos = vertices_txt.readlines()
conexoes = ligacoes.readlines()
visualizador = nx.DiGraph()
visualizador_menor = nx.DiGraph()

vertices_aeroportos = []
for aeroporto in aeroportos:
    vertices_aeroportos.append(aeroporto)
    visualizador.add_node(aeroporto)


def ver_aeroportos():
    nova_janela = tk.Toplevel()
    nova_janela.configure(bg=cor)
    nova_janela.title("Aeroportos")
    nova_janela.geometry("450x600")
    nova_janela.lift()

    def rolar_cima(event):
        canvas.yview_scroll(-1, "units")

    def rolar_baixo(event):
        canvas.yview_scroll(1, "units")

    canvas = tk.Canvas(nova_janela)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)

    scrollbar = tk.Scrollbar(nova_janela, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.config(yscrollcommand=scrollbar.set)

    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor='nw')

    cont = 1
    for aeroporto in vertices_aeroportos:
        tk.Label(frame, text=f"{cont}. {aeroporto}", padx=10, pady=0).pack()
        cont += 1

    frame.bind_all("<MouseWheel>", rolar_cima)
    frame.bind_all("<Shift-MouseWheel>", rolar_baixo)
    frame.bind_all("<Up>", rolar_cima)
    frame.bind_all("<Down>", rolar_baixo)

    nova_janela.update()
    canvas.config(scrollregion=canvas.bbox("all"))


def resposta():
    def fechar_janela():
        janela_resposta.destroy()

    def fechar_programa():
        janela_resposta.destroy()
        janela.destroy()

    def ver_grafo():
        nx.draw(visualizador, with_labels=True)
        plt.show()

    def ver_grafo_menor():
        nx.draw(visualizador_menor, with_labels=True)
        plt.show()

    janela_resposta = tk.Toplevel()
    janela_resposta.title("Bellman-Ford: Aeroportos")
    janela_resposta.geometry("600x300")
    janela_resposta.lift()
    janela_resposta.configure(bg=cor)
    visualizador.clear()
    visualizador_menor.clear()

    vert_inicial = aero_origem.get()
    vert_final = aero_destino.get()

    rota = f"Origem -> Destino: {vert_inicial} -> {vert_final}"
    if (int(vert_inicial) > vertices or int(vert_inicial) < 1) or (int(vert_final) > vertices or int(vert_final) < 1):
        texto = tk.Label(
            janela_resposta, text='Vértice fora do intervalo.', bg=cor, font=fonte)
        texto.pack(expand=True)
    else:
        texto = tk.Label(janela_resposta, text=rota)
        texto.pack(expand=True)
        grafo = Grafo(vertices)
        for conexao in conexoes:
            numeros = conexao.strip().split()
            grafo.add(int(numeros[0]), int(numeros[1]), float(numeros[2]))
            visualizador.add_edge(vertices_aeroportos[int(
                numeros[0])-1], vertices_aeroportos[int(numeros[1])-1])
        conexao, custo = grafo.bellman_ford(
            janela_resposta, int(vert_inicial), int(vert_final))
        if conexao == True:
            texto = tk.Label(janela_resposta, text=custo)
            texto.pack(expand=True)
            botao = tk.Button(
                janela_resposta, text="Ver grafo do caminho", command=ver_grafo_menor)
            botao.pack(expand=True)
        else:
            texto = tk.Label(
                janela_resposta, text=f"Não há conexão entre os aeroportos {vertices_aeroportos[int(vert_inicial)-1].strip()} e {vertices_aeroportos[int(vert_final)-1].strip()}")
            texto.pack(expand=True)

        botao = tk.Button(
            janela_resposta, text="Ver grafo completo", command=ver_grafo)
        botao.pack(expand=True)

    botao_voltar = tk.Button(
        janela_resposta, text="Voltar", command=fechar_janela)
    botao_voltar.pack(expand=True)
    botao_fechar = tk.Button(
        janela_resposta, text="Fechar", command=fechar_programa)
    botao_fechar.pack(expand=True)


janela = tk.Tk()
janela.geometry("400x260")
fonte = font.Font(family="Helvetica", size=12)
fonte_titulo = font.Font(family="Verdana", size=15)
cor = "#ADD8E6"
janela.title("Bellman-Ford: Aeroportos")
janela.configure(bg=cor)

texto = tk.Label(janela, text="Menor rota entre aeroportos",
                 font=fonte_titulo, bg=cor)
texto.pack(expand=True)
texto = tk.Label(janela, text="Aeroporto de origem", font=fonte, bg=cor)
texto.pack(expand=True)
aero_origem = tk.Entry(janela)
aero_origem.pack(expand=True)
texto = tk.Label(janela, text="Aeroporto de destino", font=fonte, bg=cor)
texto.pack(expand=True)
aero_destino = tk.Entry(janela)
aero_destino.pack(expand=True)

botao = tk.Button(janela, text="Verificar menor caminho", command=resposta)
botao.pack(expand=True)
botao = tk.Button(janela, text="Ver aeroportos", command=ver_aeroportos)
botao.pack(expand=True)

janela.mainloop()
