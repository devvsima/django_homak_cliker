-include .env

run:
	python manage.py makemigrations && \
	python manage.py migrate && \
	gunicorn -b 0.0.0.0:$(server_port) salamis.wsgi