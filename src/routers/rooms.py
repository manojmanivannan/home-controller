from ..common.logger import log
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..opts.database import engine
from ..opts.schemas import RoomCreate, RoomRead
from ..opts.crud import create_room, get_all_rooms
from typing import List


router = APIRouter()

def get_session():
    with Session(engine) as session:
        yield session

@router.post("/", response_model=RoomRead)
def add_room(room: RoomCreate, session: Session = Depends(get_session)):
    log.info(f"Received request to add room: {room.name}")
    return create_room(session, room.name)

@router.get("/", response_model=List[RoomRead])
def list_rooms(session: Session = Depends(get_session), name=None):
    log.info("Received request to list all rooms.")
    return get_all_rooms(session)