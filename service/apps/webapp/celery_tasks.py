from service.celery import app
import time


@app.task
def test():
    print('>>>>>>>')
    time.sleep(2)
    print('end>>>>')
    return ''
