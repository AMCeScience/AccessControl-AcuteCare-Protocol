from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    USER_TYPE_CHOICES = (
      (1, 'patient'),
      (2, 'ambulance'),
      (3, 'call_centre'),
      (4, 'hospital'),
      (5, 'org_admin'),
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, null=True, default=USER_TYPE_CHOICES[0][0]) 

##############################################################################
############# Patient Profile following FHIR
class Patient_Profile(models.Model):
    PAT_GENDER = (
        ('unknown', 'Unknown'),
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

    PAT_MARITAL = (
        ('UNK', 'Unknown'),
        ('M', 'Married'),
        ('S', 'Never Married'),
        ('D', 'Divorced'),
        ('A', 'Annulled'),
        ('W', 'Widowed'),
        ('U', 'Unmarried'),
        ('T', 'Domestic partner'),
        ('P', 'Polygamous'),
        ('I', 'Interlocutory'),
        ('L', 'Legally Separated')
    )

    PAT_RELATIONSHIP = (
        ('U', 'Unknown'),
        ('C', 'Emergency Contact'),
        ('E', 'Employer'),
        ('F', 'Federal Agency'),
        ('I', 'Insurance Company'),
        ('N', 'Next-of-Kin'),
        ('S', 'State Agency'),
    )

    PAT_LANGUAGE = (
        ('en', 'English'),
        ('ar', 'Arabic'),
        ('bn', 'Bengali'),
        ('cs', 'Czech'),
        ('da', 'Danish'),
        ('de','German'),
        ('de-AT', 'German (Austria)'),
        ('de-CH','German (Switzerland'),
        ('de-DE','German (Germany'),
        ('el', 'Greek'),
        ('en-AU', 'English (Australia)'),
        ('en-CA', 'English (Canada)'),
        ('en-GB', 'English (Great Britain)'),	
        ('en-IN', 'English (India)'),
        ('en-NZ', 'English (New Zeland)'),
        ('en-SG', 'English (Singapore)'),
        ('en-US', 'English (United States)'),
        ('es', 'Spanish'),
        ('es-AR', 'Spanish (Argentina)'),
        ('es-ES', 'Spanish (Spain)'),
        ('es-UY', 'Spanish (Uruguay)'),
        ('fi', 'Finnish'),
        ('fr', 'French'),
        ('fr-BE', 'French (Belgium)'),
        ('fr-CH', 'French (Switzerland)'),
        ('fr-FR', 'French (France)'),
        ('fy', 'Frysian'),
        ('fy-NL', 'Frysian (Netherlands)'),
        ('hi', 'Hindi'),
        ('hr', 'Croatian'),	
        ('it', 'Italian'),
        ('it-CH', 'Italian (Switzerland)'),
        ('it-IT', 'Italian (Italy)'),
        ('ja', 'Japanese'),
        ('ko', 'Korean'),
        ('nl', 'Dutch'),
        ('nl-BE', 'Dutch (Belgium)'),
        ('nl-NL', 'Dutch (Netherlands)'),
        ('no', 'Norwegian'),
        ('no-NO', 'Norwegian (Norway)'),
        ('pa', 'Punjabi'),
        ('pl', 'Polish'),
        ('pt', 'Portuguese'),
        ('pt-BR', 'Portuguese (Brazil)'),
        ('ru', 'Russian'),
        ('ru-RU', 'Russian (Russia)'),
        ('sr', 'Serbian'),
        ('sr-RS', 'Serbian (Serbia)'),
        ('sv', 'Swedish'),
        ('sv-SE', 'Swedish (Sweden)'),
        ('te', 'Telegu'),
        ('zh', 'Chinese'),
        ('zh-CN', 'Chinese (China)'),
        ('zh-HK', 'Chinese (Hong Kong)'),
        ('zh-SG', 'Chinese (Singapore)'),
        ('zh-TW', 'Chinese (Taiwan)'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    identifier = models.IntegerField(null=True, unique=True)
    patient_active = models.BooleanField("Active", null=True, default=False)
    patient_name = models.CharField("Name", null=True, max_length=32, blank=True)
    patient_surname = models.CharField("Surname", null=True, max_length=32, blank=True)
    patient_BSN = models.IntegerField("BSN", null=True, blank=True)
    patient_telecom =models.CharField("Phone Number", null=True, max_length=32, blank=True)
    patient_gender = models.CharField("Gender", max_length=20, choices=PAT_GENDER, default=PAT_GENDER[0][0], null=True, blank=True)
    patient_birthDate = models.DateField("Birth Date", null=True, blank=True)
    patient_address = models.CharField("Address", null=True, max_length=32, blank=True)
    patient_zipcode = models.CharField("Zip Code", null=True, max_length=32, blank=True)
    patient_maritalStatus = models.CharField("Marital Status", max_length=10, choices=PAT_MARITAL, default=PAT_MARITAL[0][0], blank=True)
    patient_photo = models.ImageField("Profile Picture", upload_to='patient_pic', blank=True, null=True)
    patient_communication_language = models.CharField("Communication Language", max_length=10, choices=PAT_LANGUAGE, default=PAT_LANGUAGE[0][0], null=True, blank=True)

    # Contact Informations
    patient_contact_name = models.CharField("Name", null=True, max_length=200)
    patient_contact_relationship = models.CharField("Relationship",max_length=20, choices=PAT_RELATIONSHIP, default=PAT_RELATIONSHIP[0][0], null=True)
    patient_contact_telecom = models.CharField("Phone Number", null=True, max_length=200)
    patient_contact_zipcode = models.CharField("Zip Code", null=True, max_length=50, blank=True)
    patient_contact_address = models.CharField("Address", null=True, max_length=200)
    patient_contact_gender = models.CharField("Gender", max_length=20, choices=PAT_GENDER, default=PAT_GENDER[0][0], null=True)
    patient_lasttime_updated = models.DateTimeField("Last Time Updated", null=True)


########################################################################################################
########################################################################################################
class Organization(models.Model):
    ORG_TYPE_CHOICES = (
        (1, 'Unspecified'),
        (2, 'Ambulance Service'),
        (3, 'Call Centre Service'),
        (4, 'Hospital Service'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    identifier = models.IntegerField(null=True, unique=True)
    organization_active = models.BooleanField(null=True)
    organization_type = models.PositiveSmallIntegerField(choices=ORG_TYPE_CHOICES, null=True, default=ORG_TYPE_CHOICES[0][0])
    organization_name = models.CharField(null=True, max_length=32)
    organization_alias = models.CharField(null=True, max_length=32)
    organization_telecom = models.CharField(null=True, max_length=32)
    organization_zipcode = models.CharField(null=True, max_length=32)
    organization_address = models.CharField(null=True, max_length=32)
    organization_country = models.CharField(null=True, max_length=32)
    organization_city = models.CharField(null=True, max_length=32)

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    identifier = models.IntegerField(unique=True, null=True)
    employee_org = models.ForeignKey(Organization, on_delete=models.CASCADE)
    employee_type = models.PositiveSmallIntegerField(null=True)
    employee_name = models.CharField(null=True, max_length=32)
    employee_surname = models.CharField(null=True, max_length=32)
    employee_BSN = models.CharField(null=True, max_length=16)
    employee_email = models.EmailField(null=True, max_length=32)
    employee_role = models.CharField(null=True, max_length=32)
    employee_department = models.CharField(null=True, max_length=32)

class Care_Team(models.Model):
    care_team_organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    identifier = models.IntegerField(null=True, unique=True)
    care_team_name = models.CharField(null=True, max_length=32)
    care_team_tag = models.CharField(null=True, max_length=32, default="")
    care_team_is_active = models.BooleanField(null=True)
    care_team_category = models.CharField(null=True, max_length=100)
    care_team_start_datetime = models.DateTimeField(null=True)
    care_team_end_datetime = models.DateTimeField(null=True)
    care_team_reason_code = models.IntegerField(null=True)
    care_team_telecom = models.IntegerField(null=True)
    care_team_note = models.CharField(null=True, max_length=100)
    care_team_current_location = models.CharField(null=True, max_length=32)
    care_team_time_to_revoke = models.IntegerField(null=True, default=True)
    care_team_breakglass = models.BooleanField(null=True, default=True)

# Relationship who is participating in each care team
class Care_Team_Participants(models.Model):
    care_team_id = models.ForeignKey(Care_Team, on_delete=models.CASCADE, related_name="care")
    participant_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    participant_role = models.CharField(null=True, max_length=100)
    care_team_responsible = models.BooleanField(null=True)
    participating = models.BooleanField(null=True)
    added_date = models.DateTimeField(null=True)