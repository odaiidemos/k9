"""
Celery application configuration for K9 Operations Management System.

This module sets up Celery with Redis broker and result backend,
configures task auto-discovery, and provides a factory function.
"""
import logging
from celery import Celery
from celery.signals import task_failure, task_success
from backend_fastapi.app.core.config import settings

logger = logging.getLogger(__name__)


def create_celery_app() -> Celery:
    """
    Factory function to create and configure Celery application.
    
    Returns:
        Celery: Configured Celery application instance
    """
    celery_app = Celery(
        "k9_tasks",
        broker=settings.CELERY_BROKER_URL,
        backend=settings.CELERY_RESULT_BACKEND
    )
    
    celery_app.conf.update(
        task_serializer=settings.CELERY_TASK_SERIALIZER,
        result_serializer=settings.CELERY_RESULT_SERIALIZER,
        accept_content=settings.CELERY_ACCEPT_CONTENT,
        timezone=settings.CELERY_TIMEZONE,
        enable_utc=True,
        task_track_started=settings.CELERY_TASK_TRACK_STARTED,
        task_time_limit=settings.CELERY_TASK_TIME_LIMIT,
        task_soft_time_limit=settings.CELERY_TASK_SOFT_TIME_LIMIT,
        worker_prefetch_multiplier=settings.CELERY_WORKER_PREFETCH_MULTIPLIER,
        worker_max_tasks_per_child=settings.CELERY_WORKER_MAX_TASKS_PER_CHILD,
        task_default_queue=settings.CELERY_TASK_DEFAULT_QUEUE,
        task_routes={
            'backend_fastapi.app.tasks.backups.*': {'queue': 'backups'},
            'backend_fastapi.app.tasks.reports.*': {'queue': 'reports'},
            'backend_fastapi.app.tasks.notifications.*': {'queue': 'notifications'},
            'backend_fastapi.app.tasks.schedules.*': {'queue': 'schedules'},
        },
        task_default_retry_delay=60,
        task_max_retries=3,
        broker_connection_retry_on_startup=True,
    )
    
    celery_app.autodiscover_tasks(['backend_fastapi.app.tasks'])
    
    return celery_app


celery_app = create_celery_app()


@task_failure.connect
def task_failure_handler(sender=None, task_id=None, exception=None, args=None, kwargs=None, traceback=None, einfo=None, **kw):
    """Handle task failures with logging"""
    task_name = sender.name if sender else 'Unknown'
    logger.error(
        f"Task {task_name} (ID: {task_id}) failed: {exception}",
        exc_info=einfo,
        extra={
            'task_name': task_name,
            'task_id': task_id,
            'args': args,
            'kwargs': kwargs,
        }
    )


@task_success.connect
def task_success_handler(sender=None, result=None, **kwargs):
    """Handle task success with logging"""
    task_name = sender.name if sender else 'Unknown'
    logger.info(
        f"Task {task_name} completed successfully",
        extra={
            'task_name': task_name,
            'result': result,
        }
    )


def get_celery_app() -> Celery:
    """
    Get the Celery application instance.
    
    Returns:
        Celery: Celery application instance
    """
    return celery_app


def is_celery_available() -> bool:
    """
    Check if Celery/Redis is available for task enqueueing.
    
    Returns:
        bool: True if Celery is available, False otherwise
    """
    try:
        celery_app.control.inspect().ping()
        return True
    except Exception as e:
        logger.warning(f"Celery not available: {e}")
        return False
