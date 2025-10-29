"""
Celery tasks for automated database backups.
"""
import logging
from datetime import datetime
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
    name='backend_fastapi.app.tasks.backups.run_automated_backup',
    max_retries=3,
    default_retry_delay=300
)
def run_automated_backup_task(self):
    """
    Run automated database backup.
    
    This task wraps BackupManager.create_backup with proper error handling
    and idempotency checks.
    """
    try:
        from k9.utils.backup_utils import BackupManager
        from k9.models.models import BackupSettings, BackupFrequency
        from k9_shared.db import db
        from app import app
        
        with app.app_context():
            try:
                settings = BackupSettings.get_settings()
                
                if not settings.auto_backup_enabled or settings.backup_frequency == BackupFrequency.DISABLED:
                    logger.info("Automated backup skipped: disabled in settings")
                    return {'status': 'skipped', 'reason': 'disabled_in_settings'}
                
                backup_manager = BackupManager()
                description = f'Automated {settings.backup_frequency.value.lower()} backup (Celery)'
                success, filename, error = backup_manager.create_backup(description, upload_to_drive=True)
                
                settings.last_backup_at = datetime.utcnow()
                if success:
                    if error:
                        settings.last_backup_status = 'partial'
                        settings.last_backup_message = f'Backup created locally but Google Drive upload failed: {error}'
                        logger.warning(f"Automated backup created locally: {filename}, but Google Drive upload failed: {error}")
                        result = {'status': 'partial', 'filename': filename, 'error': error}
                    else:
                        settings.last_backup_status = 'success'
                        settings.last_backup_message = f'Automated backup created: {filename}'
                        logger.info(f"Automated backup created successfully: {filename}")
                        result = {'status': 'success', 'filename': filename}
                    
                    if settings.retention_days > 0:
                        cleanup_count = backup_manager.cleanup_old_backups(settings.retention_days)
                        if cleanup_count > 0:
                            logger.info(f"Cleaned up {cleanup_count} old backups")
                            if isinstance(result, dict):
                                result['cleanup_count'] = cleanup_count
                else:
                    settings.last_backup_status = 'failed'
                    settings.last_backup_message = error
                    logger.error(f"Automated backup failed: {error}")
                    result = {'status': 'failed', 'error': error}
                
                db.session.commit()
                return result
                
            except Exception as e:
                logger.error(f"Scheduled backup error: {str(e)}", exc_info=True)
                db.session.rollback()
                raise
                
    except Exception as exc:
        logger.error(f"Backup task failed: {exc}", exc_info=True)
        raise self.retry(exc=exc)


@celery_app.task(
    bind=True,
    base=DatabaseTask,
    name='backend_fastapi.app.tasks.backups.cleanup_old_backups',
    max_retries=2,
    default_retry_delay=600
)
def cleanup_old_backups_task(self, retention_days: int = 30):
    """
    Clean up old database backups.
    
    Args:
        retention_days: Number of days to retain backups (default: 30)
    
    Returns:
        dict: Result with count of cleaned up backups
    """
    try:
        from k9.utils.backup_utils import BackupManager
        
        backup_manager = BackupManager()
        cleanup_count = backup_manager.cleanup_old_backups(retention_days)
        
        logger.info(f"Cleaned up {cleanup_count} old backups (retention: {retention_days} days)")
        return {'status': 'success', 'cleanup_count': cleanup_count, 'retention_days': retention_days}
        
    except Exception as exc:
        logger.error(f"Backup cleanup task failed: {exc}", exc_info=True)
        raise self.retry(exc=exc)
