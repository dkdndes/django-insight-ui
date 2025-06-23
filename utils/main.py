# websocket_main.py

import os, asyncio, json, datetime, psutil, shutil, uuid, logging, traceback
import websockets
from websockets.server import WebSocketServerProtocol

# --- Konfiguration ---
DEBUG = os.getenv("DEBUG", "true").lower() in ("1", "true", "yes")
HOST, PORT = '0.0.0.0', 8765

# --- Logging Setup (wie zuvor) ---
level = logging.DEBUG if DEBUG else logging.INFO
formatter = logging.Formatter('[%(asctime)s] %(levelname)s [%(name)s] %(message)s', datefmt='%H:%M:%S')

root = logging.getLogger()
root.setLevel(level)
ch = logging.StreamHandler()
ch.setLevel(level)
ch.setFormatter(formatter)
root.addHandler(ch)

from logging.handlers import RotatingFileHandler
fh = RotatingFileHandler('app.log', maxBytes=10*1024*1024, backupCount=3)
fh.setLevel(logging.ERROR)
fh.setFormatter(formatter)
root.addHandler(fh)

logger = logging.getLogger(__name__)

# --- Helper Funktionen ---
def safe_json(data):
    def default(o):
        if isinstance(o, (datetime.datetime, datetime.date)):
            return o.isoformat()
        if isinstance(o, uuid.UUID):
            return str(o)
        return str(o)
    return json.dumps(data, default=default)

async def system_info():
    now = datetime.datetime.utcnow()
    disk = shutil.disk_usage("/")
    mem = psutil.virtual_memory()
    return {
        "timestamp": now,
        "disk": {"total_gb": round(disk.total/2**30,2), "used_gb": round(disk.used/2**30,2), "free_gb": round(disk.free/2**30,2)},
        "memory": {"total_gb": round(mem.total/2**30,2), "available_gb": round(mem.available/2**30,2), "percent_used": mem.percent}
    }

# --- WebSocket-Handler ---
async def handler(ws: WebSocketServerProtocol):
    conn_id = str(uuid.uuid4())
    remote = ws.remote_address or ("unknown", "?")
    ip, port = remote[0], remote[1] if len(remote) > 1 else "?"
    ua = ws.request.headers.get("User-Agent", "Unknown") if ws.request else "Unknown"

    logger.info(f"[{conn_id}] Connected: {ip}:{port} ({ua})")

    try:
        while True:
            info = await system_info()
            payload = {"connection_id": conn_id, "client_info": {"ip": ip, "port": port, "user_agent": ua}, "content": info}
            await ws.send(safe_json(payload))
            await asyncio.sleep(5)

    except websockets.ConnectionClosed as e:
        logger.info(f"[{conn_id}] Disconnected (code={e.code}, reason={e.reason})")
    except Exception:
        logger.exception(f"[{conn_id}] Unexpected error in handler")
    finally:
        logger.info(f"[{conn_id}] Session closed.")

# --- Server-Start ---
async def main():
    async with websockets.serve(
            handler, HOST, PORT,
            ping_interval=20, ping_timeout=20):
        logger.info(f"WebSocket server listening on ws://{HOST}:{PORT}")
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped via CTRL+C")
    except Exception:
        logger.critical("Server crashed unexpectedly", exc_info=DEBUG)
        traceback.print_exc()
