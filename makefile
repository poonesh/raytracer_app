.PHONY: all help rabbitmq celery run production-celery production-app find-celery-process find-python-process
	
all: help

help: 
	@echo "usage:"
	@echo "make rabbitmq: runs the rabbitmq-server"
	@echo "make celery: runs celery"
	@echo "make run: runs the app"
	@echo "make production-celery: runs celery for production app"
	@echo "make production-app: runs celery for production app"
	@echo "make find-celery-process: find current celery process"
	@echo "make find-python-process: find current python process"

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

find-celery-process:
	ps -ef | grep celery

find-python-process:
	ps -ef | grep python