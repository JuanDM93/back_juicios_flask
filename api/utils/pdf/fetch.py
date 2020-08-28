# public methods
from datetime import datetime, timedelta
from .parse import (fetch_pdf, fetch_pdf_old)


def fetch_pdf_service(data=None):
    now = datetime.now().date()
    # init_date = now - timedelta(weeks=52)     # ONE year
    # init_date = date(2020, 8, 1)          # THIS year
    if data is None:
        fetch_pdf(now)
    init_date = now - timedelta(weeks=1)       # ONE week
    while now != init_date:
        fetch_pdf_old(now, data)
        # fetch_pdf(now, data)
        now = now - timedelta(days=1)           # ONE day
