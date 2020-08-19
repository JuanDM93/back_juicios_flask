# SCHEDULER
from apscheduler.schedulers.background import BackgroundScheduler

def hello_job():
    app.logger.info('Hello Job! The time is: %s' % datetime.now())

scheduler = BackgroundScheduler()
scheduler.add_job(
    hello_job,
    trigger='interval', hours=24)
scheduler.start()