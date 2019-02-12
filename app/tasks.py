from . import celery
from celery.utils.log import get_task_logger

log = get_task_logger(__name__)


@celery.task(time_limit=20)
def do_something():
    log.info("Doing something")
