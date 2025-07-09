import asyncio
import websockets
import json
import signal
import logging

URL = "ws://localhost:8765"
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s')

is_running = True

def shutdown_handler(signum, frame):
    global is_running
    is_running = False
    logging.info("Client wird beendet (Signal empfangen)")

signal.signal(signal.SIGINT, shutdown_handler)   # CTRL+C
signal.signal(signal.SIGTERM, shutdown_handler)  # kill

async def main():
    global is_running
    try:
        async with websockets.connect(URL) as websocket:
            logging.info(f"Verbunden mit {URL}")
            while is_running:
                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=10)
                    try:
                        data = json.loads(message)
                        logging.info(f"[{data.get('connection_id')}] Daten empfangen:\n{json.dumps(data['content'], indent=2)}")
                    except json.JSONDecodeError:
                        logging.warning(f"Ungültige Nachricht:\n{message}")
                except asyncio.TimeoutError:
                    logging.debug("Timeout – keine Nachricht empfangen")
    except Exception as e:
        logging.error(f"Verbindungsfehler: {e}")

if __name__ == "__main__":
    asyncio.run(main())
