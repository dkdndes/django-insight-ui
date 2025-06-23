import asyncio
import websockets
import json
import datetime
import psutil
import shutil
import logging

logging.basicConfig(level=logging.INFO)

HOST = 'localhost'
PORT = 8765

async def system_info():
    now = datetime.datetime.now().isoformat()
    disk = shutil.disk_usage("/")
    memory = psutil.virtual_memory()

    return {
        "timestamp": now,
        "disk": {
            "total_gb": round(disk.total / (1024 ** 3), 2),
            "used_gb": round(disk.used / (1024 ** 3), 2),
            "free_gb": round(disk.free / (1024 ** 3), 2),
        },
        "memory": {
            "total_gb": round(memory.total / (1024 ** 3), 2),
            "available_gb": round(memory.available / (1024 ** 3), 2),
            "percent_used": memory.percent
        }
    }

async def handler(websocket):  # Only one parameter now
    logging.info("Client connected.")
    try:
        while True:
            data = await system_info()
            await websocket.send(json.dumps(data))
            await asyncio.sleep(5)
    except websockets.exceptions.ConnectionClosed:
        logging.info("Client disconnected.")

async def main():
    async with websockets.serve(handler, HOST, PORT):
        logging.info(f"Server running on ws://{HOST}:{PORT}")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Server stopped manually.")
