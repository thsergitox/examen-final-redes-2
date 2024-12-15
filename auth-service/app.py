from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user:password@db/register_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    usuario = Column(String, primary_key=True, index=True)

app = FastAPI(
    title="Servicio de Autenticación",
    description="Servicio para autenticar usuarios",
    version="1.0.0"
)

class UserAuthenticate(BaseModel):
    usuario: str

@app.post("/authenticate")
def authenticate_user(user: UserAuthenticate):
    db = SessionLocal()
    db_user = db.query(User).filter(User.usuario == user.usuario).first()
    if db_user:
        return {"message": "Ok"}
    else:
        raise HTTPException(status_code=404, detail="Usuario no Registrado")
