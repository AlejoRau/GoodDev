# Auditor Inteligente de PR's

**GoodDev** es un sistema automatizado de revisión de código que analiza los **Pull Requests** en GitHub para verificar el cumplimiento de buenas prácticas de desarrollo.  
Funciona como un **auditor inteligente**, capaz de evaluar código fuente, detectar problemas comunes y sugerir mejoras antes de que se apruebe la fusión.

---

##  Función Principal

Cada vez que se crea o actualiza un **Pull Request**, GoodDev:

1. Extrae el código modificado (diff del PR).
2. Lo analiza mediante un modelo de IA (Gemini).
3. Evalúa si el código cumple con las reglas de buenas prácticas definidas.
4. Corrige errores estéticos o de formato en el resultado.
5. Publica automáticamente un **comentario con el informe de auditoría** en el PR.

De esta forma, **los revisores humanos reciben un análisis técnico completo sin intervención manual.**

---

## Implementaciones Futuras

El objetivo a futuro es evolucionar hacia un agente autónomo ReAct, con capacidades de auditoría de código:

Analizar PRs y repositorios completos de manera contextual, entendiendo la arquitectura del proyecto.

Aplicar razonamiento paso a paso combinando conocimiento técnico almacenado (RAG) y razonamiento dinámico (ReAct).

Sugerir automáticamente correcciones de código o mejoras en la estructura del proyecto.

Aprender de revisiones pasadas para mejorar la calidad de sus auditorías con el tiempo.

Integrarse completamente con GitHub Actions para actuar como un revisor de código inteligente, que no solo reporta problemas, sino que también propone soluciones.
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
    G --> H[El bot comenta automáticamente las sugerencias]



