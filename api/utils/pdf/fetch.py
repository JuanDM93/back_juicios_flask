# public methods
from datetime import datetime, timedelta
from .parse import fetch_pdf


def pdf_service(data, daily=False):
    now = datetime.now().date()

    if daily:
        limit_date = now - timedelta(days=1)           # ONE day
    else:
        # limit_date = now - timedelta(weeks=52)    # ONE year
        # limit_date = date(2020, 1, 1)             # THIS year
        limit_date = now - timedelta(weeks=1)       # ONE week

    while now != limit_date:
        fetch_pdf(now, data)
        now = now - timedelta(days=1)           # ONE day
