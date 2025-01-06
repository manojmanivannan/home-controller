from ..common.logger import log
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..opts.database import engine
from ..opts.schemas import DeviceCreate, DeviceRead
from ..opts.crud import create_device, get_all_devices_room_names #get_all_devices
from typing import List


router = APIRouter()

def get_session():
    with Session(engine) as session:
        yield session

@router.post("/", response_model=DeviceRead)
def add_device(device: DeviceCreate, session: Session = Depends(get_session)):
    log.info(f"Received request to add device: {device.name}")
    try:
        return create_device(session, device.name, device.room_id)
    except Exception as e:
        log.error(f"Error adding device: {e}")
        raise HTTPException(status_code=500, detail="Error adding device.")

@router.get("/", response_model=List[DeviceRead])
def list_devices(room_name: str = "", session: Session = Depends(get_session)):
    log.info("Received request to list all devices.")
    try:
        return get_all_devices_room_names(room_name, session)
    except Exception as e:
        log.error(f"Error listing devices: {e}")
        raise HTTPException(status_code=500, detail="Error listing devices.")