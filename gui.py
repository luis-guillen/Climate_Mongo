import os
from db import get_db
from forecast import get_city_forecast
from weather_api import get_location_weather, get_city_weather, get_location_name
from utils import validar_contrasena
import tkinter as tk
from tkinter import messagebox
import webview
from mapa_clima import mostrar_mapa_clima, mostrar_mapa_espana, seleccionar_imagen
from PIL import Image, ImageTk

class VentanaClima(tk.Frame):
    def __init__(self, master, username):
        super().__init__(master)
        self.master = master
        self.username = username

        self.master.title("Aplicación de Clima")
        self.master.geometry('600x400')
        self.master.minsize(height=300, width=500)

        self.create_widgets()
        self.grid(sticky="nsew")
        self.load_user_location()

    def create_widgets(self):
        # Widgets de la interfaz principal
        self.label_ciudad = tk.Label(self, text="Ciudad:", font=('Comic Sans MS', 12))
        self.entry_ciudad = tk.Entry(self, font=('Comic Sans MS', 12))
        self.button_buscar = tk.Button(self, text="Buscar Clima", command=self.obtener_clima)
        self.button_prediccion = tk.Button(self, text="Obtener Predicción", command=self.obtener_prediccion)

        self.label_ciudad.grid(column=0, row=0, padx=5, pady=5)
        self.entry_ciudad.grid(column=1, row=0, padx=5, pady=5)
        self.button_buscar.grid(column=2, row=0, padx=5, pady=5)
        self.button_prediccion.grid(column=3, row=0, padx=5, pady=5)  # Añadido el botón para la predicción

        self.label_temp = tk.Label(self, text='Temperatura:', font=('Impact', 20))
        self.label_temp.grid(column=0, row=1, padx=5, pady=5)
        self.label_temp_dato = tk.Label(self, font=('Impact', 20))
        self.label_temp_dato.grid(column=1, row=1, padx=5, pady=5)

        self.button_obtener_ubicacion = tk.Button(self, text="Obtener Clima de Ubicación Actual", command=self.show_webview)
        self.button_obtener_ubicacion.grid(column=0, row=2, columnspan=3, padx=5, pady=5)

        # Widgets para mostrar la ubicación y temperatura actual
        self.label_ubicacion_actual = tk.Label(self, text="Ubicación Actual:", font=('Comic Sans MS', 12))
        self.label_ubicacion_actual.grid(column=0, row=3, padx=5, pady=5)
        self.label_ubicacion_nombre = tk.Label(self, font=('Comic Sans MS', 12))
        self.label_ubicacion_nombre.grid(column=1, row=3, padx=5, pady=5)
        self.label_ubicacion_temp = tk.Label(self, font=('Impact', 20))
        self.label_ubicacion_temp.grid(column=2, row=3, padx=5, pady=5)

        # Botón para mostrar el mapa del clima
        self.label_capital = tk.Label(self, text="Introduce Capital:", font=('Comic Sans MS', 12))
        self.entry_capital = tk.Entry(self, font=('Comic Sans MS', 12))
        self.button_mostrar_mapa = tk.Button(self, text="Ver Mapa del Clima", command=self.mostrar_mapa)
        self.button_mapa_espana = tk.Button(self, text="Mapa España", command=self.mostrar_mapa_espana)

        self.label_capital.grid(column=0, row=4, padx=5, pady=5)
        self.entry_capital.grid(column=1, row=4, padx=5, pady=5)
        self.button_mostrar_mapa.grid(column=2, row=4, padx=5, pady=5)
        self.button_mapa_espana.grid(column=3, row=4, padx=5, pady=5)

    def obtener_clima(self):
        ciudad = self.entry_ciudad.get().strip().capitalize()
        temperature = get_city_weather(ciudad)

        if temperature is not None:
            self.label_temp_dato.config(text=f"{temperature}°C")
        else:
            self.label_temp_dato.config(text="No disponible")

    def obtener_prediccion(self):
        ciudad = self.entry_ciudad.get().strip().capitalize()
        ciudad = ciudad.upper()
        if ciudad:
            prediccion = get_city_forecast(ciudad)
            if prediccion:
                self.mostrar_prediccion(prediccion)
            else:
                messagebox.showerror("Error", "No se pudo obtener la predicción para la ciudad proporcionada.")
        else:
            messagebox.showerror("Error", "Por favor, introduce una ciudad válida.")

    def mostrar_prediccion(self, prediccion):
        ventana_prediccion = tk.Toplevel(self.master)
        ventana_prediccion.title("Predicción del Clima")

        for i, dia in enumerate(prediccion):
            dia_label = tk.Label(ventana_prediccion, text=f"Día {i + 1}: {dia['date']}", font=('Comic Sans MS', 12))
            temp_label = tk.Label(ventana_prediccion,
                                  text=f"Temp Media: {dia['temp_avg']}°C",
                                  font=('Comic Sans MS', 12))
            clima_label = tk.Label(ventana_prediccion, text=f"Clima: {dia['weather']}", font=('Comic Sans MS', 12))

            # Seleccionar y redimensionar la imagen correspondiente al clima
            imagen_path = seleccionar_imagen(dia['weather'])
            imagen = Image.open(imagen_path)
            imagen = imagen.resize((50, 50), Image.LANCZOS)  # Redimensionar la imagen
            imagen_clima = ImageTk.PhotoImage(imagen)
            imagen_label = tk.Label(ventana_prediccion, image=imagen_clima)
            imagen_label.image = imagen_clima  # Guardar una referencia para evitar que la imagen sea recolectada por el garbage collector

            dia_label.grid(row=i, column=0, padx=5, pady=5)
            temp_label.grid(row=i, column=1, padx=5, pady=5)
            clima_label.grid(row=i, column=2, padx=5, pady=5)
            imagen_label.grid(row=i, column=3, padx=5, pady=5)  # Columna para la imagen

    def mostrar_mapa(self):
        capital = self.entry_capital.get().strip().capitalize()
        if capital:
            mapa_path = mostrar_mapa_clima(capital)
            if mapa_path:
                webview.create_window('Mapa del Clima', mapa_path)
                webview.start()
            else:
                messagebox.showerror("Error", "No se pudo generar el mapa para la capital proporcionada.")
        else:
            messagebox.showerror("Error", "Por favor, introduce una capital válida.")

    def mostrar_mapa_espana(self):
        mapa_path = mostrar_mapa_espana()
        if mapa_path:
            webview.create_window('Mapa de España', mapa_path)
            webview.start()

    def show_webview(self):
        class Api:
            def __init__(self, ventana_clima):
                self.ventana_clima = ventana_clima

            def send_location(self, lat, lon):
                temperature = get_location_weather(lat, lon)
                if temperature is not None:
                    self.ventana_clima.save_user_location(lat, lon)

                    location_name = get_location_name(lat, lon)
                    if location_name is not None:
                        self.ventana_clima.label_ubicacion_nombre.config(text=f"{location_name}")
                        self.ventana_clima.label_ubicacion_temp.config(text=f"{temperature}°C")

        current_dir = os.path.abspath(os.getcwd())
        html_file = os.path.join(current_dir, "location.html")

        if os.path.exists(html_file):
            api_instance = Api(self)
            window = webview.create_window('Obtener Ubicación', html_file, js_api=api_instance)
            webview.start()
        else:
            messagebox.showerror("Error", f"No se pudo cargar el archivo HTML: {html_file}")

    def save_user_location(self, lat, lon):
        db = get_db()
        users_collection = db["usuarios"]

        location_name = get_location_name(lat, lon)

        users_collection.update_one(
            {"username": self.username},
            {"$set": {
                "location": {"lat": lat, "lon": lon},
                "location_name": location_name
            }},
            upsert=True
        )

    def load_user_location(self):
        db = get_db()
        users_collection = db["usuarios"]
        user = users_collection.find_one({"username": self.username})

        if user and "location" in user:
            lat = user["location"]["lat"]
            lon = user["location"]["lon"]
            temperature = get_location_weather(lat, lon)
            location_name = user.get("location_name", "Desconocida")

            if temperature is not None:
                self.label_ubicacion_nombre.config(text=f"{location_name}")
                self.label_ubicacion_temp.config(text=f"{temperature}°C")

