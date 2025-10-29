"""
Celery tasks for daily schedule management and auto-locking.
"""
import logging
from datetime import date, timedelta
from celery import Task
from backend_fastapi.app.core.celery_app import celery_app

logger = logging.getLogger(__name__)


class DatabaseTask(Task):
    """Base task class for tasks that need database access"""
    _db_session = None
    
    def after_return(self, *args, **kwargs):
        """Clean up database session after task completion"""
        if self._db_session is not None:
            self._db_session.close()


@celery_app.task(
    bind=True,
    base=DatabaseTask,
    name='backend_fastapi.app.tasks.schedules.auto_lock_yesterday_schedules',
    max_retries=3,
    default_retry_delay=300
)
def auto_lock_yesterday_schedules_task(self):
    """
    Automatically lock all schedules from yesterday.
    
    This task should be run daily at the end of each day to prevent
    modifications to past schedules.
    
    Returns:
        dict: Result with count of locked schedules
    """
    try:
        from k9.models.models_handler_daily import DailySchedule, ScheduleStatus
        from k9.services.handler_service import DailyScheduleService
        from k9_shared.db import db
        from app import app
        
        with app.app_context():
            try:
                yesterday = date.today() - timedelta(days=1)
                
                schedules = DailySchedule.query.filter(
                    db.and_(
                        DailySchedule.date <= yesterday,
                        DailySchedule.status == ScheduleStatus.OPEN
                    )
                ).all()
                
                locked_count = 0
                for schedule in schedules:
                    if DailyScheduleService.lock_schedule(str(schedule.id)):
                        locked_count += 1
                
                logger.info(f"Auto-locked {locked_count} schedules from {yesterday} and earlier")
                return {'status': 'success', 'locked_count': locked_count, 'date': str(yesterday)}
                
            except Exception as e:
                logger.error(f"Schedule auto-lock error: {str(e)}", exc_info=True)
                db.session.rollback()
                raise
                
    except Exception as exc:
        logger.error(f"Schedule auto-lock task failed: {exc}", exc_info=True)
        raise self.retry(exc=exc)
