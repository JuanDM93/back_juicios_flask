from datetime import datetime, timedelta

from .parse import fetch_pdf

# public methods
# --------------
def fetch_day(fecha, data):
    fetch_pdf(fecha, data)


def fetch_history(data):
    #init_date = date(2020, 8, 1)               # THIS year
    now = datetime.now().date()
    #init_date = now - timedelta(weeks=52)      # ONE year
    init_date = now - timedelta(weeks=1)       # 1 year
    while now != init_date:
        fetch_day(now, data)
        now = now - timedelta(days=1)           # 1 day