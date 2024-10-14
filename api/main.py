from flask import Flask, request, jsonify
from flask_cors import CORS
from api.geminiChatManager import GeminiChatManager
from api.NewMysqlManager import MysqlManager
from api.firebaseManager import FirebaseManager
import uuid
app=Flask(__name__)
CORS(app)
chat_manager = GeminiChatManager()
mysql_manager= MysqlManager()

@app.route("/")
def home():
    return "Hello from vercel use flask"

@app.route("/about")
def about():
    return "Hello about"
#Endpoints del chatbot
@app.route('/api/chatbot/new-session', methods=['POST'])
def new_session():
    """Crear una nueva sesión de chat."""
    data = request.json
    usuario_id=data.get('usuario_id')
    
    if not usuario_id:
        return jsonify({
            'error': 'Se requiere usuario_id'
        }), 400
    
    created = chat_manager.create_new_session(usuario_id)
    if created:
        return jsonify({
            'session_id': created,
            'message': 'Nueva sesión creada exitosamente'
        }), 200
    return jsonify({'error': 'No se pudo crear la sesión'}), 400

@app.route('/api/chatbot/ask', methods=['POST'])
def ask():
    """Enviar un mensaje a una sesión específica."""
    data = request.json
    usuario_id = data.get('usuario_id')
    session_id = data.get('session_id')
    message=data.get('message')
    
    if not session_id or not message or not usuario_id:
        return jsonify({
            'error': 'Campos incompletos'
        }), 400
    
    response_text = chat_manager.send_message(usuario_id,session_id, message)
    return jsonify({
        'response': response_text,
        'session_id': session_id
    }), 200

@app.route('/api/chatbot/get-my-sessions', methods=['POST'])
def get_my_sessions():
    """Enviar un mensaje a una sesión específica."""
    firebaseManager=FirebaseManager()
    data = request.json
    usuario_id = data.get('usuario_id')
    
    if not usuario_id:
        return jsonify({
            'error': 'Campos incompletos'
        }), 400
    
    response_text = firebaseManager.obtener_sesiones_usuario(usuario_id)
    return jsonify(response_text), 200

@app.route('/api/chatbot/delete-my-session', methods=['POST'])
def delete_my_session():
    """Enviar un mensaje a una sesión específica."""
    firebaseManager=FirebaseManager()
    data = request.json
    usuario_id = data.get('usuario_id')
    session_id = data.get('session_id')
    
    if not usuario_id or not session_id:
        return jsonify({
            'error': 'Campos incompletos'
        }), 400
    
    response_text = firebaseManager.eliminar_sesion(usuario_id,session_id)
    return jsonify(response_text), 200
    

#fin
#del
#chavo


#INICIO DE FORO    
@app.route('/api/mysqlManager/create-user', methods=['POST'])
def create_user():
    """Enviar un mensaje a una sesión específica."""
    data = request.json
    codigo = data.get('codigo')
    correo = data.get('correo')
    dni = data.get('dni')
    contrasena = data.get('contrasena')
        
    if not codigo or not correo or not dni or not contrasena:
        return jsonify({
            'error': 'Se requiere todos los campos'
        }), 400
    
    response=mysql_manager.crear_usuario(codigo,correo,dni,contrasena)
    
    return jsonify({
        'respuesta': response
    }), 200
    
@app.route('/api/mysqlManager/login', methods=['POST'])
def login():
    """Enviar un mensaje a una sesión específica."""
    data = request.json
    correo = data.get('correo')
    contrasena = data.get('contrasena')
        
    if not correo or not contrasena:
        return jsonify({
            'error': 'Se requiere todos los campos'
        }), 400
    
    response=mysql_manager.iniciar_sesion(correo,contrasena)
    
    return jsonify(response),200

@app.route('/api/mysqlManager/admin/create-topic', methods=['POST'])
def create_topic():
    """Enviar un mensaje a una sesión específica."""
    data = request.json
    tema = data.get('tema')
        
    if not tema:
        return jsonify({
            'error': 'Se requiere todos los campos'
        }), 400
    
    response=mysql_manager.insertar_tema(tema)
    
    return jsonify({
        'respuesta': response
    }), 200
    
