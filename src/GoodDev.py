import os
import sys
from rich.console import Console
from dotenv import load_dotenv
import google.generativeai as genai

# Ajuste de path para importar módulos internos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from .Utils.utils import (
    leer_archivo,
    limpiar_codigo,
    obtener_estructura_directorios
)
from .analyzer import analizar_codigo

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
# FUNCIONES AUXILIARES
# ==============================

def agrupar_errores_por_archivo(texto_resultado):
    """
    Agrupa errores por archivo detectando líneas con '📂 Archivo:'.
    """
    grupos = {}
    archivo_actual = "general"

    for linea in texto_resultado.splitlines():
        if linea.strip().startswith("📂 Archivo:"):
            archivo_actual = linea.strip().split("📂 Archivo:")[-1].strip()
            grupos.setdefault(archivo_actual, [])
        elif any(lvl in linea for lvl in ["🔴", "🟡", "🟢"]):
            grupos.setdefault(archivo_actual, []).append(linea.strip())

    return grupos


def calcular_puntaje(texto_resultado):
    """
    Calcula un puntaje del PR según la cantidad de errores graves, medios y buenas prácticas.
    """
    graves = texto_resultado.count("🔴")
    medias = texto_resultado.count("🟡")
    buenas = texto_resultado.count("🟢")

    puntaje = 100 - (graves * 10) - (medias * 5) + (buenas * 2)
    return max(0, min(100, puntaje))


# ==============================
# PROCESO PRINCIPAL
# ==============================

def main():
    console.print("🚀 Iniciando GoodDev: Auditor de código y arquitectura\n", style="bold cyan")

    # Verificar archivos necesarios
    console.print("🔍 Verificando archivos necesarios...\n", style="bold yellow")
    archivos = ["src/Rules/rules.txt", "code_changes.txt", "src/Rules/context.txt"]
    for ruta in archivos:
        if not os.path.exists(ruta):
            console.print(f"❌ No existe: {ruta}", style="red")
        else:
            size = os.path.getsize(ruta)
            console.print(f"✅ {ruta} encontrado ({size} bytes)", style="green")

    reglas = leer_archivo("src/Rules/rules.txt")
    codigo = leer_archivo("code_changes.txt")
    contexto = leer_archivo("src/Rules/context.txt")

    console.print("\n🧠 DEBUG: Vista previa de archivos cargados:", style="bold yellow")
    console.print(f"rules.txt → {len(reglas)} caracteres", style="cyan")
    console.print(f"code_changes.txt → {len(codigo)} caracteres", style="cyan")
    console.print(f"contexto.txt → {len(contexto)} caracteres", style="cyan")

    if not reglas or not codigo or not contexto:
        console.print("\n❌ Faltan archivos o están vacíos. No se puede continuar.", style="red")
        return

    console.print("\n🤖 Analizando código y estructura del proyecto...\n", style="bold cyan")
    codigo_filtrado = limpiar_codigo(codigo)
    estructura = obtener_estructura_directorios(".")
    resultado = analizar_codigo(codigo_filtrado, reglas, contexto, estructura)

    console.print("\n📊 Procesando resumen por archivo y puntaje...\n", style="bold yellow")

    grupos = agrupar_errores_por_archivo(resultado)
    puntaje = calcular_puntaje(resultado)

    resultado_final = resultado
    resultado_final += "\n\n=== ERRORES DETECTADOS POR ARCHIVO ===\n"
    for archivo, errores in grupos.items():
        resultado_final += f"\n📁 {archivo}\n"
        for e in errores:
            resultado_final += f"  {e}\n"

    resultado_final += f"\n\n🧾 PUNTAJE GLOBAL DEL PR: {puntaje} / 100\n"

    console.print("\n===== RESULTADO DEL ANÁLISIS =====", style="bold white")
    console.print(resultado_final, style="white")

    with open("pull_request.log", "w", encoding="utf-8") as log:
        log.write(resultado_final)

    console.print("\n✅ Análisis completado. Resultado guardado en pull_request.log\n", style="bold cyan")


if __name__ == "__main__":
    main()
