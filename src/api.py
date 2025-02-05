from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime
import asyncio
import uvicorn
from threading import Thread


class DataUpdate(BaseModel):
    data: Dict[str, float]


class ApiServer:
    def __init__(self, host: str = "0.0.0.0", port: int = 8000):
        self.app = FastAPI()
        self.host = host
        self.port = port
        self.rect_objects: List[Dict[str, float]] = []
        self.on_update_callback = None

        # Registrace endpointů
        self.setup_routes()

    def setup_routes(self):
        @self.app.post("/data")
        async def add_data(data_update: DataUpdate):
            """Přidá nový objekt do rect_objects"""
            try:
                self.rect_objects.append(data_update.data)
                if self.on_update_callback:
                    # Spustíme callback pro aktualizaci vizualizace
                    self.on_update_callback(self.rect_objects)
                return {"status": "success", "message": "Data byla úspěšně přidána"}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/data")
        async def get_data():
            """Vrátí všechna aktuální data"""
            return self.rect_objects

        @self.app.delete("/data")
        async def clear_data():
            """Vymaže všechna data"""
            self.rect_objects.clear()
            if self.on_update_callback:
                self.on_update_callback(self.rect_objects)
            return {"status": "success", "message": "Data byla vymazána"}

    def set_initial_data(self, initial_data: List[Dict[str, float]]):
        """Nastaví počáteční data"""
        self.rect_objects = initial_data.copy()

    def set_update_callback(self, callback):
        """Nastaví callback funkci, která se zavolá při aktualizaci dat"""
        self.on_update_callback = callback

    def run_server(self):
        """Spustí server v samostatném vlákně"""

        def run():
            uvicorn.run(self.app, host=self.host, port=self.port)

        self.server_thread = Thread(target=run, daemon=True)
        self.server_thread.start()
