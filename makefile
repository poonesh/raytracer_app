.PHONY: all help rabbitmq celery run
	
all: help

help: 
	@echo "usage:"
	@echo "make rabbitmq: runs the rabbitmq-server"
	@echo "make celery: runs celery"
	@echo "make run: runs the app"


rabbitmq:
	rabbitmq-server

celery:
	cd src && celery worker -A app.celery --loglevel=info

run:
	cd src && python app.py
