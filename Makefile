run:
	uvicorn src.main.api:app --reload
	
FASTAPI_APP=src.main.api:app

run-admin:
	python3 admin_panel/manage.py runserver

generate_migration:
	alembic revision --autogenerate -m "$(title)"

implement_migration:
	alembic upgrade head


# admin docker command
unfold-docker:
	gunicorn admin_panel.config.wsgi:application --bind 0.0.0.0:8000
	# gunicorn admin_panel.config.wsgi:application --bind 0.0.0.0:3004



# api docker command
run-docker:
	uvicorn src.main.api:app --host 0.0.0.0 --port 8001
	# uvicorn src.main.api:app --host 0.0.0.0 --port 3003



run-migrator-docker:


	alembic upgrade head

	python admin_panel/manage.py migrate --database=default
	django-admin collectstatic --settings=admin_panel.config.settings --noinput
	python admin_panel/manage.py generate_initial_admin_user
	python admin_panel/manage.py generate_initial_categories
	python admin_panel/manage.py generate_initial_articles
	python admin_panel/manage.py generate_initial_tariffs

worker:

	celery -A src.infrastructure.celery_app.celery_app worker -l INFO

# run-initial-data:
# 	python admin_panel/manage.py generate_initial_admin_user.py
