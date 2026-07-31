HTML_DASHBOARD = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Flujo Vehicular</title>
    <style>
        body { font-family: Arial, sans-serif; background: #1a1a2e; color: #eee; padding: 20px; }
        h1 { color: #00d4ff; }
        #stats { display: flex; gap: 20px; margin-bottom: 20px; flex-wrap: wrap; }
        .stat { background: #16213e; padding: 15px 25px; border-radius: 10px; text-align: center; }
        .stat h2 { margin: 0; font-size: 2em; color: #00d4ff; }
        .stat h2.flujo { color: #6bcb77; font-size: 2.2em; }
        .stat p { margin: 5px 0 0; color: #aaa; }
        .stat.highlight { border: 1px solid #6bcb77; }
        #tabla { width: 100%; border-collapse: collapse; }
        #tabla th { background: #16213e; padding: 10px; text-align: left; }
        #tabla td { padding: 8px 10px; border-bottom: 1px solid #333; }
        .auto { color: #00d4ff; } .moto { color: #ff6b6b; }
        .bus  { color: #ffd93d; } .camion { color: #6bcb77; }
        #estado { color: #aaa; font-size: 0.85em; margin-bottom: 10px; }
        #video-section { margin-bottom: 20px; display: flex; gap: 10px; flex-wrap: wrap; align-items: center; }
        .btn { padding: 10px 24px; border-radius: 8px; border: none;
            font-size: 14px; cursor: pointer; font-weight: bold; }
        #btn-video { background: #00d4ff; color: #1a1a2e; }
        #btn-video.activo { background: #ff6b6b; color: #fff; }
        #btn-csv { background: #6bcb77; color: #1a1a2e; text-decoration: none; display: inline-block; }
        #btn-calibrar { background: #ffd93d; color: #1a1a2e; }
        #video-container { margin-top: 12px; display: none; }
        #video-container img { width: 100%; max-width: 640px; border-radius: 8px; border: 2px solid #00d4ff; }
        #video-label { font-size: 12px; color: #aaa; margin-top: 6px; }
        #flujo-label { font-size: 11px; color: #6bcb77; margin-top: 2px; }
    </style>
</head>
<body>
    <h1>Monitor de Flujo Vehicular</h1>
    <div id="estado">Conectando...</div>
        <div id="fan-control" style="background:#16213e;padding:12px 18px;border-radius:10px;display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin-bottom:20px;">
            <span style="color:#a29bfe;font-weight:bold;font-size:13px;">FANS</span>
            <span id="fan-modo-badge" style="font-size:11px;padding:2px 8px;border-radius:8px;background:#1a4a1a;color:#6bcb77;">AUTO</span>
            <input type="range" id="fan-slider" min="0" max="100" step="5" value="0"
                style="width:140px;accent-color:#a29bfe;" oninput="document.getElementById('fan-slider-val').textContent=this.value+'%'">
            <span id="fan-slider-val" style="color:#eee;font-size:13px;min-width:36px;">0%</span>
            <button class="btn" style="background:#a29bfe;color:#1a1a2e;padding:8px 16px;font-size:13px;" onclick="setFanManual()">Aplicar manual</button>
            <button class="btn" style="background:#555;color:#eee;padding:8px 16px;font-size:13px;" onclick="setFanAuto()">Volver a auto</button>
        </div>
    <div id="video-section">
        <button id="btn-video" class="btn" onclick="toggleVideo()">Activar video en vivo</button>
        <a id="btn-csv" class="btn" href="/descargar">Descargar CSV</a>
        <button id="btn-calibrar" class="btn" onclick="window.location.href='/calibrar'">Calibrar lineas</button>
        <button id="btn-reset" class="btn" onclick="resetDetecciones()" style="background:#ff6b6b;color:#fff;">Resetear conteos</button>
    </div>
    <div id="video-container">
        <img id="video-stream" src="" alt="Stream de camara"/>
        <div id="video-label">Stream en vivo - 15 FPS</div>
    </div>
    <div id="stats">
        <div class="stat highlight">
            <h2 id="flujo" class="flujo">0</h2><p>Flujo (veh/h)</p>
            <div id="flujo-label">ultimos 5 min: <span id="veh5min">0</span> veh</div>
        </div>
        <div class="stat"><h2 id="total">0</h2><p>Total</p></div>
        <div class="stat"><h2 id="cnt_auto" style="color:#00d4ff">0</h2><p>Autos</p></div>
        <div class="stat"><h2 id="cnt_moto" style="color:#ff6b6b">0</h2><p>Motos</p></div>
        <div class="stat"><h2 id="cnt_bus" style="color:#ffd93d">0</h2><p>Buses</p></div>
        <div class="stat"><h2 id="cnt_camion" style="color:#6bcb77">0</h2><p>Camiones</p></div>
        <div class="stat"><h2 id="vel_prom">0</h2><p>Vel. promedio (km/h)</p></div>
        <div class="stat"><h2 id="vel_max">0</h2><p>Vel. maxima (km/h)</p></div>
        <div class="stat"><h2 id="fps_actual">0</h2><p>FPS</p></div>
        <div class="stat"><h2 id="cpu_temp" style="color:#ff9f43">--</h2><p>CPU (&deg;C)</p></div>
        <div class="stat"><h2 id="fan_pct" style="color:#a29bfe">--</h2><p>Fan (%)</p></div>
        <div class="stat"><h2 id="temp_ambiente" style="color:#fd79a8">--</h2><p>Ambiente (&deg;C)</p></div>
        <div class="stat"><h2 id="humedad" style="color:#74b9ff">--</h2><p>Humedad (%)</p></div>
    </div>
    <table id="tabla">
        <thead><tr><th>Hora</th><th>Tipo</th><th>ID</th><th>Velocidad</th><th>Flujo (veh/h)</th></tr></thead>
        <tbody id="filas"></tbody>
    </table>
    <script>

        function setFanManual() {
            const speed = parseInt(document.getElementById("fan-slider").value);
            fetch("/api/fans", {method:"POST", headers:{"Content-Type":"application/json"},
                body: JSON.stringify({modo:"manual", speed: speed})})
            .then(r => r.json()).then(d => {
                document.getElementById("fan-modo-badge").textContent = "MANUAL " + d.fan_pct + "%";
                document.getElementById("fan-modo-badge").style.background = "#5a3a00";
                document.getElementById("fan-modo-badge").style.color = "#ffd93d";
            });
        }
        function setFanAuto() {
            fetch("/api/fans", {method:"POST", headers:{"Content-Type":"application/json"},
                body: JSON.stringify({modo:"auto"})})
            .then(r => r.json()).then(d => {
                document.getElementById("fan-modo-badge").textContent = "AUTO";
                document.getElementById("fan-modo-badge").style.background = "#1a4a1a";
                document.getElementById("fan-modo-badge").style.color = "#6bcb77";
            });
        }
        let suma_vel = 0, max_vel = 0, total_vel = 0, videoEncendido = false;
        const ws = new WebSocket(`ws://${location.host}/ws`);
        ws.onopen = () => document.getElementById("estado").textContent = "Conectado a la Pi";
        ws.onclose = () => document.getElementById("estado").textContent = "Desconectado";
        ws.onmessage = (event) => {
            const d = JSON.parse(event.data);
            if (d.tipo === "estado") {
                const tot = (d.conteo.auto||0)+(d.conteo.moto||0)+(d.conteo.bus||0)+(d.conteo.camion||0);
                document.getElementById("total").textContent = tot;
                document.getElementById("cnt_auto").textContent = d.conteo.auto||0;
                document.getElementById("cnt_moto").textContent = d.conteo.moto||0;
                document.getElementById("cnt_bus").textContent = d.conteo.bus||0;
                document.getElementById("cnt_camion").textContent = d.conteo.camion||0;
                document.getElementById("flujo").textContent = d.flujo_veh_h;
                document.getElementById("veh5min").textContent = d.vehiculos_5min;
                return;
            }
            if (d.tipo === "fps") { document.getElementById("fps_actual").textContent = d.fps; return; }
            if (d.tipo === "sensores") {
                if (d.cpu_temp != null) document.getElementById("cpu_temp").textContent = d.cpu_temp;
                if (d.fan_pct != null) document.getElementById("fan_pct").textContent = d.fan_pct;
                if (d.temp_ambiente != null) document.getElementById("temp_ambiente").textContent = d.temp_ambiente;
                if (d.humedad != null) document.getElementById("humedad").textContent = d.humedad;
                if (d.fan_modo) {
                    const badge = document.getElementById("fan-modo-badge");
                    if (d.fan_modo === "auto") {
                        badge.textContent = "AUTO"; badge.style.background="#1a4a1a"; badge.style.color="#6bcb77";
                    } else {
                        badge.textContent = "MANUAL " + d.fan_pct + "%"; badge.style.background="#5a3a00"; badge.style.color="#ffd93d";
                    }
                }
                return;
            }
            if (d.tipo === "flujo") {
                document.getElementById("flujo").textContent = d.flujo_veh_h;
                document.getElementById("veh5min").textContent = d.vehiculos_5min;
                return;
            }
            suma_vel += d.velocidad_kmh; total_vel++;
            if (d.velocidad_kmh > max_vel) max_vel = d.velocidad_kmh;
            if (d.conteo) {
                const tot = (d.conteo.auto||0)+(d.conteo.moto||0)+(d.conteo.bus||0)+(d.conteo.camion||0);
                document.getElementById("total").textContent = tot;
                document.getElementById("cnt_auto").textContent = d.conteo.auto||0;
                document.getElementById("cnt_moto").textContent = d.conteo.moto||0;
                document.getElementById("cnt_bus").textContent = d.conteo.bus||0;
                document.getElementById("cnt_camion").textContent = d.conteo.camion||0;
            }
            document.getElementById("vel_prom").textContent = (suma_vel/total_vel).toFixed(1);
            document.getElementById("vel_max").textContent = max_vel.toFixed(1);
            const fila = `<tr><td>${d.timestamp}</td><td class="${d.tipo}">${d.tipo}</td><td>${d.id}</td><td>${d.velocidad_kmh} km/h</td><td>${d.flujo_veh_h} veh/h</td></tr>`;
            document.getElementById("filas").insertAdjacentHTML("afterbegin", fila);
        };
        function resetDetecciones() {
            if (!confirm("Resetear todos los conteos y velocidades?")) return;
            fetch("/api/reset", {method:"POST"})
            .then(r => r.json())
            .then(d => {
                if (d.ok) {
                    suma_vel = 0; max_vel = 0; total_vel = 0;
                    document.getElementById("filas").innerHTML = "";
                    document.getElementById("vel_prom").textContent = "0";
                    document.getElementById("vel_max").textContent = "0";
                }
            });
        }
        function toggleVideo() {
            videoEncendido = !videoEncendido;
            const btn = document.getElementById("btn-video");
            const container = document.getElementById("video-container");
            const img = document.getElementById("video-stream");
            if (videoEncendido) {
                btn.textContent = "Desactivar video"; btn.classList.add("activo");
                container.style.display = "block";
                img.src = "/video?" + Date.now();
            } else {
                btn.textContent = "Activar video en vivo"; btn.classList.remove("activo");
                container.style.display = "none";
                img.src = ""; fetch("/video/stop");
            }
        }
    </script>
</body>
</html>"""

HTML_CALIBRACION = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Calibracion - Flujo Vehicular</title>
    <style>
        * { box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #1a1a2e; color: #eee; padding: 20px; margin: 0; }
        h1 { color: #00d4ff; margin: 0 0 5px; font-size: 1.4em; }
        .back { color: #aaa; text-decoration: none; font-size: 13px; display: inline-block; margin-bottom: 12px; }
        .back:hover { color: #00d4ff; }
        .layout { display: flex; gap: 20px; flex-wrap: wrap; align-items: flex-start; margin-top: 15px; }
        #wrapper { position: relative; display: inline-block; flex-shrink: 0; max-width: 100%; }
        #cal-stream { display: block; width: 640px; max-width: 100%; border-radius: 8px;
                      border: 2px solid #333; background: #000; }
        #cal-canvas { position: absolute; top: 0; left: 0; border-radius: 6px; touch-action: none; }
        .panel { background: #16213e; padding: 20px; border-radius: 10px; width: 240px; flex-shrink: 0; }
        .panel h2 { margin: 0 0 15px; color: #00d4ff; font-size: 1em; text-transform: uppercase;
                    letter-spacing: 1px; }
        .line-block { margin-bottom: 18px; }
        .line-block label { font-size: 12px; color: #aaa; display: block; margin-bottom: 4px; }
        .line-val { font-size: 2em; font-weight: bold; line-height: 1; }
        .val-a { color: #4d9eff; }
        .val-b { color: #ff5555; }
        .val-x { color: #ffd93d; }
        .sub { font-size: 11px; color: #666; }
        .sep { border: none; border-top: 1px solid #2a3555; margin: 16px 0; }
        .field label { font-size: 12px; color: #aaa; display: block; margin-bottom: 6px; }
        .field input { width: 100%; padding: 9px 12px; background: #0f1629; border: 1px solid #2a3555;
                       color: #eee; border-radius: 6px; font-size: 15px; }
        .field input:focus { outline: none; border-color: #00d4ff; }
        .btn-save { width: 100%; padding: 12px; background: #6bcb77; color: #1a1a2e; border: none;
                    border-radius: 8px; font-size: 15px; font-weight: bold; cursor: pointer; margin-top: 16px; }
        .btn-save:hover { background: #58b864; }
        .btn-save:disabled { background: #3a6b40; color: #aaa; cursor: default; }
        .btn-cancel { width: 100%; padding: 9px; background: transparent; color: #888;
                      border: 1px solid #2a3555; border-radius: 8px; font-size: 13px;
                      cursor: pointer; margin-top: 8px; }
        .btn-cancel:hover { border-color: #aaa; color: #eee; }
        .ok-msg { color: #6bcb77; font-size: 13px; text-align: center; margin-top: 10px; display: none; }
        .hint { font-size: 12px; color: #555; line-height: 1.6; margin-top: 16px; }
        .hint b { color: #777; }
        #estado { font-size: 12px; color: #666; margin-bottom: 10px; }
        .badge { display: inline-block; padding: 2px 8px; border-radius: 10px; font-size: 11px;
                 font-weight: bold; }
        .badge-pause { background: #5a3a00; color: #ffd93d; }
        .badge-ok { background: #1a4a1a; color: #6bcb77; }
    </style>
</head>
<body>
    <a class="back" href="/" id="back-link">&#8592; Volver al dashboard</a>
    <h1>Calibracion de Lineas</h1>
    <div id="estado"><span class="badge badge-pause">Conectando...</span></div>

    <div class="layout">
        <div id="wrapper">
            <img id="cal-stream" src="/video/calibrar" alt="Stream de calibracion">
            <canvas id="cal-canvas"></canvas>
        </div>

        <div class="panel">
            <h2>Lineas de referencia</h2>

            <div class="line-block">
                <label>LINEA A (azul) &mdash; primer punto</label>
                <div class="line-val val-a" id="val-a">---</div>
                <div class="sub">pixeles desde arriba (0&ndash;480)</div>
            </div>

            <div class="line-block">
                <label>LINEA B (roja) &mdash; segundo punto</label>
                <div class="line-val val-b" id="val-b">---</div>
                <div class="sub">pixeles desde arriba (0&ndash;480)</div>
            </div>

            <div class="line-block">
                <label>LIMITE X (amarillo) &mdash; excluir zona izquierda</label>
                <div class="line-val val-x" id="val-x">---</div>
                <div class="sub">pixeles desde la izquierda (0&ndash;640). 0 = desactivado</div>
            </div>

            <hr class="sep">

            <div class="field">
                <label>Distancia real entre lineas (metros)</label>
                <input type="number" id="dist-input" value="8.0" step="0.1" min="0.5" max="500">
            </div>

            <button class="btn-save" id="btn-save" onclick="guardar()">Guardar y reanudar</button>
            <button class="btn-cancel" onclick="salir()">Cancelar</button>
            <div class="ok-msg" id="ok-msg">&#10003; Guardado &mdash; redirigiendo...</div>

            <div class="hint">
                <b>Como calibrar:</b><br>
                1. Identifica dos puntos fisicos separados por una distancia conocida (bases de postes, lineas del suelo, etc.)<br>
                2. Arrastra la Linea A al primer punto<br>
                3. Arrastra la Linea B al segundo punto<br>
                4. Escribe la distancia real entre ellos<br>
                5. Si hay vehiculos estacionados a la izquierda (zona de parqueo), arrastra el Limite X hasta el borde del carril de circulacion<br>
                6. Guarda
            </div>
        </div>
    </div>

<script>
    let lineaAy = 237, lineaBy = 337;
    let lineaXmin = 0;
    let dragging = null;
    let canvasReady = false;
    let streamLoaded = false;

    // WebSocket mantiene el modo calibracion activo en el servidor
    const wsUrl = 'ws://' + location.host + '/ws/calibrar';
    let ws = null;

    function conectarWS() {
        ws = new WebSocket(wsUrl);
        ws.onopen = () => {
            document.getElementById('estado').innerHTML =
                '<span class="badge badge-pause">Deteccion pausada</span>';
            // Ping cada 5s para mantener el modo calibracion activo
            if (window._pingInterval) clearInterval(window._pingInterval);
            window._pingInterval = setInterval(() => {
                if (ws && ws.readyState === WebSocket.OPEN) ws.send('ping');
            }, 5000);
        };
        ws.onclose = () => {
            clearInterval(window._pingInterval);
            if (document.visibilityState !== 'hidden') {
                setTimeout(conectarWS, 1000);
            }
        };
    }
    conectarWS();

    // Cargar config actual
    fetch('/api/config').then(r => r.json()).then(cfg => {
        lineaAy = cfg.linea_a_y;
        lineaBy = cfg.linea_b_y;
        lineaXmin = cfg.linea_x_min || 0;
        document.getElementById('val-a').textContent = lineaAy;
        document.getElementById('val-b').textContent = lineaBy;
        document.getElementById('val-x').textContent = lineaXmin;
        document.getElementById('dist-input').value = cfg.distancia;
        if (canvasReady) drawLines();
    });

    const img = document.getElementById('cal-stream');
    const canvas = document.getElementById('cal-canvas');

    function syncCanvas() {
        if (img.clientWidth > 0 && img.clientHeight > 0) {
            if (canvas.width !== img.clientWidth || canvas.height !== img.clientHeight) {
                canvas.width = img.clientWidth;
                canvas.height = img.clientHeight;
                canvasReady = true;
                drawLines();
            }
        }
    }

    img.addEventListener('load', () => {
        if (!streamLoaded) {
            streamLoaded = true;
            syncCanvas();
        } else {
            // Para streams MJPEG, sincronizar solo si el tamano cambio
            syncCanvas();
        }
        drawLines();
    });

    setInterval(syncCanvas, 800);

    function fy2cy(fy) {
        return fy * (canvas.height / 480);
    }
    function cy2fy(cy) {
        return Math.max(0, Math.min(479, Math.round(cy * (480 / canvas.height))));
    }
    function fx2cx(fx) {
        return fx * (canvas.width / 640);
    }
    function cx2fx(cx) {
        return Math.max(0, Math.min(639, Math.round(cx * (640 / canvas.width))));
    }

    function drawLines() {
        if (!canvas.width || !canvas.height) return;
        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        const ya = fy2cy(lineaAy);
        const yb = fy2cy(lineaBy);
        const mx = canvas.width / 2;

        // Linea A - azul
        ctx.beginPath();
        ctx.strokeStyle = dragging === 'A' ? '#99ccff' : '#4d9eff';
        ctx.lineWidth = dragging === 'A' ? 3 : 2;
        ctx.moveTo(0, ya); ctx.lineTo(canvas.width, ya);
        ctx.stroke();
        ctx.fillStyle = '#4d9eff';
        ctx.font = 'bold 13px Arial';
        ctx.fillText('A  ' + lineaAy + 'px', 8, ya - 6);
        ctx.beginPath();
        ctx.arc(mx, ya, 7, 0, Math.PI * 2);
        ctx.fill();

        // Linea B - roja
        ctx.beginPath();
        ctx.strokeStyle = dragging === 'B' ? '#ff9999' : '#ff5555';
        ctx.lineWidth = dragging === 'B' ? 3 : 2;
        ctx.moveTo(0, yb); ctx.lineTo(canvas.width, yb);
        ctx.stroke();
        ctx.fillStyle = '#ff5555';
        ctx.fillText('B  ' + lineaBy + 'px', 8, yb - 6);
        ctx.beginPath();
        ctx.arc(mx, yb, 7, 0, Math.PI * 2);
        ctx.fill();

        // Limite X - amarillo
        const xm = fx2cx(lineaXmin);
        const my = canvas.height / 2;
        ctx.beginPath();
        ctx.strokeStyle = dragging === 'X' ? '#fff0a3' : '#ffd93d';
        ctx.lineWidth = dragging === 'X' ? 3 : 2;
        ctx.moveTo(xm, 0); ctx.lineTo(xm, canvas.height);
        ctx.stroke();
        ctx.fillStyle = '#ffd93d';
        ctx.fillText('X  ' + lineaXmin + 'px', xm + 6, 16);
        ctx.beginPath();
        ctx.arc(xm, my, 7, 0, Math.PI * 2);
        ctx.fill();
    }

    function getClientY(e) {
        const rect = canvas.getBoundingClientRect();
        const clientY = e.touches ? e.touches[0].clientY : e.clientY;
        return clientY - rect.top;
    }
    function getClientX(e) {
        const rect = canvas.getBoundingClientRect();
        const clientX = e.touches ? e.touches[0].clientX : e.clientX;
        return clientX - rect.left;
    }

    function lineaNear(cx, cy) {
        const thresh = 14;
        if (Math.abs(cy - fy2cy(lineaAy)) < thresh) return 'A';
        if (Math.abs(cy - fy2cy(lineaBy)) < thresh) return 'B';
        if (Math.abs(cx - fx2cx(lineaXmin)) < thresh) return 'X';
        return null;
    }

    canvas.addEventListener('mousedown', e => {
        dragging = lineaNear(getClientX(e), getClientY(e));
        if (dragging) drawLines();
    });
    canvas.addEventListener('touchstart', e => {
        e.preventDefault();
        dragging = lineaNear(getClientX(e), getClientY(e));
        if (dragging) drawLines();
    }, { passive: false });

    canvas.addEventListener('mousemove', e => {
        const cx = getClientX(e);
        const cy = getClientY(e);
        if (!dragging) {
            const near = lineaNear(cx, cy);
            canvas.style.cursor = near === 'X' ? 'ew-resize' : (near ? 'ns-resize' : 'default');
            return;
        }
        if (dragging === 'A') {
            lineaAy = cy2fy(cy);
            document.getElementById('val-a').textContent = lineaAy;
        } else if (dragging === 'B') {
            lineaBy = cy2fy(cy);
            document.getElementById('val-b').textContent = lineaBy;
        } else {
            lineaXmin = cx2fx(cx);
            document.getElementById('val-x').textContent = lineaXmin;
        }
        drawLines();
    });
    canvas.addEventListener('touchmove', e => {
        e.preventDefault();
        if (!dragging) return;
        const cx = getClientX(e);
        const cy = getClientY(e);
        if (dragging === 'A') {
            lineaAy = cy2fy(cy);
            document.getElementById('val-a').textContent = lineaAy;
        } else if (dragging === 'B') {
            lineaBy = cy2fy(cy);
            document.getElementById('val-b').textContent = lineaBy;
        } else {
            lineaXmin = cx2fx(cx);
            document.getElementById('val-x').textContent = lineaXmin;
        }
        drawLines();
    }, { passive: false });

    canvas.addEventListener('mouseup', () => { dragging = null; drawLines(); });
    canvas.addEventListener('mouseleave', () => { dragging = null; drawLines(); });
    canvas.addEventListener('touchend', () => { dragging = null; drawLines(); });

    function guardar() {
        const dist = parseFloat(document.getElementById('dist-input').value);
        if (isNaN(dist) || dist <= 0) { alert('Ingresa una distancia valida'); return; }
        const btn = document.getElementById('btn-save');
        btn.disabled = true;
        btn.textContent = 'Guardando...';
        fetch('/api/config', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ distancia: dist, linea_a_y: lineaAy, linea_b_y: lineaBy, linea_x_min: lineaXmin })
        }).then(r => r.json()).then(data => {
            if (data.ok) {
                if (ws) ws.close();
                document.getElementById('ok-msg').style.display = 'block';
                document.getElementById('estado').innerHTML =
                    '<span class="badge badge-ok">Deteccion reanudada</span>';
                setTimeout(() => window.location.href = '/', 1200);
            }
        }).catch(() => {
            btn.disabled = false;
            btn.textContent = 'Guardar y reanudar';
            alert('Error al guardar');
        });
    }

    function salir() {
        if (ws) ws.close();
        window.location.href = '/';
    }

    document.getElementById('back-link').addEventListener('click', e => {
        e.preventDefault();
        salir();
    });

    window.addEventListener('beforeunload', () => {
        if (ws) ws.close();
    });
</script>
</body>
</html>"""
