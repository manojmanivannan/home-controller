from ..common.logger import log
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..opts.database import engine
from ..opts.schemas import DeviceCreate, DeviceRead, RoomRead
from ..opts.crud import toggle_device_state
from typing import List


turn_on = APIRouter()
turn_off = APIRouter()

def get_session():
    with Session(engine) as session:
        yield session

@turn_on.post("/", response_model=List[DeviceRead])
def turn_on_device(device: DeviceCreate, session: Session = Depends(get_session)):
    log.info(f"Received request to turn ON device: {device.name} in room '{device.room_name}'")
    return toggle_device_state(session, device.name, device.room_name, "on")

@turn_on.post("/all", response_model=List[DeviceRead])
def turn_on_all_devices(room: RoomRead, session: Session = Depends(get_session)):
    log.info(f"Received request to turn ON all devices in room '{room.room_name}'")
    return toggle_device_state(session, None, room.room_name, "on")

@turn_off.post("/", response_model=List[DeviceRead])
def turn_off_device(device: DeviceCreate, session: Session = Depends(get_session)):
    log.info(f"Received request to turn OFF device: {device.name} in room '{device.room_name}'")
    return toggle_device_state(session, device.name, device.room_name, "off")

@turn_off.post("/all", response_model=List[DeviceRead])
def turn_off_all_devices(room: RoomRead, session: Session = Depends(get_session)):
    log.info(f"Received request to turn OFF all devices in room '{room.room_name}'")
    return toggle_device_state(session, None, room.room_name, "off")
