from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

class Room(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    devices: List["Device"] = Relationship(back_populates="room")

class Device(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    state: bool = Field(default=False)  # False: Off, True: On
    room_id: int = Field(foreign_key="room.id")
    room: Optional[Room] = Relationship(back_populates="devices")