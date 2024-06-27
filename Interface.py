import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
import pyodbc
import random

# Respuestas predefinidas del chatbot
Mis_preguntas = {
    "Hola": ["¡Hola! ¿En qué puedo ayudarte?"],
    "Cómo estás": ["Estoy bien, gracias por preguntar.", "Ahora mismo, muy bien la verdad"],
    "¿Quién es el presidente de Estados Unidos?": ["El presidente de Estados Unidos es Joe Biden."],
    "¿Cuándo comenzó la Segunda Guerra Mundial?": ["La Segunda Guerra Mundial comenzó el 1 de septiembre de 1939."],
    "¿Cuál es la fórmula química del agua?": ["La fórmula química del agua es H2O."],
    "Quién eres": ["Soy un chatbot creado en Python.", "Puedes llamarme ChatBot.", "Soy un programa diseñado para chatear contigo."],
    "Cuál es tu color favorito": ["Mi color favorito es el azul.", "No tengo color favorito, soy un programa de computadora.", "Nunca he visto colores, pero me gusta el concepto de azul."],
    "Cuál es tu comida favorita": ["Mi comida favorita es la electricidad.", "No como, pero me parece interesante la pizza.", "Soy un chatbot, no tengo preferencias alimenticias."],
    "Cuál es tu pasatiempo favorito": ["Me gusta charlar contigo.", "¡Resolviendo problemas lógicos!", "Soy un chatbot, no tengo pasatiempos como los humanos."],
    "Por qué eres tan guapo": ["Gracias por el cumplido, pero soy solo un programa de computadora.", "¡Eres muy amable! Pero en realidad, no tengo apariencia física.", "¡Jaja! Gracias, pero no tengo una apariencia física como tú."],
    "Default": ["Lo siento, no entiendo eso.", "¿Podrías repetirlo, por favor?", "No estoy seguro de entender. ¿Puedes ser más claro?"]
}

# Función para que el chatbot responda
def responder_pregunta(pregunta):
    pregunta = pregunta.capitalize()  # Convertir la primera letra a mayúscula
    if pregunta in Mis_preguntas:
        return random.choice(Mis_preguntas[pregunta])
    else:
        return random.choice(Mis_preguntas["Default"])

# Función para conectar a la base de datos
def conectar_bd():
    server = 'DESKTOP-33KRJ7K\\SQLPRIMARIO'  # Nombre del servidor de SQL Server
    database = 'CS'         # Nombre de tu base de datos
    username = 'Alejandro'  # Usuario de SQL Server
    password = '147123'     # Contraseña de SQL Server
    try:
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        return conn
    except Exception as e:
        messagebox.showerror("Error de conexión", f"Error al conectar a la base de datos:\n{e}")
        return None

# Función para insertar un nuevo usuario
def insertar_usuario(conn, dni, nombre, apellidos, universidad, carrera):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Usuarios (Dni, Nombre, Apellidos, Universidad, Carrera) VALUES (?, ?, ?, ?, ?)", dni, nombre, apellidos, universidad, carrera)
        conn.commit()
        messagebox.showinfo("Registro exitoso", "Usuario registrado correctamente.")
    except Exception as e:
        messagebox.showerror("Error de registro", f"Error al insertar usuario en la base de datos:\n{e}")

# Función para manejar la consulta del usuario
def procesar_consulta(consulta_entry, chat_log, conn):
    consulta = consulta_entry.get().strip()
    if consulta.lower() == 'salir':
        respuesta = responder_pregunta("Adiós")
        chat_log.insert(tk.END, "Tú: " + consulta + "\n")
        chat_log.insert(tk.END, "Chatbot: " + respuesta + "\n\n")
        consulta_entry.delete(0, tk.END)
        return
    else:
        respuesta = responder_pregunta(consulta)
        chat_log.insert(tk.END, "Tú: " + consulta + "\n")
        chat_log.insert(tk.END, "Chatbot: " + respuesta + "\n\n")
        consulta_entry.delete(0, tk.END)

# Función principal del chatbot
def main():
    # Crear la ventana principal
    ventana = tk.Tk()
    ventana.title("Chatbot Interfaz")
    ventana.geometry("600x500")

    # Frame para la conversación
    frame_conversacion = tk.Frame(ventana, bg='#f0f0f0')
    frame_conversacion.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    # Área de texto con scroll para la conversación
    chat_log = scrolledtext.ScrolledText(frame_conversacion, wrap=tk.WORD, width=60, height=15)
    chat_log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Frame para la entrada de consulta
    frame_consulta = tk.Frame(ventana, bg='#f0f0f0')
    frame_consulta.pack(pady=10, padx=10, fill=tk.BOTH)

    # Etiqueta y entrada para la consulta
    tk.Label(frame_consulta, text="Escribe tu consulta:", bg='#f0f0f0').pack(side=tk.LEFT)
    consulta_entry = tk.Entry(frame_consulta, width=50)
    consulta_entry.pack(side=tk.LEFT, padx=10)

    # Botón para enviar la consulta
    enviar_btn = tk.Button(frame_consulta, text="Enviar", bg='#4CAF50', fg='white', command=lambda: procesar_consulta(consulta_entry, chat_log, conn))
    enviar_btn.pack(side=tk.LEFT)

    # Conexión a la base de datos
    conn = conectar_bd()
    if conn:
        # Pedir datos del usuario al inicio
        messagebox.showinfo("Bienvenida", "Bienvenido al Chatbot")
        nombre = simpledialog.askstring("Nombre", "Por favor, ingresa tu nombre:")
        apellidos = simpledialog.askstring("Apellidos", "Ahora, ingresa tus apellidos:")
        dni = simpledialog.askstring("DNI", "Ingrese su DNI:")
        universidad = simpledialog.askstring("Universidad", "Ingrese la universidad en la que está:")
        carrera = simpledialog.askstring("Carrera", "Ingrese la carrera profesional en la que usted se encuentra:")

        # Insertar usuario en la base de datos
        insertar_usuario(conn, dni, nombre, apellidos, universidad, carrera)

        # Iniciar la ventana principal
        ventana.mainloop()
        conn.close()
        print("Gracias por usar el chatbot.")
    else:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos. No se registrará el usuario.")

if __name__ == "__main__":
    main()
