# public methods
from datetime import datetime   # , timedelta
from .parse import fetch_pdf


def pdf_service(data):
    # now = datetime.now().date() - timedelta(days=6)
    now = datetime.now().date()
    fetch_pdf(now, data)


def get_response(session, url, flag=5):
    from time import sleep
    response = session.get(url)
    if response.status_code == 200:
        return response.content
    if flag > 0:
        sleep(flag)
        flag -= 1
        return get_response(session, url, flag)
    return None
