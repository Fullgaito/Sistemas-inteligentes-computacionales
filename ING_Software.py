import gradio as gr
import google.generativeai as genai

class GeminiChatBot:
    def __init__(self):
        self.init_gemini_chatbot()

    def init_gemini_chatbot(self):
        # Configuración de la API
        genai.configure(api_key="AIzaSyBzqYg321UhgfFChSso0PvSlJg1OlTtWqQ")
        
        # Creación del modelo con un mensaje inicial que limita las respuestas a Ingeniería de Software
        gemini = genai.GenerativeModel(model_name="models/gemini-1.5-pro")
        self.chatbot = gemini.start_chat(history=[
            {
                "role": "system",
                "parts": [
                    "Eres un experto en Ingeniería de Software. Solo debes responder preguntas sobre conceptos, metodologías ágiles, UML, patrones de diseño, pruebas de software, requisitos, arquitectura, etc."
                ]
            }
        ])

    def get_response(self, question: str, conversation: list):
        # Palabras clave para validar que la pregunta es sobre Ingeniería de Software
        keywords = ["software", "ingeniería", "uml", "arquitectura", "agile", "scrum", "requisitos", "pruebas", "desarrollo", "programación", "patrones de diseño", "código", "algoritmos"]

        # Si la pregunta no contiene palabras clave, respondemos con una advertencia
        if not any(keyword in question.lower() for keyword in keywords):
            conversation.append((question, "⚠️ Solo puedo responder preguntas sobre Ingeniería de Software."))
            return "", conversation
        
        # Si es válida, preguntamos al chatbot
        response = self.chatbot.send_message(question)
        conversation.append((question, response.text))
        return "", conversation

    def launch_gradio(self):
        with gr.Blocks(theme=gr.themes.Soft()) as demo:
            gr.Markdown(
                """
                # 🤖 Chat con Gemini - Ingeniería de Software
                ¡Hazme preguntas sobre Ingeniería de Software y te responderé al instante!
                """
            )

            # Definimos los avatares
            chatbot = gr.Chatbot(
                height=500,
                bubble_full_width=False,
                avatar_images=["https://cdn-icons-png.flaticon.com/512/847/847969.png",  # 👤 Usuario
                               "https://cdn-icons-png.flaticon.com/512/4712/4712027.png"]  # 🤖 Gemini
            )

            with gr.Row():
                question = gr.Textbox(
                    show_label=False,
                    placeholder="Escribe tu pregunta aquí...",
                    scale=10,
                )
                submit_btn = gr.Button("Enviar", scale=2)

            clear_btn = gr.ClearButton(components=[question, chatbot])

            # Conectamos el evento para que se envíe la pregunta y respuesta
            submit_btn.click(self.get_response, inputs=[question, chatbot], outputs=[question, chatbot])
            question.submit(self.get_response, inputs=[question, chatbot], outputs=[question, chatbot])

        demo.launch(debug=True, server_name="0.0.0.0", server_port=7860)

if __name__ == "__main__":
    gemini = GeminiChatBot()
    gemini.launch_gradio()
