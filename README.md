# Back-Juicios

Python-based Flask system

## Run options

### Dockerized compose

Once cloned, just [compose](https://docs.docker.com/compose/)

```bash
docker-compose up
```

### Container build and run

Once cloned, build [container](https://www.docker.com/resources/what-container)

```bash
docker build -t <CONTAINER_NAME> .
```

Run it

```bash
docker run -p <PORT>:5000 <CONTAINER_NAME>
```

### Local python env install

Once cloned, create new [python environment](https://docs.python.org/3/tutorial/venv.html) 'env', then activate it

```bash
python -m venv env
source env/bin/activate
```

Windows

```bash
py -3 -m venv env
env\Scripts\activate
```

and install reqs

```bash
python -m pip install --upgrade pip
pip install --upgrade setuptools wheel
pip install -r requirements.txt
```

Set ENV_VARS

```bash
export FLASK_APP=api
export FLASK_ENV=development
```

Windows

```bash
set FLASK_APP=api
set FLASK_ENV=development
```

Run service

```bash
flask run
```

## APIs endpoints
baseURL = http://localhost:5000

```bash
flask routes
```

CRUD (baseURL/admin)

```bash
../register
../desapachos

../listausuarios
../actualizarUsuario

../logotipo

../tipousuario
../eliminarUsuario
../informacionperfil

../despachos
../altaDespacho
../eliminarDespacho
../actualizarDespacho
```

Users (baseURL/users)

```bash
../login
```

Locales (baseURL/locales)

```bash
../juzgados

../juicios
../detalle_expediente

../alta_juicio
../eliminar_juicio
../actualizar_juicio

../juicios_asignados
../filtro_juicios
```

Federal (baseURL/federales)

```bash
../circuitos_federales
../juzgados_federales
../tipo_de_juicios_federales

../acuerdos_federales
../juicios_federales

../alta_juicios_federales
```

## Contributing

For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)