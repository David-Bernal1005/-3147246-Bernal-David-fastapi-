from sqlalchemy import Column, String, Float, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Muestra(Base):
    __tablename__ = "muestras"
    id = Column(String, primary_key=True, index=True)
    tipo_de_muestra = Column(String, nullable=False)
    cantidad = Column(Float, nullable=False)
    tipo_de_sangre = Column(String, nullable=False)
    fecha_de_recoleccion = Column(Date, nullable=False)
