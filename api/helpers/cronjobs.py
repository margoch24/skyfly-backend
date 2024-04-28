from api.app_scheduler import AppScheduler
from api.constants import Environment
from api.helpers.flights import update_scheduled_flights
from api.helpers.seats import create_default_seats
from api.helpers.settings import create_default_settings
from config import DefaultConfig


def create_default_data():
    create_default_seats()
    create_default_settings()


def set_cronjobs(app_context):
    if DefaultConfig.ENV == Environment.TEST:
        return

    scheduler = AppScheduler(app_context)

    scheduler.add_job(
        update_scheduled_flights,
        trigger="interval",
        hours=1,
        job_id="update_scheduled_flights",
    )

    scheduler.initiate()
