from sqlalchemy import Column, Integer, String, Boolean, DateTime, Sequence, BigInteger, func
from config.conexion import Base, get_db

from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship

import random


def id_seis_digitos():
    db=next(get_db())
    while True:
        id_seis_digitos = random.randint(100000, 9999990)
        if not db.query(Boleta).filter_by(id=id_seis_digitos).first():
            return id_seis_digitos

def obtener_siguiente_valor():
    db=next(get_db())

    consulta = db.execute("SELECT MAX(numero_increment) FROM boletas;")
    max_valor = consulta.scalar()
    if max_valor is None:
        return 1
    return max_valor + 1



"""
Modelo cliente que es la persona que compra las boletas
    id: clave primaria del cliente que se genera automaticamente
    nombre: nombre del cliente
    apellido: apellido del cliente
    celular: numero del cliente
    direccion: la direccion puede ser opcional si el cliente quiere poner
    notificacion: opcion que decide el cliente si quiere que le llegue una notificacion de la boleta ganadora

    boletas: son las boletas que se registran a su nombre si las compra
    ganador: Son los cliente que ganan la rifa
"""
class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=True, default=None)
    apellido = Column(String(20), nullable=True, default=None)
    celular = Column(String(13), unique=True, nullable=False)
    direccion = Column(String(50), nullable=True, default=None)
    notificacion = Column(Boolean, default=False)
    
    boletas = relationship("Boleta", back_populates='cliente', cascade="all, delete-orphan")
    
    ganador =  relationship("Ganador", back_populates='cliente', cascade="all, delete-orphan")
    
"""
Modelo talonario: es el paquete de boletas que el administrador crea para la venta de boletas
    id: clave primaria del talonario que se genera automaticamente
    valor_boleta: Es el precio que van a tener todas las boletas
    celular: Es el numero de la central o responsable que pueden llamar los clientes 
    cantidad: es la cantidad total de boletas que tiene el talonario
    boletas: son las boletas que contiene el talonario
    premios: Son los premios que se van a rifar 
"""

class Talonario(Base):
    __tablename__ = 'talonarios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    valor_boleta = Column(Integer)
    celular = Column(String(10))
    cantidad = Column(Integer)
    boletas = relationship("Boleta", back_populates='talonario', cascade="all, delete-orphan")
    premios = relationship("Premio",
                           back_populates='talonario', cascade="all, delete-orphan")
    
    remuneraciones = relationship("RemuneracionVendedor", back_populates='talonario', cascade="all, delete-orphan")


"""
Modelo Boleta: es la informacion de cada boleta
    id: clave primaria de la boleta que se genera automaticamente
    consecutiveid: Es el numero en orden ascendente dependiendo de la creacion
    qr_code: Es el codigo qr que contiene toda la informacion para registrar rapidamente la venta de la boleta
    estado_venta: Sirve para saber si la boleta ya fue vendida o no
    estado_pagado: Sirve para saber si la boleta fue pagada o no
    fecha_venta: Es la fecha en la que se vendio la boleta
    idTalonario: Es el id del talonario al que pertenece la boleta
    Talonario: Es el talonario al que pertenece
    numeros: Son los numeros con los que se juegan para decidir el ganador de la rifa. Los numeros deben de ser de 4 digitos y solo se puede crear (cantidad) 2, 3, 8 o 10 numeros
    ganador: Se registra la boleta ganadora

    id_cliente: Es el cliente que compro la boleta
    cliente: Es el cliente que compro la boleta

    id_vendedor: Es el id vendedor al que se le asigno la boleta para que la venda a un cliente
    vendedot: Es el vendedor que vende la boleta
    """
class Boleta(Base):
    __tablename__ = 'boletas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    consecutiva_id = Column(Integer)
    qr_code = Column(String(255))
    estado_venta = Column(Boolean, nullable=True, default=False)
    estado_pagado = Column(Boolean, nullable=True, default=False)
    fecha_venta = Column(DateTime, nullable=True)

    id_talonario = Column(Integer, ForeignKey("talonarios.id", ondelete="CASCADE"))
    talonario = relationship("Talonario", back_populates='boletas')

    numeros = relationship("NumeroBoleta", back_populates='boleta', cascade="all, delete-orphan")

    ganador = relationship("Ganador", back_populates="boleta", uselist=False)
    
    id_cliente = Column(Integer, ForeignKey("clientes.id", ondelete="CASCADE"))
    cliente = relationship("Cliente", back_populates='boletas')

    id_vendedor = Column(String(20), ForeignKey("vendedores.cedula", ondelete="CASCADE"))
    vendedor = relationship("Vendedor", back_populates='boletas')

