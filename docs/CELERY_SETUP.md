# Celery Background Task Setup

## Overview

The K9 Operations Management System now uses **Celery** with **Redis** for asynchronous background task processing. This setup provides:

- **Scalable background job processing** - offload CPU-intensive tasks from the web server
- **Task queuing and retry mechanisms** - automatic retry on failure
- **Scheduled task execution** - integrated with APScheduler for cron-like scheduling
- **Monitoring and logging** - comprehensive task execution tracking

## Architecture

```
┌─────────────────┐      ┌──────────────┐      ┌─────────────────┐
│  Flask Web App  │ ───> │    Redis     │ <─── │  Celery Worker  │
│  (APScheduler)  │      │   (Broker)   │      │   (Background)  │
└─────────────────┘      └──────────────┘      └─────────────────┘
         │                       │                       │
         │                       │                       │
         └───────────────────────┴───────────────────────┘
                            Database
```

## Components

### 1. Redis (Message Broker)

- **Image**: `redis:7-alpine`
- **Port**: 6379
- **Persistence**: Enabled with AOF (Append-Only File)
- **Databases**:
  - DB 0: General Redis cache
  - DB 1: Celery task broker
  - DB 2: Celery result backend

### 2. Celery Application

**Location**: `backend_fastapi/app/core/celery_app.py`

**Configuration**:
- Task serialization: JSON
- Timezone: Asia/Riyadh
- Task time limit: 30 minutes (hard), 25 minutes (soft)
- Auto-discovery of tasks from `backend_fastapi.app.tasks`
- Task routing by queue type

**Queues**:
- `k9_tasks` - Default queue
- `backups` - Database backup tasks
- `reports` - PDF report generation
- `notifications` - Notification cleanup
- `schedules` - Schedule management

### 3. Celery Worker

**Location**: `backend_fastapi/app/celery_worker.py`

**Docker Service**: `celery_worker`
- Concurrency: 2 workers
- Auto-restart: enabled
- Log level: info

## Implemented Tasks

### Automated Backups

**Task**: `backend_fastapi.app.tasks.backups.run_automated_backup`

**Purpose**: Creates automated database backups with optional Google Drive upload

**Schedule**: Configurable (daily/weekly/monthly)

**Features**:
- Idempotency checks
- Google Drive integration
- Automatic cleanup of old backups
- Comprehensive error handling

### Notification Cleanup

**Task**: `backend_fastapi.app.tasks.notifications.cleanup_old_notifications`

**Purpose**: Removes old read notifications to maintain database performance

**Schedule**: Weekly (Monday 2:00 AM)

**Retention**: 30 days (configurable)

### Schedule Auto-Lock

**Task**: `backend_fastapi.app.tasks.schedules.auto_lock_yesterday_schedules`

**Purpose**: Automatically locks schedules from previous days to prevent modifications

**Schedule**: Daily (configurable via `Config.SCHEDULE_AUTO_LOCK_HOUR`)

**Features**:
- Prevents data integrity issues
- Maintains audit trail

### PDF Report Generation (Placeholder)

**Task**: `backend_fastapi.app.tasks.reports.generate_pdf_report`

**Purpose**: Asynchronous PDF report generation

**Status**: Placeholder implementation for future integration

## APScheduler Integration

The system maintains **dual-run capability** during migration:

1. **Try Celery first**: APScheduler jobs attempt to enqueue tasks to Celery
2. **Fallback to synchronous**: If Celery is unavailable, run tasks synchronously
3. **Logging**: Track which execution path was used

**Example from `app.py`**:
```python
def run_scheduled_backup():
    # Try Celery first
    try:
        from backend_fastapi.app.tasks.backups import run_automated_backup_task
        task = run_automated_backup_task.delay()
        print(f"✓ Task enqueued to Celery (task_id: {task.id})")
        return
    except Exception as celery_error:
        print(f"⚠ Celery not available, falling back: {celery_error}")
    
    # Fallback to synchronous execution
    # ... existing backup logic ...
```

## Environment Variables

Required environment variables (set in `docker-compose.yml`):

