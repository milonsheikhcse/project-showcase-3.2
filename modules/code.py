import random
from django.contrib.auth.models import User

def id_generate():
    code_in_db = list(User.objects.all().values_list('username', flat=True))
    while True:
        code_ = random.randint(1000000, 9999999)
        if code_ not in code_in_db:
            return code_
