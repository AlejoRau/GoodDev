import os

def leer_archivo(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""

def limpiar_codigo(codigo):
    return "\n".join([l for l in codigo.splitlines() if "# devguardian: ignore" not in l])

def obtener_estructura_directorios(base_path="."):
    estructura = []
    for root, dirs, files in os.walk(base_path):
        if any(skip in root for skip in ["venv", "__pycache__", ".git"]):
            continue
        nivel = root.replace(base_path, "").count(os.sep)
        indent = "  " * nivel
        estructura.append(f"{indent}{os.path.basename(root)}/")
        for f in files:
            estructura.append(f"{indent}  {f}")
    return "\n".join(estructura)
