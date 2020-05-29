from db_model.models import Patient_Profile
from django.shortcuts import get_object_or_404
from timeit import default_timer as timer
import json

time_verification = {}
patient_name = "John"
patient_surname = "Sullivan"


for i in range(100000):
    start = timer()

    patient = Patient_Profile.objects.filter(patient_name=patient_name, patient_surname=patient_surname)
    repr(patient)
    patient_id = patient[0].pk

    time_verification[i] = round(timer() - start, 7)

with open('patient_identification_100k.json', 'w') as f:
    json.dump(time_verification, f)