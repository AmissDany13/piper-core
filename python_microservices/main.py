import asyncio
import asyncpg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import logging

app = FastAPI(title="Piper Local Core")
logging.basicConfig(level=logging.INFO)

# Credenciales de tu base de datos local
DB_DSN = "postgresql://admin:adminpassword@localhost:5432/piper_db"

class ContextPayload(BaseModel):
    session_id: str
    role: str
    content: str

class CommandPayload(BaseModel):
    action: str
    target: str

# Lógica de reintentos con backoff exponencial para evitar colisiones de escritura
def retry_with_backoff(max_retries=5, base_delay=0.5):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return await func(*args, **kwargs)
                except (asyncpg.exceptions.DeadlockDetectedError, asyncpg.exceptions.SerializationError, Exception) as e:
                    retries += 1
                    if retries == max_retries:
                        logging.error(f"Fallo definitivo tras {max_retries} intentos. Error: {e}")
                        raise HTTPException(status_code=500, detail="Database write collision")
                    
                    delay = base_delay * (2 ** (retries - 1))
                    logging.warning(f"Colisión en BD detectada. Reintentando en {delay}s... (Intento {retries}/{max_retries})")
                    await asyncio.sleep(delay)
        return wrapper
    return decorator

@app.post("/api/memory/context")
@retry_with_backoff(max_retries=5, base_delay=0.5)
async def save_context(payload: ContextPayload):
    """Guarda la memoria a corto plazo en PostgreSQL."""
    conn = await asyncpg.connect(DB_DSN)
    try:
        await conn.execute(
            "INSERT INTO active_context (session_id, role, content) VALUES ($1, $2, $3)",
            payload.session_id, payload.role, payload.content
        )
        return {"status": "success", "message": "Contexto guardado en la memoria de Piper."}
    finally:
        await conn.close()

@app.post("/api/os/execute")
async def execute_os_command(payload: CommandPayload):
    """Ejecuta comandos nativos en Windows."""
    if payload.action == "open_vscode":
        # Comando no bloqueante para abrir VSCode
        subprocess.Popen(["cmd", "/c", "code", payload.target], shell=True)
        return {"status": "success", "executed": "vscode", "target": payload.target}
    
    return {"status": "unsupported_action"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)