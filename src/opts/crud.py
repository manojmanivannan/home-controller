import logging
from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from .models import Room, Device
import csv
from fastapi import HTTPException
from ..common.logger import log

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("crud")

def create_room(session: Session, name: str):
    log.debug(f"Creating room with name: {name}")
    room = Room(name=name)
    session.add(room)
    session.commit()
    session.refresh(room)
    log.info(f"Room created with ID: {room.id}")
    return room

def get_all_rooms(session: Session):
    log.debug("Fetching all rooms.")
    rooms = session.scalars(select(Room)).all()
    log.info(f"Fetched {len(rooms)} rooms.")
    return rooms

def create_device(session: Session, name: str, room_id: int):
    log.debug(f"Creating device with name: {name}, room_id: {room_id}")
    device = Device(name=name, room_id=room_id)
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
        select(Device).options(joinedload(Device.room)).order_by(Device.room_id, Device.name)
    ).all()

    # Adding room name to the device information
    devices_with_room_name = [
        {"id": device.id, "name": device.name, "room_id": device.room_id, "room_name": device.room.name, "state": device.state}
        for device in devices
    ]

    # Filter devices by room name if provided
    if room_name:
        devices_with_room_name = [
            device for device in devices_with_room_name if device["room_name"] == room_name
        ]

    log.info(f"Fetched {len(devices)} devices.")
    return devices_with_room_name

def toggle_device_state(session: Session, device_name: str, room_id: int, action: str):
    log.debug(f"{action.capitalize()} {device_name} in room ID {room_id}")

    # Fetch the device from the database
    device = session.scalars(
        select(Device).where(Device.name == device_name, Device.room_id == room_id)
    ).first()

    if not device:
        log.error(f"Device {device_name} not found in room ID {room_id}.")
        raise HTTPException(status_code=404, detail=f"Device {device_name} not found in room ID {room_id}.")

    room = session.scalars(
        select(Room).where(Room.id == room_id)
    ).first()
    
    # Determine the desired state based on action
    desired_state = action.lower() == "on"

    if device.state == desired_state:
        log.info(f"Device {device_name} is already {'on' if desired_state else 'off'} in {room.name} (room_id: {room_id}).")
        return device

    # Update the device's state
    device.state = desired_state
    session.add(device)
    session.commit()
    session.refresh(device)

    log.info(f"Device {device_name} turned {'on' if desired_state else 'off'} in {room.name} (room_id: {room_id}).")
    return device

def setup_database_from_csv(session: Session, csv_file_path: str):
    log.info(f"Setting up database from CSV file: {csv_file_path}")
    with open(csv_file_path, mode="r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            room_name = row["room_name"]
            device_name = row["device_name"]
            # status = row["status"].lower() == "on"

            # Check if room exists, create if not
            room = session.scalars(select(Room).where(Room.name == room_name)).first()
            if not room:
                log.debug(f"Room '{room_name}' not found. Creating new room.")
                room = create_room(session, room_name)

            # Create the device
            log.debug(f"Adding device '{device_name}' to room '{room_name}' with status 'off'.")
            create_device(session, name=device_name, room_id=room.id)

    log.info("Database setup from CSV file completed.")
