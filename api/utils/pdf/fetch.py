# public methods
from datetime import datetime
from .parse import fetch_pdf


def pdf_service(data):
    now = datetime.now().date()
    fetch_pdf(now, data)
