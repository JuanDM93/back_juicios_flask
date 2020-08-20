# Back-Juicios

Python-based Flask system

## Installation

Once cloned, create new [python environment](https://docs.python.org/3/tutorial/venv.html) 'env', activate it

```bash
python -m venv env
source env/bin/activate
```

Windows

```bash
py -3 -m venv venv
env\Scripts\activate
```

and install reqs

```bash
pip install --upgrade pip setuptools
pip install -r requirements.txt
```

## Usage

Run service

```bash
export FLASK_APP=api
export FLASK_ENV=development
```

Windows

```bash
set FLASK_APP=api
set FLASK_ENV=development
```

```bash
flask run
```

## APIs
baseURL = http://127.0.0.1:5000

```bash
flask routes
```

Users (baseURL/users)

```bash
../login
../register
```

Locales (baseURL/locales)

```bash
../juzgados

../juicios

../alta_juicio
../eliminar_juicio
../actualizar_juicio

../juicios_asignados
../filtro_juicios
```

Federal (baseURL/federales)

```bash
../
```

## Contributing

For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)