run:
	uvicorn src.main.api:app --reload
	
run-admin:
	python3 admin_panel/manage.py runserver

generate_migration:
	alembic revision --autogenerate -m "$(title)"

implement_migration:
	alembic upgrade head