"""
Modelo Numero Boleta
    id: clave primaria del numero de la boleta que se genera automaticamente
    numero: Es el numero con el que se juega en la rifa. El numero debe de ser de 4 digitos
    id_boleta: Es el id de la boleta al que pertenece este numero
    boleta: Es el numero al que pertenece la boleta

"""

class NumeroBoleta(Base):
    __tablename__ = 'Numero_boletas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    numero = Column(String(4))

    id_boleta = Column(Integer, ForeignKey("boletas.id", ondelete="CASCADE"))
    boleta = relationship("Boleta", back_populates='numeros')

"""
Modelo Premio
    id: clave primaria del premio que se genera automaticamente
    premio: Es el nombre del premio que se va a rifar
    imagen: Es la url de la imagen del premio
    fecha juego: es la fecha en la que se va a rifar el premio
    id_talonario: Es el id del talonario al que pertenece los premio
    talonario: es el talonario que pertenece el premio

    ganador: es a quien se le va a asignar el premio

"""

class Premio(Base):
    __tablename__ = 'premios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    premio = Column(String(255))
    imagen = Column(String(255), nullable=True)
    fecha_juego = Column(DateTime)

    id_talonario = Column(Integer, ForeignKey("talonarios.id", ondelete="CASCADE"))    
    talonario = relationship("Talonario", back_populates='premios')

    ganador = relationship("Ganador", back_populates='premio', uselist=False)



"""
Modelo Ganador
    id: clave primaria del ganador que se genera automaticamente
    numero_ganador: Es el numero ganador que gano la rifa
    estado: es el estado de la entrega del premio puede ser ENTREGADO, PENDIENTE, NO VENDIDO

    id_boleta: Es el id de la boleta ganadora
    boleta: Es la boleta ganadora

    id_premio: Es el id del premio que gano
    boleta: Es el premio que gano

    id_cliente: Es el id del cliente que gano la rifa
    boleta: Es el cliente que gano la rifa
"""
class Ganador(Base):
    ENTREGADO = "Entregado"
    PENDIENTE = "Pendiente"
    NO_VENDIDO = "No vendido"
    __tablename__ = "Ganador"
    id = Column(Integer, primary_key=True, autoincrement=True)
    numero_ganador = Column(Integer)
    estado = Column(String(50), default=PENDIENTE)


    id_boleta = Column(Integer, ForeignKey("boletas.id"))
    boleta = relationship("Boleta", back_populates="ganador", uselist=False)

    id_premio = Column(Integer, ForeignKey("premios.id"))
    premio = relationship("Premio", back_populates='ganador', uselist=False)
    
    id_cliente = Column(Integer, ForeignKey("clientes.id"))
    cliente = relationship("Cliente", back_populates='ganador', uselist=False)
    
"""
Modelo vendedor: Es la persona encargada de vender las boletas
    cedula: La clave primara es la cedula
    nombre: Es el nombre del vendedor
    apellido: Es el apellido a vendedor
    celular: Es el celular del vendedor
    correo: Es el correo del vendedor
    contraseña: ES la contraseña que el vendedor debe de registrar
    boletas: Son las boletas que el administrador le asigna al vendedor para que lo venda

"""
    
class Vendedor(Base):
    __tablename__ = 'vendedores'
    cedula = Column(String(20), primary_key=True)
    nombre = Column(String(200))
    apellido = Column(String(20))
    celular = Column(String(13))
    correo = Column(String(100))
    contraseña = Column(String(20))
    
    boletas = relationship("Boleta", back_populates='vendedor', cascade="all, delete-orphan")

"""
Modelo Remuneracion Vendedor: Es donde se registra el porcentaje que se le va a pagar a un vendedor dependiendo del talonario por lo general se les paga el 20% de la cantidad de boletas vendidas
porcentaje: Es el porcentaje que se le va a pagar al vendedor
talonario: Es el talonario que se le paga al vendedor
"""
class RemuneracionVendedor(Base):
    __tablename__ = 'remuneracion_vendedores'
    id = Column(Integer, primary_key=True, autoincrement=True)
    porcentaje = Column(Integer, default=20)

    # ForeignKey hacia Talonario
    id_talonario = Column(Integer, ForeignKey("talonarios.id", ondelete="CASCADE"))
    # Relación con Talonario
    talonario = relationship("Talonario", back_populates='remuneraciones')