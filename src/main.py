from .common.logger import log
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import rooms, devices, turn_on_off
from .opts.database import create_db_and_tables



app = FastAPI()

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