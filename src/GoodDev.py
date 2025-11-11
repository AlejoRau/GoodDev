import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rich.console import Console
from dotenv import load_dotenv
from .Utils.utils import (
    leer_archivo,
    limpiar_codigo,
    obtener_estructura_directorios,
    cargar_cache,
    guardar_cache,
    hash_string
)
from .analyzer import analizar_codigo

import google.generativeai as genai

# ==============================
# CONFIGURACIÓN INICIAL
# ==============================
load_dotenv()  
API_KEY = os.getenv("GOOGLE_API_KEY")

console = Console()

if not API_KEY:
    console.print("⚠️ GOOGLE_API_KEY no encontrada. Verificá tus secrets o .env.", style="yellow")
    exit(1)

genai.configure(api_key=API_KEY)


# ==============================
# FUNCIÓN PRINCIPAL
# ==============================
def main():
    console.print("🚀 Iniciando GoodDev: Auditor de código y arquitectura\n", style="bold cyan")

    # Leer reglas y contexto general del proyecto
    reglas = leer_archivo("src/Rules/rules.txt")
    contexto = leer_archivo("src/Rules/contexto.txt")

    # Leer estructura del proyecto (generada por el workflow)
    estructura = leer_archivo("estructura.txt")

    # Leer código modificado (solo cambios del PR, con contexto)
    codigo = leer_archivo("code_changes.txt")

    if not codigo or not reglas or not contexto:
        console.print("❌ Faltan archivos o están vacíos. No se puede continuar.", style="red")
        return

   
    codigo_filtrado = limpiar_codigo(codigo)

  
    if not estructura:
        estructura = obtener_estructura_directorios(".")

    cache = cargar_cache()
    code_hash = hash_string(codigo_filtrado)

    if cache.get("code_hash") == code_hash:
        console.print("🟢 El código no cambió, usando análisis previo", style="green")
        resultado = cache.get("analysis_result", "⚠️ No hay análisis previo guardado")
    else:
        console.print("\n🤖 Analizando código y estructura del proyecto...\n", style="bold yellow")
        resultado = analizar_codigo(codigo_filtrado, reglas, contexto, estructura)

        # Guardar hash y resultado
        cache["code_hash"] = code_hash
        cache["analysis_result"] = resultado
        guardar_cache(cache)

    # ==============================
    # RESULTADOS
    # ==============================
    console.print("\n===== RESULTADO DEL ANÁLISIS =====", style="bold white")
    console.print(resultado, style="white")

    # Guardar log para el comentario automático en el PR
    with open("pull_request.log", "w", encoding="utf-8") as log:
        log.write(resultado)

    console.print("\n✅ Análisis completado. Resultado guardado en pull_request.log\n", style="bold cyan")



if __name__ == "__main__":
    main()
