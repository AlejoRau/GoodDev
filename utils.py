import os, json, hashlib

CACHE_FILE = ".gooddev_cache.json"

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

def cargar_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def guardar_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)

def hash_string(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()
