import asyncio
import json
import logging
import signal

import websockets

URL = "ws://localhost:8765"
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s - %(message)s")

is_running = True


def shutdown_handler(signum, frame) -> None:  # noqa: ANN001
    global is_running
    is_running = False
    logging.info("Client wird beendet (Signal empfangen)")


signal.signal(signal.SIGINT, shutdown_handler)  # CTRL+C
signal.signal(signal.SIGTERM, shutdown_handler)  # kill


async def main() -> None:
    global is_running
    try:
        async with websockets.connect(URL) as websocket:
            logging.info("Verbunden mit %s", URL)
            while is_running:
                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=10)
                    try:
                        data = json.loads(message)
                        logging.info(
                            "[%s] Daten empfangen:\n%s",
                            data.get("connection_id"),
                            json.dumps(data["content"], indent=2),
                        )
                    except json.JSONDecodeError:
                        logging.warning("Ungültige Nachricht:\n%s", message)
                except TimeoutError:
                    logging.debug("Timeout – keine Nachricht empfangen")
    except Exception as e:
        logging.exception("Verbindungsfehler: %s", e)


if __name__ == "__main__":
    asyncio.run(main())
