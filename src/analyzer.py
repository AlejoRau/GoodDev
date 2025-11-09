import google.generativeai as genai

def analizar_codigo(codigo, reglas, contexto, estructura):
    """
    Envía toda la información al modelo Gemini para que realice la auditoría.
    Incluye revisión de buenas prácticas, estructura y documentación.
    """
    try:
        # Inicializamos el modelo Gemini Pro 2.5
        model = genai.GenerativeModel("gemini-2.5-pro")

        # Construimos el prompt principal de auditoría
        prompt = f"""
Eres GoodDev, un asistente experto en revisión de código, arquitectura y organización de proyectos.
Tu tarea es auditar el código recibido y devolver el resultado en **formato plano y claro**, 
pensado para guardarse en un archivo .txt.

🎯 Objetivo:
Identificar errores, sugerir mejoras y generar el código corregido correspondiente,
listo para copiar y pegar. No uses colores ni símbolos especiales, solo texto plano.

=== FORMATO DE RESPUESTA REQUERIDO ===

1 Sección: CODIGO CORREGIDO
- Mostrá únicamente los fragmentos o líneas que deberían cambiarse, dentro de un bloque de código markdown.
- No incluyas todo el archivo, solo lo que deba reemplazarse.

2 Sección: PROBLEMAS DETECTADOS
- Listá cada error o mejora con su respectiva categoría:
    🔴 (GRAVE): Mala práctica, error crítico o vulnerabilidad.
    🟡 (MEDIA): Mejora sugerida, advertencia, código redundante o poco claro.
    🟢 (BUENA): Buenas prácticas detectadas o aspectos positivos.

Cada punto debe tener una breve justificación y, si aplica, referenciar la regla que se violó.

3 Sección: DOCUMENTACION PROPUESTA
- Si el código no tiene documentación, generá una propuesta.
- Si existe pero no cumple las reglas, mostrá una versión corregida.
- Si ya está correcta, indicalo explícitamente.

📘 IMPORTANTE:
- Evitá caracteres de formato innecesarios (tablas, símbolos raros o delimitadores).
- La respuesta debe ser solo texto con interlineado.
- Revisá la gramática y ortografía antes de finalizar.

=== CONTEXTO DEL PROYECTO ===
{contexto}

=== REGLAS DEL EQUIPO ===
{reglas}

=== ESTRUCTURA DE DIRECTORIOS ===
{estructura}

=== CODIGO A ANALIZAR ===
{codigo}
"""

        # Llamada al modelo
        response = model.generate_content(prompt)

        # Validación del resultado
        if not response:
            return "⚠️ No se obtuvo respuesta del modelo (response vacío). Verificá la API Key o conexión."
        if not hasattr(response, "text"):
            return "⚠️ La respuesta del modelo no contiene texto. Revisa la versión de la librería o el método usado."
        if not response.text or not response.text.strip():
            return "⚠️ El modelo no devolvió contenido analizable. Revisá el prompt o el tamaño del código enviado."

        # Retornamos el texto limpio
        return response.text.strip()

    except Exception as e:
        return f"❌ Error durante la auditoría del código: {str(e)}"
