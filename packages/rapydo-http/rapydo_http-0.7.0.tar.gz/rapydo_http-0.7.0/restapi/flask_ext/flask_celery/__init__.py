# -*- coding: utf-8 -*-

"""
Celery extension wrapper

"""
from celery import Celery
from functools import wraps
import traceback

from restapi.services.mail import send_mail_is_active, send_mail
from restapi.flask_ext import BaseExtension
from restapi.confs import get_project_configuration

from restapi.utilities.logs import get_logger
log = get_logger(__name__)


class CeleryExt(BaseExtension):

    CELERY_BEAT_SCHEDULER = None
    REDBEAT_KEY_PREFIX = "redbeat:"
    celery_app = None

    def custom_connection(self, **kwargs):

        worker_mode = self.args.get("worker_mode", False)

        broker = self.variables.get("broker")

        if broker is None:
            log.exit("Unable to start Celery, missing broker service")
            # celery_app = None
            # return celery_app

        BROKER_HOST = self.variables.get("broker_host")
        BROKER_PORT = int(self.variables.get("broker_port"))
        BROKER_USER = self.variables.get("broker_user", "")
        BROKER_PASSWORD = self.variables.get("broker_password", "")
        BROKER_VHOST = self.variables.get("broker_vhost", "")

        if BROKER_USER == "":
            BROKER_USER = None
        if BROKER_PASSWORD == "":
            BROKER_PASSWORD = None

        if BROKER_VHOST != "":
            BROKER_VHOST = "/%s" % BROKER_VHOST

        backend = self.variables.get("backend", broker)
        BACKEND_HOST = self.variables.get("backend_host", BROKER_HOST)
        BACKEND_PORT = int(self.variables.get("backend_port", BROKER_PORT))
        BACKEND_USER = self.variables.get("backend_user", BROKER_USER)
        BACKEND_PASSWORD = self.variables.get("backend_password", BROKER_PASSWORD)

        if BACKEND_USER == "":
            BACKEND_USER = None
        if BACKEND_PASSWORD == "":
            BACKEND_PASSWORD = None

        if BROKER_USER is not None and BROKER_PASSWORD is not None:
            BROKER_CREDENTIALS = "%s:%s@" % (BROKER_USER, BROKER_PASSWORD)
        else:
            BROKER_CREDENTIALS = ""

        if broker == 'RABBIT':
            BROKER_URL = 'amqp://%s%s%s' % (
                BROKER_CREDENTIALS,
                BROKER_HOST,
                BROKER_VHOST,
            )
            log.info("Configured RabbitMQ as Celery broker %s", BROKER_URL)
        elif broker == 'REDIS':
            BROKER_URL = 'redis://%s%s:%s/0' % (
                BROKER_CREDENTIALS,
                BROKER_HOST,
                BROKER_PORT,
            )
            log.info("Configured Redis as Celery broker %s", BROKER_URL)
        else:
            log.error("Unable to start Celery unknown broker service: %s", broker)
            celery_app = None
            return celery_app

        if BACKEND_USER is not None and BACKEND_PASSWORD is not None:
            BACKEND_CREDENTIALS = "%s:%s@" % (BACKEND_USER, BACKEND_PASSWORD)
        else:
            BACKEND_CREDENTIALS = ""

        if backend == 'RABBIT':
            BACKEND_URL = 'rpc://%s%s:%s/0' % (
                BACKEND_CREDENTIALS,
                BACKEND_HOST,
                BACKEND_PORT,
            )
            log.info("Configured RabbitMQ as Celery backend %s", BACKEND_URL)
        elif backend == 'REDIS':
            BACKEND_URL = 'redis://%s%s:%s/0' % (
                BACKEND_CREDENTIALS,
                BACKEND_HOST,
                BACKEND_PORT,
            )
            log.info("Configured Redis as Celery backend %s", BACKEND_URL)
        elif backend == 'MONGODB':
            BACKEND_URL = 'mongodb://%s%s:%s' % (
                BACKEND_CREDENTIALS,
                BACKEND_HOST,
                BACKEND_PORT,
            )
            log.info("Configured MongoDB as Celery backend %s", BACKEND_URL)
        else:
            log.exit("Unable to start Celery unknown backend service: %s", backend)
            # celery_app = None
            # return celery_app

        celery_app = Celery('RestApiQueue', broker=BROKER_URL, backend=BACKEND_URL)

        # if not worker_mode:

        #     from celery.task.control import inspect

        #     insp = inspect()
        #     if not insp.stats():
        #         log.warning("No running Celery workers were found")

        # Skip initial warnings, avoiding pickle format (deprecated)
        celery_app.conf.accept_content = ['json']
        celery_app.conf.task_serializer = 'json'
        celery_app.conf.result_serializer = 'json'
        # Max priority default value for all queues
        # Required to be able to set priority parameter on apply_async calls
        # celery_app.conf.task_queue_max_priority = 10

        # default_exchange = Exchange('default', type='direct')
        # priority_exchange = Exchange('priority', type='direct')
        # celery_app.conf.task_queues = [
        #     Queue(
        #         'priority',
        #         priority_exchange,
        #         routing_key='priority',
        #         queue_arguments={
        #             'x-max-priority': 10
        #         }
        #     )
        # ]
        # If you want to apply a more strict priority to items
        # probably prefetching should also be disabled:

        # CELERY_ACKS_LATE = True
        # CELERYD_PREFETCH_MULTIPLIER = 1

        """
        This is a workaround, please fix me!

        This workaround is required to avoid the work be freeze when is
        the connection to rabbit is temporary lost.
        Behavious without the option:
        connection lost
        => trying to connect - repeat until the connection is back
        => once the connection is back Celery raise an exception and stops:
        ConnectionResetError: [Errno 104] Connection reset by peer

        broker_pool_limit = None means that the connection pool is disabled
        and connections will be established and closed for every use
        I found this workaround here:

        https://github.com/celery/celery/issues/4226
        """
        # celery_app.conf.broker_pool_limit = None

        # Do not import before loading the ext!
        from restapi.services.detect import Detector

        if Detector.get_bool_from_os('CELERY_BEAT_ENABLED'):

            CeleryExt.CELERY_BEAT_SCHEDULER = backend

            if backend == 'MONGODB':
                SCHEDULER_DB = 'celery'
                celery_app.conf['CELERY_MONGODB_SCHEDULER_DB'] = SCHEDULER_DB
                celery_app.conf['CELERY_MONGODB_SCHEDULER_COLLECTION'] = "schedules"
                celery_app.conf['CELERY_MONGODB_SCHEDULER_URL'] = BACKEND_URL

                import mongoengine

                m = mongoengine.connect(SCHEDULER_DB, host=BACKEND_URL)
                log.info("Celery-beat connected to MongoDB: %s", m)
            elif backend == 'REDIS':

                BEAT_BACKEND_URL = 'redis://%s%s:%s/1' % (
                    BACKEND_CREDENTIALS,
                    BACKEND_HOST,
                    BACKEND_PORT,
                )

                celery_app.conf['REDBEAT_REDIS_URL'] = BEAT_BACKEND_URL
                celery_app.conf['REDBEAT_KEY_PREFIX'] = CeleryExt.REDBEAT_KEY_PREFIX
                log.info("Celery-beat connected to Redis: %s", BEAT_BACKEND_URL)
            else:
                log.warning("Cannot configure mongodb celery beat scheduler")

        if CeleryExt.celery_app is None:
            CeleryExt.celery_app = celery_app

        return celery_app

    @classmethod
    def get_periodic_task(cls, name):

        if cls.CELERY_BEAT_SCHEDULER == 'MONGODB':
            from celerybeatmongo.models import PeriodicTask, DoesNotExist
            try:
                return PeriodicTask.objects.get(name=name)
            except DoesNotExist:
                return None
        elif cls.CELERY_BEAT_SCHEDULER == 'REDIS':
            from redbeat.schedulers import RedBeatSchedulerEntry
            try:
                task_key = "%s%s" % (cls.REDBEAT_KEY_PREFIX, name)
                return RedBeatSchedulerEntry.from_key(
                    task_key, app=CeleryExt.celery_app)
            except KeyError:
                return None
        else:
            log.error(
                "Unsupported celery-beat scheduler: %s", cls.CELERY_BEAT_SCHEDULER)

    @classmethod
    def delete_periodic_task(cls, name):
        t = cls.get_periodic_task(name)
        if t is None:
            return False
        t.delete()
        return True

    # period = ('days', 'hours', 'minutes', 'seconds', 'microseconds')
    @classmethod
    def create_periodic_task(cls, name, task, every,
                             period='seconds', args=[], kwargs={}):

        if cls.CELERY_BEAT_SCHEDULER == 'MONGODB':
            from celerybeatmongo.models import PeriodicTask
            PeriodicTask(
                name=name,
                task=task,
                enabled=True,
                args=args,
                kwargs=kwargs,
                interval=PeriodicTask.Interval(every=every, period=period),
            ).save()
        elif cls.CELERY_BEAT_SCHEDULER == 'REDIS':
            from celery.schedules import schedule
            from redbeat.schedulers import RedBeatSchedulerEntry
            if period != 'seconds':

                # do conversion... run_every should be a datetime.timedelta
                log.error("Unsupported period %s for redis beat", period)

            interval = schedule(run_every=every)  # seconds
            entry = RedBeatSchedulerEntry(
                name,
                task,
                interval,
                args=args,
                app=CeleryExt.celery_app
            )
            entry.save()

        else:
            log.error(
                "Unsupported celery-beat scheduler: %s", cls.CELERY_BEAT_SCHEDULER)

    @classmethod
    def create_crontab_task(
        cls,
        name,
        task,
        minute,
        hour,
        day_of_week="*",
        day_of_month="*",
        month_of_year="*",
        args=[],
        kwargs={},
    ):

        if cls.CELERY_BEAT_SCHEDULER == 'MONGODB':
            from celerybeatmongo.models import PeriodicTask
            PeriodicTask(
                name=name,
                task=task,
                enabled=True,
                args=args,
                kwargs=kwargs,
                crontab=PeriodicTask.Crontab(
                    minute=minute,
                    hour=hour,
                    day_of_week=day_of_week,
                    day_of_month=day_of_month,
                    month_of_year=month_of_year,
                ),
            ).save()
        elif cls.CELERY_BEAT_SCHEDULER == 'REDIS':
            from celery.schedules import crontab
            from redbeat.schedulers import RedBeatSchedulerEntry
            interval = crontab(
                minute=minute,
                hour=hour,
                day_of_week=day_of_week,
                day_of_month=day_of_month,
                month_of_year=month_of_year
            )

            entry = RedBeatSchedulerEntry(
                name,
                task,
                interval,
                args=args,
                app=CeleryExt.celery_app
            )
            entry.save()

        else:
            log.error(
                "Unsupported celery-beat scheduler: %s", cls.CELERY_BEAT_SCHEDULER)


def send_errors_by_email(func):
    """
    Send a notification email to a given recipient to the
    system administrator with details about failure.
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):

        try:
            return func(self, *args, **kwargs)

        except BaseException:

            task_id = self.request.id
            task_name = self.request.task

            log.error("Celery task %s failed (%s)", task_id, task_name)
            arguments = str(self.request.args)
            log.error("Failed task arguments: %s", arguments[0:256])
            log.error("Task error: %s", traceback.format_exc())

            if send_mail_is_active():
                log.info("Sending error report by email", task_id, task_name)

                body = "Celery task %s failed" % task_id
                body += "\n\n"
                body += "Name: %s" % task_name
                body += "\n\n"
                body += "Arguments: %s" % str(self.request.args)
                body += "\n\n"
                body += "Error: %s" % (traceback.format_exc())

                project = get_project_configuration(
                    "project.title",
                    default='Unkown title',
                )
                subject = "%s: task %s failed" % (project, task_name)
                send_mail(body, subject)

    return wrapper
