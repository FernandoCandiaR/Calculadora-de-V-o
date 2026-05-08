import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from mpl_toolkits.mplot3d import Axes3D
from ttkthemes import ThemedStyle 
from scipy.optimize import fsolve
import customtkinter as ctk


class CatenaryAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Analisador de Vão")
        
        # ThemedStyle para setar um estilo de UI
        self.style = ThemedStyle(self.root)
        self.style.set_theme("equilux")  # "equilux" tema escro


        #Barra de menu
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=file_menu)

        file_menu.add_command(label="Abrir", command=self.open_file)
        file_menu.add_command(label="Salvar Configurações", command=self.save_to_file)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.root.destroy)

        #Coluna esquerda - Parâmetros de entrada
        self.left_frame = ctk.CTkScrollableFrame(self.root, width=400)
        self.left_frame.grid_columnconfigure(0, weight=2)
        self.left_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        ctk.CTkLabel(master=self.left_frame, text="---Parâmetros iniciais---").grid(row=0, column=0, columnspan=3, pady=10)

        ctk.CTkLabel(self.left_frame, text="Tensão axial de ruptura [kgf]")     
        ctk.CTkLabel(self.left_frame, text="T rup").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.T_rup = ctk.CTkEntry(self.left_frame, placeholder_text=7725)
        self.T_rup.grid(row=2, column=1, pady=5)
        self.T_rup.insert(0, "7725")
        
        ctk.CTkLabel(self.left_frame, text="Percentual Efetivo da Tensão Axial [%]").grid(row=3, column=0, sticky=tk.W, pady=5)     
        ctk.CTkLabel(self.left_frame, text="%").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.perc = ctk.CTkEntry(self.left_frame)
        self.perc.grid(row=4, column=1, pady=5)
        self.perc.insert(0, "20")
                
        ctk.CTkLabel(self.left_frame, text="Peso líquido do cabo [kgf/m]").grid(row=5, column=0, sticky=tk.W, pady=5)     
        ctk.CTkLabel(self.left_frame, text="p").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.p_liq = ctk.CTkEntry(self.left_frame)
        self.p_liq.grid(row=6, column=1, pady=5)
        self.p_liq.insert(0, "0.7816")
        
        ctk.CTkLabel(self.left_frame, text="Distância horizontal do vão [m]").grid(row=7, column=0, sticky=tk.W, pady=5)     
        ctk.CTkLabel(self.left_frame, text="A").grid(row=8, column=0, sticky=tk.W, pady=5)
        self.Avao = ctk.CTkEntry(self.left_frame)
        self.Avao.grid(row=8, column=1, pady=5)
        self.Avao.insert(0, "350")
        
        ctk.CTkLabel(self.left_frame, text="Diferença de altura do vão [m]").grid(row=9, column=0, sticky=tk.W, pady=5)     
        ctk.CTkLabel(self.left_frame, text="h").grid(row=10, column=0, sticky=tk.W, pady=5)
        self.h_alt = ctk.CTkEntry(self.left_frame)
        self.h_alt.grid(row=10, column=1, pady=5)
        self.h_alt.insert(0, "40")
        
        ctk.CTkLabel(self.left_frame, text="Altura do primeiro poste [m]").grid(row=11, column=0, sticky=tk.W, pady=5)     
        ctk.CTkLabel(self.left_frame, text="H poste").grid(row=12, column=0, sticky=tk.W, pady=5)
        self.H_p = ctk.CTkEntry(self.left_frame)
        self.H_p.grid(row=12, column=1, pady=5)
        self.H_p.insert(0, "30")
        
        ctk.CTkLabel(self.left_frame, text="---Parâmetros para condições com vento---").grid(row=13, column=0, columnspan=2, pady=10)
        
        ctk.CTkLabel(self.left_frame, text="Diâmetro do cabo [m]").grid(row=14, column=0, sticky=tk.W, pady=5)     
        ctk.CTkLabel(self.left_frame, text="D cabo").grid(row=15, column=0, sticky=tk.W, pady=5)
        self.D_c = ctk.CTkEntry(self.left_frame)
        self.D_c.grid(row=15, column=1, pady=5)
        self.D_c.insert(0, "0.001883")

        ctk.CTkLabel(self.left_frame, text="{Pressão calculável do vento} [kgf/m²]").grid(row=16, column=0, sticky=tk.W, pady=5)     
        ctk.CTkLabel(self.left_frame, text="q0").grid(row=17, column=0, sticky=tk.W, pady=5)
        self.q_0 = ctk.CTkEntry(self.left_frame)
        self.q_0.grid(row=17, column=1, pady=5)
        self.q_0.insert(0, "43.56")

        ctk.CTkLabel(self.left_frame, text="---Parâmetros para condições de variação de temperatura---").grid(row=18, column=0, columnspan=2, pady=10)

        ctk.CTkLabel(self.left_frame, text="Temperatura inicial [°C]").grid(row=19, column=0, sticky=tk.W, pady=5)     
        ctk.CTkLabel(self.left_frame, text="t1").grid(row=20, column=0, sticky=tk.W, pady=5)
        self.t_1 = ctk.CTkEntry(self.left_frame)
        self.t_1.grid(row=20, column=1, pady=5)
        self.t_1.insert(0, "25")

        ctk.CTkLabel(self.left_frame, text="Temperatura final [°C]").grid(row=21, column=0, sticky=tk.W, pady=5)     
        ctk.CTkLabel(self.left_frame, text="t2").grid(row=22, column=0, sticky=tk.W, pady=5)
        self.t_2 = ctk.CTkEntry(self.left_frame)
        self.t_2.grid(row=22, column=1, pady=5)
        self.t_2.insert(0, "35")

        ctk.CTkLabel(self.left_frame, text="Coeficiente de dilatação térmica do material [1/°C]").grid(row=23, column=0, sticky=tk.W, pady=5)     
        ctk.CTkLabel(self.left_frame, text="alfa t").grid(row=24, column=0, sticky=tk.W, pady=5)
        self.a_t = ctk.CTkEntry(self.left_frame)
        self.a_t.grid(row=24, column=1, pady=5)
        self.a_t.insert(0, "0.00001886")

        ctk.CTkLabel(self.left_frame, text="Módulo de Young (elasticidade) [kgf/mm²]").grid(row=25, column=0, sticky=tk.W, pady=5)     
        ctk.CTkLabel(self.left_frame, text="E").grid(row=26, column=0, sticky=tk.W, pady=5)
        self.E_yng = ctk.CTkEntry(self.left_frame)
        self.E_yng.grid(row=26, column=1, pady=5)
        self.E_yng.insert(0, "8086")

        ctk.CTkLabel(self.left_frame, text="Área transversal do cabo [mm²]").grid(row=27, column=0, sticky=tk.W, pady=5)     
        ctk.CTkLabel(self.left_frame, text="S").grid(row=28, column=0, sticky=tk.W, pady=5)
        self.S_mm = ctk.CTkEntry(self.left_frame)
        self.S_mm.grid(row=28, column=1, pady=5)
        self.S_mm.insert(0, "210.3")          

        # Centro - Viewports 2D e 3D
        self.center_panedwindow = ttk.PanedWindow(self.root, orient=tk.VERTICAL)
        self.center_panedwindow.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.center_panedwindow.rowconfigure(0, weight=1)
        self.center_panedwindow.rowconfigure(1, weight=1)

        self.fig_3d = plt.Figure()
        self.ax_3d = self.fig_3d.add_subplot(111, projection='3d')
        self.ax_3d.grid(False)
        self.canvas_3d = FigureCanvasTkAgg(self.fig_3d, master=self.center_panedwindow)
        self.canvas_3d_widget = self.canvas_3d.get_tk_widget()
        self.canvas_3d_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.fig_2d, self.ax_2d = plt.subplots()
        self.ax_2d.grid(False)
        self.canvas_2d = FigureCanvasTkAgg(self.fig_2d, master=self.center_panedwindow)
        self.canvas_2d_widget = self.canvas_2d.get_tk_widget()
        self.canvas_2d_widget.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

        self.center_panedwindow.add(self.canvas_3d_widget)
        self.center_panedwindow.add(self.canvas_2d_widget)

        # Zoom e Pan para o vieweport 2D
        self.canvas_2d.mpl_connect('button_press_event', self.on_press)
        self.canvas_2d.mpl_connect('motion_notify_event', self.on_motion)
        self.canvas_2d.mpl_connect('button_release_event', self.on_release)
        self._zooming = False
        self.canvas_2d.mpl_connect('scroll_event', self.on_scroll)        


        # Coluna da Direita
        
        self.right_frame = ctk.CTkScrollableFrame(self.root, width=300)
        self.right_frame.grid(row=0, column=0, padx=1, pady=0, sticky="nsew")
        self.right_frame.grid(row=0, column=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        ctk.CTkLabel(self.right_frame, text="Vão sem vento nem variação de T[°C]").grid(row=0, column=0, columnspan=2, pady=10)
        ctk.CTkLabel(self.right_frame, text="Vão com vento nem variação de T[°C]").grid(row=10, column=0, columnspan=2, pady=10)
        ctk.CTkLabel(self.right_frame, text="Vão sem vento com variação de T[°C]").grid(row=20, column=0, columnspan=2, pady=10)



        ttk.Button(self.right_frame, text="Calcular", command=self.calculate_catenary).grid(row=30, column=0, columnspan=2, pady=10)
        

        #Configurando a janela root para que esta se expanda verticalmente
        self.root.rowconfigure(0, weight=1)
 
                
    def calculate_catenary(self):
        try:
            #Parâmetros Gerais de Cálculo
            h = float(self.h_alt.get())
            k = float(self.perc.get())/100
            T_01 = k*float(self.T_rup.get())
            p = float(self.p_liq.get())
            C1 = T_01/p
            A = float(self.Avao.get())
            Ap1 = 2*C1*np.arcsinh(h/(2*C1*np.sinh(A/(2*C1))))
            Ae1 = A + Ap1
            x11 = (Ae1/2) - A
            Hp = float(self.H_p.get())
            kx1 = (x11/C1)
            ky1 = Hp - C1*(np.cosh(x11/C1)-1)
            theta_a1 = np.arctan(np.sinh(kx1))
            theta_b1 = np.arctan(np.sinh((A/C1)+kx1))
            m1 = h/A
            xtan1 = C1*(np.arcsinh(m1)-kx1)
            ytan1 = C1*(np.cosh(xtan1/C1 + (kx1))-1)+ky1
                     
            #Cálculos sob ação do vento
            fv = float(self.q_0.get())*float(self.D_c.get())
            if p>0:
               pr = np.sqrt(p**2 + fv**2)
            elif p<=0:
                pr= -np.sqrt(p**2 + fv**2)
            p2 = pr
            C2 = T_01/pr
            Ap2 = 2*C2*np.arcsinh(h/(2*C2*np.sinh(A/(2*C2))))
            Ae2 = A + Ap2
            x21 = (Ae2/2) - A
            kx2 = (x21/C2)
            ky2 = Hp - C2*(np.cosh(x21/C2)-1)
            gamma = np.arctan(fv/p)
            l_eixo = np.sqrt(A**2 + h**2)
            eixox = A/l_eixo
            eixoz = h/l_eixo    
            
            #Função para rotacionar o vetor v ao redor de um eixo k por um ângulo theta utilizando a fórmula de rotação de Rodrigues
            def rodrigues_rotation(v, k, gamma):
                k = k / np.linalg.norm(k)  # Ensure k is a unit vector
                cross_product = np.cross(k, v)
                rotated_vector = v * np.cos(gamma) + cross_product * np.sin(gamma) + k * np.dot(k, v) * (1 - np.cos(gamma))
                return rotated_vector            

            # Definindo o eixo de rotação e posição do pivô
            axis_of_rotation = np.array([eixox, 0, eixoz])
            pivot_point = np.array([0, 0, Hp])
            
            #Calculos para a catenária sob ação da variação de temperatura
            E = float(self.E_yng.get())
            S = float(self.S_mm.get())
            aterm = float(self.a_t.get())
            Delta = float(self.t_2.get()) - float(self.t_1.get())

            # Definindo as fun;'oes
            def D(x):
                return (1/aterm) * ((x/p2) * np.sinh((p2 * Ae1)/(2 * x)) / (C1 * np.sinh(Ae1/(2 * C1))) - 1)
            
            def V(x):
                return (1/aterm) * ((x - T_01) / (E * S)) + (Delta)
            

            #Definindo a função que representa a equação V(x) - D(x) = 0
            def equation(x):
                return V(x) - D(x)
            
            # Estimativa inicial para calcular a raiz
            initial_guess = 3000

            # Find the root using fsolve
            root = fsolve(equation, initial_guess)
            #print("Intercept at x:", root[0])
            
            C3 = root[0]/p
            p = float(self.p_liq.get())
            A = float(self.Avao.get())
            Ap3 = 2*C3*np.arcsinh(h/(2*C3*np.sinh(A/(2*C3))))
            Ae3 = A + Ap3
            x31 = (Ae3/2) - A
            #Deslocador da curva 3
            kx3 = (x31/C3)
            ky3 = Hp - C3*(np.cosh(x31/C3)-1)
            
            #Ângulos da segunda extremidade da curva 2
            theta_a2 = np.arctan(np.sinh(kx2))
            theta_b2 = np.arctan(np.sinh((A/C2)+kx2))            
            
            #Ângulos da segunda extremidade da curva 3
            theta_a3 = np.arctan(np.sinh(kx3))
            theta_b3 = np.arctan(np.sinh((A/C3)+kx3))

            xtan2 = C2*(np.arcsinh(m1)-kx2)
            ytan2 = C2*(np.cosh(xtan2/C2 + (kx2))-1)+ky2
            xtan3 = C3*(np.arcsinh(m1)-kx3)
            ytan3 = C3*(np.cosh(xtan3/C3 + (kx3))-1)+ky3
             
            #Determinação das flechas
            flex1a = m1*1 - (m1*xtan1) + ytan1
            flex1b = m1*1 + Hp
            flecha1 = flex1b-flex1a ##print
            psi = np.arctan(m1)
            flecha1_desn= flecha1*np.cos(psi)   ##print         
            #Curva sem vento sem variação de °T
            flex2a = m1*1 - (m1*xtan2) + ytan2
            flex2b = m1*1 + Hp
            flecha2 = flex2b-flex2a ##print
            flecha2_desn= flecha2*np.cos(psi)##print
            #Curva sem vento com variação de °T
            flex3a = m1*1 - (m1*xtan3) + ytan3
            flex3b = m1*1 + Hp
            flecha3 = flex3b-flex3a##print
            flecha3_desn= flecha2*np.cos(psi)##print
            
            #Vetores de tração            
            def vect2d(theta,Txx):
                Taxial = Txx*np.cos(theta)
                Txa = Txx
                Tza = Taxial*np.sin(theta)
                return [Txa,Tza]            
            def vect3d(theta,fvv,Txx):
                Taxial = Txx*np.cos(theta)
                Tx = Txx
                Ty = fvv
                Tz = Taxial*np.sin(theta)
                return [Tx,Ty,Tz]   
            
            #Vetores do cabo sem vento e sem variação de °T
            u1_2d = vect2d(theta_a1,T_01) 
            u1_3d = vect3d(theta_a1,0,T_01)
            
            v1_2d = vect2d(theta_b1,-1*T_01)
            v1_3d = vect3d(theta_b1,0,-1*T_01)
            
            #Vetores do cabo sem vento e sem variação de °T
            u2_2d = vect2d(theta_a2,T_01) 
            u2_3d = vect3d(theta_a2,fv,T_01)
            
            v2_2d = vect2d(theta_b2,-1*T_01) 
            v2_3d = vect3d(-theta_b2,0,-1*T_01)
            
            #Vetores do cabo sem vento e sem variação de °T
            u3_2d = vect2d(theta_a3,root[0]) 
            u3_3d = vect3d(theta_a3,0,root[0])
            
            v3_2d = vect2d(theta_b3,-1*root[0]) 
            v3_3d = vect3d(theta_b3,0,-1*root[0])
            
            Tax1a = 0.980665*np.linalg.norm(u1_3d)
            Tax1b = 0.980665*np.linalg.norm(v1_3d)
            Tax2a = 0.980665*np.linalg.norm(u2_3d)
            Tax2b = 0.980665*np.linalg.norm(v2_3d)            
            Tax3a = 0.980665*np.linalg.norm(u3_3d)
            Tax3b = 0.980665*np.linalg.norm(v3_3d)

            Thor1a = 0.980665*(np.abs(u1_3d[0]))
            Thor1b = 0.980665*(np.abs(v1_3d[0]))
            Thor2a = 0.980665*np.sqrt(T_01**2 + fv**2)
            Thor2b = 0.980665*np.sqrt(T_01**2 + fv**2)            
            Thor3a = 0.980665*(np.abs(u3_3d[0]))
            Thor3b = 0.980665*(np.abs(v3_3d[0]))

            Tvert1a = 0.980665*(np.abs(u1_3d[2]))
            Tvert1b = 0.980665*(np.abs(v1_3d[2])) 
            Tvert2a = 0.980665*(np.abs(u2_3d[2]))
            Tvert2b = 0.980665*(np.abs(v2_3d[2]))
            Tvert3a = 0.980665*(np.abs(u3_3d[2]))
            Tvert3b = 0.980665*(np.abs(v3_3d[2]))

            #Determinação das curvas no espaço
            
            
            #Curva 1 sem vento nem variação de T°C
            x = np.linspace(0, A, 1000)
            #y1 = C1*(np.cosh(x/C1 + (kx1))-1)+ky1
            y1 = C1*(np.cosh(x / C1 + kx1) - 1) + ky1
            ssec1 = m1*x + Hp
            #Curva 2 com vento sem variação de T°C
            y2 = C2*(np.cosh(x / C2 + kx2) - 1) + ky2
            stan2 = m1*x - (m1*xtan2) + ytan2
            ssec2 = m1*x + Hp
            
            #Curva 3 sem vento e com variação de T°C
            y3 = C3*(np.cosh(x / C3 + kx3) - 1) + ky3
            
            #Postes
            x_value1 = 0
            x_value2 = A
            z_values1 = np.linspace(0, Hp, 100)
            z_values2 = np.linspace(0, Hp+h, 100)
            
            #Comprimento da curva
            #Definindo a função
            
            def tancurv(m,xtan,ytan):
                try:
                    mm=m
                    x_tan=xtan
                    y_tan=ytan
                    return mm*x - (mm*x_tan) + y_tan
                except Exception as e:
                    # Handle exceptions if needed
                    #print(f"An error occurred: {e}")
                    return None
                
            stan1 = tancurv(m1,xtan1,ytan1)
            stan2 = tancurv(m1,xtan2,ytan2)
            stan3 = tancurv(m1,xtan3,ytan3)
            
            def dcat(VAR, aa, xx, yy):
                try:
                    CC = aa
                    kxxx = xx
                    xxx = VAR
                    return np.sinh(xxx / CC + kxxx)
                except Exception as e:
                    # Handle exceptions if needed
                    #print(f"An error occurred: {e}")
                    return None
            
            def Length1(x):
                return np.sqrt(1**2 + (dcat(x,C1,kx1,ky1))**2)
            
            #Definir domínio
            bound1 = 0
            bound2 = A
            
            # Number of intervals
            n = 1000
            
            #Cálculo pela régra do trapézio
            x_valuess = np.linspace(bound1, bound2, n+1)
            y_valuess = Length1(x_valuess)
            delta_x = (bound2 - bound1) / n
            trapezoids = (y_valuess[:-1] + y_valuess[1:]) / 2
            L1 = np.sum(trapezoids * delta_x)
            
            # #print o valor
            #print("Length of the curve:", L1)
    
            def Length2(x):
                return np.sqrt(1**2 + (dcat(x,C2,kx2,ky2))**2)
            #Cálculo pela régra do trapézio
            x_valuess = np.linspace(bound1, bound2, n+1)
            y_valuess = Length2(x_valuess)
            delta_x = (bound2 - bound1) / n
            trapezoids = (y_valuess[:-1] + y_valuess[1:]) / 2
            L2 = np.sum(trapezoids * delta_x)
            # #print o valor calculado
            #print("Length of the curve:", L2)
            
            def Length3(x):
                return np.sqrt(1**2 + (dcat(x,C3,kx3,ky3))**2)
            #Cálculo pela régra do trapézio
            x_valuess = np.linspace(bound1, bound2, n+1)
            y_valuess = Length3(x_valuess)
            delta_x = (bound2 - bound1) / n
            trapezoids = (y_valuess[:-1] + y_valuess[1:]) / 2
            L3 = np.sum(trapezoids * delta_x)
            
            # #print o valor calculado
            #print("Length of the curve:", L3)
            def draw_vector(ax, pos, vector, scale_factor, color='red', linewidth=0.5,alpha=1.0):
                """
                Desenhar um vetor no viewport 2D.
            
                Parâmetros:
                    ax (Eixos): obj de eixo Matplotlib.
                    pos (numpy.array): Posição do vetor.
                    vector (numpy.array): Vetor a ser desenhado.
                    scale_factor (float): Fator de escalonamento.
                    color (str): Cor do vetor.
            
                Returns:
                    None
                """
                arrowprops = dict(facecolor=color, edgecolor=color, linewidth=linewidth, alpha=alpha)
                ax.annotate('', xy=pos + scale_factor * vector, xytext=pos, arrowprops=arrowprops, ha='center', va='center')
    
            # Atualizar desenhos 2D e 3D
            self.ax_2d.clear()
            self.ax_2d.plot(x, y1, label='sem vento, sem variação de T°C', color='blue')
            self.ax_2d.plot(x, y2, label='com vento, sem variação de T°C', color='green')
            self.ax_2d.plot(x, y3, label='sem vento, com variação de T°C', color='brown')
            self.ax_2d.plot(x, stan1,'--',linewidth=0.5,color='blue')
            self.ax_2d.plot(x, stan2,'--',linewidth=0.5,color='green')
            self.ax_2d.plot(x, stan3,'--',linewidth=0.5,color='brown')
            self.ax_2d.plot(x, ssec1,'--',linewidth=0.5,color='orange')
            self.ax_2d.set_title('Catenárias no Plano (Viewport-2D)')
            self.ax_2d.set_xlabel('Eixo do Vão (m)')
            self.ax_2d.set_ylabel('Altura (m)')
            self.ax_2d.legend()
            #self.ax_2d.set_aspect('equal')
            sc=float(self.Avao.get())/10000
            #print(sc)
            # print('zu1')
            # print(u1_2d[1])
            
            # print('zu2')
            # print(u2_2d[1])
            
            # print('zu3')
            # print(u3_2d[1])
            
            if theta_a1>0:
                draw_vector(self.ax_2d, np.array([x_value1, Hp]), np.array(u1_2d), scale_factor=sc, color='blue', linewidth=0.001,alpha=0.5)
            elif theta_a1<0:
                draw_vector(self.ax_2d, np.array([x_value1, Hp]), np.array(u1_2d), scale_factor=sc, color='red', linewidth=0.001,alpha=1.0)
            if theta_a2>0:    
                draw_vector(self.ax_2d, np.array([x_value1, Hp]), np.array(u2_2d), scale_factor=sc, color='green',linewidth=0.001,alpha=0.5)
            elif theta_a2<0:
                draw_vector(self.ax_2d, np.array([x_value1, Hp]), np.array(u2_2d), scale_factor=sc, color='red',linewidth=0.001,alpha=1.0)
            if u3_2d[1]>0:    
                draw_vector(self.ax_2d, np.array([x_value1, Hp]), np.array(u3_2d), scale_factor=sc, color='brown',linewidth=0.001,alpha=0.5)
            elif u3_2d[1]<=0:
                draw_vector(self.ax_2d, np.array([x_value1, Hp]), np.array(u3_2d), scale_factor=sc, color='red',linewidth=0.001,alpha=1.0)
            
            
            if theta_b1>0:
                draw_vector(self.ax_2d, np.array([x_value2, Hp+h]), np.array(v1_2d), scale_factor=sc, color='blue', linewidth=0.001,alpha=0.5)
            elif theta_b1<=0:
                draw_vector(self.ax_2d, np.array([x_value2, Hp+h]), np.array(v1_2d), scale_factor=sc, color='red', linewidth=0.001,alpha=1.0)            
            if theta_b2>0:
                draw_vector(self.ax_2d, np.array([x_value2, Hp+h]), np.array(v2_2d), scale_factor=sc, color='green',linewidth=0.001,alpha=0.5)
            elif theta_b2<=0:
                draw_vector(self.ax_2d, np.array([x_value2, Hp+h]), np.array(v2_2d), scale_factor=sc, color='red',linewidth=0.001,alpha=1.0)
            if theta_b3>0:
                draw_vector(self.ax_2d, np.array([x_value2, Hp+h]), np.array(v3_2d), scale_factor=sc, color='brown',linewidth=0.001,alpha=0.5)
            elif theta_b3<=0:
                draw_vector(self.ax_2d, np.array([x_value2, Hp+h]), np.array(v3_2d), scale_factor=sc, color='red',linewidth=0.001,alpha=1.0)
    
            self.canvas_2d.draw()
            
            
            #Definindo a curva como um conjunto de pontos no  espaço 3D
            points_original = np.vstack([x, np.zeros_like(x), y2])
            
            
            #Transformar a curva para a origem de rotação e depois, transformar de volta
            #Rotação pelo método de Rodrigues
            points_translated = points_original - np.array([pivot_point]).T
            points_rotated = np.array([rodrigues_rotation(point, axis_of_rotation, gamma) for point in points_translated.T]).T
            points_rotated += np.array([pivot_point]).T 
            
            self.ax_3d.clear()
            self.ax_3d.plot(x, np.zeros_like(x), y1, label='sem vento, sem variação de T°C',color='blue')
            
            self.ax_3d.plot([x_value1] * len(z_values1), np.zeros_like(z_values1), z_values1, color='grey')
            self.ax_3d.plot([x_value2] * len(z_values2), np.zeros_like(z_values2), z_values2, color='grey')
            
            
            #Desenha a curva rotacionada
            self.ax_3d.plot(points_rotated[0], points_rotated[1], points_rotated[2], label='com vento, sem variação de T°C', color='green')
            self.ax_3d.plot(x, np.zeros_like(x), y3, label='sem vento, com variação de T°C',color='brown')
            self.ax_3d.set_title('Catenárias no Espaço (Viewport-3D)')
            self.ax_3d.set_xlabel('Eixo do Vão (m)')
            self.ax_3d.set_ylabel('Eixo do plano do vento (m)')
            self.ax_3d.set_zlabel('Altura (m)')
            self.ax_3d.legend()
            self.ax_3d.axes.set_ylim3d(bottom=0.5*(-A/2), top=0.5*(A/2))
            self.ax_3d.set_aspect('equal')
            self.ax_3d.plot(x, np.zeros_like(x),stan1,'--',linewidth=0.5)
            self.ax_3d.plot(x, np.zeros_like(x),ssec1,'--',linewidth=0.5)
            self.canvas_2d.draw()
            self.canvas_3d.draw()
            

            #Após criar o subplot 3D, ajusta-se o aspect ratio e normaliza o layout
            self.ax_3d.set_box_aspect([2, 1, 1])  # Ajustar [2, 1, 1] de acordo com a preferência
            self.fig_3d.tight_layout()
         
            ctk.CTkLabel(self.right_frame, text="Comprimento").grid(row=1, column=0, sticky=tk.W, pady=5)
            self.length_label1 = ctk.CTkLabel(self.right_frame, text=f"L1={L1:.3f}"' metros')
            self.length_label1.grid(row=1, column=1, pady=5)
            ctk.CTkLabel(self.right_frame, text="Flecha").grid(row=2, column=0, sticky=tk.W, pady=5)
            self.flex_label2 = ctk.CTkLabel(self.right_frame, text=f"f={flecha1:.3f}"' metros')
            self.flex_label2.grid(row=2, column=1, pady=5)
            ctk.CTkLabel(self.right_frame, text="Flecha Inclinada").grid(row=3, column=0, sticky=tk.W, pady=5)
            self.flex_label2 = ctk.CTkLabel(self.right_frame, text=f"f={flecha1_desn:.3f}"' metros')
            self.flex_label2.grid(row=3, column=1, pady=5)
            ctk.CTkLabel(self.right_frame, text="Tração Axial 1").grid(row=4, column=0, sticky=tk.W, pady=5)
            self.flex_label2 = ctk.CTkLabel(self.right_frame, text=f"Tax1={Tax1a:.3f}"' daN')
            self.flex_label2.grid(row=4, column=1, pady=5)
            ctk.CTkLabel(self.right_frame, text="***Tração horizontal 1").grid(row=5, column=0, sticky=tk.W, pady=5)
            self.flex_label2 = ctk.CTkLabel(self.right_frame, text=f"Th1={Thor1a:.3f}"' daN')
            self.flex_label2.grid(row=5, column=1, pady=5)
            ctk.CTkLabel(self.right_frame, text="***Tração vertical 1").grid(row=6, column=0, sticky=tk.W, pady=5)
            self.flex_label2 = ctk.CTkLabel(self.right_frame, text=f"Tv1={Tvert1a:.3f}"' daN')
            self.flex_label2.grid(row=6, column=1, pady=5)
            ctk.CTkLabel(self.right_frame, text="Tração Axial 2").grid(row=7, column=0, sticky=tk.W, pady=5)
            self.flex_label2 = ctk.CTkLabel(self.right_frame, text=f"Tax1={Tax1b:.3f}"' daN')
            self.flex_label2.grid(row=7, column=1, pady=5)
            ctk.CTkLabel(self.right_frame, text="***Tração horizontal 2").grid(row=8, column=0, sticky=tk.W, pady=5)
            self.flex_label2 = ctk.CTkLabel(self.right_frame, text=f"Th1={Thor1b:.3f}"' daN')
            self.flex_label2.grid(row=8, column=1, pady=5)
            ctk.CTkLabel(self.right_frame, text="***Tração vertical 2").grid(row=9, column=0, sticky=tk.W, pady=5)
            self.flex_label2 = ctk.CTkLabel(self.right_frame, text=f"Tv1={Tvert1b:.3f}"' daN')
            self.flex_label2.grid(row=9, column=1, pady=5)
            
            ctk.CTkLabel(self.right_frame, text="Comprimento").grid(row=11, column=0, sticky=tk.W, pady=5)
            self.length_label1 = ctk.CTkLabel(self.right_frame, text=f"L2={L2:.3f}"' metros')
            self.length_label1.grid(row=11, column=1, pady=5)
            ctk.CTkLabel(self.right_frame, text="Flecha").grid(row=12, column=0, sticky=tk.W, pady=5)
            self.flex_label2 = ctk.CTkLabel(self.right_frame, text=f"f={flecha2:.3f}"' metros')
            self.flex_label2.grid(row=12, column=1, pady=5)
            ctk.CTkLabel(self.right_frame, text="Flecha Inclinada").grid(row=13, column=0, sticky=tk.W, pady=5)
            self.flex_label2 = ctk.CTkLabel(self.right_frame, text=f"f={flecha2_desn:.3f}"' metros')
            self.flex_label2.grid(row=13, column=1, pady=5)
            ctk.CTkLabel(self.right_frame, text="Tração Axial 1").grid(row=14, column=0, sticky=tk.W, pady=5)
            self.flex_label2 = ctk.CTkLabel(self.right_frame, text=f"Tax1={Tax2a:.3f}"' daN')
            self.flex_label2.grid(row=14, column=1, pady=5)
            ctk.CTkLabel(self.right_frame, text="***Tração horizontal 1").grid(row=15, column=0, sticky=tk.W, pady=5)
            self.flex_label2 = ctk.CTkLabel(self.right_frame, text=f"Th1={Thor2a:.3f}"' daN')
            self.flex_label2.grid(row=15, column=1, pady=5)
            ctk.CTkLabel(self.right_frame, text="***Tração vertical 1").grid(row=16, column=0, sticky=tk.W, pady=5)
            self.flex_label2 = ctk.CTkLabel(self.right_frame, text=f"Tv1={Tvert2a:.3f}"' daN')
            self.flex_label2.grid(row=16, column=1, pady=5)
            ctk.CTkLabel(self.right_frame, text="Tração Axial 2").grid(row=17, column=0, sticky=tk.W, pady=5)
            self.flex_label2 = ctk.CTkLabel(self.right_frame, text=f"Tax1={Tax2b:.3f}"' daN')
            self.flex_label2.grid(row=17, column=1, pady=5)
            ctk.CTkLabel(self.right_frame, text="***Tração horizontal 2").grid(row=18, column=0, sticky=tk.W, pady=5)
            self.flex_label2 = ctk.CTkLabel(self.right_frame, text=f"Th1={Thor2b:.3f}"' daN')
            self.flex_label2.grid(row=18, column=1, pady=5)
            ctk.CTkLabel(self.right_frame, text="***Tração vertical 2").grid(row=19, column=0, sticky=tk.W, pady=5)
            self.flex_label2 = ctk.CTkLabel(self.right_frame, text=f"Tv1={Tvert2b:.3f}"' daN')
            self.flex_label2.grid(row=19, column=1, pady=5)
            
            ctk.CTkLabel(self.right_frame, text="Comprimento").grid(row=21, column=0, sticky=tk.W, pady=5)
            self.length_label1 = ctk.CTkLabel(self.right_frame, text=f"L3={L3:.3f}"' metros')
            self.length_label1.grid(row=21, column=1, pady=5)
            ctk.CTkLabel(self.right_frame, text="Flecha").grid(row=22, column=0, sticky=tk.W, pady=5)
            self.flex_label2 = ctk.CTkLabel(self.right_frame, text=f"f={flecha3:.3f}"' metros')
            self.flex_label2.grid(row=22, column=1, pady=5)
            ctk.CTkLabel(self.right_frame, text="Flecha Inclinada").grid(row=23, column=0, sticky=tk.W, pady=5)
            self.flex_label2 = ctk.CTkLabel(self.right_frame, text=f"f={flecha3_desn:.3f}"' metros')
            self.flex_label2.grid(row=23, column=1, pady=5)
            ctk.CTkLabel(self.right_frame, text="Tração Axial 1").grid(row=24, column=0, sticky=tk.W, pady=5)
            self.flex_label2 = ctk.CTkLabel(self.right_frame, text=f"Tax1={Tax3a:.3f}"' daN')
            self.flex_label2.grid(row=24, column=1, pady=5)
            ctk.CTkLabel(self.right_frame, text="***Tração horizontal 1").grid(row=25, column=0, sticky=tk.W, pady=5)
            self.flex_label2 = ctk.CTkLabel(self.right_frame, text=f"Th1={Thor3a:.3f}"' daN')
            self.flex_label2.grid(row=25, column=1, pady=5)
            ctk.CTkLabel(self.right_frame, text="***Tração vertical 1").grid(row=26, column=0, sticky=tk.W, pady=5)
            self.flex_label2 = ctk.CTkLabel(self.right_frame, text=f"Tv1={Tvert3a:.3f}"' daN')
            self.flex_label2.grid(row=26, column=1, pady=5)
            ctk.CTkLabel(self.right_frame, text="Tração Axial 2").grid(row=27, column=0, sticky=tk.W, pady=5)
            self.flex_label2 = ctk.CTkLabel(self.right_frame, text=f"Tax1={Tax3b:.3f}"' daN')
            self.flex_label2.grid(row=27, column=1, pady=5)
            ctk.CTkLabel(self.right_frame, text="***Tração horizontal 2").grid(row=28, column=0, sticky=tk.W, pady=5)
            self.flex_label2 = ctk.CTkLabel(self.right_frame, text=f"Th1={Thor3b:.3f}"' daN')
            self.flex_label2.grid(row=28, column=1, pady=5)
            ctk.CTkLabel(self.right_frame, text="***Tração vertical 2").grid(row=29, column=0, sticky=tk.W, pady=5)
            self.flex_label2 = ctk.CTkLabel(self.right_frame, text=f"Tv1={Tvert3b:.3f}"' daN')
            self.flex_label2.grid(row=29, column=1, pady=5)
            

        
        except ValueError:
            tk.messagebox.showerror("Erro!", "Entrada inválida")
            return
      

        
        
    def on_press(self, event):
        if event.button == 1:
            self._panning = True
            self._pan_start = (event.x, event.y)
        elif event.button == 'up':
            self._zooming = True
            self._zoom_start = (event.x, event.y)

    def on_motion(self, event):
        if hasattr(self, '_panning') and self._panning:
            dx = event.x - self._pan_start[0]
            dy = event.y - self._pan_start[1]
            self.ax_2d.set_xlim(self.ax_2d.get_xlim()[0] - dx, self.ax_2d.get_xlim()[1] - dx)
            self.ax_2d.set_ylim(self.ax_2d.get_ylim()[0] - dy, self.ax_2d.get_ylim()[1] - dy)
            self.canvas_2d.draw()
            self._pan_start = (event.x, event.y)

    def on_release(self, event):
        if hasattr(self, '_panning') and self._panning:
            delattr(self, '_panning')


    
    # Métodos para a função de Zoom in e Zoom out
    def zoom_in_2d(self, factor):
        self._zoom_2d(factor)
    
    def zoom_out_2d(self, factor):
        self._zoom_2d(1/factor)
    
    def _zoom_2d(self, factor):
        xlim = self.ax_2d.get_xlim()
        ylim = self.ax_2d.get_ylim()
        x_center = np.mean(xlim)
        y_center = np.mean(ylim)
        self.ax_2d.set_xlim((xlim - x_center) * factor + x_center)
        self.ax_2d.set_ylim((ylim - y_center) * factor + y_center)
        self.canvas_2d.draw()
        
        # Alterações no método On Scroll
    def on_scroll(self, event):
        if event.button == 'up':
            self.zoom_in_2d(1.2)
        elif event.button == 'down':
            self.zoom_out_2d(0.8)
            


    def zoom_in_2d(self, factor):
        xlim = self.ax_2d.get_xlim()
        ylim = self.ax_2d.get_ylim()
        new_xlim = (
            (xlim[0] + xlim[1]) / 2 - (xlim[1] - xlim[0]) / (2 * factor),
            (xlim[0] + xlim[1]) / 2 + (xlim[1] - xlim[0]) / (2 * factor)
        )
        new_ylim = (
            (ylim[0] + ylim[1]) / 2 - (ylim[1] - ylim[0]) / (2 * factor),
            (ylim[0] + ylim[1]) / 2 + (ylim[1] - ylim[0]) / (2 * factor)
        )
        self.ax_2d.set_xlim(new_xlim)
        self.ax_2d.set_ylim(new_ylim)
        self.canvas_2d.draw()

    def zoom_out_2d(self,   factor):
        xlim = self.ax_2d.get_xlim()
        ylim = self.ax_2d.get_ylim()
        new_xlim = (
            (xlim[0] + xlim[1]) / 2 - (xlim[1] - xlim[0]) / (2 * factor),
            (xlim[0] + xlim[1]) / 2 + (xlim[1] - xlim[0]) / (2 * factor)
        )
        new_ylim = (
            (ylim[0] + ylim[1]) / 2 - (ylim[1] - ylim[0]) / (2 * factor),
            (ylim[0] + ylim[1]) / 2 + (ylim[1] - ylim[0]) / (2 * factor)
        )
        self.ax_2d.set_xlim(new_xlim)
        self.ax_2d.set_ylim(new_ylim)
        self.canvas_2d.draw()
        


    def open_file(self):
        file_path = tkinter.filedialog.askopenfilename(defaultextension=".ctn", filetypes=[("Arquivos de catenária", "*.ctn")])
    
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    content = file.readlines()
    
                    # Atualizar valores conforme o arquivo
                    input_values = {}
                    for line in content:
                        key_value = line.split(':')
                        if len(key_value) == 2:
                            key = key_value[0].strip()
                            value = key_value[1].strip()
                            input_values[key] = value
    
                    # Update the entry widgets
                    for key, value in input_values.items():
                        widget = getattr(self, key, None)
                        if widget:
                            widget.delete(0, tk.END)
                            widget.insert(0, value)
    
                tk.messagebox.showinfo("Configurações atualizadas", "Valores carregados desde o arquivo.")
                self.calculate_catenary()  #Recalcula e atualiza o plot de acordo com os valores carregados
                
            except Exception as e:
                tk.messagebox.showerror("Erro", f"Erro ao processar o arquivo: {e}")

    def get_input_values(self):
        # Recupera todos os valores a partir dos valores digitados nos widgets
        input_values = {
            "T_rup": self.T_rup.get(),
            "perc": self.perc.get(),
            "p_liq": self.p_liq.get(),
            "Avao": self.Avao.get(),
            "h_alt": self.h_alt.get(),
            "H_p": self.H_p.get(),
            "D_c": self.D_c.get(),
            "q_0": self.q_0.get(),
            "t_1": self.t_1.get(),
            "t_2": self.t_2.get(),
            "a_t": self.a_t.get(),
            "E_yng": self.E_yng.get(),
            "S_mm": self.S_mm.get(),
        }
        return input_values

    def save_to_file(self):
        try:
            input_values = self.get_input_values()
            file_path = tkinter.filedialog.asksaveasfilename(defaultextension=".ctn", filetypes=[("", "*.ctn")])

            if file_path:
                with open(file_path, 'w') as file:
                    for key, value in input_values.items():
                        file.write(f"{key}: {value}\n")

                tk.messagebox.showinfo("Configurações Salvas", "Valores salvos em arquivo.")

        except Exception as e:
            tk.messagebox.showerror("Error", f"Erro ao salvar o arquivo: {e}")



if __name__ == "__main__":
    root = tk.Tk()
    app = CatenaryAnalyzer(root)
    root.geometry("1200x800")  # Tamanho inicial da janela
    root.columnconfigure(1, weight=1)  # Permite que a coluna central se expanda horizontalmente
    root.mainloop()
