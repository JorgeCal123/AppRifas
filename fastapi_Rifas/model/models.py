from sqlalchemy import Column, Integer, String, Boolean, DateTime
from config.Conexion import Base
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship
import uuid


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
    fecha_Juego = Column(DateTime)
    boletas = relationship("ModelBoleta", back_populates='talonario', cascade="all, delete-orphan")
    cantidad = Column(Integer)


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


class ModelNumeroBoleta(Base):
    __tablename__ = 'numero_boleta'
    id = Column(Integer, primary_key=True, autoincrement=True)
    numero = Column(Integer)
    id_boleta = Column(Integer, ForeignKey("Boleta.id", ondelete="CASCADE"))
    boleta = relationship("ModelBoleta", back_populates='numeros')
