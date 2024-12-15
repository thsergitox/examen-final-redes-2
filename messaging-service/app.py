from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests
import uuid

DATABASE_URL = "postgresql://user:password@db/register_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Message(Base):
    __tablename__ = "messages"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    usuario = Column(String, index=True)
    mensaje = Column(Text)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Servicio de Mensajería",
    description="Servicio para enviar y leer mensajes",
    version="1.0.0"
)

class MessageCreate(BaseModel):
    usuario: str
    mensaje: str

class User(BaseModel):
    usuario: str

def authenticate_user(usuario: str):
    response = requests.post("http://auth-service:8000/authenticate", json={"usuario": usuario})
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Usuario no Registrado")

@app.post("/write")
def write_message(message: MessageCreate):
    authenticate_user(message.usuario)
    db = SessionLocal()
    new_message = Message(id=str(uuid.uuid4()), usuario=message.usuario, mensaje=message.mensaje)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return {"message": "Mensaje guardado exitosamente"}

@app.post("/read")
def read_messages(user: User):
    authenticate_user(user.usuario)
    db = SessionLocal()
    messages = db.query(Message).filter(Message.usuario == user.usuario).all()
    return {"messages": messages}
