# 🤖 SmartDoc Enterprise AI: Asistente RAG Local y Privado

SmartDoc es una solución de **IA Generativa (GenAI)** de alto rendimiento diseñada para entornos corporativos. Permite transformar manuales, normativas y protocolos extensos en una base de conocimientos interactiva. 

A diferencia de las soluciones comerciales, SmartDoc se ejecuta **100% en infraestructura local**, garantizando que la propiedad intelectual y los datos sensibles de la empresa nunca salgan de su red.

---

## 📈 Valor Estratégico para la Empresa

Este proyecto resuelve tres desafíos críticos en la adopción de IA a nivel organizacional:

1. **Privacidad de Datos (Data Sovereignty):** Cumple con las normativas más estrictas de protección de datos al procesar todo localmente. No hay riesgo de filtración de información en nubes públicas.
2. **Reducción de Costos (Zero Token Cost):** Sin facturas mensuales por uso de APIs. Una vez desplegado, el costo por consulta es inexistente.
3. **Eficiencia Operativa:** Reduce el tiempo de búsqueda en documentos técnicos de minutos a segundos, permitiendo a los empleados tomar decisiones informadas con mayor rapidez.

---
## 📌 **Características Principales**
✅ **Procesamiento 100% local** (sin enviar datos a la nube).
✅ **Persistencia de datos** con FAISS (guarda el índice para consultas futuras).
✅ **Interfaz intuitiva** con Gradio (diseño moderno y responsivo).
✅ **Soporte para Ollama** (modelos locales como Llama 3.2).
✅ **Historial de consultas** en formato de chat.

---

## 📐 Arquitectura y Lógica del Sistema

SmartDoc utiliza una arquitectura **RAG (Retrieval-Augmented Generation)**. A continuación, se presenta la lógica algorítmica simplificada (Pseudocódigo):

INICIO SmartDoc
  
  // 1. Fase de Inicialización
  SI existe carpeta "faiss_index":
      CARGAR base de datos vectorial desde disco
  
  // 2. Fase de Ingesta (Procesamiento del PDF)
  
  FUNCIÓN Procesar_PDF(archivo):
      fragmentos = DIVIDIR documento EN bloques de 2000 caracteres (Overlap 400)
      vectores = CONVERTIR fragmentos A Embeddings (all-mpnet-base-v2)
      GUARDAR vectores EN disco (Persistencia FAISS)

  // 3. Fase de Consulta (Conversación)
  
  FUNCIÓN Responder_Chat(pregunta):
      contexto = BUSCAR en FAISS los 3 bloques más relevantes
      respuesta = LLM(pregunta + contexto) usando Llama 3.2 (1B)
      ENVIAR respuesta vía Streaming a la interfaz
FIN

## 📌 **Interfaz y Pruebas de Funcionamiento**
![Demo](https://github.com/CrhistianZahir/Asistente-RAG-Local-y-Privado/blob/main/Pruebas/CapturaSistema.JPG) 
Pregunta de prueba 1: ¿Qué es la red nacional de laboratorios según el manual?
![Demo](https://github.com/CrhistianZahir/Asistente-RAG-Local-y-Privado/blob/main/Pruebas/Captura1.JPG)

Pregunta de prueba 2: ¿Cuáles son las funciones específicas de los laboratorios de salud pública departamental?
![Demo](https://github.com/CrhistianZahir/Asistente-RAG-Local-y-Privado/blob/main/Pruebas/Captura2.JPG)

Pregunta de prueba 3: ¿Qué normas rigen el sistema de gestión de calidad en esta red?
![Demo](https://github.com/CrhistianZahir/Asistente-RAG-Local-y-Privado/blob/main/Pruebas/Captura3.JPG)
