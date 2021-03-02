import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTGRESQL = {
    'default':{
        'ENGINE':'django.db.backends.postgresql_psycopg2',
        'NAME': 'dat4tq7voll6q5',
        'USER': 'wtvrvuplylwluf',
        'PASSWORD': 'fb62f69d0d8b23fd162cf33746c59cf4cf2f8040fb9847dd85f236b1c8af17d5',
        'HOST': 'ec2-3-232-163-23.compute-1.amazonaws.com',
        'PORT': '5432'
    }
}
