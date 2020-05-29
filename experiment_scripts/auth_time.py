# Imports
from db_model.models import User
from django.contrib.auth import authenticate, login as auth_login
from timeit import default_timer as timer
import json, sys
import time
from django.db import reset_queries


auth_times = {}

# Example username, pwd authentication
username = "anne"
password = "pwd123"

for i in range(100000):
    start = timer()

    # Authenticates with django authenticate method
    #user = authenticate(username=username, password=password)

    # Searchs for the user with the First and Last Name
    user = User.objects.filter(first_name="John", last_name="Sullivan")
    repr(user)

    ######################## DO TEAM VERIFICATION ############################
    reset_queries()
    auth_times[i] = round(timer() - start, 7)

with open('user_search_100k.json', 'w') as f:
    json.dump(auth_times, f)
