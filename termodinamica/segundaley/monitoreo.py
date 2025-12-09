import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports
import threading
import time
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from collections import deque

class MonitorArduino:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitor de Sistema de Bombeo")
        self.root.geometry("1200x800")
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
        
        # Historial para gráficas (últimos 50 puntos)
        self.historial_temp1 = deque(maxlen=50)
        self.historial_temp2 = deque(maxlen=50)
        self.historial_temp3 = deque(maxlen=50)
        self.historial_caudal1 = deque(maxlen=50)
        self.historial_caudal2 = deque(maxlen=50)
        self.historial_tiempo = deque(maxlen=50)
        
        self.crear_interfaz()
        
    def crear_interfaz(self):
        # ========== PANEL DE CONEXIÓN ==========
        frame_conexion = tk.Frame(self.root, bg='#2b2b2b')
        frame_conexion.pack(pady=10, padx=10, fill='x')
        
        tk.Label(frame_conexion, text="Puerto:", bg='#2b2b2b', fg='white', font=('Arial', 10)).pack(side='left', padx=5)
        
        self.combo_puertos = ttk.Combobox(frame_conexion, width=15, state='readonly')
        self.combo_puertos.pack(side='left', padx=5)
        self.actualizar_puertos()
        
        self.btn_refresh = tk.Button(frame_conexion, text="🔄", command=self.actualizar_puertos, 
                                     bg='#404040', fg='white', font=('Arial', 10))
        self.btn_refresh.pack(side='left', padx=5)
        
        self.btn_conectar = tk.Button(frame_conexion, text="Conectar", command=self.toggle_conexion,
                                      bg='#28a745', fg='white', font=('Arial', 10, 'bold'), width=12)
        self.btn_conectar.pack(side='left', padx=5)
        
        self.label_estado = tk.Label(frame_conexion, text="● Desconectado", bg='#2b2b2b', 
                                     fg='#dc3545', font=('Arial', 10, 'bold'))
        self.label_estado.pack(side='left', padx=20)
        
        # ========== PANEL DE TEMPERATURAS ==========
        frame_temp = tk.LabelFrame(self.root, text="TEMPERATURAS", bg='#363636', fg='white',
                                  font=('Arial', 12, 'bold'), padx=10, pady=10)
        frame_temp.pack(pady=10, padx=10, fill='x')
        
        self.crear_display_sensor(frame_temp, "Sensor 1 (Pin 11)", self.temp1, "°C", 0)
        self.crear_display_sensor(frame_temp, "Sensor 2 (Pin 12)", self.temp2, "°C", 1)
        self.crear_display_sensor(frame_temp, "Sensor 3 (Pin 4)", self.temp3, "°C", 2)
        
        # ========== PANEL DE CAUDALES ==========
        frame_caudal = tk.LabelFrame(self.root, text="CAUDALÍMETROS", bg='#363636', fg='white',
                                    font=('Arial', 12, 'bold'), padx=10, pady=10)
        frame_caudal.pack(pady=10, padx=10, fill='x')
        
        # Caudalímetro 1
        frame_c1 = tk.Frame(frame_caudal, bg='#363636')
        frame_c1.pack(side='left', expand=True, fill='both', padx=10)
        
        tk.Label(frame_c1, text="Caudalímetro 1 (Pin 2)", bg='#363636', fg='#ffc107',
                font=('Arial', 10, 'bold')).pack()
        
        frame_c1_data = tk.Frame(frame_c1, bg='#363636')
        frame_c1_data.pack()
        
        tk.Label(frame_c1_data, text="Caudal:", bg='#363636', fg='white',
                font=('Arial', 9)).grid(row=0, column=0, sticky='w', padx=5)
        tk.Label(frame_c1_data, textvariable=self.caudal1, bg='#363636', fg='#00ff00',
                font=('Arial', 14, 'bold')).grid(row=0, column=1, padx=5)
        tk.Label(frame_c1_data, text="L/min", bg='#363636', fg='white',
                font=('Arial', 9)).grid(row=0, column=2, sticky='w')
        
        tk.Label(frame_c1_data, text="Volumen:", bg='#363636', fg='white',
                font=('Arial', 9)).grid(row=1, column=0, sticky='w', padx=5)
        tk.Label(frame_c1_data, textvariable=self.volumen1, bg='#363636', fg='#00ff00',
                font=('Arial', 14, 'bold')).grid(row=1, column=1, padx=5)
        tk.Label(frame_c1_data, text="L", bg='#363636', fg='white',
                font=('Arial', 9)).grid(row=1, column=2, sticky='w')
        
        # Caudalímetro 2
        frame_c2 = tk.Frame(frame_caudal, bg='#363636')
        frame_c2.pack(side='left', expand=True, fill='both', padx=10)
        
        tk.Label(frame_c2, text="Caudalímetro 2 (Pin 3)", bg='#363636', fg='#ffc107',
                font=('Arial', 10, 'bold')).pack()
        
        frame_c2_data = tk.Frame(frame_c2, bg='#363636')
        frame_c2_data.pack()
        
        tk.Label(frame_c2_data, text="Caudal:", bg='#363636', fg='white',
                font=('Arial', 9)).grid(row=0, column=0, sticky='w', padx=5)
        tk.Label(frame_c2_data, textvariable=self.caudal2, bg='#363636', fg='#00ff00',
                font=('Arial', 14, 'bold')).grid(row=0, column=1, padx=5)
        tk.Label(frame_c2_data, text="L/min", bg='#363636', fg='white',
                font=('Arial', 9)).grid(row=0, column=2, sticky='w')
        
        tk.Label(frame_c2_data, text="Volumen:", bg='#363636', fg='white',
                font=('Arial', 9)).grid(row=1, column=0, sticky='w', padx=5)
        tk.Label(frame_c2_data, textvariable=self.volumen2, bg='#363636', fg='#00ff00',
                font=('Arial', 14, 'bold')).grid(row=1, column=1, padx=5)
        tk.Label(frame_c2_data, text="L", bg='#363636', fg='white',
                font=('Arial', 9)).grid(row=1, column=2, sticky='w')
        
        # ========== PANEL DE BOMBAS ==========
        frame_bombas = tk.LabelFrame(self.root, text="ESTADO DE BOMBAS", bg='#363636', fg='white',
                                    font=('Arial', 12, 'bold'), padx=10, pady=10)
        frame_bombas.pack(pady=10, padx=10, fill='x')
        
        # Bomba 1
        frame_b1 = tk.Frame(frame_bombas, bg='#363636')
        frame_b1.pack(side='left', expand=True, padx=20)
        
        tk.Label(frame_b1, text="Bomba 1", bg='#363636', fg='white',
                font=('Arial', 11, 'bold')).pack()
        tk.Label(frame_b1, textvariable=self.bomba1_estado, bg='#363636', fg='#00ff00',
                font=('Arial', 16, 'bold')).pack()
        
        # Bomba 2
        frame_b2 = tk.Frame(frame_bombas, bg='#363636')
        frame_b2.pack(side='left', expand=True, padx=20)
        
        tk.Label(frame_b2, text="Bomba 2", bg='#363636', fg='white',
                font=('Arial', 11, 'bold')).pack()
        tk.Label(frame_b2, textvariable=self.bomba2_estado, bg='#363636', fg='#00ff00',
                font=('Arial', 16, 'bold')).pack()
        
        # Botón reset volumen
        self.btn_reset = tk.Button(frame_bombas, text="Reset Volúmenes", command=self.reset_volumenes,
                                   bg='#dc3545', fg='white', font=('Arial', 10, 'bold'), 
                                   state='disabled', width=15)
        self.btn_reset.pack(side='left', expand=True, padx=20)
        
        # ========== GRÁFICAS ==========
        frame_graficas = tk.LabelFrame(self.root, text="GRÁFICAS EN TIEMPO REAL", bg='#363636', 
                                      fg='white', font=('Arial', 12, 'bold'))
        frame_graficas.pack(pady=10, padx=10, fill='both', expand=True)
        
        # Crear figura con subplots
        self.fig = Figure(figsize=(10, 4), facecolor='#363636')
        
        # Subplot temperaturas
        self.ax1 = self.fig.add_subplot(121)
        self.ax1.set_facecolor('#2b2b2b')
        self.ax1.set_title('Temperaturas', color='white')
        self.ax1.set_xlabel('Tiempo', color='white')
        self.ax1.set_ylabel('°C', color='white')
        self.ax1.tick_params(colors='white')
        self.ax1.grid(True, alpha=0.3)
        
        # Subplot caudales
        self.ax2 = self.fig.add_subplot(122)
        self.ax2.set_facecolor('#2b2b2b')
        self.ax2.set_title('Caudales', color='white')
        self.ax2.set_xlabel('Tiempo', color='white')
        self.ax2.set_ylabel('L/min', color='white')
        self.ax2.tick_params(colors='white')
        self.ax2.grid(True, alpha=0.3)
        
        self.fig.tight_layout()
        
        # Canvas para las gráficas
        self.canvas = FigureCanvasTkAgg(self.fig, frame_graficas)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        
    def crear_display_sensor(self, parent, nombre, variable, unidad, columna):
        frame = tk.Frame(parent, bg='#363636')
        frame.pack(side='left', expand=True, fill='both', padx=10)
        
        tk.Label(frame, text=nombre, bg='#363636', fg='#ffc107',
                font=('Arial', 10, 'bold')).pack()
        
        frame_valor = tk.Frame(frame, bg='#363636')
        frame_valor.pack()
        
        tk.Label(frame_valor, textvariable=variable, bg='#363636', fg='#00ff00',
                font=('Arial', 20, 'bold')).pack(side='left')
        tk.Label(frame_valor, text=unidad, bg='#363636', fg='white',
                font=('Arial', 12)).pack(side='left', padx=5)
    
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
            time.sleep(2)  # Esperar a que Arduino se reinicie
            self.is_connected = True
            self.is_monitoring = True
            
            # Actualizar interfaz
            self.btn_conectar.config(text="Desconectar", bg='#dc3545')
            self.label_estado.config(text="● Conectado", fg='#28a745')
            self.combo_puertos.config(state='disabled')
            self.btn_reset.config(state='normal')
            
            # Iniciar hilo de lectura
            self.thread_lectura = threading.Thread(target=self.leer_datos, daemon=True)
            self.thread_lectura.start()
            
            # Iniciar actualización de gráficas
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
    
    def leer_datos(self):
        buffer = ""
        datos_actuales = {}
        
        while self.is_monitoring:
            try:
                if self.serial_connection.in_waiting:
                    linea = self.serial_connection.readline().decode('utf-8', errors='ignore').strip()
                    
                    # Parsear datos
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
                        estado = linea.split(":")[1].strip()
                        datos_actuales['bomba1'] = estado
                    
                    elif "Bomba 2:" in linea:
                        estado = linea.split(":")[1].strip()
                        datos_actuales['bomba2'] = estado
                    
                    # Si tenemos un conjunto completo de datos, actualizar
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
        
        # Agregar timestamp
        if any(key in datos for key in ['temp1', 'caudal1']):
            self.historial_tiempo.append(time.time())
    
    def actualizar_graficas(self):
        if not self.is_monitoring:
            return
        
        try:
            # Limpiar gráficas
            self.ax1.clear()
            self.ax2.clear()
            
            # Configurar gráfica de temperaturas
            self.ax1.set_facecolor('#2b2b2b')
            self.ax1.set_title('Temperaturas', color='white')
            self.ax1.set_ylabel('°C', color='white')
            self.ax1.tick_params(colors='white')
            self.ax1.grid(True, alpha=0.3)
            
            if len(self.historial_tiempo) > 0:
                tiempo_relativo = [t - self.historial_tiempo[0] for t in self.historial_tiempo]
                
                if len(self.historial_temp1) > 0:
                    self.ax1.plot(tiempo_relativo, list(self.historial_temp1), 
                                 'r-', label='Sensor 1', linewidth=2)
                if len(self.historial_temp2) > 0:
                    self.ax1.plot(tiempo_relativo, list(self.historial_temp2), 
                                 'g-', label='Sensor 2', linewidth=2)
                if len(self.historial_temp3) > 0:
                    self.ax1.plot(tiempo_relativo, list(self.historial_temp3), 
                                 'b-', label='Sensor 3', linewidth=2)
                
                self.ax1.legend(facecolor='#363636', edgecolor='white', 
                              labelcolor='white', loc='upper left')
            
            # Configurar gráfica de caudales
            self.ax2.set_facecolor('#2b2b2b')
            self.ax2.set_title('Caudales', color='white')
            self.ax2.set_ylabel('L/min', color='white')
            self.ax2.tick_params(colors='white')
            self.ax2.grid(True, alpha=0.3)
            
            if len(self.historial_tiempo) > 0:
                if len(self.historial_caudal1) > 0:
                    self.ax2.plot(tiempo_relativo, list(self.historial_caudal1), 
                                 'c-', label='Caudal 1', linewidth=2)
                if len(self.historial_caudal2) > 0:
                    self.ax2.plot(tiempo_relativo, list(self.historial_caudal2), 
                                 'm-', label='Caudal 2', linewidth=2)
                
                self.ax2.legend(facecolor='#363636', edgecolor='white', 
                              labelcolor='white', loc='upper left')
            
            self.canvas.draw()
            
        except Exception as e:
            print(f"Error actualizando gráficas: {e}")
        
        # Programar siguiente actualización
        if self.is_monitoring:
            self.root.after(1000, self.actualizar_graficas)
    
    def reset_volumenes(self):
        if self.is_connected and self.serial_connection:
            try:
                self.serial_connection.write(b'r')
                messagebox.showinfo("Reset", "Comando de reset enviado")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo enviar comando:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MonitorArduino(root)
    root.mainloop()