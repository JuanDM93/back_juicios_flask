from flask_apscheduler import APScheduler
from flask import current_app

##
# test job
##
from datetime import datetime
def hello_job():
    with current_app.app_context():
        current_app.logger.info(
            'Hello Job! The time is: %s' % datetime.now())

# SCHEDULER
scheduler = APScheduler()

def add_job(job, interval):
    scheduler.add_job(
        job, 
        trigger='interval',
        seconds=interval
    )
    
def add_s_jobs(job, interval=60):
    # days
    if interval<7:
        add_job(job, interval*24*60*60)
    # hrs
    if interval<24:
        add_job(job, interval*60*60)
    # mins
    if interval<60:
        add_job(job, interval*60)  
    # secs
    if interval<3600:
        add_job(job, interval)  

def start_jobs():
    scheduler.init_app(current_app)
    add_s_jobs(hello_job)
    scheduler.start()
