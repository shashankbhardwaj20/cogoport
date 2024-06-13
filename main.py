from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/create_configuration", response_model=schemas.Configuration)
def create_configuration(config: schemas.ConfigurationCreate, db: Session = Depends(get_db)):
    db_config = crud.get_configuration(db, config.country_code)
    if db_config:
        raise HTTPException(status_code=400, detail="Configuration already exists")
    return crud.create_configuration(db, config)

@app.get("/get_configuration/{country_code}", response_model=schemas.Configuration)
def get_configuration(country_code: str, db: Session = Depends(get_db)):
    db_config = crud.get_configuration(db, country_code)
    if db_config is None:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return db_config

@app.post("/update_configuration", response_model=schemas.Configuration)
def update_configuration(config: schemas.ConfigurationUpdate, db: Session = Depends(get_db)):
    db_config = crud.update_configuration(db, config)
    if db_config is None:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return db_config

@app.delete("/delete_configuration/{country_code}")
def delete_configuration(country_code: str, db: Session = Depends(get_db)):
    success = crud.delete_configuration(db, country_code)
    if not success:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return {"detail": "Configuration deleted"}
