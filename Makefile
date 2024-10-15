run:
	uvicorn src.main.api:app --reload
	
FASTAPI_APP=src.main.api:app

run-admin:
	python3 admin_panel/manage.py runserver

generate_migration:
	alembic revision --autogenerate -m "$(title)"

implement_migration:
	alembic upgrade head



unfold-docker:
	gunicorn admin_panel.config.wsgi:application --bind 0.0.0.0:8000

	# gunicorn admin_panel.config.wsgi:application --bind 0.0.0.0:8000
	# uvicorn admin_panel.config.wsgi:application --host 0.0.0.0 --port 8000
	# django-admin check

run-docker:
	uvicorn src.main.api:app --host 0.0.0.0 --port 8000



run-migrator-docker:


	alembic upgrade head

	python admin_panel/manage.py migrate --database=default
	django-admin collectstatic --settings=admin_panel.config.settings
	python admin_panel/manage.py generate_initial_admin_user


# run-initial-data:
# 	python admin_panel/manage.py generate_initial_admin_user.py
