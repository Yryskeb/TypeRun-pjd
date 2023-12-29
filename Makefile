#make run	-	команда терминал
run:
	python3 manage.py runserver

#make migrate
migrate:
	python3 manage.py makemigrations 
	python3 manage.py migrate

superuser:
	python3 manage.py createsuperuser

install:
	pip3 install -r requirements.txt 

celery:
	celery -A typerun worker -l info