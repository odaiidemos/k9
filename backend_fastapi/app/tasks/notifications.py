"""
Celery tasks for notification management and cleanup.
"""
import logging
from datetime import datetime, timedelta
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
    name='backend_fastapi.app.tasks.notifications.cleanup_old_notifications',
    max_retries=2,
    default_retry_delay=600
)
def cleanup_old_notifications_task(self, days: int = 30):
    """
    Clean up read notifications older than specified days.
    
    Args:
        days: Number of days to keep notifications (default: 30)
    
    Returns:
        dict: Result with count of cleaned up notifications
    """
    try:
        from k9.models.models_handler_daily import Notification
        from k9_shared.db import db
        from app import app
        
        with app.app_context():
            try:
                cutoff_date = datetime.utcnow() - timedelta(days=days)
                
                old_notifications = Notification.query.filter(
                    db.and_(
                        Notification.created_at < cutoff_date,
                        Notification.read == True
                    )
                ).all()
                
                count = len(old_notifications)
                for notif in old_notifications:
                    db.session.delete(notif)
                
                db.session.commit()
                
                logger.info(f"Cleaned up {count} old notifications (older than {days} days)")
                return {'status': 'success', 'cleanup_count': count, 'retention_days': days}
                
            except Exception as e:
                logger.error(f"Notification cleanup error: {str(e)}", exc_info=True)
                db.session.rollback()
                raise
                
    except Exception as exc:
        logger.error(f"Notification cleanup task failed: {exc}", exc_info=True)
        raise self.retry(exc=exc)
