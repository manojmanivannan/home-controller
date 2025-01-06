from ..common.logger import log
from sqlmodel import SQLModel, create_engine, Session, select
from .crud import setup_database_from_csv
from fastapi import HTTPException
import os

engine = create_engine(
    os.getenv("DATABASE_URL")
)

def create_db_and_tables():
    log.info(f"Creating database tables using connection")
    try:
        SQLModel.metadata.create_all(engine)
    except Exception as e:
        log.error(f"Error setting up engine: {e}")

    
    # Load initial data from CSV
    csv_file_path = "/app/src/etc/home_devices.csv"
    with Session(engine) as session:
        try:
            setup_database_from_csv(session, csv_file_path)
        except Exception as e:
            log.error(f"Error setting up database from CSV: {e}")
            raise HTTPException(status_code=500, detail="Error setting up database from CSV.")
