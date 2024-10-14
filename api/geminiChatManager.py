import os
import time

from api.firebaseManager import FirebaseManager 
import google.generativeai as genai
from typing import Dict
from datetime import datetime


api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

class GeminiChatManager:
  def __init__(self):
      self.firebase=FirebaseManager()
      self.chat_sessions: Dict[str, genai.GenerativeModel.start_chat] = {}
      self.generation_config = {
          "temperature": 1,
          "top_p": 0.95,
          "top_k": 64,
          "max_output_tokens": 50,
      }
      self.model = genai.GenerativeModel(
          model_name="gemini-1.5-flash",
          generation_config=self.generation_config,
      )
      
      # Cargar el archivo TXT una sola vez
      with open("reglamento.txt", "r", encoding="utf-8") as file:
          self.txt_file_content = file.read()
      
      # Historial de entrenamiento inicial
      self.initial_history = [
          {
              "role": "user",
              "parts": [
                  self.txt_file_content,
                  "comprende lo que está en ese pdf ",
              ],
          },
          {
              "role": "model",
              "parts": [
                  "The document you shared is a comprehensive guide for the admission process at the Universidad Nacional Mayor de San Marcos (UNMSM) in Peru for the 2024-II academic year. It covers a wide range of topics, including:\n\n**1.  Legal Framework:**\n    * The document begins by outlining the legal framework that governs the admission process, including the Peruvian Constitution, university laws, and relevant decrees.\n\n**2.  Glossary:**\n    * A glossary defines essential terms used throughout the document, such as \"Aspirante,\" \"Postulante,\" \"Vacante,\" \"Constancia de Ingreso,\" and \"Actos de Fraude.\"\n\n**3.  General Provisions:**\n    * This section describes the general organization of the university and its academic structure. It lists the different areas of study offered, including the schools of Medicine, Sciences, Engineering, Economics, Humanities, and Law.\n\n**4.  Admission Procedures:**\n    * The document details the various admission modalities available to prospective students, such as regular admission, first-place admission for secondary school graduates, admission for students with disabilities, admission for Indigenous students, and admission for athletes. \n    * It outlines the steps involved in each modality, from pre-registration and application to taking exams, completing medical evaluations, and receiving final admission documents.\n\n**5.  Exam Structure and Content:**\n    * The document provides detailed information about the general and special exams, including the format, sections, number of questions, subject areas, and time allotted. It also outlines the exam procedures and scoring criteria.\n\n**6.  Exonerations and Special Cases:**\n    * The document outlines various situations where students may be exempt from taking exams or may be eligible for special admission procedures, such as for diplomatic representatives, refugees, or those with certain academic backgrounds. \n\n**7.  Important Dates and Deadlines:**\n    * A detailed timeline outlines all important dates for the admission process, including deadlines for registration, pre-registration, exams, and receiving final admission documents.\n\n**8.  Ethics Guidelines:**\n    * A separate section dedicated to ethical guidelines emphasizes the importance of honesty, responsibility, and transparency during the admission process.\n\n**9.  Biosecurity Protocol:**\n    * The document emphasizes the importance of following biosecurity protocols during the admission process due to the COVID-19 pandemic.\n\n**10. Annexes:**\n    * The document concludes with annexes that provide further details and specific information, including:\n        * A list of schools and the number of available spots for each.\n        * A detailed pre-registration schedule for each school.\n        *  Instructions for completing the application form and uploading required documents.\n        *  The format for the official admission documents.\n        *  Ethical guidelines for applicants.\n        *  The structure of the general exam and special exams.\n        *  A model of the exam identification and answer sheet.\n        *  A timeline for receiving admission documents.\n        *  A sample certificate of original studies.\n        *  A map of the UNMSM campus.\n        *  A list of Banco de la Nación branches where admission fees can be paid.\n        *  A list of codes for specific admission fees.\n        *  Detailed content information for specific subject areas, such as mathematics, language, literature, psychology, history, geography, and economics.\n\nThe document is a comprehensive resource for prospective students who wish to apply to the UNMSM. It provides a clear, detailed, and user-friendly guide to the entire admission process, ensuring that applicants have a thorough understanding of their responsibilities and the procedures they need to follow. \n",
              ],
          },
          {
              "role": "user",
              "parts": [
                  "que se dice del articulo 2",
              ],
          },
          {
              "role": "model",
              "parts": [
                  "The article 2 of the document states that the admission process is in charge of the Oficina Central de Admisión (OCA), which was established by Resolution Rectoral N.°03028-R-04. The faculties and other university departments must provide the OCA with the resources and support it needs to carry out its work.\n",
              ],
          },
          {
              "role": "user",
              "parts": [
                  "tus respuestas no pueden estar en español?\n",
              ],
          },
          {
              "role": "model",
              "parts": [
                  "¡Lo siento!  Me olvidé de cambiar el idioma a español.  Voy a intentar hablar solo español a partir de ahora.  ¿Qué más te gustaría saber? \n",
              ],
          },
          {
              "role": "user",
              "parts": [
                  "quiero que cualquier pregunta de ahora en adelante sea respondida con informacion solo de los documentos que te doy\n",
              ],
          },
          {
              "role": "model",
              "parts": [
                  "¡Entendido! A partir de este momento, solo responderé con información de los documentos que me proporciones. \n\n¿Qué te gustaría saber?  😊 \n",
              ],
          },
          {
            "role": "user",
            "parts": [
              "cuando se fundó el perú",
            ],
          },
          {
            "role": "model",
            "parts": [
              "Lo siento, no puedo responder a esa pregunta. El documento que me proporcionaste no contiene información sobre la fecha de fundación del Perú. \n\n¿Te gustaría preguntarme algo sobre la información del documento? \n",
            ],
          },
          {
            "role": "user",
            "parts": [
              "quien es el presidente del peru",
            ],
          },
          {
            "role": "model",
            "parts": [
              "El documento no menciona el nombre del actual presidente del Perú.  \n\n¿Hay alguna otra pregunta que te gustaría hacer sobre la información contenida en el documento? \n",
            ],
          },
          {
            "role": "user",
            "parts": [
              "que dice el articulo 4 del reglamento",
            ],
          },
          {
            "role": "model",
            "parts": [
              "El artículo 4 del reglamento establece que si un estudiante quiere postular a la Escuela Profesional de Danza o Educación Física, tiene que pasar un examen médico y un examen de aptitud. Si pasa esos exámenes, puede inscribirse para la prueba general, siguiendo las instrucciones del artículo 35 del reglamento. \n",
            ],
          },
          {
            "role": "user",
            "parts": [
              "Que dice el articulo 3",
            ],
          },
          {
            "role": "model",
            "parts": [
              "El artículo 3 describe los diferentes tipos de modalidades de admisión disponibles para los estudiantes.  Aquí están las modalidades que menciona: \n\n* **Admisión Regular:** Esta modalidad es para estudiantes que han completado el ciclo de educación secundaria y quieren postular para estudios de pregrado. \n* **Admisión para estudiantes que se ubican entre los primeros puestos en su secundaria:** Esta modalidad es para estudiantes que se ubicaron entre los primeros puestos en su secundaria (colegio o instituto).\n* **Admisión para estudiantes con discapacidad:** Esta modalidad es para estudiantes con discapacidad.\n* **Admisión para estudiantes indígenas:** Esta modalidad es para estudiantes indígenas.\n* **Admisión para atletas:** Esta modalidad es para estudiantes que son atletas.\n\nEl artículo 3 también incluye las fechas límite para registrarse e inscribirse en cada una de las modalidades. \n\n\n",
            ],
          },
          {
            "role": "user",
            "parts": [
              "dime el articulo 5",
            ],
          },
          {
            "role": "model",
            "parts": [
              "El artículo 5 del reglamento indica que pueden postular por la modalidad de Educación Básica Regular (EBR) y Educación Básica Alternativa (EBA) las siguientes personas:\n\n* **Egresados de Educación Básica Regular (EBR)**\n* **Egresados de Educación Básica Alternativa (EBA)** \n",
            ],
          },
          {
            "role": "user",
            "parts": [
              "dime el articulo 3\n",
            ],
          },
          {
            "role": "model",
            "parts": [
              "El artículo 3 del reglamento describe el proceso de admisión como un proceso que se divide en dos etapas: \n\n* **Admisión 2024-I:** Esta etapa se realiza en el segundo semestre del 2023. \n* **Admisión 2024-II:** Esta etapa se realiza en el primer semestre del 2024. \n\nLos estudiantes que ingresen en cualquiera de estas dos etapas empezarán sus clases en el primer periodo académico del 2024. \n",
            ],
          }
          
      ]

  def load_local_file(self, path):
      """Lee el contenido de un archivo local"""
      try:
          with open(path, "r", encoding="utf-8") as file:
              return file.read()
      except Exception as e:
          print(f"Error al leer el archivo: {e}")
          return ""

  def recreate_chat_session(self, hash_sesion: str) -> genai.GenerativeModel.start_chat:
      """Recrea una sesión de chat con todo el historial de Firebase"""
      try:
          # Obtener todos los mensajes de Firebase
          mensajes_firebase = self.firebase.obtener_mensajes_sesion(hash_sesion)
          
          # Crear una nueva sesión con el historial inicial
          chat_session = self.model.start_chat(history=self.initial_history)
          
          # Construir el historial completo combinando el inicial y Firebase
          historial_completo = []
          
          # Agregar solo los mensajes que no sean del sistema
          for mensaje in mensajes_firebase:
              if mensaje.get('role') in ['user', 'assistant']:
                  historial_completo.append({
                      "role": "user" if mensaje['role'] == 'user' else "model",
                      "parts": [mensaje['contenido']]
                  })
          
          # Aplicar el historial completo a la sesión
          for mensaje in historial_completo:
              chat_session.history.append(mensaje)
          
          return chat_session
          
      except Exception as e:
          print(f"Error al recrear la sesión: {e}")
          return None

  def create_new_session(self, usuario_id: str):
      """Crear una nueva sesión de chat y guardarla en Firebase"""
      try:
          # Crear sesión en Gemini
          chat_session = self.model.start_chat(history=self.initial_history)
          
          # Crear sesión en Firebase
          hash_sesion = self.firebase.crear_sesion(
              usuario_id,
              mensaje_inicial={
                  "role": "system",
                  "contenido": "Inicio de sesión",
                  "timestamp": str(datetime.now())
              }
          )
          
          # Guardar la sesión
          self.chat_sessions[hash_sesion] = chat_session
          
          return hash_sesion
      except Exception as e:
          print(f"Error al crear nueva sesión: {e}")
          return None

  def get_session(self, hash_sesion: str, usuario_id: str):
      """Obtener una sesión existente o crear una nueva si no existe"""
      try:
          if hash_sesion not in self.chat_sessions:
              # Verificar si la sesión existe en Firebase
              sesion = self.firebase.obtener_mensajes_sesion(hash_sesion)
              if sesion:
                  # Recrear la sesión con todo el historial
                  chat_session = self.recreate_chat_session(hash_sesion)
                  if chat_session:
                      self.chat_sessions[hash_sesion] = chat_session
                  else:
                      raise ValueError("No se pudo recrear la sesión")
              else:
                  # Si no existe, crear una nueva
                  return self.create_new_session(usuario_id)
          return hash_sesion
      except Exception as e:
          print(f"Error al obtener sesión: {e}")
          return None

  def send_message(self, usuario_id: str, hash_sesion: str, message: str) -> str:
      """Enviar mensaje y guardarlo en Firebase"""
      try:
          # Si el usuario es invitado, crear una sesión temporal sin almacenarla
          if usuario_id == "invitado" and hash_sesion == "invitado":
              if "invitado" not in self.chat_sessions:
                  # Crear una nueva sesión para el invitado si no existe
                  self.chat_sessions["invitado"] = self.model.start_chat(history=self.initial_history.copy())

              # Obtener la sesión de chat para el invitado
              chat_session = self.chat_sessions["invitado"]
              #chat_session.history.append(fire)
              # Enviar el mensaje a Gemini
              response = chat_session.send_message(message)
              response_text = response.text

              return response_text

          # Asegurar que tenemos una sesión válida
          hash_sesion = self.get_session(hash_sesion, usuario_id)
          if not hash_sesion:
              raise ValueError("No se pudo obtener una sesión válida")

          # Obtener la sesión del chat
          chat_session = self.chat_sessions[hash_sesion]
          # Enviar mensaje a Gemini
          response = chat_session.send_message(message)
          response_text = response.text
          
          # Guardar mensaje del usuario en Firebase
          timestamp = str(datetime.now())
          self.firebase.agregar_mensaje_sesion(hash_sesion, {
              "role": "user",
              "contenido": message,
              "timestamp": timestamp
          })
          
          # Guardar respuesta en Firebase
          self.firebase.agregar_mensaje_sesion(hash_sesion, {
              "role": "assistant",
              "contenido": response_text,
              "timestamp": timestamp
          })
          
          return response_text
          
      except Exception as e:
          return f"Error: {str(e)}"

  def delete_session(self, session_id: str) -> bool:
      """Eliminar una sesión de chat."""
      if session_id in self.chat_sessions:
          del self.chat_sessions[session_id]
          return True
      return False