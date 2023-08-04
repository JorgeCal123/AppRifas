# CRUD CON FASTAPI, SQLALCHEMY Y MYSQL



## PASOS PARA INSTALAR
1. Crear un ambiente virtual con Python3
```
virtualenv env -p python3

```
2. Activar el ambiente virtual
```
source env/bin/activate

```
3. Instalar las librerías necesarias que se encuentran en el archivo requirements.txt
```
pip install -r requiritements.txt

```
4. forma 2 para instalar
pip install mysql-connector-python
pip install mysqlclient
pip install sqlalchemy
pip install fastapi uvicorn
## virtualEnv desde python (forma 2 usar virtualenv)
1. crear el ambiente virtual
python -m venv envfastapi
2. ejecutar ambiente arvitual
.\envfastapi\Scripts\activate

## DESPLEGANDO EL AMBIENTE
```
uvicorn main:app --reload

```
* main es el nombre del archivo main.py
* app es el nombre de la variable de FASTAPI inicializada en el archivo main


Para encontrar una explicación detallada, puedes acceder al video en YouTube

[![](http://img.youtube.com/vi/2ZXiW1ZQqqU/0.jpg)](https://www.youtube.com/watch?v=2ZXiW1ZQqqU "")