@app.route('/api/mysqlManager/add-question', methods=['POST'])
def add_question():
    """Enviar un mensaje a una sesión específica."""
    data = request.json
    usuario_id=data.get('usuario_id')
    nombre=data.get('nombre')
    tema_id=data.get('tema_id')
    pregunta=data.get('pregunta')
    contenido=data.get('contenido')
        
    if not usuario_id or not nombre or not tema_id or not pregunta or not contenido:
        return jsonify({
            'error': 'Se requiere todos los campos'
        }), 400
    
    response=mysql_manager.agregar_pregunta(usuario_id,nombre,tema_id,pregunta,contenido)
    
    return jsonify({
        'respuesta': response
    }), 200
    
    
@app.route('/api/mysqlManager/add-answer', methods=['POST'])
def add_answer():
    """Enviar un mensaje a una sesión específica."""
    data = request.json
    usuario_id=data.get('usuario_id')
    nombre=data.get('nombre')
    pregunta_id=data.get('pregunta_id')
    contenido=data.get('contenido')
        
    if not usuario_id or not nombre or not pregunta_id or not contenido:
        return jsonify({
            'error': 'Se requiere todos los campos'
        }), 400
    
    response=mysql_manager.agregar_respuesta(usuario_id,nombre,pregunta_id,contenido)
    
    return jsonify({
        'respuesta': response
    }), 200
    
@app.route('/api/mysqlManager/show-questions-answers', methods=['GET'])
def show_questions_answers():
        
    response=mysql_manager.ver_preguntas_y_respuestas()
    
    return jsonify({
        'respuesta': response
    }), 200
    
@app.route('/api/mysqlManager/show-questions-answers-ID', methods=['POST'])
def show_questions_answers_ID():
    """Enviar un mensaje a una sesión específica."""
    data = request.json
    pregunta_id=data.get('pregunta_id')
        
    if not pregunta_id:
        return jsonify({
            'error': 'Se requiere todos los campos'
        }), 400
    
    response=mysql_manager.ver_pregunta_y_respuestas_por_id(pregunta_id)
    
    return jsonify({
        'respuesta': response
    }), 200
    
@app.route('/api/mysqlManager/show-questions', methods=['GET'])
def show_questions():
        
    response=mysql_manager.mostrar_solo_preguntas()
    
    return jsonify({
        'respuesta': response
    }), 200

@app.route('/api/mysqlManager/show-questions-topic', methods=['POST'])
def show_questions_topic():
    """Enviar un mensaje a una sesión específica."""
    data = request.json
    tema_id=data.get('tema_id')
        
    if not tema_id:
        return jsonify({
            'error': 'Se requiere todos los campos'
        }), 400
    
    response=mysql_manager.mostrar_preguntas_por_tema(tema_id)
    
    return jsonify({
        'respuesta': response
    }), 200
    
@app.route('/api/mysqlManager/show-questions-answers-topic', methods=['POST'])
def show_questions_answers_topic():
    """Enviar un mensaje a una sesión específica."""
    data = request.json
    tema_id=data.get('tema_id')
        
    if not tema_id:
        return jsonify({
            'error': 'Se requiere todos los campos'
        }), 400
    
    response=mysql_manager.obtener_preguntas_y_respuestas_por_tema(tema_id)
    
    return jsonify({
        'respuesta': response
    }), 200
    
@app.route('/api/mysqlManager/delete-user', methods=['POST'])
def delete_user():
    """Enviar un mensaje a una sesión específica."""
    data = request.json
    usuario_id=data.get('usuario_id')
        
    if not usuario_id:
        return jsonify({
            'error': 'Se requiere todos los campos'
        }), 400
    
    response=mysql_manager.eliminar_usuario_por_id(usuario_id)
    
    return jsonify({
        'respuesta': response
    }), 200

    
    

      
