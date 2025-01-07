import logging
from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from .models import Room, Device
import csv
from fastapi import HTTPException
from ..common.logger import log

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("crud")

def create_room(session: Session, name: str):
    log.debug(f"Creating room with name: {name}")
    room = Room(room_name=name)
    session.add(room)
    session.commit()
    session.refresh(room)
    log.info(f"Room created with ID: {room.id}")
    return room

def get_all_rooms(session: Session):
    log.debug("Fetching all rooms.")
    rooms = session.scalars(select(Room)).all()
    log.info(f"Fetched {len(rooms)} rooms.")
    rooms_list = [{'id':room.id,'name':room.room_name} for room in rooms]
    log.debug(f"Fetched rooms {rooms_list}")
    return rooms

def create_device(session: Session, device_name: str, room_id: str):
    log.debug(f"Creating device with name: {device_name}, room_id: {room_id}")
    device = Device(device_name=device_name, room_id=room_id)
    session.add(device)
    session.commit()
    session.refresh(device)
    log.info(f"Device created with ID: {device.id}")
    return device

# def get_all_devices(session: Session):
#     log.debug("Fetching all devices.")
#     devices = session.scalars(select(Device)).all()
#     log.info(f"Fetched {len(devices)} devices.")
#     return devices

def get_all_devices_room_names(room_name: str, session: Session):
    log.debug("Fetching all devices.")
    devices = session.scalars(
        select(Device).options(joinedload(Device.room)).order_by(Device.room_id, Device.device_name)
    ).all()

    # Adding room name to the device information
    devices_with_room_name = [
        {"id": device.id, "device_name": device.device_name, "room_id": device.room_id, "room_name": device.room.room_name, "state": device.state}
        for device in devices
    ]

    # Filter devices by room name if provided
    if room_name:
        log.debug(f"Filtering devices by room name: {room_name}")
        devices_with_room_name = [
            device for device in devices_with_room_name if device["room_name"].lower() == room_name.lower()
        ]

    log.info(f"Fetched {len(devices_with_room_name)} devices.")
    log.debug(f"Fetched devices {devices_with_room_name}")
    if not devices_with_room_name:
        log.error(f"No devices found in room '{room_name}'.")
        raise HTTPException(status_code=404, detail=f"No devices found in room '{room_name}'. Check if the room name is correct.")
    return devices_with_room_name

def toggle_device_state(session: Session, device_name: str, room_name: str, action: str):
    log.debug(f"Turning {action.capitalize()} {'all devices' if not device_name else device_name} in room '{room_name}'")

    # find if the room exists
    room = session.scalars(
        select(Room).where(func.lower(Room.room_name) == room_name.lower())
    ).first()

    if not room:
        log.error(f"Room {room_name} not found.")
        raise HTTPException(status_code=404, detail=f"Room {room_name} not found.")
    else:
        log.debug(f"Room {room_name} found with ID: {room.id}")
    # Fetch the device from the database

    if device_name=="":
        log.error(f"Device name cannot be empty.")
        raise HTTPException(status_code=404, detail=f"Device name cannot be empty.")
   
    devices = session.scalars(
        select(Device)
        .where(Device.room_id == room.id)
        .where(func.lower(Device.device_name) == device_name.lower() if device_name else True)
    ).all()

    if not devices:
        log.error(f"No devices {device_name if device_name else None} found in room '{room_name}'.")
        raise HTTPException(status_code=404, detail=f"No devices {device_name if device_name else None} found in room '{room_name}'.")

    desired_state = action.lower() == "on"
    for device in devices:
        if device.state != desired_state:
            device.state = desired_state
            session.add(device)
            session.commit()
            session.refresh(device)
            log.info(f"Device {device.device_name} turned {'on' if desired_state else 'off'} in room {room_name}.")
        else:
            log.info(f"Device {device.device_name} is already {'on' if desired_state else 'off'} in room {room_name}.")
    return devices

def setup_database_from_csv(session: Session, csv_file_path: str):
    log.info(f"Setting up database from CSV file: {csv_file_path}")
    with open(csv_file_path, mode="r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            room_name = row["room_name"]
            device_name = row["device_name"]
            # status = row["status"].lower() == "on"

            # Check if room exists, create if not
            room = session.scalars(select(Room).where(Room.room_name == room_name)).first()
            if not room:
                log.debug(f"Room '{room_name}' not found. Creating new room.")
                room = create_room(session, room_name)

            # Create the device
            log.debug(f"Adding device '{device_name}' to room '{room_name}' with status 'off'.")
            create_device(session, device_name=device_name, room_id=room.id)

    log.info("Database setup from CSV file completed.")
