import os
from flask_socketio import SocketIO
from flask_celery import make_celery

def set_config(app):
	app.config['SECRET_KEY'] = 'secret!'
	password = os.environ['POSTGRES_PWD']

	app.config.update(
	# Broker settings
	CELERY_BROKER_URL='amqp://localhost//',
	# Using the database to store task state and results
	CELERY_RESULT_BACKEND='db+postgresql://postgres:{}@localhost/user_data'.format(password)
	)

	socketio = SocketIO(app, engineio_logger=True, ping_timeout=120, message_queue='amqp://')
	celery = make_celery(app)
	return (socketio, celery)