# Función para registrar un nuevo usuario
def registrar_usuario():
    def realizar_registro():
        username = entry_registro_username.get()
        password = entry_registro_password.get()

        if not username or not password:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if not validar_contrasena(password):
            messagebox.showerror("Error",
                                 "La contraseña debe tener al menos 8 caracteres, incluyendo letras y números.")
            return

        db = get_db()
        usuarios = db["usuarios"]

        if usuarios.find_one({"username": username}):
            messagebox.showerror("Error", "¡El usuario ya existe!")
        else:
            usuarios.insert_one({"username": username, "password": password})
            messagebox.showinfo("Registro exitoso", "¡Usuario registrado correctamente!")
            ventana_registro.destroy()
            ventana_login.deiconify()

    ventana_login.withdraw()
    ventana_registro = tk.Toplevel()
    ventana_registro.title("Registro de Usuario")

    label_registro_username = tk.Label(ventana_registro, text="Usuario:")
    entry_registro_username = tk.Entry(ventana_registro)
    label_registro_password = tk.Label(ventana_registro, text="Contraseña:")
    entry_registro_password = tk.Entry(ventana_registro, show="*")

    button_registro_realizar = tk.Button(ventana_registro, text="Registrarse", command=realizar_registro)
    button_registro_cancelar = tk.Button(ventana_registro, text="Cancelar",
                                         command=lambda: [ventana_registro.destroy(), ventana_login.deiconify()])

    label_registro_username.grid(row=0, column=0, padx=10, pady=5)
    entry_registro_username.grid(row=0, column=1, padx=10, pady=5)
    label_registro_password.grid(row=1, column=0, padx=10, pady=5)
    entry_registro_password.grid(row=1, column=1, padx=10, pady=5)
    button_registro_realizar.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="we")
    button_registro_cancelar.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")


