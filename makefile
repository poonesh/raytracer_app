.PHONY: all help rabbitmq celery run production-celery production-app
	
all: help

help: 
	@echo "usage:"
	@echo "make rabbitmq: runs the rabbitmq-server"
	@echo "make celery: runs celery"
	@echo "make run: runs the app"
	@echo "make production-celery: runs celery for production app"
	@echo "make production-app: runs celery for production app"

rabbitmq:
	rabbitmq-server

celery:
	cd src && celery worker -A app.celery --loglevel=info

run:
	cd src && python app.py

production-celery:
	cd src && nohup celery worker -A app.celery >/dev/null 2>/dev/null &

production-app:
	cd src && nohup python app.py >/dev/null 2>/dev/null &
