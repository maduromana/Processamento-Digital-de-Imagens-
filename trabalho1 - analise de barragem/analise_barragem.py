# TRABALHO 1 - MARIA EDUARDA S. ROMANA - 2408830
# ANALISE DE BARRAGEM 

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import cv2
import numpy as np
import matplotlib.pyplot as plt
import collections

class AnalisadorBarragem:
    def __init__(self, janela_principal):
        self.janela_principal = janela_principal
        self.janela_principal.title("Analisador de Barragem")
        self.janela_principal.geometry("1000x600")

        # VARIAVEIS QUE ARMAZENAM O ESTADO ATUAL E OS DADOS COLETADOS POSTERIORMENTE 
        self.caminho_video = None # caminho do arq 
        self.captura = None
        self.esta_pausado = True
        self.roi = None  
        self.ponto_inicio_roi = None
        self.modo_atual = "ocioso"  
        
        self.ponto_calibracao1, self.ponto_calibracao2, self.px_por_cm = None, None, None
        self.pontos_analise_x = []
        
        # INTERFACE 
        frame_controles = tk.Frame(janela_principal, relief=tk.RAISED, borderwidth=1)
        frame_controles.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        self.frame_video = tk.Frame(janela_principal, bg="black")
        self.frame_video.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.canvas_video = tk.Canvas(self.frame_video, bg="black")
        self.canvas_video.pack()

        self.frame_sliders = tk.Frame(janela_principal, width=250, relief=tk.SUNKEN, borderwidth=1)
        self.frame_sliders.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        self.frame_sliders.pack_propagate(False)
        
        # BARRA DE INSTRUÇÃO PARA O USUARIO 
        self.label_status = tk.Label(janela_principal, text="Abra um arquivo de vídeo para começar.", relief=tk.SUNKEN, anchor=tk.W)
        self.label_status.pack(side=tk.BOTTOM, fill=tk.X)

        # BOTOES 
        self.btn_abrir = tk.Button(frame_controles, text="1. Abrir Vídeo", command=self.abrir_arquivo)
        self.btn_abrir.pack(side=tk.LEFT, padx=5, pady=5)
        self.btn_roi = tk.Button(frame_controles, text="2. Selecionar Área (ROI)", state=tk.DISABLED, command=self.iniciar_selecao_roi)
        self.btn_roi.pack(side=tk.LEFT, padx=5, pady=5)
        self.btn_calibrar = tk.Button(frame_controles, text="3. Iniciar Calibração", state=tk.DISABLED, command=self.iniciar_calibracao)
        self.btn_calibrar.pack(side=tk.LEFT, padx=5, pady=5)
        self.btn_selecionar_pontos = tk.Button(frame_controles, text="4. Selecionar Pontos", state=tk.DISABLED, command=self.iniciar_selecao_pontos)
        self.btn_selecionar_pontos.pack(side=tk.LEFT, padx=5, pady=5)
        self.btn_processar = tk.Button(frame_controles, text="5. Processar e Salvar", state=tk.DISABLED, command=self.iniciar_processamento)
        self.btn_processar.pack(side=tk.LEFT, padx=5, pady=5)

        # FILTRO DE COR - ANALISE DA AGUA - LARANJA / MARROM 
        tk.Label(self.frame_sliders, text="Controles de Cor (HSV)").pack(pady=5)
        self.h_min = self.criar_slider(self.frame_sliders, "Matiz Mín (H)", 0, 179, 10)
        self.h_max = self.criar_slider(self.frame_sliders, "Matiz Máx (H)", 0, 179, 25)
        self.s_min = self.criar_slider(self.frame_sliders, "Saturação Mín (S)", 0, 255, 80)
        self.s_max = self.criar_slider(self.frame_sliders, "Saturação Máx (S)", 0, 255, 255)
        self.v_min = self.criar_slider(self.frame_sliders, "Valor Mín (V)", 0, 255, 50)
        self.v_max = self.criar_slider(self.frame_sliders, "Valor Máx (V)", 0, 255, 255)

        self.janela_principal.protocol("WM_DELETE_WINDOW", self.ao_fechar)

    def criar_slider(self, pai, texto, de, para, valor_inicial):
        frame = tk.Frame(pai)
        frame.pack(fill=tk.X, pady=2, padx=5)
        tk.Label(frame, text=texto, anchor=tk.W).pack(fill=tk.X)
        slider = tk.Scale(frame, from_=de, to=para, orient=tk.HORIZONTAL)
        slider.set(valor_inicial)
        slider.pack(fill=tk.X)
        return slider

    def abrir_arquivo(self):
        caminho = filedialog.askopenfilename(filetypes=[("Arquivos de vídeo", "*.mp4 *.avi *.mov")])
        if not caminho: return
        self.reiniciar_estado()
        self.caminho_video = caminho
        self.captura = cv2.VideoCapture(self.caminho_video)
        if not self.captura.isOpened():
            messagebox.showerror("Erro", "Não foi possível abrir o arquivo.")
            return

        # OBTEM AS DIMENSOES E FPS DO VIDEO 
        self.largura = int(self.captura.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.altura = int(self.captura.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.captura.get(cv2.CAP_PROP_FPS)
        self.canvas_video.config(width=self.largura, height=self.altura)
        
        # EXIBE O PRIMEIRO FRAME DO VIDEO 
        ret, frame = self.captura.read()
        if ret:
            self.primeiro_frame = frame.copy()
            self.mostrar_frame(self.primeiro_frame)
        
        # HABILITA O PROXIMO BOTAO 
        self.btn_roi.config(state=tk.NORMAL)
        self.atualizar_status("Vídeo carregado. Selecione a área de análise (Passo 2).")

    def mostrar_frame(self, frame_para_mostrar):
        # DESENHA AS MARCAÇÕES NO VIDEO
        if self.roi:
            x1, y1, x2, y2 = self.roi
            cv2.rectangle(frame_para_mostrar, (x1, y1), (x2, y2), (255, 0, 255), 2)
        if self.ponto_calibracao1: cv2.circle(frame_para_mostrar, self.ponto_calibracao1, 5, (0, 255, 255), -1)
        if self.ponto_calibracao2: cv2.circle(frame_para_mostrar, self.ponto_calibracao2, 5, (255, 255, 0), -1)
        for x in self.pontos_analise_x:
            cv2.line(frame_para_mostrar, (x, 0), (x, self.altura), (0, 255, 0), 2)

        self.foto_video = self.converter_frame_para_foto(frame_para_mostrar)
        self.canvas_video.create_image(0, 0, anchor=tk.NW, image=self.foto_video)

    # SELECIONA A AREA DO VIDEO A SER ANALISADA 
    def iniciar_selecao_roi(self):
        self.modo_atual = "selecionando_roi"
        self.roi = None
        self.canvas_video.bind("<ButtonPress-1>", self.ao_pressionar_roi)
        self.canvas_video.bind("<B1-Motion>", self.ao_arrastar_roi)
        self.canvas_video.bind("<ButtonRelease-1>", self.ao_soltar_roi)
        self.atualizar_status("SELEÇÃO DE ÁREA (ROI): Clique e arraste para desenhar um retângulo sobre a área do tanque.")
    
    # SALVA A POSIÇÃO INICIAL AO CLICAR PARA DESENHAR ROI 
    def ao_pressionar_roi(self, evento):
        if self.modo_atual == "selecionando_roi":
            self.ponto_inicio_roi = (evento.x, evento.y)
    
    # DESENHA O RETANGULO NA TELA ENQUANTO O MAOUSE É ARRASTADO NA TELA 
    def ao_arrastar_roi(self, evento):
        if self.modo_atual == "selecionando_roi" and self.ponto_inicio_roi:
            frame_copia = self.primeiro_frame.copy()
            x0, y0 = self.ponto_inicio_roi
            x1, y1 = evento.x, evento.y
            cv2.rectangle(frame_copia, (x0, y0), (x1, y1), (0, 255, 0), 2)
            self.mostrar_frame(frame_copia)
    
    # FINALIZA A SELEÇÃO DA ROI AO SOLTAR O MOUSE 
    def ao_soltar_roi(self, evento):
        if self.modo_atual == "selecionando_roi" and self.ponto_inicio_roi:
            x0, y0 = self.ponto_inicio_roi
            x1, y1 = evento.x, evento.y
            self.roi = (min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))
            self.ponto_inicio_roi = None
            
            # para eventos do mouse 
            for seq_evento in ["<ButtonPress-1>", "<B1-Motion>", "<ButtonRelease-1>"]:
                self.canvas_video.unbind(seq_evento)
            
            # proximo estado 
            self.modo_atual = "ocioso"
            self.btn_calibrar.config(state=tk.NORMAL)
            self.atualizar_status("Área selecionada. Prossiga para a calibração (Passo 3).")
            self.mostrar_frame(self.primeiro_frame.copy())
    
    def iniciar_calibracao(self):
        self.modo_atual = "calibrando_p1"
        self.ponto_calibracao1, self.ponto_calibracao2, self.px_por_cm = None, None, None
        self.canvas_video.bind("<Button-1>", self.ao_clicar_canvas)
        self.atualizar_status("CALIBRAÇÃO (1/2): Clique no ponto de referência ZERO (ex: fundo do tanque).")

    def iniciar_selecao_pontos(self):
        self.modo_atual = "selecionando_pontos"
        self.pontos_analise_x = []
        self.btn_processar.config(state=tk.DISABLED)
        self.canvas_video.bind("<Button-1>", self.ao_clicar_canvas)
        self.canvas_video.bind("<Button-3>", self.ao_clicar_direito_canvas)
        self.atualizar_status("SELEÇÃO DE PONTOS (MÍNIMO 4): Clique para adicionar uma linha de análise. Clique direito para limpar.")

    # ANALISE CLIQUES DO MOUSE 
    def ao_clicar_canvas(self, evento):
        if self.modo_atual == "selecionando_pontos":
            # verifica se o clique foi dentro da ROI 
            if self.roi and not (self.roi[0] <= evento.x < self.roi[2]):
                self.atualizar_status("Ponto fora da área selecionada (ROI)! Escolha um ponto dentro do retângulo magenta.")
                return
            
            # ADD O PONTO A ANALISE 
            self.pontos_analise_x.append(evento.x)
            contagem_pontos = len(self.pontos_analise_x)
            
            # SE TIVER MAIS DE 4 PONTOS, HABILITA O PROXIMO BOTAO 
            if contagem_pontos < 4:
                self.atualizar_status(f"{contagem_pontos}/4 pontos selecionados. Faltam {4 - contagem_pontos}.")
                self.btn_processar.config(state=tk.DISABLED)
            else:
                self.atualizar_status(f"{contagem_pontos} pontos selecionados. Pronto para processar (Passo 5).")
                self.btn_processar.config(state=tk.NORMAL)
        # MODO DE CALIBRAÇÃO - PASSO 1 
        elif self.modo_atual == "calibrando_p1":
            self.ponto_calibracao1 = (evento.x, evento.y)
            self.modo_atual = "calibrando_p2" # AVANÇA PARA PASSO 2 
            self.atualizar_status("CALIBRAÇÃO (2/2): Agora clique em um ponto com altura conhecida.")
        # MODO DE CALIBRAÇÃO - PASSO 2 
        elif self.modo_atual == "calibrando_p2":
            self.ponto_calibracao2 = (evento.x, evento.y)
            # pede ao usuario o valor real em cm 
            val_cm = simpledialog.askfloat("Entrada", f"Qual a altura REAL (em cm) do ponto clicado?", parent=self.janela_principal)
            if val_cm is not None and val_cm > 0:
                # calcula o fator de conversao : pixels por centimetros
                dist_pixel = abs(self.ponto_calibracao1[1] - self.ponto_calibracao2[1])
                self.px_por_cm = dist_pixel / val_cm
                self.atualizar_status(f"Calibrado! {self.px_por_cm:.2f} px/cm. Prossiga para selecionar pontos (Passo 4).")
                self.btn_selecionar_pontos.config(state=tk.NORMAL)
                self.modo_atual = "ocioso"
            else:
                self.ponto_calibracao2 = None; self.atualizar_status("Calibração cancelada. Tente novamente.")
        # mostra novas marcações 
        self.mostrar_frame(self.primeiro_frame.copy())

    # LIMPA MARCAÇÕES AO CLICAR COM BOTAO DIREITO 
    def ao_clicar_direito_canvas(self, evento):
        if self.modo_atual == "selecionando_pontos":
            self.pontos_analise_x = []
            self.btn_processar.config(state=tk.DISABLED)
            self.atualizar_status("Pontos de análise limpos. Selecione no mínimo 4 novos pontos.")
            self.mostrar_frame(self.primeiro_frame.copy())
            
    def iniciar_processamento(self):
        # VERIFICA SE TODAS AS ETAPAS FORAM CONCLUIDAS 
        if not self.roi:
            messagebox.showerror("Etapa Incompleta", "Por favor, selecione a área de análise (ROI) primeiro (Passo 2).")
            return
        if not self.px_por_cm:
            messagebox.showerror("Etapa Incompleta", "Por favor, complete a calibração primeiro (Passo 3).")
            return
        if len(self.pontos_analise_x) < 4:
            messagebox.showwarning("Pontos Insuficientes", f"É necessário selecionar no mínimo 4 pontos de análise.\n\nVocê selecionou apenas {len(self.pontos_analise_x)}.")
            return
        # DESABILITA TODOS OS BOTOES DURANTE O PROCESSAMENTO 
        for btn in [self.btn_abrir, self.btn_roi, self.btn_calibrar, self.btn_selecionar_pontos, self.btn_processar]:
            btn.config(state=tk.DISABLED)
        
        # SALVAR NOVO VIDEO COM AS MARCAÇÕES 
        caminho_saida = self.caminho_video.replace('.mp4', '_analisado.mp4')
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        escritor_video = cv2.VideoWriter(caminho_saida, fourcc, self.fps, (self.largura, self.altura))
        
        hsv_inferior = np.array([self.h_min.get(), self.s_min.get(), self.v_min.get()])
        hsv_superior = np.array([self.h_max.get(), self.s_max.get(), self.v_max.get()])
 
        # LEITURA DO VIDEO - FRAME 1 
        self.captura.set(cv2.CAP_PROP_POS_FRAMES, 0)
        dados_altura_cm = collections.defaultdict(list)
        total_frames = int(self.captura.get(cv2.CAP_PROP_FRAME_COUNT))
        x1, y1, x2, y2 = self.roi

        # PROCESSA CADA FRAME DO VIDEO 
        for contagem_frame in range(total_frames):
            ret, frame = self.captura.read()
            if not ret: break
            
            # recorta o frama para a ROI selecionada e aplica ol filtro de cor 
            frame_roi = frame[y1:y2, x1:x2]
            hsv = cv2.cvtColor(frame_roi, cv2.COLOR_BGR2HSV)
            mascara = cv2.inRange(hsv, hsv_inferior, hsv_superior)

            for x_orig in self.pontos_analise_x:
                x_crop = x_orig - x1 # converte a coordenada para a ROI 
                coluna = mascara[:, x_crop]
                indices_y_agua = np.where(coluna > 0)[0]
                altura_cm = 0.0
                if indices_y_agua.size > 0:
                    y_crop = np.min(indices_y_agua)
                    y_orig = y_crop + y1 # volta as coordenadas para o frame origianl 

                    # calcula a altura em cm e desenha no frame original 
                    altura_pixels = self.ponto_calibracao1[1] - y_orig
                    altura_cm = max(0, altura_pixels / self.px_por_cm)
                    cv2.circle(frame, (x_orig, y_orig), 5, (0, 0, 255), -1)
                    cv2.putText(frame, f"{altura_cm:.1f}cm", (x_orig + 10, y_orig), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
                dados_altura_cm[x_orig].append(altura_cm) # salva dados de altura 
            # escreve o frame com as marcações no novo video 
            escritor_video.write(frame)
            self.atualizar_status(f"Processando: Quadro {contagem_frame+1}/{total_frames}")
            self.janela_principal.update()
        
        # finaliza o processamento, salva video com as marcações, plota o grafico e reinicia a interface 
        escritor_video.release()
        messagebox.showinfo("Concluído", f"Processamento finalizado!\nVídeo salvo como '{caminho_saida}'")
        self.plotar_resultados(dados_altura_cm, total_frames)
        self.reiniciar_estado()
        self.atualizar_status("Processo concluído. Abra um novo vídeo para começar.")

    def plotar_resultados(self, dados, num_frames):
        plt.figure(figsize=(15, 8));
        for x, alturas in dados.items():
            plt.plot(range(num_frames), alturas, label=f'Ponto em x={x}px')
        plt.title('Variação da Altura da Água ao Longo do Tempo'); plt.xlabel('Quadro'); plt.ylabel('Altura (cm)')
        plt.legend(); plt.grid(True); plt.xlim(left=0); plt.ylim(bottom=0); plt.show()

    def reiniciar_estado(self):
        if self.captura: self.captura.release()
        self.esta_pausado = True; self.modo_atual = "ocioso"
        self.roi, self.ponto_calibracao1, self.ponto_calibracao2, self.px_por_cm = None, None, None, None
        self.pontos_analise_x = []
        for btn in [self.btn_roi, self.btn_calibrar, self.btn_selecionar_pontos, self.btn_processar]:
            btn.config(state=tk.DISABLED)
        self.btn_abrir.config(state=tk.NORMAL)
        if hasattr(self, 'canvas_video'): self.canvas_video.delete("all")

    # ATUALIZA TEXTO NA BARRA DE AJUDA AO USUARIO 
    def atualizar_status(self, texto): 
        self.label_status.config(text=texto)
        
    def ao_fechar(self):
        if self.captura: self.captura.release()
        self.janela_principal.destroy()

    # CONVERTE UM FRAME DO OPENCV PARA UMA IMAGEM QUE O TK PODE EXIBIR NA INTERFACE    
    def converter_frame_para_foto(self, frame):
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        return ImageTk.PhotoImage(image=img)

if __name__ == "__main__":
    root = tk.Tk()
    app = AnalisadorBarragem(root)
    root.mainloop()