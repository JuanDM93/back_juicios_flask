# public methods
from datetime import datetime, timedelta

from parse import fetch_pdf


def fetch_history(data):
    # init_date = date(2020, 8, 1)          # THIS year
    now = datetime.now().date()
    # init_date = now - timedelta(weeks=52)     # ONE year
    init_date = now - timedelta(weeks=1)       # ONE week
    while now != init_date:
        fetch_pdf(now, data)
        now = now - timedelta(days=1)           # ONE day


def fetch_day(fecha, data):
    # TODO
    # 1 - traer el pdf del dia
    # 2 - extraer acuerdos (TODOS)
    # 3 - SQL (TODOS)
    fetch_pdf(fecha, data)
