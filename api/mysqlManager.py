import mysql.connector
from mysql.connector import Error

class mysqlManager:
        def __init__(self)->None:
            self.connection = None 
            
        def iniciar_sesion(self,correo, contrasena):
            try:
                connection = mysql.connector.connect(
                    host='mysql-29b3c4f7-chatyforodb.h.aivencloud.com',
                    port=26304,
                    user='avnadmin',
                    password='AVNS_cmGIRvjscOE68heqsJy',
                    database='defaultdb'
                )

                if connection.is_connected():
                    print("Conexión exitosa a la base de datos.")

                    cursor = connection.cursor()

                    # Consulta para verificar el usuario
                    sql_select_query = """SELECT id FROM usuarios WHERE correo = %s AND contrasena = %s"""
                    cursor.execute(sql_select_query, (correo, contrasena))
                    result = cursor.fetchone()

                    if result:
                        print("Inicio de sesión exitoso.")
                        return result[0]  # Retorna el ID del usuario
                    else:
                        print("Correo o contraseña incorrectos.")
                        return None

            except Error as e:
                print(f"Error al conectar a MySQL: {e}")

            finally:
                if 'connection' in locals() and connection.is_connected():
                    cursor.close()
                    connection.close()

        def insertar_pregunta(self,usuario_id, nombre, tema_id, pregunta, contenido):
            try:
                connection = mysql.connector.connect(
                    host='mysql-29b3c4f7-chatyforodb.h.aivencloud.com',
                    port=26304,
                    user='avnadmin',
                    password='AVNS_cmGIRvjscOE68heqsJy',
                    database='defaultdb'
                )

                if connection.is_connected():
                    print("Conexión exitosa a la base de datos.")

                    cursor = connection.cursor()

                    # Consulta SQL para insertar una nueva pregunta
                    sql_insert_query = """INSERT INTO pregunta_foro (nombre, usuario_id, tema_id, pregunta, contenido) 
                                        VALUES (%s, %s, %s, %s, %s)"""
                    record = (nombre, usuario_id, tema_id, pregunta, contenido)

                    cursor.execute(sql_insert_query, record)
                    connection.commit()  # Confirmar los cambios
                    print("Pregunta agregada exitosamente.")

            except mysql.connector.Error as e:
                print(f"Error al insertar datos en MySQL: {e}")

            finally:
                if 'connection' in locals() and connection.is_connected():
                    cursor.close()
                    connection.close()

        def insertar_respuesta(self,usuario_id, nombre, pregunta_id, contenido):
            try:
                connection = mysql.connector.connect(
                    host='mysql-29b3c4f7-chatyforodb.h.aivencloud.com',
                    port=26304,
                    user='avnadmin',
                    password='AVNS_cmGIRvjscOE68heqsJy',
                    database='defaultdb'
                )

                if connection.is_connected():
                    print("Conexión exitosa a la base de datos.")

                    cursor = connection.cursor()

                    # Consulta SQL para insertar una nueva respuesta
                    sql_insert_query = """INSERT INTO respuestas_foro (nombre, usuario_id, contenido, pregunta_id) 
                                        VALUES (%s, %s, %s, %s)"""
                    record = (nombre, usuario_id, contenido, pregunta_id)

                    cursor.execute(sql_insert_query, record)
                    connection.commit()  # Confirmar los cambios
                    print("Respuesta agregada exitosamente.")

            except Error as e:
                print(f"Error al insertar datos en MySQL: {e}")

            finally:
                if 'connection' in locals() and connection.is_connected():
                    cursor.close()
                    connection.close()
                    
        def insertar_usuario(self,nombre, correo, contrasena):
            try:
                connection = mysql.connector.connect(
                    host='mysql-29b3c4f7-chatyforodb.h.aivencloud.com',
                    port=26304,
                    user='avnadmin',
                    password='AVNS_cmGIRvjscOE68heqsJy',
                    database='defaultdb'
                )

                if connection.is_connected():
                    cursor = connection.cursor()
                    sql_insert_query = """INSERT INTO usuarios (nombre, correo, contrasena) VALUES (%s, %s, %s)"""
                    cursor.execute(sql_insert_query, (nombre, correo, contrasena))
                    connection.commit()
                    print("Usuario agregado exitosamente.")

            except Error as e:
                print(f"Error al agregar usuario: {e}")

            finally:
                if 'connection' in locals() and connection.is_connected():
                    cursor.close()
                    connection.close()
                    
        def eliminar_usuario(self,usuario_id):
            try:
                connection = mysql.connector.connect(
                    host='mysql-29b3c4f7-chatyforodb.h.aivencloud.com',
                    port=26304,
                    user='avnadmin',
                    password='AVNS_cmGIRvjscOE68heqsJy',
                    database='defaultdb'
                )

                if connection.is_connected():
                    cursor = connection.cursor()
                    sql_delete_query = """DELETE FROM usuarios WHERE id = %s"""
                    cursor.execute(sql_delete_query, (usuario_id,))
                    connection.commit()

                    if cursor.rowcount > 0:
                        print("Usuario eliminado exitosamente.")
                    else:
                        print("No se encontró un usuario con ese ID.")

            except Error as e:
                print(f"Error al eliminar usuario: {e}")

            finally:
                if 'connection' in locals() and connection.is_connected():
                    cursor.close()
                    connection.close()
                    
        def insertar_tema(self,tema):
            try:
                connection = mysql.connector.connect(
                    host='mysql-29b3c4f7-chatyforodb.h.aivencloud.com',
                    port=26304,
                    user='avnadmin',
                    password='AVNS_cmGIRvjscOE68heqsJy',
                    database='defaultdb'
                )

                if connection.is_connected():
                    cursor = connection.cursor()
                    sql_insert_query = """INSERT INTO temas (tema) VALUES (%s)"""
                    cursor.execute(sql_insert_query, (tema,))  # Aquí se corrigió el paso de argumento
                    connection.commit()
                    print("Tema agregado exitosamente.")

            except Error as e:
                print(f"Error al agregar tema: {e}")

            finally:
                if 'connection' in locals() and connection.is_connected():
                    cursor.close()
                    connection.close()
                    
        def obtener_preguntas_y_respuestas(imprimir=False):
            try:
                connection = mysql.connector.connect(
                    host='mysql-29b3c4f7-chatyforodb.h.aivencloud.com',
                    port=26304,
                    user='avnadmin',
                    password='AVNS_cmGIRvjscOE68heqsJy',
                    database='defaultdb'
                )

                if connection.is_connected():
                    cursor = connection.cursor(dictionary=True)

                    # Consulta base para obtener preguntas y sus respuestas
                    sql_query = """
                    SELECT p.id AS pregunta_id, p.nombre AS pregunta_autor, p.tema_id AS tema, p.pregunta, p.contenido AS pregunta_contenido,
                        r.id AS respuesta_id, r.nombre AS respuesta_autor, r.contenido AS respuesta_contenido
                    FROM pregunta_foro p
                    LEFT JOIN respuestas_foro r ON p.id = r.pregunta_id
                    """

                    # Ejecutar la consulta sin condición WHERE
                    cursor.execute(sql_query)
                    resultados = cursor.fetchall()

                    preguntas_respuestas = {}

                    # Procesamos las preguntas y respuestas
                    for fila in resultados:
                        pregunta_id = fila['pregunta_id']
                        if pregunta_id not in preguntas_respuestas:
                            preguntas_respuestas[pregunta_id] = {
                                'autor': fila['pregunta_autor'],
                                'tema_id': fila['tema'],
                                'pregunta': fila['pregunta'],
                                'contenido': fila['pregunta_contenido'],
                                'respuestas': []
                            }
                        
                        # Si hay respuestas, las añadimos
                        if fila['respuesta_id'] is not None:
                            preguntas_respuestas[pregunta_id]['respuestas'].append({
                                'respuesta_id': fila['respuesta_id'],
                                'autor': fila['respuesta_autor'],
                                'contenido': fila['respuesta_contenido']
                            })

                    # Imprimir si el parámetro imprimir es True
                    if imprimir:
                        for pregunta_id, datos in preguntas_respuestas.items():
                            print(f"Pregunta ID: {pregunta_id}")
                            print(f"Autor: {datos['autor']}")
                            print(f"Tema: {datos['tema_id']}")
                            print(f"Pregunta: {datos['pregunta']}")
                            print(f"Contenido: {datos['contenido']}")
                            print("Respuestas:")
                            for respuesta in datos['respuestas']:
                                print(f"  Respuesta ID: {respuesta['respuesta_id']}")
                                print(f"  Autor: {respuesta['autor']}")
                                print(f"  Contenido: {respuesta['contenido']}")
                            print()

                    return preguntas_respuestas

            except Error as e:
                print(f"Error al conectar a MySQL: {e}")

            finally:
                if 'connection' in locals() and connection.is_connected():
                    cursor.close()
                    connection.close()

            
                

