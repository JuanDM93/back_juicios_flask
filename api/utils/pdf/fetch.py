# public methods
from datetime import datetime
from .parse import fetch_pdf


def pdf_service(data):
    #now = datetime.now().date() - timedelta(days=5)
    now = datetime.now().date()- timedelta(days=6)
    fetch_pdf(now, data)
