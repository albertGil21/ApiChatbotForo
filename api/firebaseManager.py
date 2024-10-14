import pyrebase
from datetime import datetime
import hashlib
import json

class FirebaseManager:
    def __init__(self):
        # Configura tus credenciales de Firebase aquí
        config= {
            "apiKey": "AIzaSyD0o7Z1OXRrGTBEJCnAtClNxD4NmU2vnps",
            "authDomain": "epen-92888.firebaseapp.com",
            "databaseURL": "https://epen-92888-default-rtdb.firebaseio.com",
            "projectId": "epen-92888",
            "storageBucket": "epen-92888.appspot.com",
            "messagingSenderId": "734148026861",
            "appId": "1:734148026861:web:b747a7e8696033ccc3c7e4",
            "measurementId": "G-9NT8GNMJY9"
        }
        
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()

    def crear_usuario(self, email, nombre, otros_datos=None):
        """Crea un nuevo usuario y devuelve su ID"""
        datos_usuario = {
            "email": email,
            "nombre": nombre,
            "fecha_registro": str(datetime.now()),
            "sesiones": []  # Array para almacenar los hashes de las sesiones
        }
        
        if otros_datos:
            datos_usuario.update(otros_datos)
            
        # Crear un ID único para el usuario
        usuario_id = self.db.child("usuarios").push(datos_usuario)
        return usuario_id["name"]  # Retorna el ID generado

    def obtener_usuario(self, usuario_id):
        """Obtiene los datos de un usuario por su ID"""
        return self.db.child("usuarios").child(usuario_id).get().val()

    def crear_sesion(self, usuario_id, mensaje_inicial=None):
        """
        Crea una nueva sesión para un usuario (identificado por un hash proporcionado) 
        y la asocia con él. Retorna el hash de la sesión.
        """
        # Crear un hash único para la sesión
        timestamp = str(datetime.now())
        hash_sesion = hashlib.sha256(f"{usuario_id}{timestamp}".encode()).hexdigest()[:16]
        
        datos_sesion = {
            "usuario_id": usuario_id,
            "fecha_creacion": timestamp,
            "mensajes": []
        }
        
        if mensaje_inicial:
            datos_sesion["mensajes"].append(mensaje_inicial)
        
        # Guardar la sesión en la tabla de sesiones
        self.db.child("sesiones").child(hash_sesion).set(datos_sesion)
        
        # Verificar si el usuario ya tiene sesiones registradas
        usuario = self.db.child("usuarios").child(usuario_id).get().val()
        
        if not usuario:
            # Si el usuario no existe, crear un nuevo nodo con una lista de sesiones
            self.db.child("usuarios").child(usuario_id).set({
                "sesiones": [hash_sesion]
            })
        else:
            # Si el usuario ya existe, añadir el nuevo hash_sesion a su lista de sesiones
            if "sesiones" in usuario:
                usuario["sesiones"].append(hash_sesion)
            else:
                usuario["sesiones"] = [hash_sesion]
            
            # Actualizar la base de datos con la nueva lista de sesiones
            self.db.child("usuarios").child(usuario_id).update({
                "sesiones": usuario["sesiones"]
            })
        
        return hash_sesion

    def agregar_mensaje_sesion(self, hash_sesion, mensaje):
        """Agrega un mensaje a una sesión existente"""
        sesion = self.db.child("sesiones").child(hash_sesion).get().val()
        if not sesion:
            raise ValueError("Sesión no encontrada")
            
        mensajes = sesion.get("mensajes", [])
        mensajes.append({
            "contenido": mensaje,
            "timestamp": str(datetime.now())
        })
        
        self.db.child("sesiones").child(hash_sesion).update({"mensajes": mensajes})

    def obtener_sesiones_usuario(self, usuario_id):
        """Obtiene todas las sesiones de un usuario"""
        usuario = self.obtener_usuario(usuario_id)
        if not usuario or not usuario.get("sesiones"):
            return []
            
        sesiones = []
        for hash_sesion in usuario["sesiones"]:
            sesion = self.db.child("sesiones").child(hash_sesion).get().val()
            if sesion:
                sesiones.append({
                    "hash": hash_sesion,
                    "datos": sesion
                })
                
        return sesiones

    def obtener_mensajes_sesion(self, hash_sesion):
        """Obtiene todos los mensajes de una sesión específica"""
        sesion = self.db.child("sesiones").child(hash_sesion).get().val()
        if not sesion:
            return []
        return sesion.get("mensajes", [])
    
    def eliminar_sesion(self, usuario_id, hash_sesion):
        """
        Elimina una sesión para un usuario dado y elimina el hash_sesion de la lista de sesiones del usuario.
        """
        # Verificar si el usuario existe
        usuario = self.db.child("usuarios").child(usuario_id).get().val()
        
        if not usuario or not usuario.get("sesiones"):
            return {
                "error": "Usuario o sesiones no encontrados."
            }
        
        # Verificar si el hash_sesion está asociado al usuario
        if hash_sesion not in usuario["sesiones"]:
            return {
                "error": "Sesión no encontrada para este usuario."
            }

        # Eliminar la sesión de la base de datos
        self.db.child("sesiones").child(hash_sesion).remove()
        
        # Eliminar el hash_sesion de la lista de sesiones del usuario
        usuario["sesiones"].remove(hash_sesion)
        
        # Actualizar la lista de sesiones del usuario en la base de datos
        self.db.child("usuarios").child(usuario_id).update({
            "sesiones": usuario["sesiones"]
        })
        
        return {
            "success": "Sesión eliminada exitosamente."
        }
    
    

#firebasemanager.agregar_mensaje_sesion('e08cffc7b45dd698','hola soy pedrito creo')
