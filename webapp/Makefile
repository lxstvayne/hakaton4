export POSTGRES_DB=hakaton
export POSTGRES_HOST=195.2.76.179
export POSTGRES_PORT=5432
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=crazyadmin228


run-dev:
	python manage.py runserver 0.0.0.0:8888

shell:
	python manage.py shell

migrate:
	python manage.py migrate $(ARGS)

makemigrations:
	python manage.py makemigrations

flush:
	python manage.py flush

createsuperuser:
	python manage.py createsuperuser $(ARGS)

manage:
	python manage.py $(ARGS)