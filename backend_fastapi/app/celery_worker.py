"""
Celery Worker Entrypoint for K9 Operations Management System.

This module serves as the entry point for running Celery workers.
It initializes the Celery app and makes it available for worker processes.

Usage:
    celery -A backend_fastapi.app.celery_worker.celery_app worker --loglevel=info

Docker usage:
    docker-compose up celery_worker
"""
import logging
import sys
from pathlib import Path

# Add project root to Python path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from backend_fastapi.app.core.celery_app import celery_app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

logger.info("Celery worker entrypoint initialized")
logger.info(f"Celery broker: {celery_app.conf.broker_url}")
logger.info(f"Celery result backend: {celery_app.conf.result_backend}")
logger.info(f"Task default queue: {celery_app.conf.task_default_queue}")

# Export celery_app for Celery worker to discover
__all__ = ['celery_app']
