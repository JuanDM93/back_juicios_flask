from flask_apscheduler import APScheduler
from flask import current_app


# SCHEDULER
scheduler = APScheduler()

def start_jobs():
    scheduler.init_app(current_app)
    scheduler.start()

# test job
@scheduler.task(
    'interval', id='hello_job',
    seconds=30, misfire_grace_time=900)
from datetime import datetime
def hello_job():
    with current_app.app_context():
        current_app.logger.warn(
            'Hello Job! The time is: %s' % datetime.now())

# interval examples
@scheduler.task(
    'interval', id='do_job_1',
    seconds=30, misfire_grace_time=900)
def job1():
    print('Job 1 executed')


# cron examples
@scheduler.task(
    'cron', id='do_job_2',
    minute='*')
def job2():
    print('Job 2 executed')


@scheduler.task(
    'cron', id='do_job_3',
    week='*', day_of_week='thu')
def job3():
    print('Job 3 executed')
