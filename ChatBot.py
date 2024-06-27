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
        print("Error al conectar a la base de datos:", e)
        return None

# Función para insertar un nuevo usuario
def insertar_usuario(conn, dni, nombre, apellidos, universidad, carrera):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Usuarios (Dni, Nombre, Apellidos, Universidad, Carrera) VALUES (?, ?, ?, ?, ?)", dni, nombre, apellidos, universidad, carrera)
        conn.commit()
        print("Usuario registrado correctamente.")
    except Exception as e:
        print("Error al insertar usuario en la base de datos:", e)

# Función principal del chatbot
def main():
    print("Bienvenido al Chatbot")
    print("Puedes preguntarme cosas como 'Qué es 2 + 2'")
    nombre = input("Por favor, ingresa tu nombre: ")
    apellidos = input("Ahora, ingresa tus apellidos: ")
    dni = input("Ingrese su DNI: ")
    universidad = input("Ingrese en la universidad en la que está: ")
    carrera = input("Ingrese la carrera profesional en la que usted se encuentra: ")

    # Conexión a la base de datos
    conn = conectar_bd()
    if conn:
        # Insertar usuario en la base de datos
        insertar_usuario(conn, dni, nombre, apellidos, universidad, carrera)

        while True:
            consulta = input("Escribe la consulta que quieras hacer (escribe 'salir' para terminar): ")
            if consulta.lower() == 'salir':
                print(responder_pregunta("Adiós"))
                break
            else:
                respuesta = responder_pregunta(consulta)
                print("Chatbot:", respuesta)
        conn.close()
        print("Gracias por usar el chatbot.")
    else:
        print("No se pudo conectar a la base de datos. No se registrará el usuario.")

if __name__ == "__main__":
    main()
