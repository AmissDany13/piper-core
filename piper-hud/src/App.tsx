import { useEffect, useState } from 'react';
import './App.css';

function App() {
  // Estado dinámico del HUD
  const [status, setStatus] = useState({ 
    title: "INICIANDO...", 
    message: "Conectando al núcleo local de Piper" 
  });

  useEffect(() => {
    // Conexión al túnel de WebSocket de Python
    const ws = new WebSocket('ws://127.0.0.1:8000/api/ws/hud');

    ws.onopen = () => {
      setStatus({ title: "PIPER CORE", message: "Sistemas en línea. Esperando..." });
    };

    ws.onmessage = (event) => {
      // Cuando Python nos envía un aviso, actualizamos la pantalla
      const data = JSON.parse(event.data);
      setStatus({ title: data.title, message: data.message });
    };

    ws.onclose = () => {
      setStatus({ title: "PIPER DESCONECTADO", message: "Se perdió conexión con el núcleo. Revisa la terminal." });
    };

    // Limpieza al cerrar
    return () => ws.close();
  }, []);

  return (
    <div className="hud-container">
      <div className="glass-panel">
        <h3 className={status.title === "PIPER DESCONECTADO" ? "error-text" : ""}>
          {status.title}
        </h3>
        <p>{status.message}</p>
      </div>
    </div>
  );
}

export default App;