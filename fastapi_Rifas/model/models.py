from sqlalchemy import Column, Integer, String, Boolean, DateTime
from config.conexion import Base
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'usuario'
    id = Column(Integer,primary_key=True, autoincrement=True)
    username = Column(String(20))
    nombre = Column(String(200))
    rol = Column(String(20))
    estado = Column(Integer)


class ModelTalonario(Base):
    __tablename__ = 'Talonario'
    id = Column(Integer,primary_key=True, autoincrement=True)
    valor_boleta = Column(Integer)
    celular = Column(String(10))
    fecha_Juego = Column(DateTime)
    boletas = relationship("ModelBoleta", back_populates='talonario')
    cantidad = Column(Integer)


class ModelBoleta(Base):
    __tablename__ = 'Boleta'
    id = Column(Integer,primary_key=True, autoincrement=True)
    id_cliente = Column(Integer)
    id_vendedor = Column(Integer)
    qr_code = Column(String(255))
    detalle = Column(String(255))
    pagado = Column(Boolean)
    fecha_venta = Column(DateTime)
    id_talonario = Column(Integer, ForeignKey("Talonario.id"))
    talonario = relationship("ModelTalonario", back_populates='boletas')
