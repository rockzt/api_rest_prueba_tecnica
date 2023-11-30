# Proyecto

Prueba Técnica liverpool

## Instrucciones para levantar el proyecto

### Prerequisitos

- Python version superior a 3.0
- Sistema Operativo: macOS

### Installación

1. Clona el repositorio:
   ```bash
   git clone git@github.com:rockzt/api_rest_prueba_tecnica.git

2. Posterios a esto es necesario que crees un ambiente virtual y lo actives:
   ```bash
   virtualenv venv --python=$(which python3)
   source venv/bin/activate
   
3. Posterior a esto corremos un script el cual instalara por nosotros postgres asi como la creación de la DB
   ```bash
   ./setup_postgres.sh
 
4. Procedemos a instalar los paquetes necesarios con el siguiente comando
   ```bash
   pip install requirements.txt
   
5. Por último, levantamos la aplicación corriendo el siguiente comando
   ```bash
   flask --app api/__init__.py  run --debug

6. Para correr las migraciones necesarias y crear las tablas, es necesario realizar un GET request a:
    ```bash
   http://127.0.0.1:5000/bd/create

7. Sin necesitas hacer un drop a la DB, simplemente has un GET request a:
   ```bash
   http://127.0.0.1:5000/bd/drop


### Correr Tests

1. Para correr los test simplemente debes correr los siguientes comandos para probar cada endpoint
   ```bash
   pytest -rP  tests/test_orders_cancel.py
   pytest -rP  tests/test_orders_create.py
   pytest -rP  tests/test_orders_get_all.py
   pytest -rP  tests/test_orders_get_single.py
   
2. Cuando termines de correr las pruebas es necesario que hagas drop en la DB y la vuelvas a levantar
para esto es necesario que hagas un get a los siguientes endpoints en el orden mostrado.
De esta manera podrás usar los endpoints sin ningun problema
   ```bash
   http://127.0.0.1:5000/bd/drop
   http://127.0.0.1:5000/bd/create

### API Información
- [Aqui](https://docs.google.com/document/d/15Rl9UKw1Nc8J62t0o9GfaOX1sT325Y5KoGfJCY6eSmg/edit#heading=h.2et92p0) encontraras toda la información acerca de los endpoints


### POSTMAN Collection
- En este [enlace](postman_collection/liv_test.postman_collection.json) encontrarás el archivo json de la colección de los endpoints disponibles 