```bash
# Redis
REDIS_URL=redis://redis:6379/0

# Celery
CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/2
CELERY_TASK_DEFAULT_QUEUE=k9_tasks
CELERY_TIMEZONE=Asia/Riyadh
```

## Usage

### Starting Services with Docker Compose

```bash
# Start all services (database, redis, web, celery_worker)
docker-compose up -d

# Start specific services
docker-compose up redis -d
docker-compose up celery_worker -d

# View logs
docker-compose logs -f celery_worker
docker-compose logs -f redis
```

### Manual Celery Worker (Development)

```bash
# From project root
celery -A backend_fastapi.app.celery_worker.celery_app worker --loglevel=info

# With multiple workers
celery -A backend_fastapi.app.celery_worker.celery_app worker --loglevel=info --concurrency=4

# With specific queue
celery -A backend_fastapi.app.celery_worker.celery_app worker --loglevel=info -Q backups,reports
```

### Monitoring Tasks

```bash
# List active tasks
celery -A backend_fastapi.app.celery_worker.celery_app inspect active

# List registered tasks
celery -A backend_fastapi.app.celery_worker.celery_app inspect registered

# Check worker status
celery -A backend_fastapi.app.celery_worker.celery_app status

# View statistics
celery -A backend_fastapi.app.celery_worker.celery_app inspect stats
```

### Manual Task Execution

```python
from backend_fastapi.app.tasks.backups import run_automated_backup_task

# Async execution
task = run_automated_backup_task.delay()
print(f"Task ID: {task.id}")

# Sync execution (for testing)
result = run_automated_backup_task.apply()
print(f"Result: {result}")
```

## Verification

Run the verification script to check the setup:

```bash
python backend_fastapi/verify_celery_setup.py
```

This verifies:
- Celery imports
- Configuration
- Task discovery
- Redis settings

## Migration Path

### Current State (Phase 4)

- ✅ Redis container configured
- ✅ Celery app created
- ✅ All background tasks implemented
- ✅ APScheduler integration with fallback
- ✅ Celery worker configured

### Future Phases

1. **Monitor dual-run** - Track Celery vs synchronous execution
2. **Verify reliability** - Ensure Celery handles all tasks correctly
3. **Remove APScheduler fallback** - Once Celery is proven stable
4. **Add monitoring** - Integrate Flower or similar for task monitoring
5. **Scale workers** - Add more workers as needed

## Troubleshooting

### Celery worker not starting

**Check**:
1. Redis is running: `docker-compose ps redis`
2. Redis connection: `redis-cli -h localhost ping`
3. Environment variables are set correctly
4. Check worker logs: `docker-compose logs celery_worker`

### Tasks not executing

**Check**:
1. Task is registered: `celery inspect registered`
2. Worker is consuming from correct queue
3. Redis broker URL is correct
4. Check task state: `task.state` and `task.info`

### Redis connection errors

**Solutions**:
1. Ensure Redis container is running
2. Check network connectivity between services
3. Verify Redis URL in environment variables
4. Check Redis logs: `docker-compose logs redis`

## Security Considerations

1. **Redis password**: Production deployments should use Redis password authentication
2. **Network isolation**: Redis should not be exposed publicly
3. **Task permissions**: Tasks run with application database permissions
4. **Secrets management**: Use environment variables for sensitive configuration

## Performance Tuning

### Worker Concurrency

Adjust based on workload:
```bash
# CPU-bound tasks (reports, backups)
celery worker --concurrency=2

# I/O-bound tasks (notifications, API calls)
celery worker --concurrency=10
```

### Task Priorities

Configure in `celery_app.py`:
```python
task_routes = {
    'backend_fastapi.app.tasks.backups.*': {
        'queue': 'backups',
        'priority': 9  # High priority
    },
    'backend_fastapi.app.tasks.notifications.*': {
        'queue': 'notifications',
        'priority': 1  # Low priority
    },
}
```

## References

- [Celery Documentation](https://docs.celeryproject.org/)
- [Redis Documentation](https://redis.io/documentation)
- [APScheduler Documentation](https://apscheduler.readthedocs.io/)
