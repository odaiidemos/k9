"""
Celery tasks package for K9 Operations Management System.

This package contains all asynchronous background tasks:
- backups: Automated database backups
- notifications: Notification cleanup tasks
- schedules: Daily schedule auto-lock tasks
- reports: PDF report generation tasks
"""

from backend_fastapi.app.tasks.backups import (
    run_automated_backup_task,
    cleanup_old_backups_task,
)

from backend_fastapi.app.tasks.notifications import (
    cleanup_old_notifications_task,
)

from backend_fastapi.app.tasks.schedules import (
    auto_lock_yesterday_schedules_task,
)

__all__ = [
    'run_automated_backup_task',
    'cleanup_old_backups_task',
    'cleanup_old_notifications_task',
    'auto_lock_yesterday_schedules_task',
]
