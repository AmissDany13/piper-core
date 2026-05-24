import sys
import json
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import requests

# Cola para guardar el audio en tiempo real
q = queue.Queue()

def callback(indata, frames, time, status):
    """Esta función captura el audio del micrófono continuamente."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

print("Cargando modelo de voz Vosk (100% local y privado)...")
# Carga la carpeta 'model' que acabas de descomprimir
model = Model("model")
rec = KaldiRecognizer(model, 16000)

print("\n👂 Oídos de Piper activos.")
print("Di 'piper' para despertar al sistema (Presiona Ctrl+C para apagar).")

try:
    # Abre el micrófono por defecto de Windows
    with sd.RawInputStream(samplerate=16000, blocksize=8000, device=None, dtype='int16',
                           channels=1, callback=callback):
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                # Extrae el texto que entendió Vosk
                result = json.loads(rec.Result())
                text = result.get("text", "")
                
                # Revisa si la palabra mágica está en el audio
                if "piper" in text.lower():
                    print("\n¡Despertando a Piper!")
                    
                    # Le avisa a n8n que empiece el flujo
                    try:
                        requests.post("http://localhost:5678/webhook-test/piper-comando")
                        print("Señal enviada al orquestador.")
                    except Exception as e:
                        print("Error al contactar a n8n:", e)
                        
except KeyboardInterrupt:
    print("\nOídos apagados.")
except Exception as e:
    print(f"\nOcurrió un error con el micrófono: {e}")