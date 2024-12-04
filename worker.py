import os
from celery import Celery

# Initialize Celery instance with a specific name
celery = Celery("codejudge_worker")

# Configure broker and result backend from environment variables, with defaults
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
celery.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)

# Automatically discover tasks in the specified modules
celery.autodiscover_tasks(["submit.tasks", "problem.tasks"])
