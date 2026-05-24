import { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [status, setStatus] = useState({ 
    title: "INICIANDO...", 
    message: "Buscando señal de Python..." 
  });

  useEffect(() => {
    let ws: WebSocket;
    let reconnectTimer: NodeJS.Timeout;

    const connectWebSocket = () => {
      // Usamos localhost en lugar de 127.0.0.1 para evitar bloqueos de Windows
      ws = new WebSocket('ws://localhost:8000/api/ws/hud');

      ws.onopen = () => {
        setStatus({ title: "PIPER CORE", message: "Sistemas en línea. Esperando..." });
        if (reconnectTimer) clearTimeout(reconnectTimer);
      };

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        setStatus({ title: data.title, message: data.message });
      };

      ws.onclose = () => {
        setStatus({ title: "PIPER DESCONECTADO", message: "Reconectando en 3 segundos..." });
        // Si se cae, intentará conectarse de nuevo automáticamente
        reconnectTimer = setTimeout(connectWebSocket, 3000);
      };

      ws.onerror = () => {
        // En caso de error, forzamos el cierre para que onclose dispare la reconexión
        ws.close();
      };
    };

    connectWebSocket();

    // Limpieza al cerrar la aplicación
    return () => {
      if (reconnectTimer) clearTimeout(reconnectTimer);
      if (ws) ws.close();
    };
  }, []);

  return (
    <div className="hud-container">
      <div className="glass-panel">
        <h3 style={{ color: status.title.includes("DESCONECTADO") ? '#ff4444' : '#00ffcc' }}>
          {status.title}
        </h3>
        <p>{status.message}</p>
      </div>
    </div>
  );
}

export default App;