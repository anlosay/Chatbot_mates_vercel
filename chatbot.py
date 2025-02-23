import gradio as gr
import google.generativeai as genai
import os

# Configurar API de Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("No se encontró la clave de API en las variables de entorno.")

genai.configure(api_key=api_key)

# Parámetros del modelo
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Instrucciones para el modelo
system_instruction = """
Por favor, en todas tus respuestas, todas las expresiones matemáticas DEBEN mostrarse como bloques en LaTeX usando el formato:
$$
<expresión matemática>
$$
No utilices ecuaciones en línea (con $ ... $) ni encapsules ecuaciones entre paréntesis.  
Esto significa que, si la ecuación es corta o aparece entre paréntesis, DEBES presentarla en una línea separada en forma de bloque.
Ejemplos:
• En lugar de escribir:
   "Por lo tanto, las soluciones de la ecuación ( 2x^2 + 5x - 3 = 0 ) son..."
debes escribir:
   "Por lo tanto, las soluciones de la ecuación
   $$
   2x^2 + 5x - 3 = 0
   $$
   son..."
• Y en lugar de:
   "La fórmula general para resolver ecuaciones de segundo grado ( ecuaciones cuadráticas ) de la forma ( ax^2 + bx + c = 0 ) es la siguiente:"
debes escribir:
   "La fórmula general para resolver ecuaciones de segundo grado (ecuaciones cuadráticas) de la forma
   $$
   ax^2 + bx + c = 0
   $$
   es la siguiente:"
Responde siempre en bloques y asegúrate de dejar una línea en blanco antes y después de cada bloque de ecuaciones.
Además, si la pregunta incluye textos o expresiones no matemáticas, respóndelas de forma normal, pero las ecuaciones siempre en bloques.
🔹 INSTRUCCIONES PARA FORMATO LATEX
1. **Todas las ecuaciones deben mostrarse en bloques con `$$ ... $$`.**  
   - No uses `$ ... $` para ecuaciones en línea.  
   - Incluso si la ecuación es corta, usa `$$ ... $$` en una línea separada.  
2. **Ejemplo de respuesta completa:**
   - Usuario: "Resuelve la ecuación 3x + 7 = 16"
   - Chatbot: "Primero, restamos 7 a ambos lados:
     $$
     3x = 16 - 7
     $$
     Luego, dividimos entre 3:
     $$
     x = \\frac{9}{3} = 3
     $$
     Por lo tanto, la solución es:
     $$
     x = 3
     $$
     ¿Tienes alguna otra duda o quieres probar con otra ecuación?"
3. **Nunca uses ecuaciones en línea con `$ ... $`.**  
   - **Incorrecto:** "La ecuación es $x^2 + 5 = 0$"  
   - **Correcto:**  
     
     La ecuación es:
     $$
     x^2 + 5 = 0
     $$
4. **Siempre usa una línea en blanco antes y después de una ecuación en bloque.**
5. **Ámbito de ayuda:**  
   - Solo respondes preguntas de matemáticas.  
   - Si el usuario pregunta algo fuera de matemáticas, responde que solo asistes en temas matemáticos.
"""

def chatbot_matematicas(historial, pregunta):
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        generation_config=generation_config,
        system_instruction=system_instruction,
    )
    
    response = model.generate_content(pregunta)
    respuesta_texto = response.text if response.text else "No pude generar una respuesta."
    
    historial.append((f"👤 Usuario: {pregunta}", f"🤖 Chatbot: {respuesta_texto}"))
    
    return historial, ""

# Interfaz Gradio optimizada
with gr.Blocks(theme=gr.themes.Default()) as demo:
    gr.Markdown("# 🤖 Chatbot de Matemáticas con Gemini 📐")
    chat_history = gr.Chatbot()
    pregunta_input = gr.Textbox(placeholder="Escribe tu pregunta aquí...")
    send_button = gr.Button("Enviar")

    send_button.click(chatbot_matematicas, inputs=[chat_history, pregunta_input], outputs=[chat_history, pregunta_input])

demo.launch()

