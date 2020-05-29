# Imports
from db_model.models import Care_Team_Participants
from django.contrib.auth import authenticate, login as auth_login
from timeit import default_timer as timer
from asclepiosapi import settings
import json, datetime, jwt

team_verification_times = {}

SECRET_KEY = settings.SECRET_KEY

# User example to search the stroke team
username = "anne"
password = "pwd123"
user = authenticate(username=username, password=password)

for i in range(100000):
    start = timer()

    # Team search
    employee = user.employee
    team = Care_Team_Participants.objects.filter(participant_id=employee)
    repr(team)
    team = team[0].care_team_id

    # Authorization token
    HEADERS = {	
		'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=90000),
		'nbf': datetime.datetime.utcnow(),
		'user_id' : user.pk,
		'team_id' : team.pk,
	}
    enconded_token = jwt.encode(HEADERS, SECRET_KEY, algorithm='HS256')
    #print(enconded_token)

    ########## HEALTHCARE PROFESSIONAL NOW CAN DO THE BREAKGLASS REQUEST############

    team_verification_times[i] = round(timer() - start, 7)

with open('time_100k.json', 'w') as f:
    json.dump(team_verification_times, f)