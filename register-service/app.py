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

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Servicio de Registro de Usuarios",
    description="Servicio para registrar usuarios",
    version="1.0.0"
)

class UserCreate(BaseModel):
    usuario: str

@app.post("/register")
def register_user(user: UserCreate):
    db = SessionLocal()
    db_user = db.query(User).filter(User.usuario == user.usuario).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Usuario ya registrado")
    new_user = User(usuario=user.usuario)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Usuario registrado exitosamente"}
