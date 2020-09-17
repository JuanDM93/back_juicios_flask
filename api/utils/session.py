from time import sleep


def get_response(session, url, flag=10):
    response = session.get(url)
    if response.status_code == 200:
        return response.content
    if flag > 0:
        sleep(flag)
        flag -= 1
        return get_response(session, url, flag)
    return None
