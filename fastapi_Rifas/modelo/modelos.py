from sqlalchemy import Column, Integer, String, Boolean, DateTime
from config.conexion import Base

from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship

def id_seis_digitos():
    db=next(get_db())
    while True:
        id_seis_digitos = random.randint(100000, 9999990)
        if not db.query(Boleta).filter_by(id=id_seis_digitos).first():
            return id_seis_digitos


class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200))
    apellido = Column(String(20))
    celular = Column(String(13))
    direccion = Column(String(50))
    notificacion = Column(Boolean)


class Talonario(Base):
    __tablename__ = 'talonarios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    valor_boleta = Column(Integer)
    celular = Column(String(10))
    cantidad = Column(Integer)
    boletas = relationship("Boleta", back_populates='talonario', cascade="all, delete-orphan")
    premios = relationship("Premio",
                           back_populates='talonario', cascade="all, delete-orphan")


class Boleta(Base):
    __tablename__ = 'boletas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    qr_code = Column(String(255))
    estado_venta = Column(Boolean, nullable=True)
    estado_pagado = Column(Boolean, nullable=True)
    fecha_venta = Column(DateTime, nullable=True)

    id_talonario = Column(Integer, ForeignKey("talonarios.id", ondelete="CASCADE"))
    talonario = relationship("Talonario", back_populates='boletas')

    numeros = relationship("NumeroBoleta", back_populates='boleta', cascade="all, delete-orphan")

    ganador = relationship("Ganador", back_populates="boleta", uselist=False)


class NumeroBoleta(Base):
    __tablename__ = 'Numero_boletas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    numero = Column(Integer)

    id_boleta = Column(Integer, ForeignKey("boletas.id", ondelete="CASCADE"))
    boleta = relationship("Boleta", back_populates='numeros')

class Premio(Base):
    __tablename__ = 'premios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    premio = Column(String(255))
    imagen = Column(String(255), nullable=True)
    fecha_Juego = Column(DateTime)

    id_talonario = Column(Integer, ForeignKey("talonarios.id", ondelete="CASCADE"))    
    talonario = relationship("Talonario", back_populates='premios')

    ganador = relationship("Ganador", back_populates='premio', uselist=False)

class Ganador(Base):
    ENTREGADO = "entregado"
    PENDIENTE = "pendiente"
    NO_VENDIDO = "No vendido"
    __tablename__ = "Ganador"
    id = Column(Integer, primary_key=True)
    numeroGanador = Column(Integer)
    estado = Column(String(50), default=PENDIENTE)


    id_boleta = Column(Integer, ForeignKey("boletas.id"))
    boleta = relationship("Boleta", back_populates="ganador", uselist=False)

    id_premio = Column(Integer, ForeignKey("premios.id"))
    premio = relationship("Premio", back_populates='ganador', uselist=False)
