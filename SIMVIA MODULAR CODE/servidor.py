import asyncio
import json
import threading

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse, FileResponse
import uvicorn

from fans import FanController
from dht11 import DHT11Sensor

import config
import estado
import vision
import comunicacion
from plantillas import HTML_DASHBOARD, HTML_CALIBRACION

app = FastAPI()
fan_controller = None
dht_sensor = None


@app.get("/")
async def dashboard():
    return HTMLResponse(HTML_DASHBOARD)


@app.get("/calibrar")
async def pagina_calibracion():
    return HTMLResponse(HTML_CALIBRACION)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    comunicacion.clientes.append(websocket)
    print(f"Cliente conectado. Total: {len(comunicacion.clientes)}")
    flujo_ini, veh5_ini = estado.calcular_flujo()
    await websocket.send_text(json.dumps({
        "tipo": "estado",
        "conteo": dict(estado.conteo),
        "flujo_veh_h": flujo_ini,
        "vehiculos_5min": veh5_ini
    }))
    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        comunicacion.clientes.remove(websocket)
        print(f"Cliente desconectado. Total: {len(comunicacion.clientes)}")


@app.websocket("/ws/calibrar")
async def ws_calibrar(websocket: WebSocket):
    await websocket.accept()
    vision.modo_calibracion.set()
    print("Modo calibracion activado")
    try:
        while True:
            # Ping cada 5s; si el cliente no responde en 10s, cierra
            await asyncio.wait_for(websocket.receive_text(), timeout=10.0)
    except (WebSocketDisconnect, asyncio.TimeoutError, Exception):
        vision.modo_calibracion.clear()
        print("Modo calibracion desactivado — deteccion reanudada")


@app.get("/api/config")
async def get_config():
    return JSONResponse(config.snapshot())


@app.post("/api/config")
async def set_config(request: Request):
    body = await request.json()
    config.actualizar(
        body["distancia"], body["linea_a_y"], body["linea_b_y"],
        body.get("linea_x_min", config.LINEA_X_MIN)
    )
    return JSONResponse({"ok": True, **config.snapshot()})


@app.get("/calibrar/salir")
async def salir_calibracion():
    vision.modo_calibracion.clear()
    return JSONResponse({"ok": True})


@app.get("/video")
async def video_stream():
    return StreamingResponse(
        vision.generar_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )


@app.get("/video/calibrar")
async def video_calibrar():
    return StreamingResponse(
        vision.generar_frames_calibracion(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )


@app.get("/video/stop")
async def video_stop():
    vision.stream_activo = False
    return {"status": "stopped"}


@app.get("/descargar")
async def descargar_csv():
    nombre = "flujo_historico.csv"
    return FileResponse(config.LOG_FILE, media_type="text/csv", filename=nombre)


@app.post("/api/reset")
async def reset_detecciones():
    estado.resetear()
    vision.reset_pendiente.set()
    estado.guardar_estado()
    flujo, vehiculos_5min = estado.calcular_flujo()
    await comunicacion.enviar_datos({
        "tipo": "estado", "conteo": dict(estado.conteo),
        "flujo_veh_h": flujo, "vehiculos_5min": vehiculos_5min
    })
    return JSONResponse({"ok": True})


@app.post("/api/fans")
async def set_fans(request: Request):
    body = await request.json()
    if fan_controller is None:
        return JSONResponse({"ok": False, "error": "fans no disponible"})
    modo = body.get("modo", "auto")
    if modo == "manual":
        speed = max(0, min(100, int(body.get("speed", 0))))
        fan_controller.set_manual(speed)
    else:
        fan_controller.set_manual(None)
    return JSONResponse({"ok": True, "modo": fan_controller.modo, "fan_pct": fan_controller.velocidad})


@app.get("/api/fans")
async def get_fans():
    if fan_controller is None:
        return JSONResponse({"ok": False})
    return JSONResponse({"ok": True, **fan_controller.datos()})


@app.on_event("startup")
async def startup():
    loop = asyncio.get_event_loop()
    config.cargar_config()
    estado.cargar_estado()
    global fan_controller, dht_sensor
    dht_sensor = DHT11Sensor()
    fan_controller = FanController(dht_sensor=dht_sensor)
    threading.Thread(target=vision.hilo_captura, daemon=True).start()
    threading.Thread(target=vision.hilo_inferencia, args=(loop,), daemon=True).start()
    threading.Thread(
        target=comunicacion.hilo_log_flujo,
        args=(loop, fan_controller, dht_sensor),
        daemon=True
    ).start()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80, timeout_graceful_shutdown=5)
