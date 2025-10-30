import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rich.console import Console
from dotenv import load_dotenv
from .Utils.utils import leer_archivo, limpiar_codigo, obtener_estructura_directorios
from .Utils.utils import cargar_cache, guardar_cache, hash_string
from .analyzer import analizar_codigo

# === CONFIGURACIÓN ===
load_dotenv()
#API_KEY = os.getenv("GOOGLE_API_KEY")
API_KEY = "AIzaSyBTVGsfvoys5SIdzJDMRJ5_unUkR_2atyw"  # Clave fija para pruebas locales
console = Console()

if not API_KEY:
    console.print("❌ No se encontró la API Key. Asegúrate de tener el archivo .env con GOOGLE_API_KEY.", style="red")
    exit()


import google.generativeai as genai
genai.configure(api_key=API_KEY)

def main():
    console.print("🚀 Iniciando DevGuardian: Auditor de código y arquitectura\n", style="bold cyan")

    reglas = leer_archivo("src/Rules/rules.txt")
    codigo = leer_archivo("code.js")
    contexto = leer_archivo("src/Rules/contexto.txt")

    if not codigo:
        console.print("❌ Faltan archivos o están vacíos. No se puede continuar.", style="red")
        return

    
    # --- Bloque de análisis ---
    codigo_filtrado = limpiar_codigo(codigo)
    estructura = obtener_estructura_directorios(".")

    # Cargar cache
    cache = cargar_cache()
    code_hash = hash_string(codigo_filtrado)

    if cache.get("code_hash") == code_hash:
        console.print("🟢 El código no cambió, usando análisis previo", style="green")
        resultado = cache.get("analysis_result", "⚠️ No hay análisis previo guardado")
    else:
        console.print("\n🤖 Analizando código y estructura del proyecto...\n", style="bold cyan")
        resultado = analizar_codigo(codigo_filtrado, reglas, contexto, estructura)
        
        # Guardar hash y resultado
        cache["code_hash"] = code_hash
        cache["analysis_result"] = resultado
        guardar_cache(cache)

    # Mostrar resultado
    console.print("\n===== RESULTADO DEL ANÁLISIS =====", style="bold white")
    console.print(resultado, style="white")


if __name__ == "__main__":
    main()
