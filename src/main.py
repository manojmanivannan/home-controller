from .common.logger import log
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import rooms, devices, turn_on_off
from .opts.database import create_db_and_tables

description = """
This is a Home Automation Server API built with FastAPI. 
It allows users to manage rooms and devices in a home automation system. 
The API supports operations to turn devices on and off. 
The database and tables are created on application startup.
"""

app = FastAPI(
    title="Home Automation Server",
    docs_url="/swagger", 
    description=description,
    openapi_url="/api/v1/openapi.json",
    defaultModelRendering=["example*", "model"],  # ["example", "model"]"example", "model"],
    defaultModelExpandDepth=5,

    )

# Allow all origins (you can restrict this to specific origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.on_event("startup")
def on_startup():
    log.info("Application startup: Creating database and tables.")
    create_db_and_tables()

app.include_router(rooms.router, prefix="/rooms", tags=["Rooms"])
app.include_router(devices.router, prefix="/devices", tags=["Devices"])
app.include_router(turn_on_off.turn_on,prefix="/turnon", tags=["Toggle Device"])
app.include_router(turn_on_off.turn_off,prefix="/turnoff", tags=["Toggle Device"])