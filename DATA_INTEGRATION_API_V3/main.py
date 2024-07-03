from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import re

from database import SessionLocal, engine, Base
from models import DataReading

app = FastAPI()

Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/data")
async def add_data(data: str, db: Session = Depends(get_db)):
    readings = data.strip().split('\n')
    pattern = re.compile(r'^\d+ \w+ \d+(\.\d+)?$')
    
    readings_to_store = []

    for reading in readings:
        if not pattern.match(reading):
            raise HTTPException(status_code=400, detail="Malformed data")
        
        timestamp, metric_name, metric_value = reading.split()
        readings_to_store.append(DataReading(
            timestamp=int(timestamp),
            metric_name=metric_name,
            metric_value=float(metric_value)
        ))

    for reading in readings_to_store:
        db.add(reading)
    db.commit()
    
    return {"success": True}

@app.get("/data")
async def get_data(from_date: str, to_date: str, db: Session = Depends(get_db)):
    try:
        from_date_dt = datetime.strptime(from_date, "%Y-%m-%d")
        to_date_dt = datetime.strptime(to_date, "%Y-%m-%d") + timedelta(days=1)  # Include the end day
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")
    
    readings = db.query(DataReading).filter(
        DataReading.timestamp >= int(from_date_dt.timestamp()),
        DataReading.timestamp < int(to_date_dt.timestamp())
    ).all()
    
    result = []
    voltage_sum = current_sum = voltage_count = current_count = 0

    for reading in readings:
        result.append({
            "time": datetime.utcfromtimestamp(reading.timestamp).isoformat() + "Z",
            "name": reading.metric_name,
            "value": reading.metric_value
        })
        if reading.metric_name == 'Voltage':
            voltage_sum += reading.metric_value
            voltage_count += 1
        elif reading.metric_name == 'Current':
            current_sum += reading.metric_value
            current_count += 1
    
    average_power = None
    if voltage_count > 0 and current_count > 0:
        average_power = (voltage_sum / voltage_count) * (current_sum / current_count)
        result.append({
            "time": from_date_dt.isoformat() + "Z",
            "name": "Power",
            "value": average_power
        })
    
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
