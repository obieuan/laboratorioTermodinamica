import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports
import threading
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from collections import deque

class MonitorArduino:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitor y Control de Sistema de Bombeo")
        self.root.geometry("1800x900")
        self.root.configure(bg='#2b2b2b')
        
        # Variables
        self.serial_connection = None
        self.is_connected = False
        self.is_monitoring = False
        
        # Datos de sensores
        self.temp1 = tk.StringVar(value="--")
        self.temp2 = tk.StringVar(value="--")
        self.temp3 = tk.StringVar(value="--")
        self.caudal1 = tk.StringVar(value="--")
        self.caudal2 = tk.StringVar(value="--")
        self.volumen1 = tk.StringVar(value="--")
        self.volumen2 = tk.StringVar(value="--")
        self.bomba1_estado = tk.StringVar(value="DESCONOCIDO")
        self.bomba2_estado = tk.StringVar(value="DESCONOCIDO")
        
        # Variables de control
        self.pwm1 = tk.StringVar(value="0")
        self.pwm2 = tk.StringVar(value="0")
        self.duty1 = tk.StringVar(value="0.0")
        self.duty2 = tk.StringVar(value="0.0")
        self.modo1 = tk.StringVar(value="MANUAL")
        self.modo2 = tk.StringVar(value="MANUAL")
        self.error1 = tk.StringVar(value="--")
        self.error2 = tk.StringVar(value="--")
        
        # Historial para gráficas
        self.historial_temp1 = deque(maxlen=50)
        self.historial_temp2 = deque(maxlen=50)
        self.historial_temp3 = deque(maxlen=50)
        self.historial_caudal1 = deque(maxlen=50)
        self.historial_caudal2 = deque(maxlen=50)
        self.historial_tiempo = deque(maxlen=50)
        
        self.crear_interfaz()
        
    def crear_interfaz(self):
        # ========== PANEL DE CONEXIÓN (TOP) ==========
        frame_top = tk.Frame(self.root, bg='#2b2b2b')
        frame_top.pack(side='top', pady=10, padx=10, fill='x')
        
        tk.Label(frame_top, text="Puerto:", bg='#2b2b2b', fg='white', 
                font=('Arial', 10)).pack(side='left', padx=5)
        
        self.combo_puertos = ttk.Combobox(frame_top, width=15, state='readonly')
        self.combo_puertos.pack(side='left', padx=5)
        self.actualizar_puertos()
        
        self.btn_refresh = tk.Button(frame_top, text="🔄", command=self.actualizar_puertos, 
                                     bg='#404040', fg='white', font=('Arial', 10))
        self.btn_refresh.pack(side='left', padx=5)
        
        self.btn_conectar = tk.Button(frame_top, text="Conectar", command=self.toggle_conexion,
                                      bg='#28a745', fg='white', font=('Arial', 10, 'bold'), width=12)
        self.btn_conectar.pack(side='left', padx=5)
        
        self.label_estado = tk.Label(frame_top, text="● Desconectado", bg='#2b2b2b', 
                                     fg='#dc3545', font=('Arial', 10, 'bold'))
        self.label_estado.pack(side='left', padx=20)
        
        self.btn_emergencia = tk.Button(frame_top, text="⚠ DETENER TODO", 
                                        command=self.detener_todo,
                                        bg='#dc3545', fg='white', 
                                        font=('Arial', 10, 'bold'), state='disabled')
        self.btn_emergencia.pack(side='right', padx=5)
        
        # ========== CONTENEDOR PRINCIPAL ==========
        frame_principal = tk.Frame(self.root, bg='#2b2b2b')
        frame_principal.pack(fill='both', expand=True, padx=10, pady=5)
        
        # ========== COLUMNA 1: CONTROL DE BOMBAS ==========
        frame_col1 = tk.Frame(frame_principal, bg='#2b2b2b', width=450)
        frame_col1.pack(side='left', fill='both', expand=False, padx=(0, 5))
        frame_col1.pack_propagate(False)
        
        frame_control = tk.LabelFrame(frame_col1, text="CONTROL DE BOMBAS", 
                                     bg='#363636', fg='white', 
                                     font=('Arial', 12, 'bold'), padx=10, pady=10)
        frame_control.pack(fill='both', expand=True)
        
        # Bomba 1
        frame_b1 = tk.LabelFrame(frame_control, text="BOMBA 1 - Circuito Caliente", 
                                bg='#404040', fg='#ffc107', 
                                font=('Arial', 10, 'bold'), padx=15, pady=10)
        frame_b1.pack(fill='both', expand=True, padx=5, pady=(5, 10))
        
        tk.Label(frame_b1, text="Caudal Deseado (L/min):", bg='#404040', fg='white',
                font=('Arial', 9)).pack(anchor='w', pady=(0, 5))
        
        self.slider_setpoint1 = tk.Scale(frame_b1, from_=0, to=10, resolution=0.1,
                                         orient='horizontal', bg='#404040', fg='white',
                                         font=('Arial', 9), length=380, 
                                         command=self.actualizar_setpoint1,
                                         state='disabled')
        self.slider_setpoint1.pack(fill='x', padx=5)
        
        self.label_setpoint1 = tk.Label(frame_b1, text="Setpoint: 0.0 L/min", 
                                       bg='#404040', fg='#00ff00', 
                                       font=('Arial', 11, 'bold'))
        self.label_setpoint1.pack(anchor='w', padx=5, pady=5)
        
        # Separador
        ttk.Separator(frame_b1, orient='horizontal').pack(fill='x', pady=8)
        
        # Info de control
        info_frame1 = tk.Frame(frame_b1, bg='#404040')
        info_frame1.pack(fill='x', padx=5)
        
        # Fila 1: PWM y Ciclo
        row1 = tk.Frame(info_frame1, bg='#404040')
        row1.pack(fill='x', pady=2)
        
        tk.Label(row1, text="PWM:", bg='#404040', fg='white',
                font=('Arial', 9), width=6, anchor='w').pack(side='left')
        tk.Label(row1, textvariable=self.pwm1, bg='#404040', fg='#00ff00',
                font=('Arial', 11, 'bold'), width=4, anchor='center').pack(side='left', padx=5)
        
        tk.Label(row1, text="Ciclo:", bg='#404040', fg='white',
                font=('Arial', 9), width=6, anchor='w').pack(side='left', padx=(20, 0))
        tk.Label(row1, textvariable=self.duty1, bg='#404040', fg='#00ff00',
                font=('Arial', 11, 'bold'), width=6, anchor='center').pack(side='left', padx=5)
        tk.Label(row1, text="%", bg='#404040', fg='white',
                font=('Arial', 9)).pack(side='left')
        
        # Fila 2: Modo y Error
        row2 = tk.Frame(info_frame1, bg='#404040')
        row2.pack(fill='x', pady=2)
        
        tk.Label(row2, text="Modo:", bg='#404040', fg='white',
                font=('Arial', 9), width=6, anchor='w').pack(side='left')
        tk.Label(row2, textvariable=self.modo1, bg='#404040', fg='#ffc107',
                font=('Arial', 11, 'bold'), width=8, anchor='w').pack(side='left', padx=5)
        
        tk.Label(row2, text="Error:", bg='#404040', fg='white',
                font=('Arial', 9), width=6, anchor='w').pack(side='left', padx=(20, 0))
        tk.Label(row2, textvariable=self.error1, bg='#404040', fg='#ff6b6b',
                font=('Arial', 11, 'bold'), width=8, anchor='w').pack(side='left', padx=5)
        
        # Bomba 2
        frame_b2 = tk.LabelFrame(frame_control, text="BOMBA 2 - Circuito Frío", 
                                bg='#404040', fg='#17a2b8', 
                                font=('Arial', 10, 'bold'), padx=15, pady=10)
        frame_b2.pack(fill='both', expand=True, padx=5, pady=(5, 10))
        
        tk.Label(frame_b2, text="Caudal Deseado (L/min):", bg='#404040', fg='white',
                font=('Arial', 9)).pack(anchor='w', pady=(0, 5))
        
        self.slider_setpoint2 = tk.Scale(frame_b2, from_=0, to=10, resolution=0.1,
                                         orient='horizontal', bg='#404040', fg='white',
                                         font=('Arial', 9), length=380,
                                         command=self.actualizar_setpoint2,
                                         state='disabled')
        self.slider_setpoint2.pack(fill='x', padx=5)
        
        self.label_setpoint2 = tk.Label(frame_b2, text="Setpoint: 0.0 L/min", 
                                       bg='#404040', fg='#00ff00', 
                                       font=('Arial', 11, 'bold'))
        self.label_setpoint2.pack(anchor='w', padx=5, pady=5)
        
        ttk.Separator(frame_b2, orient='horizontal').pack(fill='x', pady=8)
        
        info_frame2 = tk.Frame(frame_b2, bg='#404040')
        info_frame2.pack(fill='x', padx=5)
        
        row3 = tk.Frame(info_frame2, bg='#404040')
        row3.pack(fill='x', pady=2)
        
        tk.Label(row3, text="PWM:", bg='#404040', fg='white',
                font=('Arial', 9), width=6, anchor='w').pack(side='left')
        tk.Label(row3, textvariable=self.pwm2, bg='#404040', fg='#00ff00',
                font=('Arial', 11, 'bold'), width=4, anchor='center').pack(side='left', padx=5)
        
        tk.Label(row3, text="Ciclo:", bg='#404040', fg='white',
                font=('Arial', 9), width=6, anchor='w').pack(side='left', padx=(20, 0))
        tk.Label(row3, textvariable=self.duty2, bg='#404040', fg='#00ff00',
                font=('Arial', 11, 'bold'), width=6, anchor='center').pack(side='left', padx=5)
        tk.Label(row3, text="%", bg='#404040', fg='white',
                font=('Arial', 9)).pack(side='left')
        
        row4 = tk.Frame(info_frame2, bg='#404040')
        row4.pack(fill='x', pady=2)
        
        tk.Label(row4, text="Modo:", bg='#404040', fg='white',
                font=('Arial', 9), width=6, anchor='w').pack(side='left')
        tk.Label(row4, textvariable=self.modo2, bg='#404040', fg='#ffc107',
                font=('Arial', 11, 'bold'), width=8, anchor='w').pack(side='left', padx=5)
        
        tk.Label(row4, text="Error:", bg='#404040', fg='white',
                font=('Arial', 9), width=6, anchor='w').pack(side='left', padx=(20, 0))
        tk.Label(row4, textvariable=self.error2, bg='#404040', fg='#ff6b6b',
                font=('Arial', 11, 'bold'), width=8, anchor='w').pack(side='left', padx=5)
        
        # ========== COLUMNA 2: TEMPERATURAS Y CAUDALES ==========
        frame_col2 = tk.Frame(frame_principal, bg='#2b2b2b', width=450)
        frame_col2.pack(side='left', fill='both', expand=False, padx=5)
        frame_col2.pack_propagate(False)
        
        # --- TEMPERATURAS ---
        frame_temp = tk.LabelFrame(frame_col2, text="TEMPERATURAS", 
                                  bg='#363636', fg='white',
                                  font=('Arial', 12, 'bold'), padx=15, pady=10)
        frame_temp.pack(fill='x', pady=(0, 10))
        
        # Temperatura 1
        temp1_frame = tk.Frame(frame_temp, bg='#363636')
        temp1_frame.pack(fill='x', pady=8)
        
        tk.Label(temp1_frame, text="Entrada Caliente (Pin 11)", bg='#363636', fg='#ffc107',
                font=('Arial', 9, 'bold')).pack(anchor='w')
        
        temp1_val = tk.Frame(temp1_frame, bg='#363636')
        temp1_val.pack(fill='x')
        
        tk.Label(temp1_val, textvariable=self.temp1, bg='#363636', fg='#00ff00',
                font=('Arial', 24, 'bold'), width=8, anchor='e').pack(side='left')
        tk.Label(temp1_val, text="°C", bg='#363636', fg='white',
                font=('Arial', 14)).pack(side='left', padx=5)
        
        # Temperatura 2
        temp2_frame = tk.Frame(frame_temp, bg='#363636')
        temp2_frame.pack(fill='x', pady=8)
        
        tk.Label(temp2_frame, text="Salida Caliente (Pin 12)", bg='#363636', fg='#ffc107',
                font=('Arial', 9, 'bold')).pack(anchor='w')
        
        temp2_val = tk.Frame(temp2_frame, bg='#363636')
        temp2_val.pack(fill='x')
        
        tk.Label(temp2_val, textvariable=self.temp2, bg='#363636', fg='#00ff00',
                font=('Arial', 24, 'bold'), width=8, anchor='e').pack(side='left')
        tk.Label(temp2_val, text="°C", bg='#363636', fg='white',
                font=('Arial', 14)).pack(side='left', padx=5)
        
        # Temperatura 3
        temp3_frame = tk.Frame(frame_temp, bg='#363636')
        temp3_frame.pack(fill='x', pady=8)
        
        tk.Label(temp3_frame, text="Circuito Frío (Pin 4)", bg='#363636', fg='#17a2b8',
                font=('Arial', 9, 'bold')).pack(anchor='w')
        
        temp3_val = tk.Frame(temp3_frame, bg='#363636')
        temp3_val.pack(fill='x')
        
        tk.Label(temp3_val, textvariable=self.temp3, bg='#363636', fg='#00ff00',
                font=('Arial', 24, 'bold'), width=8, anchor='e').pack(side='left')
        tk.Label(temp3_val, text="°C", bg='#363636', fg='white',
                font=('Arial', 14)).pack(side='left', padx=5)
        
        # --- CAUDALÍMETROS ---
        frame_caudal = tk.LabelFrame(frame_col2, text="CAUDALÍMETROS", 
                                    bg='#363636', fg='white',
                                    font=('Arial', 12, 'bold'), padx=15, pady=10)
        frame_caudal.pack(fill='both', expand=True)
        
        # Caudalímetro 1
        caudal1_frame = tk.Frame(frame_caudal, bg='#363636')
        caudal1_frame.pack(fill='x', pady=8)
        
        tk.Label(caudal1_frame, text="Circuito Caliente (Pin 2)", bg='#363636', fg='#ffc107',
                font=('Arial', 9, 'bold')).pack(anchor='w')
        
        c1_row1 = tk.Frame(caudal1_frame, bg='#363636')
        c1_row1.pack(fill='x', pady=2)
        
        tk.Label(c1_row1, text="Caudal:", bg='#363636', fg='white',
                font=('Arial', 9), width=10, anchor='w').pack(side='left')
        tk.Label(c1_row1, textvariable=self.caudal1, bg='#363636', fg='#00ff00',
                font=('Arial', 16, 'bold'), width=8, anchor='e').pack(side='left')
        tk.Label(c1_row1, text="L/min", bg='#363636', fg='white',
                font=('Arial', 10)).pack(side='left', padx=5)
        
        c1_row2 = tk.Frame(caudal1_frame, bg='#363636')
        c1_row2.pack(fill='x', pady=2)
        
        tk.Label(c1_row2, text="Volumen:", bg='#363636', fg='white',
                font=('Arial', 9), width=10, anchor='w').pack(side='left')
        tk.Label(c1_row2, textvariable=self.volumen1, bg='#363636', fg='#00ff00',
                font=('Arial', 16, 'bold'), width=8, anchor='e').pack(side='left')
        tk.Label(c1_row2, text="L", bg='#363636', fg='white',
                font=('Arial', 10)).pack(side='left', padx=5)
        
        ttk.Separator(frame_caudal, orient='horizontal').pack(fill='x', pady=10)
        
        # Caudalímetro 2
        caudal2_frame = tk.Frame(frame_caudal, bg='#363636')
        caudal2_frame.pack(fill='x', pady=8)
        
        tk.Label(caudal2_frame, text="Circuito Frío (Pin 3)", bg='#363636', fg='#17a2b8',
                font=('Arial', 9, 'bold')).pack(anchor='w')
        
        c2_row1 = tk.Frame(caudal2_frame, bg='#363636')
        c2_row1.pack(fill='x', pady=2)
        
        tk.Label(c2_row1, text="Caudal:", bg='#363636', fg='white',
                font=('Arial', 9), width=10, anchor='w').pack(side='left')
        tk.Label(c2_row1, textvariable=self.caudal2, bg='#363636', fg='#00ff00',
                font=('Arial', 16, 'bold'), width=8, anchor='e').pack(side='left')
        tk.Label(c2_row1, text="L/min", bg='#363636', fg='white',
                font=('Arial', 10)).pack(side='left', padx=5)
        
        c2_row2 = tk.Frame(caudal2_frame, bg='#363636')
        c2_row2.pack(fill='x', pady=2)
        
        tk.Label(c2_row2, text="Volumen:", bg='#363636', fg='white',
                font=('Arial', 9), width=10, anchor='w').pack(side='left')
        tk.Label(c2_row2, textvariable=self.volumen2, bg='#363636', fg='#00ff00',
                font=('Arial', 16, 'bold'), width=8, anchor='e').pack(side='left')
        tk.Label(c2_row2, text="L", bg='#363636', fg='white',
                font=('Arial', 10)).pack(side='left', padx=5)
        
        # Botón reset
        self.btn_reset = tk.Button(frame_caudal, text="Reset Volúmenes", 
                                   command=self.reset_volumenes,
                                   bg='#dc3545', fg='white', font=('Arial', 10, 'bold'), 
                                   state='disabled', width=20)
        self.btn_reset.pack(pady=15)
        
        # ========== COLUMNA 3: GRÁFICAS ==========
        frame_col3 = tk.Frame(frame_principal, bg='#2b2b2b')
        frame_col3.pack(side='left', fill='both', expand=True, padx=(5, 0))
        
        frame_graficas = tk.LabelFrame(frame_col3, text="GRÁFICAS EN TIEMPO REAL", 
                                      bg='#363636', fg='white', 
                                      font=('Arial', 12, 'bold'))
        frame_graficas.pack(fill='both', expand=True)
        
        self.fig = Figure(figsize=(8, 8), facecolor='#363636')
        
        self.ax1 = self.fig.add_subplot(211)
        self.ax1.set_facecolor('#2b2b2b')
        self.ax1.set_title('Temperaturas', color='white', fontsize=12, fontweight='bold')
        self.ax1.set_xlabel('Tiempo (s)', color='white')
        self.ax1.set_ylabel('°C', color='white')
        self.ax1.tick_params(colors='white')
        self.ax1.grid(True, alpha=0.3)
        
        self.ax2 = self.fig.add_subplot(212)
        self.ax2.set_facecolor('#2b2b2b')
        self.ax2.set_title('Caudales', color='white', fontsize=12, fontweight='bold')
        self.ax2.set_xlabel('Tiempo (s)', color='white')
        self.ax2.set_ylabel('L/min', color='white')
        self.ax2.tick_params(colors='white')
        self.ax2.grid(True, alpha=0.3)
        
        self.fig.tight_layout(pad=3.0)
        
        self.canvas = FigureCanvasTkAgg(self.fig, frame_graficas)
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)
        
    def actualizar_puertos(self):
        puertos = serial.tools.list_ports.comports()
        lista_puertos = [puerto.device for puerto in puertos]
        self.combo_puertos['values'] = lista_puertos
        if lista_puertos:
            self.combo_puertos.current(0)
    
    def toggle_conexion(self):
        if not self.is_connected:
            self.conectar()
        else:
            self.desconectar()
    
    def conectar(self):
        puerto = self.combo_puertos.get()
        if not puerto:
            messagebox.showerror("Error", "Selecciona un puerto COM")
            return
        
        try:
            self.serial_connection = serial.Serial(puerto, 115200, timeout=1)
            time.sleep(2)
            self.is_connected = True
            self.is_monitoring = True
            
            self.btn_conectar.config(text="Desconectar", bg='#dc3545')
            self.label_estado.config(text="● Conectado", fg='#28a745')
            self.combo_puertos.config(state='disabled')
            self.btn_reset.config(state='normal')
            self.btn_emergencia.config(state='normal')
            self.slider_setpoint1.config(state='normal')
            self.slider_setpoint2.config(state='normal')
            
            self.thread_lectura = threading.Thread(target=self.leer_datos, daemon=True)
            self.thread_lectura.start()
            
            self.actualizar_graficas()
            
        except Exception as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar:\n{str(e)}")
    
    def desconectar(self):
        self.is_monitoring = False
        time.sleep(0.5)
        
        if self.serial_connection:
            self.serial_connection.close()
        
        self.is_connected = False
        self.btn_conectar.config(text="Conectar", bg='#28a745')
        self.label_estado.config(text="● Desconectado", fg='#dc3545')
        self.combo_puertos.config(state='readonly')
        self.btn_reset.config(state='disabled')
        self.btn_emergencia.config(state='disabled')
        self.slider_setpoint1.config(state='disabled')
        self.slider_setpoint2.config(state='disabled')
    
    def actualizar_setpoint1(self, valor):
        valor_float = float(valor)
        self.label_setpoint1.config(text=f"Setpoint: {valor_float:.1f} L/min")
        if self.is_connected:
            comando = f"S1:{valor_float}\n"
            try:
                self.serial_connection.write(comando.encode())
            except Exception as e:
                print(f"Error enviando setpoint 1: {e}")
    
    def actualizar_setpoint2(self, valor):
        valor_float = float(valor)
        self.label_setpoint2.config(text=f"Setpoint: {valor_float:.1f} L/min")
        if self.is_connected:
            comando = f"S2:{valor_float}\n"
            try:
                self.serial_connection.write(comando.encode())
            except Exception as e:
                print(f"Error enviando setpoint 2: {e}")
    
    def detener_todo(self):
        if self.is_connected:
            try:
                self.serial_connection.write(b"OFF\n")
                self.slider_setpoint1.set(0)
                self.slider_setpoint2.set(0)
                messagebox.showwarning("Detenido", "Todas las bombas han sido detenidas")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo detener:\n{str(e)}")
    
    def reset_volumenes(self):
        if self.is_connected and self.serial_connection:
            try:
                self.serial_connection.write(b'r\n')
                messagebox.showinfo("Reset", "Volúmenes reiniciados")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo enviar comando:\n{str(e)}")
    
    def leer_datos(self):
        datos_actuales = {}
        
        while self.is_monitoring:
            try:
                if self.serial_connection.in_waiting:
                    linea = self.serial_connection.readline().decode('utf-8', errors='ignore').strip()
                    
                    if "Sensor 1 (pin11):" in linea:
                        try:
                            temp = linea.split(":")[1].replace("°C", "").replace("C", "").strip()
                            datos_actuales['temp1'] = float(temp)
                        except:
                            pass
                    
                    elif "Sensor 2 (pin12):" in linea:
                        try:
                            temp = linea.split(":")[1].replace("°C", "").replace("C", "").strip()
                            datos_actuales['temp2'] = float(temp)
                        except:
                            pass
                    
                    elif "Sensor 3 (pin4):" in linea:
                        try:
                            temp = linea.split(":")[1].replace("°C", "").replace("C", "").strip()
                            datos_actuales['temp3'] = float(temp)
                        except:
                            pass
                    
                    elif "Caudal 1 (pin2):" in linea:
                        try:
                            partes = linea.split("|")
                            caudal = partes[0].split(":")[1].replace("L/min", "").strip()
                            volumen = partes[1].split(":")[1].replace("L", "").strip()
                            datos_actuales['caudal1'] = float(caudal)
                            datos_actuales['volumen1'] = float(volumen)
                        except:
                            pass
                    
                    elif "Caudal 2 (pin3):" in linea:
                        try:
                            partes = linea.split("|")
                            caudal = partes[0].split(":")[1].replace("L/min", "").strip()
                            volumen = partes[1].split(":")[1].replace("L", "").strip()
                            datos_actuales['caudal2'] = float(caudal)
                            datos_actuales['volumen2'] = float(volumen)
                        except:
                            pass
                    
                    elif "Bomba 1:" in linea:
                        try:
                            partes = linea.split("|")
                            estado = partes[0].split(":")[1].strip()
                            pwm_str = partes[1].split(":")[1].strip()
                            pwm = pwm_str.split("(")[0].strip()
                            duty = pwm_str.split("(")[1].replace("%)", "").strip()
                            modo = partes[2].split(":")[1].strip()
                            
                            datos_actuales['bomba1'] = estado
                            datos_actuales['pwm1'] = pwm
                            datos_actuales['duty1'] = duty
                            datos_actuales['modo1'] = modo
                        except:
                            pass
                    
                    elif "Bomba 2:" in linea:
                        try:
                            partes = linea.split("|")
                            estado = partes[0].split(":")[1].strip()
                            pwm_str = partes[1].split(":")[1].strip()
                            pwm = pwm_str.split("(")[0].strip()
                            duty = pwm_str.split("(")[1].replace("%)", "").strip()
                            modo = partes[2].split(":")[1].strip()
                            
                            datos_actuales['bomba2'] = estado
                            datos_actuales['pwm2'] = pwm
                            datos_actuales['duty2'] = duty
                            datos_actuales['modo2'] = modo
                        except:
                            pass
                    
                    elif "Setpoint 1:" in linea:
                        try:
                            error = linea.split("Error:")[1].strip()
                            datos_actuales['error1'] = error
                        except:
                            pass
                    
                    elif "Setpoint 2:" in linea:
                        try:
                            error = linea.split("Error:")[1].strip()
                            datos_actuales['error2'] = error
                        except:
                            pass
                    
                    if "========================================" in linea and datos_actuales:
                        self.actualizar_display(datos_actuales)
                        datos_actuales = {}
                        
            except Exception as e:
                print(f"Error leyendo datos: {e}")
                time.sleep(0.1)
    
    def actualizar_display(self, datos):
        if 'temp1' in datos:
            self.temp1.set(f"{datos['temp1']:.2f}")
            self.historial_temp1.append(datos['temp1'])
        
        if 'temp2' in datos:
            self.temp2.set(f"{datos['temp2']:.2f}")
            self.historial_temp2.append(datos['temp2'])
        
        if 'temp3' in datos:
            self.temp3.set(f"{datos['temp3']:.2f}")
            self.historial_temp3.append(datos['temp3'])
        
        if 'caudal1' in datos:
            self.caudal1.set(f"{datos['caudal1']:.3f}")
            self.historial_caudal1.append(datos['caudal1'])
        
        if 'caudal2' in datos:
            self.caudal2.set(f"{datos['caudal2']:.3f}")
            self.historial_caudal2.append(datos['caudal2'])
        
        if 'volumen1' in datos:
            self.volumen1.set(f"{datos['volumen1']:.3f}")
        
        if 'volumen2' in datos:
            self.volumen2.set(f"{datos['volumen2']:.3f}")
        
        if 'bomba1' in datos:
            self.bomba1_estado.set(datos['bomba1'])
        
        if 'bomba2' in datos:
            self.bomba2_estado.set(datos['bomba2'])
        
        if 'pwm1' in datos:
            self.pwm1.set(datos['pwm1'])
        
        if 'pwm2' in datos:
            self.pwm2.set(datos['pwm2'])
        
        if 'duty1' in datos:
            self.duty1.set(datos['duty1'])
        
        if 'duty2' in datos:
            self.duty2.set(datos['duty2'])
        
        if 'modo1' in datos:
            self.modo1.set(datos['modo1'])
        
        if 'modo2' in datos:
            self.modo2.set(datos['modo2'])
        
        if 'error1' in datos:
            self.error1.set(datos['error1'])
        else:
            if self.modo1.get() == "MANUAL":
                self.error1.set("--")
        
        if 'error2' in datos:
            self.error2.set(datos['error2'])
        else:
            if self.modo2.get() == "MANUAL":
                self.error2.set("--")
        
        if any(key in datos for key in ['temp1', 'caudal1']):
            self.historial_tiempo.append(time.time())
    
    def actualizar_graficas(self):
        if not self.is_monitoring:
            return
        
        try:
            self.ax1.clear()
            self.ax2.clear()
            
            self.ax1.set_facecolor('#2b2b2b')
            self.ax1.set_title('Temperaturas', color='white', fontsize=12, fontweight='bold')
            self.ax1.set_xlabel('Tiempo (s)', color='white')
            self.ax1.set_ylabel('°C', color='white')
            self.ax1.tick_params(colors='white')
            self.ax1.grid(True, alpha=0.3)
            
            if len(self.historial_tiempo) > 0:
                tiempo_relativo = [t - self.historial_tiempo[0] for t in self.historial_tiempo]
                
                if len(self.historial_temp1) > 0:
                    self.ax1.plot(tiempo_relativo, list(self.historial_temp1), 
                                 'r-', label='T1 (Entrada)', linewidth=2)
                if len(self.historial_temp2) > 0:
                    self.ax1.plot(tiempo_relativo, list(self.historial_temp2), 
                                 'g-', label='T2 (Salida)', linewidth=2)
                if len(self.historial_temp3) > 0:
                    self.ax1.plot(tiempo_relativo, list(self.historial_temp3), 
                                 'b-', label='T3 (Frío)', linewidth=2)
                
                self.ax1.legend(facecolor='#363636', edgecolor='white', 
                              labelcolor='white', loc='best')
            
            self.ax2.set_facecolor('#2b2b2b')
            self.ax2.set_title('Caudales', color='white', fontsize=12, fontweight='bold')
            self.ax2.set_xlabel('Tiempo (s)', color='white')
            self.ax2.set_ylabel('L/min', color='white')
            self.ax2.tick_params(colors='white')
            self.ax2.grid(True, alpha=0.3)
            
            if len(self.historial_tiempo) > 0:
                if len(self.historial_caudal1) > 0:
                    self.ax2.plot(tiempo_relativo, list(self.historial_caudal1), 
                                 'c-', label='Q1 (Caliente)', linewidth=2)
                if len(self.historial_caudal2) > 0:
                    self.ax2.plot(tiempo_relativo, list(self.historial_caudal2), 
                                 'm-', label='Q2 (Frío)', linewidth=2)
                
                self.ax2.legend(facecolor='#363636', edgecolor='white', 
                              labelcolor='white', loc='best')
            
            self.fig.tight_layout(pad=3.0)
            self.canvas.draw()
            
        except Exception as e:
            print(f"Error actualizando gráficas: {e}")
        
        if self.is_monitoring:
            self.root.after(1000, self.actualizar_graficas)

if __name__ == "__main__":
    root = tk.Tk()
    app = MonitorArduino(root)
    root.mainloop()