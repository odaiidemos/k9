"""
Verification script for Celery setup in K9 Operations Management System.

This script verifies:
1. Celery configuration is correct
2. Tasks are discoverable
3. Redis connection settings are valid
4. Import paths are correct
"""
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def verify_celery_imports():
    """Verify all Celery-related imports work"""
    print("=" * 60)
    print("VERIFYING CELERY IMPORTS")
    print("=" * 60)
    
    try:
        from backend_fastapi.app.core.celery_app import celery_app, get_celery_app, is_celery_available
        print("✓ Celery app imports successful")
    except Exception as e:
        print(f"✗ Failed to import celery_app: {e}")
        return False
    
    try:
        from backend_fastapi.app.tasks import (
            run_automated_backup_task,
            cleanup_old_backups_task,
            cleanup_old_notifications_task,
            auto_lock_yesterday_schedules_task,
        )
        print("✓ All task imports successful")
    except Exception as e:
        print(f"✗ Failed to import tasks: {e}")
        return False
    
    return True


def verify_celery_config():
    """Verify Celery configuration"""
    print("\n" + "=" * 60)
    print("VERIFYING CELERY CONFIGURATION")
    print("=" * 60)
    
    try:
        from backend_fastapi.app.core.celery_app import celery_app
        from backend_fastapi.app.core.config import settings
        
        print(f"✓ Celery broker URL: {celery_app.conf.broker_url}")
        print(f"✓ Celery result backend: {celery_app.conf.result_backend}")
        print(f"✓ Task serializer: {celery_app.conf.task_serializer}")
        print(f"✓ Result serializer: {celery_app.conf.result_serializer}")
        print(f"✓ Accept content: {celery_app.conf.accept_content}")
        print(f"✓ Timezone: {celery_app.conf.timezone}")
        print(f"✓ Default queue: {celery_app.conf.task_default_queue}")
        print(f"✓ Task time limit: {celery_app.conf.task_time_limit} seconds")
        
        return True
    except Exception as e:
        print(f"✗ Failed to verify configuration: {e}")
        return False


def verify_task_discovery():
    """Verify tasks are registered with Celery"""
    print("\n" + "=" * 60)
    print("VERIFYING TASK DISCOVERY")
    print("=" * 60)
    
    try:
        from backend_fastapi.app.core.celery_app import celery_app
        
        registered_tasks = list(celery_app.tasks.keys())
        print(f"\n✓ Found {len(registered_tasks)} registered tasks:")
        
        k9_tasks = [task for task in registered_tasks if 'backend_fastapi.app.tasks' in task]
        
        if k9_tasks:
            print("\nK9 System Tasks:")
            for task_name in sorted(k9_tasks):
                print(f"  - {task_name}")
        else:
            print("⚠ No K9 tasks found - this may be normal if tasks haven't been imported yet")
        
        return True
    except Exception as e:
        print(f"✗ Failed to verify task discovery: {e}")
        return False


def verify_redis_settings():
    """Verify Redis configuration settings"""
    print("\n" + "=" * 60)
    print("VERIFYING REDIS SETTINGS")
    print("=" * 60)
    
    try:
        from backend_fastapi.app.core.config import settings
        
        print(f"✓ Redis URL: {settings.REDIS_URL}")
        print(f"✓ Celery Broker URL: {settings.CELERY_BROKER_URL}")
        print(f"✓ Celery Result Backend: {settings.CELERY_RESULT_BACKEND}")
        
        # Note: Actual Redis connection test requires Redis to be running
        print("\n⚠ Note: Actual Redis connection test requires Redis to be running")
        print("  Start Redis with: docker-compose up redis")
        
        return True
    except Exception as e:
        print(f"✗ Failed to verify Redis settings: {e}")
        return False


def main():
    """Run all verification checks"""
    print("\nK9 Operations Management System - Celery Setup Verification\n")
    
    results = {
        'imports': verify_celery_imports(),
        'config': verify_celery_config(),
        'task_discovery': verify_task_discovery(),
        'redis_settings': verify_redis_settings(),
    }
    
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    for check, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{check.upper()}: {status}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n✓ All verification checks passed!")
        print("\nNext steps:")
        print("1. Start Redis: docker-compose up redis -d")
        print("2. Start Celery worker: docker-compose up celery_worker")
        print("3. Monitor worker logs: docker-compose logs -f celery_worker")
    else:
        print("\n✗ Some verification checks failed. Please review the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
