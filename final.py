from tkinter import *

# Constantes para as dimensões do Canvas
CANVAS_X, CANVAS_Y = 360, 450

#---------------------------------
# Classe principal para a animação
#---------------------------------
class Animation:
    def __init__(self):

        # Objeto da classe Tk do pacote de tkinter
        self.raiz = Tk()

        # Título
        self.raiz.title('Animação')

        # Frames
        self.controle_frame = Frame(self.raiz)
        self.menu_frame = Frame(self.raiz)
        self.animacao_frame = Frame(self.raiz)
        self.status_frame = Frame(self.raiz)

        # Inserindo os Frames
        self.controle_frame.pack(side = LEFT)
        self.status_frame.pack(side = RIGHT)
        self.menu_frame.pack(side = BOTTOM)
        self.animacao_frame.pack(side = TOP)

        # Canvas, espaço para a animação
        self.canvas = Canvas(self.animacao_frame, width = CANVAS_X, height = CANVAS_Y)

        # Inserindo canvas
        self.canvas.pack()

        # Widgets do frame de status
        self.texto_status = Label(self.status_frame, text = 'STATUS:', width = 15)
        self.mostrar_status_nome = Label(self.status_frame, text = 'NOME', fg = 'green')
        self.mostrar_status_start = Label(self.status_frame, text = 'START', fg = 'blue')
        self.mostrar_status_tipo = Label(self.status_frame, text = 'TIPO', fg = 'blue')

        # Inserindo widgets do frame de status
        self.texto_status.pack()
        self.mostrar_status_nome.pack()
        self.mostrar_status_start.pack()
        self.mostrar_status_tipo.pack()

        # Botões menu
        self.arvore_botao = Button(self.menu_frame, text = 'Arvore', width = 10, cursor = 'hand2', command = self.arvore)
        self.start_botao = Button(self.menu_frame, text = 'Start', width = 10, cursor = 'hand2' ,command = self.start)
        self.mario_botao = Button(self.menu_frame, text = 'Mario', width = 10, cursor = 'hand2', command = self.mario)

        # Inserindo botões no frame de menu
        self.arvore_botao.pack(side = LEFT)
        self.start_botao.pack(side = LEFT)
        self.mario_botao.pack(side = LEFT)

        # Objetos do frame de controle
        self.caixa_texto = Entry(self.controle_frame)

        # Comando 'enter' na caixa de texto para assionar um evento
        self.caixa_texto.bind('<Return>', self.controle)

        # Inserindo onjetos do frame de controle
        self.caixa_texto.pack()

        # Variaveis e contadores
        self.cont_entrada = 0 # Contador de entrada da animação da arvore
        self.cont_saida = 0 # Contador de saida da animação da arvore
        self.controle = False # Controle de animação da arvore
        self.controle_mario = 0 # Controle de animação do mario
        self.cont_loop = 0 # Contador de loop da animação da Arvore
        self.cont_mario = 0 # Contador da animação do mario
        self.x = CANVAS_X # Variavel para o local x do canvas
        self.y = CANVAS_Y # Variavel para o local y  do canvas
        self.side = 0 # Variavel para controlar o lado do personagem do mario
        self.modo_manual = True # Ativar ou Desativar o modo manual
        self.eventoStart = True # A animação só vai ocorrer se tiver ativado

        # Variavel de controle de animação utilizada na função de 'start'
        self.start_status_nome = ''

        # Inicio
        self.carregarImagens()

        # Manter a tela em sua forma de origem e continuar aberta até pressionar o 'X'
        self.raiz.resizable(False, False)
        self.raiz.mainloop()

    #------------------
    # Funções de evento
    #------------------

    # Função para o evento de clickar o botão 'Start'
    def start(self):
        if(self.start_status_nome == 'Arvore'):
            self.canvas.delete(ALL)
            self.canvas.create_image((CANVAS_X/2, CANVAS_Y/2), image = self.imagem_parada)
            self.status() # Atualizar os status
        elif(self.start_status_nome == 'Mario'):
            self.canvas.delete(ALL)
            if(self.side == 0):
                self.canvas.create_image((self.x/2, self.y/2), image = self.imagens_mario_parado[0])
            elif(self.side == 1):
                self.canvas.create_image((self.x/2, self.y/2), image = self.imagens_mario_parado[1])
            self.status() # Atualizar o status

        # Ligar o comando start
        self.eventoStart = True
        self.mostrar_status_start['text'] = 'Ativado'
        self.mostrar_status_start['fg'] = 'green'

    # Função para o evendo de clickar o botão 'Arvore'
    def arvore(self):
        # Comando para quando outra animação que estiver acontecendo parar, e depois mudar para a que foi selecionada
        if(self.start_status_nome == 'Mario'):
            self.controle_mario = 0
            self.manualParar() # Desativar o modo manual do mario, para evitar problemas
            self.canvas.delete(ALL)

        # Mudar para a animação da árvore
        self.start_status_nome = 'Arvore'
        self.umEnter = 0
        self.eventoStart = False # Desativar o start, será ativado denovo quando for selecionar o botão start
        self.mostrar_status_start['text'] = 'Desativado'
        self.mostrar_status_start['fg'] = 'red'

    # Função para o evento de clickar o botão 'Mario'
    def mario(self):
        # Comando para quando outra animação que estiver acontecendo parar, e depois mudar para a que foi selecionada
        if(self.start_status_nome == 'Arvore'):
            self.cont_entrada = 0
            self.controle = False
            self.canvas.delete(ALL)

        # Mudar para a anumação do mario
        self.start_status_nome = 'Mario'
        self.umEnter = 0
        self.eventoStart = False # Desativar o start, será ativado denovo quando for selecionar o botão start
        self.mostrar_status_start['text'] = 'Desativado'
        self.mostrar_status_start['fg'] = 'red'

    # Função para o evento de dar enter na caixa de texto
    def controle(self, event):
        #-----------------------------------
        # Comandos para a animação da arvore
        #-----------------------------------
        if(self.start_status_nome == 'Arvore' and self.eventoStart):
            if(self.verificarCodigo(self.caixa_texto.get()) == 'NEVAR' and self.controle != True):
                self.status() # Atualizar status
                self.controle = True
                self.nevar()
            elif(self.verificarCodigo(self.caixa_texto.get()) == 'PARAR' and self.controle):
                self.status() # Atualizar status
                self.cont_entrada = 0 # Contador para as imagens de entrada da animação de 'Nevar'
                self.controle = False
                self.pararNevar()

        #----------------------------------
        # Comandos para a animação do mario
        #----------------------------------
        elif(self.start_status_nome == 'Mario' and self.eventoStart):
            if(self.verificarCodigo(self.caixa_texto.get()) == 'ESQUERDA' and self.controle_mario != 1):
                self.status() # Atualizar status
                self.manualParar() # Desativar o modo manual do mario, para evitar problemas
                self.controle_mario = 1 # Controlar a animação para andar para esquerda e conseguir mudar essa animação
                self.marioAndandoEsquerda()
            elif(self.verificarCodigo(self.caixa_texto.get()) == 'DIREITA' and self.controle_mario != 2):
                self.status() # Atualizar status
                self.manualParar() # Desativar o modo manual do mario, para evitar problemas
                self.controle_mario = 2 # Controlar a animação para andar para direita e conseguir mudar essa animação
                self.marioAndandoDireita()
            elif(self.verificarCodigo(self.caixa_texto.get()) == 'MANUAL'):
                self.status() # Atualizar status
                self.manualLigar() # Ativar o modo manual
                self.controle_mario = 0
                self.canvas.focus_force() # Ativar o foco no canvas
                self.start()
                self.manual()
            elif(self.verificarCodigo(self.caixa_texto.get()) == 'PARAR'):
                self.status() # Atualizar status
                self.manualParar() # Desativar o modo manual do mario, para evitar problemas
                self.controle_mario = 0 # Controlar a animação de ficar parado e conseguir mudar essa animação
                self.start()


    # Função para carregar imagens
    def carregarImagens(self):
        #---------------
        # ARVORE NEVANDO
        #---------------
        # Vetores e variavel para armazenar as imagens da Arvore nevando
        self.imagens_entrada = []
        self.imagens_loop = []
        self.imagens_saida = []
        self.imagem_parada = PhotoImage(file = 'sprites\pinheiro\pinheiro_parado.png')

        # Loop para armazenar as imagens de entrada
        for i in range(5):
            self.imagens_entrada.append(PhotoImage(file = 'sprites\pinheiro\pinheiro_entrada_%d.png' %i))

        # Loop para armazenar as imagens de meio(loop)
        for i in range(3):
            self.imagens_loop.append(PhotoImage(file = 'sprites\pinheiro\pinheiro_loop_%d.png' %i))

        # Loop para armazenar as imagens de saida
        for i in range(6):
            self.imagens_saida.append(PhotoImage(file = 'sprites\pinheiro\pinheiro_saida_%d.png' %i))

        #--------------
        # MARIO ANDANDO
        #--------------
        # Vetores e variavel para armazenar as imagens do Mario
        self.imagens_mario_esquerda = []
        self.imagens_mario_direita = []
        self.imagens_mario_parado = [PhotoImage(file = 'sprites\mario\m_left_stop.png'), PhotoImage(file = 'sprites\mario\m_right_stop.png')]

        # Loop para armazenar as imagens do mario de esquerda
        for i in range(3):
            self.imagens_mario_esquerda.append(PhotoImage(file = 'sprites\mario\m_left_%d.png' %i))

        # Loop para armazenar as imagens do mario de direita
        for i in range(3):
            self.imagens_mario_direita.append(PhotoImage(file = 'sprites\mario\m_right_%d.png' %i))

    # ---------------------------------
    # FUNÇÕES PARA A ANIMAÇÃO DA ARVORE
    # ---------------------------------
    # Função para a animação da arvore ao colocar o comando 'Nevar'
    def nevar(self):
        if(self.cont_entrada < 5 and self.controle):
            self.canvas.delete(ALL)
            self.canvas.create_image((CANVAS_X/2, CANVAS_Y/2), image = self.imagens_entrada[self.cont_entrada])

            self.cont_entrada += 1
            self.raiz.after(300, self.nevar)
        elif(self.cont_entrada >= 5 and self.controle):
            self.canvas.delete(ALL)
            self.canvas.create_image((CANVAS_X/2, CANVAS_Y/2), image = self.imagens_loop[self.cont_loop])
            self.update()
            self.raiz.after(300, self.nevar)

    # Função para parar a animação de nevar
    def pararNevar(self):
        if(self.cont_saida <= 5 and not(self.controle)):
            self.canvas.delete(ALL)
            self.canvas.create_image((CANVAS_X/2, CANVAS_Y/2), image = self.imagens_saida[self.cont_saida])

            self.cont_saida += 1

            self.raiz.after(300, self.pararNevar)
        else:
            self.start()

    # --------------------------------
    # FUNÇÕES PARA A ANIMAÇÃO DO MARIO
    # --------------------------------
    # Função para a animação do mario andando para a esquerda
    def marioAndandoEsquerda(self):
        self.side = 0
        if(self.controle_mario == 1):
            self.canvas.delete(ALL)
            self.canvas.create_image((self.x/2, self.y/2), image = self.imagens_mario_esquerda[self.cont_mario])
            self.update()
            self.x -= 20

            # Função para passar a parede
            self.passarParede()

            self.raiz.after(100, self.marioAndandoEsquerda)

    # Função para a animação do mario andando para a direita
    def marioAndandoDireita(self):
        self.side = 1
        if(self.controle_mario == 2):
            self.canvas.delete(ALL)
            self.canvas.create_image((self.x/2, self.y/2), image = self.imagens_mario_direita[self.cont_mario])
            self.update()
            self.x += 20

            # Função para passar a parede
            self.passarParede()

            self.raiz.after(100, self.marioAndandoDireita)

    # Função para deixa o comando do mario manualmente
    def manual(self):
        # Comando para quando não tiver sendo executado nada o mario fica parado
        if(self.modo_manual):
            self.start()
            self.raiz.after(600, self.manual)

        # Função para lidar com o evento de clickar na seta esquerda e na seta direita do teclado
        self.canvas.bind("<Left>", self.manualLeft)
        self.canvas.bind("<Right>", self.manualRight)

    # Função para desativar o modo manual do mario
    def manualParar(self):
        self.modo_manual = False

    # Função para ativar o modo manual do mario
    def manualLigar(self):
        self.modo_manual = True

    # Função para quando apertar a seta esquerda do teclado na animação manual do mario
    def manualLeft(self, event):
        self.canvas.delete(ALL)
        if(self.side == 1):
            self.canvas.create_image((self.x/2, self.y/2), image = self.imagens_mario_parado[0])
            self.side = 0
        else:
            self.canvas.create_image((self.x/2, self.y/2), image = self.imagens_mario_esquerda[self.cont_mario])
            self.update()
            self.x -= 20
            self.passarParede()

    # Função para quando apertar a seta direita do teclado na animação manual do mario
    def manualRight(self, event):
        self.canvas.delete(ALL)
        if(self.side == 0):
            self.canvas.create_image((self.x/2, self.y/2), image = self.imagens_mario_parado[1])
            self.side = 1
        else:
            self.canvas.create_image((self.x/2, self.y/2), image = self.imagens_mario_direita[self.cont_mario])
            self.update()
            self.x += 20
            self.passarParede()

    # Função para o mario passar a parede
    def passarParede(self):
        if(self.side == 0): # Esquerda
            # Comando para quando passar na parede do canvas aparecer do outro lado
            if(self.x < 0 - 50):
                self.x = 2*CANVAS_X + 55
        elif(self.side == 1): # Direita
            # Comando para quando passar na parede do canvas aparecer do outro lado
            if(self.x > 2*CANVAS_X + 55):
                self.x = 0

    # -------------------------------
    # FUNÇÕES PARA TODAS AS ANIMAÇÕES
    # -------------------------------
    # Função para atualizar os contadores das listas onde estão as imagens
    def update(self):
        if(self.start_status_nome == 'Arvore'):
            self.cont_saida = 0
            self.cont_loop += 1
            if(self.cont_loop > 2):
                self.cont_loop = 0
        elif(self.start_status_nome == 'Mario'):
            self.cont_mario += 1
            if(self.cont_mario > 2):
                self.cont_mario = 0

    # Função para atualizar o status
    def status(self):
        if(self.start_status_nome == 'Arvore'):
            self.mostrar_status_nome['text'] = self.start_status_nome
        elif(self.start_status_nome == 'Mario'):
            self.mostrar_status_nome['text'] = self.start_status_nome

        # Tipo de animação
        self.mostrar_status_tipo['text'] = self.caixa_texto.get()

    # Função para colocar o texto da caixa de texto em caixa alta
    def verificarCodigo(self, codigo):
        return codigo.upper()

#----------------------------------------
# Chamando classe para iniciar o programa
#----------------------------------------
Animation()
