from fastapi import FastAPI, Depends, Query
from datetime import datetime, timedelta
from celery import Celery
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from celery_worker import create_task
from models import SensorData
from schemas import Temperature
from database import SessionLocal,db_dependency
from dotenv import load_dotenv

load_dotenv()

app= FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/temperature")
def receive_temperature(data: Temperature):
    db = SessionLocal()
    db_temperature = SensorData(**data)
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    db.close()
    return {"message": "Temperature data received and stored."}

@app.get("/get_timeseries_data/{device_name}")
async def get_timeseries_data(db_sess: db_dependency,device_name:str):
    result =  db_sess.query(SensorData).filter(SensorData.device_name==device_name).all()
    return result


@app.get("/get_timeseries_data_all")
async def get_timeseries_data(db_sess: db_dependency,interval: int = Query(default=10, description="Resampling interval in minutes")):

    result =  db_sess.query(SensorData).all()  
    data = [obj.__dict__ for obj in result]
    df = pd.DataFrame(data)
    df = df.drop('_sa_instance_state', axis=1, errors='ignore')
    df = df.drop('id', axis=1, errors='ignore')
    df = df.drop('device_name', axis=1, errors='ignore')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')
    df_result = df.resample(f'{interval}T').mean().reset_index()
    average_temperatures_json=df_result.to_json(orient='records')
    return JSONResponse(content=average_temperatures_json)