# Función para abrir la ventana principal después del inicio de sesión exitoso
def abrir_ventana_principal(username):
    ventana_login.destroy()
    ventana_principal = tk.Tk()
    ventana_clima = VentanaClima(ventana_principal, username)
    ventana_clima.mainloop()


# Función para manejar el inicio de sesión
def iniciar_sesion():
    username = entry_username.get()
    password = entry_password.get()

    db = get_db()
    usuarios = db["usuarios"]

    usuario = usuarios.find_one({"username": username, "password": password})
    if usuario:
        abrir_ventana_principal(username)
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")


# Ventana de inicio de sesión
ventana_login = tk.Tk()
ventana_login.title("Inicio de Sesión")

label_username = tk.Label(ventana_login, text="Usuario:")
entry_username = tk.Entry(ventana_login)
label_password = tk.Label(ventana_login, text="Contraseña:")
entry_password = tk.Entry(ventana_login, show="*")

button_iniciar_sesion = tk.Button(ventana_login, text="Iniciar Sesión", command=iniciar_sesion)
button_registrarse = tk.Button(ventana_login, text="Registrarse", command=registrar_usuario)

label_username.grid(row=0, column=0, padx=10, pady=5)
entry_username.grid(row=0, column=1, padx=10, pady=5)
label_password.grid(row=1, column=0, padx=10, pady=5)
entry_password.grid(row=1, column=1, padx=10, pady=5)
button_iniciar_sesion.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="we")
button_registrarse.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")

ventana_login.mainloop()
