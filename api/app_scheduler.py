from apscheduler.schedulers.background import BackgroundScheduler

from api.singleton_meta import SingletonMeta


class AppScheduler(metaclass=SingletonMeta):

    def __init__(self, app_context):
        self.__scheduler = BackgroundScheduler()
        self.__app_context = app_context

    def initiate(self):
        self.__scheduler.start()

    def add_job(
        self, job_func, trigger, job_id, hours=None, minutes=None, seconds=None
    ):
        time = {"minutes": minutes, "hours": hours, "seconds": seconds}

        valid_time = {key: value for key, value in time.items() if value}

        self.__scheduler.add_job(
            func=lambda: self.__app_context.push() or job_func(),
            trigger=trigger,
            id=job_id,
            **valid_time
        )

    def remove_job(self, job_id):
        self.__scheduler.remove_job(job_id)
