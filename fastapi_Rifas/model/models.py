from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, CheckConstraint
from config.Conexion import Base
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship
from typing import Optional

import uuid

class EstadoEnum(Enum):
    ENTREGADO = "entregado"
    PENDIENTE = "pendiente"
    NO_VENDIDO = "No vendido"
    def __init__(self,length: Optional[int] = None):
        self.length = length


class User(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True, autoincrement=True)

    username = Column(String(20))
    nombre = Column(String(200))
    rol = Column(String(20))
    estado = Column(Integer)


class ModelTalonario(Base):
    __tablename__ = 'Talonario'
    id = Column(Integer, primary_key=True, autoincrement=True)
    valor_boleta = Column(Integer)
    celular = Column(String(10))
    cantidad = Column(Integer)

    boletas = relationship("ModelBoleta", back_populates='talonario', cascade="all, delete-orphan")
    premios = relationship("ModelPremio", back_populates='talonario', cascade="all, delete-orphan")


class ModelBoleta(Base):
    __tablename__ = 'Boleta'
    id = Column(Integer, primary_key=True, autoincrement=True)
    qr_code = Column(String(255))
    estado_venta = Column(Boolean, nullable=True)
    estado_pagado = Column(Boolean, nullable=True)
    fecha_venta = Column(DateTime, nullable=True)

    id_talonario = Column(Integer, ForeignKey("Talonario.id", ondelete="CASCADE"))  # <- Agregar "ondelete='CASCADE'"
    talonario = relationship("ModelTalonario", back_populates='boletas')

    numeros = relationship("ModelNumeroBoleta", back_populates='boleta', cascade="all, delete-orphan")

    ganador = relationship("ModelGanador", back_populates="boleta", uselist=False)


class ModelNumeroBoleta(Base):
    __tablename__ = 'Numero_boleta'
    id = Column(Integer, primary_key=True, autoincrement=True)
    numero = Column(Integer)

    id_boleta = Column(Integer, ForeignKey("Boleta.id", ondelete="CASCADE"))
    boleta = relationship("ModelBoleta", back_populates='numeros')

class ModelPremio(Base):
    __tablename__ = 'Premio'
    id = Column(Integer, primary_key=True, autoincrement=True)
    premio = Column(String(255))
    imagen = Column(String(255), nullable=True)
    fecha_Juego = Column(DateTime)

    id_talonario = Column(Integer, ForeignKey("Talonario.id", ondelete="CASCADE"))    
    talonario = relationship("ModelTalonario", back_populates='premios')

    ganador = relationship("ModelGanador", back_populates='premio', uselist=False)

class ModelGanador(Base):
    __tablename__ = "Ganador"
    id = Column(Integer, primary_key=True)
    numeroGanador = Column(Integer)
    estado = Column(String(50), default=EstadoEnum.PENDIENTE)


    id_boleta = Column(Integer, ForeignKey("Boleta.id"))
    boleta = relationship("ModelBoleta", back_populates="ganador", uselist=False)

    id_premio = Column(Integer, ForeignKey("Premio.id"))
    premio = relationship("ModelPremio", back_populates='ganador', uselist=False)



