import gradio as gr
import os
import google.generativeai as genai

class GeminiChatBot:
    def __init__(self):
        self.init_gemini_chatbot()
    def init_gemini_chatbot(self):
        genai.configure(api_key="AIzaSyBzqYg321UhgfFChSso0PvSlJg1OlTtWqQ")  # Pega tu llave aquí entre comillas
        gemini = genai.GenerativeModel(model_name="models/gemini-1.5-pro")
        self.chatbot=gemini.start_chat()
    def get_response(self,question:str,conversation:list):
        response = self.chatbot.send_message(question)
        conversation.append((question, response.text))
        return "", conversation
    def lauch_gradio(self):
        with gr.Blocks() as demo:
            chatbot=gr.Chatbot()
            question=gr.Textbox(label="Preguntame")
            clear=gr.ClearButton(question, chatbot)
            question.submit(self.get_response, [question, chatbot], [question, chatbot])
        demo.launch(debug=True,server_name="0.0.0.0",server_port=7860)
if __name__=="__main__":
    gemini=GeminiChatBot()
    gemini.lauch_gradio()