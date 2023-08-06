import schedule
import time
from datetime import datetime, timedelta

class GynxScheduler:
    """Run gynx commands on a schedule"""

    def __init__(self, duration=60, days=None, hours=None, *args, **kwargs):
        self.duration = duration
        self.days = days
        self.hours = hours

    def add_job(self, callback):
        schedule.every(self.duration).minutes.do(callback)

    def start(self):
        start_time = datetime.now()
        if self.days and self.hours:
            end_time = start_time + timedelta(days=self.days, hours=self.hours)
        elif self.days:
            end_time = start_time + timedelta(days=self.days)
        elif self.hours:
            end_time = start_time + timedelta(hours=self.hours)
        while True:
            schedule.run_pending()
            if self.days or self.hours:
                if datetime.now() >= end_time:
                    return
            time.sleep(1)
