import time
from django.shortcuts import render, redirect, get_object_or_404

# Constants

# Patients that has an account inside our application without any record
PATIENTS_WITHOUT_RECORDS_NUMBER = 150000

# Organizations, call centre, ambulance & hospitals
CALL_CENTRE_ORG_NUMBER = 1 
AMBULANCE_ORG_NUMBER = 2
HOSPITAL_ORG_NUMBER = 7

ORGANIZATION_TEAMS_NUMBER = 100
EMPLOYEES_PER_ORG_NUMBER = 5000


class Generate_Script:

    def __init__(self):
        self.gender = ['male', 'female']

        self.hospitals = [('VU medisch centrum','VUMC'), ('Academisch Medisch Centrum', 'AMC'), ('Universitair Medisch Centrum Groningen', 'UMCG'), ('Universitair Medisch Centrum Utrecht', 'UMCU'), ('Leids Universitair Medisch Centrum', 'LUMC'),
        ('Maastricht Universitair Medisch Centrum', 'MUMC+'), ('Erasmus MC', 'EMC'), ('Sint Lucas Andreas Ziekenhuis', '')]
        self.ambulances = [('Ambulancezorg Nederland', 'AN'), ('UMCG Ambulancezorg', 'UMCGA'),]
        self.call_centre = [('Emergency Call Centre', 'ECC')]


    # Help functions
    def generate_bsn(self):
        import random
        return random.randint(100000000,999999999)

    def generate_salt(self):
        import random
        return random.randint(10000000,99999999)

    def generate_age(self, age=0):
        import random
        year = 2020 - age
        month = str(random.randint(1,12))
        day = str(random.randint(1,28))
        if len(month) == 1:
            month = "0{}".format(month)
        if len(day) == 1:
            day = "0{}".format(day)

        response = "{}-{}-{}".format(year, month, day)
        return response
    
    def generate_allergy_int_record(self):
        pass
    
    def generate_condition_record(self):
        pass
    
    def generate_family_member_history_record(self):
        pass

    def generate_patients(self, pn=0, records=False, allergies_n=0, conditions_n=0, fmh_n=0):
        from db_model.models import Patient_Profile, User   
        import random, names
        from datetime import datetime
        from faker import Faker
        fake = Faker('nl_NL')

        if records:
            print("     - patients with records")
        else:
            print("     - patients without records")

        for i in range(pn):
            first_name = names.get_first_name()
            last_name = names.get_last_name()
            salt = self.generate_salt()

            user_pat = User.objects.create_user(first_name+last_name+str(salt), first_name+last_name+"@protonmail.com", "pwd123")
            user_pat.first_name = first_name
            user_pat.last_name = last_name
            user_pat.user_type = 1
            user_pat.save()

            patient = Patient_Profile.objects.create(user=user_pat, patient_active=True, patient_name=first_name, patient_surname=last_name,
            patient_BSN=self.generate_bsn(), patient_birthDate=self.generate_age(random.randint(1,60)), patient_gender=random.choice(self.gender),
            patient_zipcode=fake.address().split("\n")[1], patient_address=fake.address().split("\n")[0])
            #print("Patient {} created".format(first_name+" "+last_name))

        
    def generate_organizations(self, pn=0, org_type=None, teams_number=0, employees_number=0):
        from django.shortcuts import render, redirect, get_object_or_404
        from db_model.models import User, Organization, Care_Team, Employee, Care_Team_Participants
        import names, random
        from datetime import datetime
        from faker import Faker
        fake = Faker('nl_NL')

        if org_type == "Hospital":
            print("     - hospitals")
            org = self.hospitals.pop()
            org_name = org[0]
            org_alias = org[1]
            org_type = 4
        elif org_type == "Ambulance":
            print("     - ambulances")
            org = self.ambulances.pop()
            org_name = org[0]
            org_alias = org[1]
            org_type = 2
        elif org_type == "Call Centre":
            print("     - call centre")
            org = self.call_centre.pop()
            org_name = org[0]
            org_alias = org[1]
            org_type = 3
        else:
            return print("Organization type must be Hospital, Ambulance or Call Centre")
        
        username = org_name.replace(" ",'').lower()
        user_org = User.objects.create_user(username, username+"@org.com", "pwd123")
        user_org.first_name = org_name
        user_org.last_name = ""
        user_org.user_type = 5
        user_org.save()

        org = Organization.objects.create(user=user_org, organization_active=True, organization_type=org_type, 
        organization_name=org_name, organization_alias=org_alias, organization_zipcode=fake.address().split("\n")[1],
        organization_address=fake.address().split("\n")[0], organization_country="The Netherlands", organization_telecom=fake.phone_number())

        print("     --- creating teams for organization")
        for i in range(0, teams_number):
            Care_Team.objects.create(care_team_organization=org, care_team_name="Emergency Team {}".format(i),
                care_team_tag="ET-{}".format(i), care_team_is_active=True, care_team_category="Emergency",
                care_team_start_datetime=datetime.now(), care_team_note=fake.sentence(nb_words=5))
        
        for i in range(0, employees_number):
            first_name = names.get_first_name()
            last_name = names.get_last_name()
            salt = self.generate_salt()

            user_emp = User.objects.create_user(first_name+last_name+str(salt), "employee@example.com", "pwd123")
            user_emp.first_name = first_name
            user_emp.first_name = last_name
            user_emp.user_type = 3
            user_emp.save()

            emp = Employee.objects.create(user=user_emp, employee_org=org, employee_name=first_name, employee_surname=last_name,
                employee_BSN=self.generate_bsn(), employee_email="employee@example.com", employee_role="", employee_department="")
            
            care_team = Care_Team.objects.filter(care_team_organization=org)[0]
            participant_team = Care_Team_Participants.objects.create(care_team_id=care_team, participant_id=emp, added_date=datetime.now())
        

# This only happens when module is called directly
print("\nStarting Generate Script")
print("\n * loading generate scrip")
time.sleep(1)
gs = Generate_Script()

print("\n * generating organizations")
time.sleep(1)
gs.generate_organizations(pn=HOSPITAL_ORG_NUMBER, org_type="Hospital", teams_number=ORGANIZATION_TEAMS_NUMBER, employees_number=EMPLOYEES_PER_ORG_NUMBER)
gs.generate_organizations(pn=AMBULANCE_ORG_NUMBER, org_type="Ambulance", teams_number=ORGANIZATION_TEAMS_NUMBER, employees_number=EMPLOYEES_PER_ORG_NUMBER)
gs.generate_organizations(pn=CALL_CENTRE_ORG_NUMBER, org_type="Call Centre", teams_number=ORGANIZATION_TEAMS_NUMBER, employees_number=EMPLOYEES_PER_ORG_NUMBER)

print("\n * generating patients")
time.sleep(1)
gs.generate_patients(pn=PATIENTS_WITHOUT_RECORDS_NUMBER, records=False)
print()