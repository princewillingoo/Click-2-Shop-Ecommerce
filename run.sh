#!/bin/bash

source /home/princewillingoo/django\ projects/env/myshop/bin/activate
python3 manage.py runserver
sudo docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management
celery -A myshop worker -l info
ngrok http 8000