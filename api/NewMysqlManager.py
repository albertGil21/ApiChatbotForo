import hashlib
import random
import string
import os
import mysql.connector
from mysql.connector import Error
from datetime import datetime

class MysqlManager:
    def __init__(self)->None:
            self.connection = None 
    
    def crear_conexion(self):
        """Crea la conexión a la base de datos."""
        try:
            conexion = mysql.connector.connect(
                host='mysql-29b3c4f7-chatyforodb.h.aivencloud.com',
                port=26304,
                user='avnadmin',
                password=os.environ.get("MYSQL_KEY_PASSWORD"),
                database='defaultdb'
            )
            if conexion.is_connected():
                return conexion
        except Error as e:
            return None

    def verificar_usuario(self, conexion, codigo, correo, dni):
        """Verifica si un usuario existe con el código, correo y DNI."""
        try:
            cursor = conexion.cursor()
            query = """
            SELECT *, (contrasena IS NOT NULL AND contrasena != '') AS tiene_contrasena 
            FROM usuarios WHERE codigo = %s AND correo = %s AND dni = %s
            """
            cursor.execute(query, (codigo, correo, dni))
            resultado = cursor.fetchone()
            return resultado
        except Error as e:
            return f'Error al verificar usuario: {e}'

    def actualizar_contrasena(self,conexion, codigo, nueva_contrasena):
        """Actualiza la contraseña y hash id del usuario."""
        hash_id = self.generar_hash()
        try:
            cursor = conexion.cursor()
            query = "UPDATE usuarios SET contrasena = %s, hash_id = %s WHERE codigo = %s"
            cursor.execute(query, (nueva_contrasena, hash_id, codigo))
            conexion.commit()
            return True
        except Error as e:
            return 'Error al actualizar la contraseña.'
    

    def generar_hash(self):
        numero_aleatorio = str(random.randint(0, 10**10)).encode('utf-8')
        hash_obj = hashlib.sha256(numero_aleatorio)
        hash_hex = hash_obj.hexdigest()
        return hash_hex[:20]

    def crear_usuario(self, codigo, correo, dni, nueva_contrasena):
        conexion = self.crear_conexion()
        if conexion:
            usuario = self.verificar_usuario(conexion, codigo, correo, dni)
            if usuario:
                if usuario[-1]:  # Verificar si tiene_contrasena es True
                    resultado = self.actualizar_contrasena(conexion, codigo, nueva_contrasena)
                    if resultado:
                        return {'Registro': 'Contraseña cambiada exitosamente'}
                    else:
                        return {'Registro': 'Error al actualizar la contraseña'}
                else:
                    resultado = self.actualizar_contrasena(conexion, codigo, nueva_contrasena)
                    if resultado:
                        return {'Registro': 'Exitoso'}
                    else:
                        return {'Registro': 'Error al actualizar la contraseña'}
            else:
                return {'Registro': 'Denegado. Usuario no encontrado.'}
            
            conexion.close()
            
    def iniciar_sesion(self,correo, contrasena):
        """Permite al usuario iniciar sesión verificando su correo y contraseña."""
        conexion = self.crear_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                query = "SELECT * FROM usuarios WHERE correo = %s AND contrasena = %s"
                cursor.execute(query, (correo, contrasena))
                resultado = cursor.fetchone()
                
                if resultado:
                    usuario_id = resultado[0]
                    contrasena = resultado[1]
                    hash_id = resultado[6]

                    datos_usuario = {
                        'Acceso': 'Permitido',
                        'usuario_id': usuario_id,
                        'contrasena': contrasena,
                        'hash_id': hash_id
                    }
                    return datos_usuario
                else:
                    dato_acceso = {
                        'Acceso': 'Denegado',
                        'System': 'Correo o contraseña incorrectos. Inténtalo de nuevo.'
                    }
                    return dato_acceso
            
            except Error as e:
                return {
                    'Acceso': 'Error',
                    'mensaje': f'Error al intentar iniciar sesión: {str(e)}'
                }
            
            
            finally:
                conexion.close()
                
    def insertar_tema(self,tema):
        """Permite añadir temas nuevos a escoger."""
        conexion = self.crear_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql_insert_query = """INSERT INTO temas (tema) VALUES (%s)"""
                cursor.execute(sql_insert_query, (tema,))
                conexion.commit()
                return 'Tema agregado exitosamente.'

            except Error as e:
                return f'Error al agregar tema: {e}'

            finally:
                if 'conexion' in locals() and conexion.is_connected():
                    cursor.close()
                    conexion.close()

    def agregar_pregunta(self,usuario_id, nombre, tema_id, pregunta, contenido):
        """Agrega una pregunta a la base de datos usando ID del usuario."""
        conexion = self.crear_conexion()
        if conexion:
            fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            try:
                cursor = conexion.cursor()
                query = """
                INSERT INTO pregunta (usuario_id, nombre, tema_id, pregunta, contenido, fecha)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                valores = (usuario_id, nombre, tema_id, pregunta, contenido, fecha_actual)
                cursor.execute(query, valores)
                conexion.commit()
                return 'Pregunta agregada exitosamente.'
            
            except Error as e:
                return f'Error al agregar la pregunta: {e}'
            
            finally:
                conexion.close()

    def agregar_respuesta(self,usuario_id, nombre, pregunta_id, contenido):
        """Agrega una respuesta a la base de datos usando ID del usuario."""
        conexion = self.crear_conexion()
        if conexion:
            fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            try:
                cursor = conexion.cursor()
                query = """
                INSERT INTO respuesta (usuario_id, nombre, pregunta_id, contenido, fecha)
                VALUES (%s, %s, %s, %s, %s)
                """
                valores = (usuario_id, nombre, pregunta_id, contenido, fecha_actual)
                cursor.execute(query, valores)
                conexion.commit()
                return 'Respuesta agregada exitosamente.'
            
            except Error as e:
                return f'Error al agregar la respuesta: {e}'
            
            finally:
                conexion.close()

    def ver_preguntas_y_respuestas(self):
        """Devuelve todas las preguntas y sus respuestas en el foro."""
        conexion = self.crear_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                
                # Consulta para obtener todas las preguntas y sus respuestas
                query = """
                SELECT p.id AS pregunta_id, p.nombre AS pregunta_autor, p.tema_id AS tema, p.pregunta, p.contenido AS pregunta_contenido,
                    r.id AS respuesta_id, r.nombre AS respuesta_autor, r.contenido AS respuesta_contenido
                FROM pregunta p
                LEFT JOIN respuesta r ON p.id = r.pregunta_id
                """
                cursor.execute(query)
                resultados = cursor.fetchall()

                preguntas_respuestas = {}

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
                    
                    if fila['respuesta_id'] is not None:
                        preguntas_respuestas[pregunta_id]['respuestas'].append({
                            'respuesta_id': fila['respuesta_id'],
                            'autor': fila['respuesta_autor'],
                            'contenido': fila['respuesta_contenido']
                        })

                return preguntas_respuestas
            
            except Error as e:
                return f'Error al obtener preguntas y respuestas: {e}'
            
            finally:
                conexion.close()

    def ver_pregunta_y_respuestas_por_id(self,pregunta_id):
        """Devuelve una pregunta específica y sus respuestas."""
        conexion = self.crear_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                
                # Consulta para obtener la pregunta y sus respuestas
                query = """
                SELECT p.id AS pregunta_id, p.nombre AS pregunta_autor, p.tema_id AS tema, p.pregunta, p.contenido AS pregunta_contenido,
                    r.id AS respuesta_id, r.nombre AS respuesta_autor, r.contenido AS respuesta_contenido
                FROM pregunta p
                LEFT JOIN respuesta r ON p.id = r.pregunta_id
                WHERE p.id = %s
                """
                cursor.execute(query, (pregunta_id,))
                resultados = cursor.fetchall()

                if not resultados:
                    return f'No se encontró ninguna pregunta con el ID {pregunta_id}'
                
                pregunta_respuestas = {}

                for fila in resultados:
                    if pregunta_id not in pregunta_respuestas:
                        pregunta_respuestas[pregunta_id] = {
                            'autor': fila['pregunta_autor'],
                            'tema_id': fila['tema'],
                            'pregunta': fila['pregunta'],
                            'contenido': fila['pregunta_contenido'],
                            'respuestas': []
                        }
                    
                    if fila['respuesta_id'] is not None:
                        pregunta_respuestas[pregunta_id]['respuestas'].append({
                            'respuesta_id': fila['respuesta_id'],
                            'autor': fila['respuesta_autor'],
                            'contenido': fila['respuesta_contenido']
                        })

                return pregunta_respuestas
            
            except Error as e:
                return f'Error al obtener la pregunta y sus respuestas: {e}'
            
            finally:
                conexion.close()

    def mostrar_solo_preguntas(self):
        """Obtiene todas las preguntas del foro sin incluir las respuestas."""
        conexion = self.crear_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                query = """
                SELECT p.id AS pregunta_id, p.nombre AS pregunta_autor, p.tema_id AS tema, 
                    p.pregunta, p.contenido AS pregunta_contenido, p.fecha
                FROM pregunta p
                """
                cursor.execute(query)
                resultados = cursor.fetchall()

                solo_preguntas = []

                for fila in resultados:
                    solo_preguntas.append({
                        'pregunta_id': fila['pregunta_id'],
                        'autor': fila['pregunta_autor'],
                        'tema_id': fila['tema'],
                        'pregunta': fila['pregunta'],
                        'contenido': fila['pregunta_contenido'],
                        'fecha': fila['fecha']
                    })

                return solo_preguntas
            
            except Error as e:
                return f'Error al obtener las preguntas: {e}'
            
            finally:
                cursor.close()
                conexion.close()

    def mostrar_preguntas_por_tema(self,tema_id):
        """Obtiene todas las preguntas de un tema específico por su ID."""
        conexion = self.crear_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                query = """
                SELECT p.id AS pregunta_id, p.nombre AS pregunta_autor, p.tema_id AS tema, 
                    p.pregunta, p.contenido AS pregunta_contenido, p.fecha
                FROM pregunta p
                WHERE p.tema_id = %s
                """
                cursor.execute(query, (tema_id,))
                resultados = cursor.fetchall()

                preguntas_por_tema = []

                for fila in resultados:
                    preguntas_por_tema.append({
                        'pregunta_id': fila['pregunta_id'],
                        'autor': fila['pregunta_autor'],
                        'tema_id': fila['tema'],
                        'pregunta': fila['pregunta'],
                        'contenido': fila['pregunta_contenido'],
                        'fecha': fila['fecha']
                    })

                return preguntas_por_tema
            
            except Error as e:
                return f'Error al obtener las preguntas por tema: {e}'
            
            finally:
                cursor.close()
                conexion.close()

    def obtener_preguntas_y_respuestas_por_tema(self,tema_id):
        """Obtiene todas las preguntas y sus respuestas de un tema específico por su ID."""
        conexion = self.crear_conexion()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                query = """
                SELECT p.id AS pregunta_id, p.nombre AS pregunta_autor, p.tema_id AS tema, 
                    p.pregunta, p.contenido AS pregunta_contenido, p.fecha AS pregunta_fecha,
                    r.id AS respuesta_id, r.nombre AS respuesta_autor, r.contenido AS respuesta_contenido,
                    r.fecha AS respuesta_fecha
                FROM pregunta p
                LEFT JOIN respuesta r ON p.id = r.pregunta_id
                WHERE p.tema_id = %s
                """
                cursor.execute(query, (tema_id,))
                resultados = cursor.fetchall()

                preguntas_respuestas_por_tema = {}

                for fila in resultados:
                    pregunta_id = fila['pregunta_id']
                    if pregunta_id not in preguntas_respuestas_por_tema:
                        preguntas_respuestas_por_tema[pregunta_id] = {
                            'autor': fila['pregunta_autor'],
                            'tema_id': fila['tema'],
                            'pregunta': fila['pregunta'],
                            'contenido': fila['pregunta_contenido'],
                            'fecha': fila['pregunta_fecha'],
                            'respuestas': []
                        }
                    
                    if fila['respuesta_id'] is not None:
                        preguntas_respuestas_por_tema[pregunta_id]['respuestas'].append({
                            'respuesta_id': fila['respuesta_id'],
                            'autor': fila['respuesta_autor'],
                            'contenido': fila['respuesta_contenido'],
                            'fecha': fila['respuesta_fecha']
                        })

                return preguntas_respuestas_por_tema
            
            except Error as e:
                return f'Error al obtener preguntas y respuestas por tema: {e}'
            
            finally:
                cursor.close()
                conexion.close()

    def eliminar_usuario_por_id(self,usuario_id):
        """Elimina un usuario de la base de datos utilizando su ID."""
        conexion = self.crear_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                query = "DELETE FROM usuarios WHERE id = %s"
                cursor.execute(query, (usuario_id,))
                conexion.commit()
                
                if cursor.rowcount > 0:
                    return f'Usuario con ID {usuario_id} eliminado exitosamente.'
                else:
                    return f'No se encontró ningún usuario con ID {usuario_id}.'
            
            except Error as e:
                return f'Error al eliminar el usuario: {e}'
            
            finally:
                cursor.close()
                conexion.close()