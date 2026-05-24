# ⚡ Piper Core - Asistente Multimodal de Escritorio

Piper es una arquitectura modular y escalable para un asistente personal estilo "Copilot/JARVIS", diseñado para operar estrictamente en local (Windows) garantizando privacidad, baja latencia y control total del sistema operativo.

## 🏗️ Arquitectura del Sistema

El proyecto está dividido en tres pilares fundamentales:

1. **Cerebro (Orquestación & Memoria):**
   - **n8n:** Orquestador visual de flujos lógicos y conexión con APIs externas.
   - **PostgreSQL + pgvector:** Memoria a largo plazo (RAG) y almacenamiento vectorial de contexto conversacional.
2. **Sistema Nervioso Central (Microservicios Locales):**
   - **FastAPI (Python):** Interfaz de control a bajo nivel.
   - Manejo de ejecución de comandos en Windows (VSCode, terminales).
   - Servidor WebSocket para empujar actualizaciones de estado en tiempo real.
3. **Rostro (Interfaz Visual HUD):**
   - **Tauri + React (TypeScript):** Overlay transparente, sin bordes y de bajo consumo (RAM < 30MB).
   - Escucha eventos a través de WebSockets para actualizar el estado del asistente dinámicamente.

## 🚀 Stack Tecnológico

* **Backend:** Python 3, FastAPI, asyncpg, WebSockets.
* **Frontend:** Tauri, React, Vite, CSS (Glassmorphism).
* **Infraestructura:** Docker Compose.
* **Voz y Visión (En desarrollo):** Picovoice Porcupine (Wake word), Whisper (STT).

## 📂 Estructura del Directorio

\`\`\`text
PIPER/
├── docker-compose.yml         # Infraestructura base (n8n + Postgres)
├── python_microservices/      # Core local (FastAPI, control OS, websockets)
└── piper-hud/                 # Interfaz visual translúcida (Tauri)
\`\`\`