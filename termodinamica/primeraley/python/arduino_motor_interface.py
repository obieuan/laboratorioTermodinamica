import tkinter as tk
from tkinter import ttk, scrolledtext
import serial
import serial.tools.list_ports
import threading
import csv
from datetime import datetime
import os


class MotorControlGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Control de Motor y Sensor de Presión")
        self.root.geometry("800x600")
        
        self.serial_connection = None
        self.is_reading = False
        self.csv_file = None
        self.csv_writer = None
        self.is_logging = False
        self.current_operation = None  # 'extension' o 'retraction'
        
        self.setup_gui()
        
    def setup_gui(self):
        # Frame de conexión serial
        connection_frame = ttk.LabelFrame(self.root, text="Conexión Serial", padding=10)
        connection_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(connection_frame, text="Puerto:").grid(row=0, column=0, padx=5)
        self.port_combo = ttk.Combobox(connection_frame, width=15)
        self.port_combo.grid(row=0, column=1, padx=5)
        self.refresh_ports()
        
        ttk.Button(connection_frame, text="Actualizar", 
                  command=self.refresh_ports).grid(row=0, column=2, padx=5)
        ttk.Button(connection_frame, text="Conectar", 
                  command=self.connect_serial).grid(row=0, column=3, padx=5)
        ttk.Button(connection_frame, text="Desconectar", 
                  command=self.disconnect_serial).grid(row=0, column=4, padx=5)
        
        self.connection_label = ttk.Label(connection_frame, text="Desconectado", 
                                         foreground="red")
        self.connection_label.grid(row=0, column=5, padx=10)
        
        # Frame de configuración de tiempo
        time_frame = ttk.LabelFrame(self.root, text="Configuración de Tiempo", padding=10)
        time_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(time_frame, text="Duración del movimiento (ms):").pack(side="left", padx=5)
        self.time_entry = ttk.Entry(time_frame, width=10)
        self.time_entry.insert(0, "10000")
        self.time_entry.pack(side="left", padx=5)
        
        ttk.Button(time_frame, text="Actualizar Tiempo", 
                  command=self.update_motor_time).pack(side="left", padx=10)
        
        self.time_status_label = ttk.Label(time_frame, text="", foreground="green")
        self.time_status_label.pack(side="left", padx=5)
        
        # Frame de control del motor
        control_frame = ttk.LabelFrame(self.root, text="Control del Motor", padding=20)
        control_frame.pack(fill="x", padx=10, pady=5)
        
        self.extend_btn = ttk.Button(control_frame, text="EXTENDER", 
                                     command=self.extend_motor, width=20)
        self.extend_btn.pack(side="left", padx=20, pady=10)
        
        self.retract_btn = ttk.Button(control_frame, text="RETRAER", 
                                      command=self.retract_motor, width=20)
        self.retract_btn.pack(side="left", padx=20, pady=10)
        
        # Frame de información del sensor
        sensor_frame = ttk.LabelFrame(self.root, text="Datos del Sensor", padding=10)
        sensor_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(sensor_frame, text="Presión Actual:").pack(side="left", padx=5)
        self.pressure_label = ttk.Label(sensor_frame, text="-- kPa", 
                                       font=("Arial", 16, "bold"), 
                                       foreground="blue")
        self.pressure_label.pack(side="left", padx=10)
        
        # Frame de consola
        console_frame = ttk.LabelFrame(self.root, text="Consola", padding=10)
        console_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.console_text = scrolledtext.ScrolledText(console_frame, 
                                                     height=15, 
                                                     state='disabled',
                                                     font=("Consolas", 9))
        self.console_text.pack(fill="both", expand=True)
        
        # Frame de control CSV
        csv_frame = ttk.LabelFrame(self.root, text="Registro de Datos", padding=10)
        csv_frame.pack(fill="x", padx=10, pady=5)
        
        self.csv_label = ttk.Label(csv_frame, text="CSV: Esperando comando...", 
                                  foreground="orange")
        self.csv_label.pack(side="left", padx=10)
        
        # Deshabilitar botones de control inicialmente
        self.extend_btn.config(state="disabled")
        self.retract_btn.config(state="disabled")
        
    def refresh_ports(self):
        ports = serial.tools.list_ports.comports()
        port_list = [port.device for port in ports]
        self.port_combo['values'] = port_list
        if port_list:
            self.port_combo.current(0)
    
    def connect_serial(self):
        try:
            port = self.port_combo.get()
            if not port:
                self.log_console("Error: Selecciona un puerto")
                return
            
            self.serial_connection = serial.Serial(port, 9600, timeout=1)
            self.connection_label.config(text="Conectado", foreground="green")
            self.log_console(f"Conectado a {port}")
            
            # Habilitar botones
            self.extend_btn.config(state="normal")
            self.retract_btn.config(state="normal")
            
            # Iniciar lectura de datos
            self.is_reading = True
            self.read_thread = threading.Thread(target=self.read_serial, daemon=True)
            self.read_thread.start()
            
        except Exception as e:
            self.log_console(f"Error al conectar: {str(e)}")
    
    def disconnect_serial(self):
        self.is_reading = False
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            self.connection_label.config(text="Desconectado", foreground="red")
            self.log_console("Desconectado")
            
            # Deshabilitar botones
            self.extend_btn.config(state="disabled")
            self.retract_btn.config(state="disabled")
            
        self.stop_csv()
    
    def extend_motor(self):
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.write(b'E')
            self.log_console("Comando enviado: EXTENDER")
            self.start_csv_for_operation("extension")
    
    def retract_motor(self):
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.write(b'R')
            self.log_console("Comando enviado: RETRAER")
            self.start_csv_for_operation("retraction")
    
    def update_motor_time(self):
        if self.serial_connection and self.serial_connection.is_open:
            try:
                time_ms = int(self.time_entry.get())
                if time_ms < 1000 or time_ms > 60000:
                    self.log_console("Error: El tiempo debe estar entre 1000 y 60000 ms")
                    return
                
                # Enviar comando con formato T:valor
                command = f"T:{time_ms}\n"
                self.serial_connection.write(command.encode())
                self.log_console(f"Tiempo actualizado a: {time_ms} ms")
                self.time_status_label.config(text=f"✓ {time_ms} ms configurado")
            except ValueError:
                self.log_console("Error: Ingresa un valor numérico válido")
        else:
            self.log_console("Error: No hay conexión serial")
    
    def read_serial(self):
        while self.is_reading:
            try:
                if self.serial_connection and self.serial_connection.is_open:
                    if self.serial_connection.in_waiting > 0:
                        line = self.serial_connection.readline().decode('utf-8', 
                                                                        errors='ignore').strip()
                        if line:
                            self.log_console(line)
                            
                            # Extraer presión si está en la línea
                            if "Pressure:" in line:
                                try:
                                    pressure_str = line.split("Pressure:")[1].split("kPa")[0].strip()
                                    pressure = float(pressure_str)
                                    self.root.after(0, self.update_pressure, pressure)
                                    
                                    # Guardar en CSV si está activo
                                    if self.is_logging and self.csv_writer:
                                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                                        self.csv_writer.writerow([timestamp, pressure])
                                        self.csv_file.flush()
                                except:
                                    pass
                            
                            # Detectar cuando termina la operación
                            if "completada" in line.lower() or "completado" in line.lower():
                                if self.is_logging:
                                    self.root.after(0, self.stop_csv)
            except Exception as e:
                self.log_console(f"Error de lectura: {str(e)}")
                break
    
    def update_pressure(self, pressure):
        self.pressure_label.config(text=f"{pressure:.2f} kPa")
    
    def log_console(self, message):
        def append():
            self.console_text.config(state='normal')
            self.console_text.insert(tk.END, message + '\n')
            self.console_text.see(tk.END)
            self.console_text.config(state='disabled')
        
        self.root.after(0, append)
    
    def start_csv_for_operation(self, operation_type):
        # Cerrar CSV anterior si existe
        if self.csv_file:
            self.stop_csv()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        operation_name = "extension" if operation_type == "extension" else "retraccion"
        filename = f"presion_{operation_name}_{timestamp}.csv"
        
        try:
            self.csv_file = open(filename, 'w', newline='')
            self.csv_writer = csv.writer(self.csv_file)
            self.csv_writer.writerow(['Timestamp', 'Presion (kPa)', 'Tipo'])
            self.csv_writer.writerow(['', '', operation_name])  # Fila de identificación
            self.csv_writer.writerow(['Timestamp', 'Presion (kPa)'])  # Headers de datos
            
            self.is_logging = True
            self.current_operation = operation_type
            self.csv_label.config(text=f"CSV: Registrando - {filename}", foreground="green")
            self.log_console(f"Registro CSV iniciado: {filename}")
        except Exception as e:
            self.log_console(f"Error al crear CSV: {str(e)}")
    
    def stop_csv(self):
        if self.csv_file:
            self.csv_file.close()
            self.csv_file = None
            self.csv_writer = None
            self.is_logging = False
            self.current_operation = None
            self.csv_label.config(text="CSV: Esperando comando...", foreground="orange")
            self.log_console("Registro CSV completado y guardado")
    
    def on_closing(self):
        self.disconnect_serial()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MotorControlGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
