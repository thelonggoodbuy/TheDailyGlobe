from celery import Celery

celery_app = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
)

# celery_app.conf.task_routes = {"tasks.*": {"queue": "default"}}
celery_app.autodiscover_tasks([
    "src.application.tasks.notification_tasks"
])
