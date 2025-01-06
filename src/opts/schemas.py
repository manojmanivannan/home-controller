from pydantic import BaseModel, Field
from typing import List

class RoomCreate(BaseModel):
    name: str

class RoomRead(BaseModel):
    id: int
    name: str

class DeviceCreate(BaseModel):
    name: str
    room_id: int

class DeviceRead(BaseModel):
    id: int
    name: str
    state: bool
    room_id: int
    room_name: str = None

class RoomWithDevices(BaseModel):
    id: int
    name: str
    devices: List[DeviceRead]
    
# class TurnOnOff(BaseModel):
#     device_name: str = Field(
#         description="Name of the device"
#     )
#     room_id: int = Field(
#         description="room_id corresponding to the room"
#     )