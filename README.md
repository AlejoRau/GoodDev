# 🧠 GoodDev — Auditor Inteligente de Pull Requests

**GoodDev** es un sistema automatizado de revisión de código que analiza los **Pull Requests** en GitHub para verificar el cumplimiento de buenas prácticas de desarrollo.  
Funciona como un **auditor técnico inteligente**, capaz de evaluar código fuente, detectar problemas comunes y sugerir mejoras antes de que se apruebe la fusión.

---

## 🚀 Función Principal

Cada vez que se crea o actualiza un **Pull Request**, GoodDev:

1. Extrae el código modificado (diff del PR).
2. Lo analiza mediante un modelo de IA (Gemini).
3. Evalúa si el código cumple con las reglas de buenas prácticas definidas.
4. Corrige errores estéticos o de formato en el resultado.
5. Publica automáticamente un **comentario con el informe de auditoría** en el PR.

De esta forma, **los revisores humanos reciben un análisis técnico completo sin intervención manual.**

---

## ⚙️ Flujo de Trabajo del Auditor

```mermaid
flowchart TD
    A[Creación o actualización de PR] --> B[GitHub Actions ejecuta el workflow]
    B --> C[Se extrae el diff del código]
    C --> D[Se envía el código a GoodDev.py]
    D --> E[Analyzer analiza el código con IA]
    E --> F[Auditor Corrector limpia y valida la respuesta]
    F --> G[Se genera el informe final]
    G --> H[El bot comenta automáticamente en el Pull Request]
