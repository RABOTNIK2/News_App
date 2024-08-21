FROM python:3.12-alpine

WORKDIR /kyrsach
COPY . /kyrsach/

RUN pip install -r requirements/prod.txt

CMD python manage.py makemigrations --settings=project.settings.prod \
    && python manage.py migrate --settings=project.settings.prod \
    && python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(email='admin@admin.ru').exists() or User.objects.create_superuser('admin@admin.ru', 'admin', 'admin', 18)" --settings=project.settings.prod \
    && python manage.py shell -c "from django.contrib.sites.models import Site; site = Site.objects.filter( domain='example.com').update(name='127.0.0.1:8001', domain='127.0.0.1:8001')" --settings=project.settings.prod \
    && python manage.py runserver 0.0.0.0:8000 --settings=project.settings.prod 
