from ..common.logger import log
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..opts.database import engine
from ..opts.schemas import DeviceCreate, DeviceRead
from ..opts.crud import toggle_device_state


turn_on = APIRouter()
turn_off = APIRouter()

def get_session():
    with Session(engine) as session:
        yield session

@turn_on.post("/", response_model=DeviceRead)
def turn_on_device(device: DeviceCreate, session: Session = Depends(get_session)):
    log.info(f"Received request to turn ON device: {device.name} in room_id {device.room_id}")
    return toggle_device_state(session, device.name, device.room_id, "on")

@turn_off.post("/", response_model=DeviceRead)
def turn_off_device(device: DeviceCreate, session: Session = Depends(get_session)):
    log.info(f"Received request to turn OFF device: {device.name} in room_id {device.room_id}")
    return toggle_device_state(session, device.name, device.room_id, "off")
