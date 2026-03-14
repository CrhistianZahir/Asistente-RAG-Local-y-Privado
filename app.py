import sys
import types
import os
import shutil
import gradio as gr

# --- PARCHE PARA WINDOWS ---
if sys.platform == "win32":
    m = types.ModuleType("pwd")
    sys.modules["pwd"] = m

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM 
from langchain_core.prompts import ChatPromptTemplate

# --- CONFIGURACIÓN DE PERSISTENCIA ---
DB_FAISS_PATH = "faiss_index"
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
vectorstore_storage = {"db": None}

def cargar_db_existente():
    if os.path.exists(DB_FAISS_PATH):
        try:
            vectorstore_storage["db"] = FAISS.load_local(
                DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True
            )
            return "🟢 **Sistema Listo:** Base de datos cargada."
        except:
            return "⚠️ Error al recuperar datos previos."
    return "⚪ **Estado:** Esperando documento PDF..."

def procesar_pdf(archivo):
    if archivo is None: return "⚠️ Por favor, sube un PDF."
    try:
        loader = PyPDFLoader(archivo.name)
        documentos = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=400)
        fragmentos = text_splitter.split_documents(documentos)
        vectorstore = FAISS.from_documents(fragmentos, embeddings)
        vectorstore.save_local(DB_FAISS_PATH)
        vectorstore_storage["db"] = vectorstore
        return "✅ **Documento analizado y persistido.**"
    except Exception as e:
        return f"❌ **Error:** {str(e)}"

def borrar_db():
    vectorstore_storage["db"] = None
    if os.path.exists(DB_FAISS_PATH):
        shutil.rmtree(DB_FAISS_PATH)
    return "🗑️ **Memoria limpiada.**", []

# --- RESPUESTA CON STREAMING Y FORMATO DE MENSAJES ---
def responder_chat(mensaje, historial):
    if vectorstore_storage["db"] is None:
        historial.append({"role": "user", "content": mensaje})
        historial.append({"role": "assistant", "content": "❌ Primero sube un PDF."})
        yield "", historial
        return

    try:
        retriever = vectorstore_storage["db"].as_retriever(search_kwargs={"k": 3})
        docs = retriever.invoke(mensaje)
        contexto = "\n\n".join([doc.page_content for doc in docs])

        template = "Responde como experto técnico usando este contexto:\n{context}\n\nPregunta: {question}"
        prompt_txt = template.format(context=contexto, question=mensaje)
        
        llm = OllamaLLM(model="llama3.2:1b", temperature=0.3)
        
        # Agregamos los mensajes en formato de DICCIONARIO (lo que pide el error)
        historial.append({"role": "user", "content": mensaje})
        historial.append({"role": "assistant", "content": ""})
        
        acumulado = ""
        for token in llm.stream(prompt_txt):
            acumulado += token
            # Actualizamos el contenido del último mensaje (el del asistente)
            historial[-1]["content"] = acumulado
            yield "", historial
            
    except Exception as e:
        historial.append({"role": "user", "content": mensaje})
        historial.append({"role": "assistant", "content": f"❌ Error: {str(e)}"})
        yield "", historial

# --- DISEÑO CSS ---
custom_css = """
footer {visibility: hidden}
.header-text { text-align: center; color: #1a2a6c; padding: 15px; }
.status-box { background: white; border-radius: 10px; padding: 10px; border: 1px solid #ddd; }
"""

# --- INTERFAZ ---
with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue"), css=custom_css) as demo:
    
    gr.HTML("<div class='header-text'><h1>🤖 SmartDoc Enterprise AI</h1><p>Consulta técnica local segura y privada</p></div>")

    with gr.Row():
        with gr.Column(scale=1):
            with gr.Group():
                gr.Markdown("### 📂 Carga de Manuales")
                pdf_input = gr.File(label=None, file_types=[".pdf"])
                btn_procesar = gr.Button("⚙️ Analizar y Guardar", variant="primary")
            
            with gr.Accordion("🛠️ Herramientas", open=False):
                btn_borrar = gr.Button("🗑️ Resetear Sistema", variant="stop")
            
            gr.Markdown("### 📶 Conexión")
            status = gr.Markdown(value=cargar_db_existente(), elem_classes="status-box")
            
        with gr.Column(scale=2):
            # NO usamos type="messages" aquí para evitar el TypeError de inicialización
            chatbot = gr.Chatbot(label="Asistente Virtual", height=500)
            
            with gr.Row():
                txt_input = gr.Textbox(placeholder="Haz tu pregunta...", show_label=False, scale=4)
                btn_enviar = gr.Button("Enviar 🚀", variant="primary", scale=1)

            gr.Examples(
                examples=["¿Qué dice el manual sobre la seguridad?", "Resume este documento."],
                inputs=txt_input
            )

    btn_procesar.click(fn=procesar_pdf, inputs=[pdf_input], outputs=[status])
    btn_borrar.click(fn=borrar_db, outputs=[status, chatbot])
    
    btn_enviar.click(fn=responder_chat, inputs=[txt_input, chatbot], outputs=[txt_input, chatbot])
    txt_input.submit(fn=responder_chat, inputs=[txt_input, chatbot], outputs=[txt_input, chatbot])

if __name__ == "__main__":
    demo.launch()