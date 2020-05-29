
# Imports
from django.shortcuts import render, redirect, get_object_or_404
from timeit import default_timer as timer
from asclepiosapi import settings
from dn_model.models import Care_Team, Care_Team_Participants, Employee, Patient_Profile
import json, jwt, binascii
from datetime import datetime
from datetime import timedelta
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.Cipher import PKCS1_OAEP

keyPair = RSA.generate(4096)
pubKey = keyPair.publickey()

# Example Token
# This token may be require to change if signature expired error ocurs, just run a one-time team verification and copy the token from the print to here
auth_token = b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTA3MDU5MDIsIm5iZiI6MTU5MDYxNTkwMiwidXNlcl9pZCI6OTA4OTUsIm9yZ2FuaXphdGlvbl9pZCI6NDgsInRlYW1faWQiOjcxNTV9.1Do6ZfZIEt51042LwkbnbanP4T5ixSL6Or-7kNbnP4g'

# Example encrypted message
patient_info = {"name" : "John" , "surname" : "Sullivan"}
t_start = str(datetime.now())
encrypted_message = {
	'patient_info' : patient_info,
	't_start' : t_start,
}

### Encrypting message
encrypted_message = json.dumps(encrypted_message).encode('utf-8')
encryptor = PKCS1_OAEP.new(pubKey)
encrypted = encryptor.encrypt(encrypted_message)

# Example signed message
message_to_sign = {
    'auth' : auth_token.decode('utf-8'),
    'patient_info' : patient_info,
    't_start' : t_start
}

message_to_sign = json.dumps(message_to_sign).encode('utf-8')

digest = SHA256.new()
digest.update(message_to_sign)
signer = PKCS1_v1_5.new(keyPair)
signed_message = signer.sign(digest)

breakglass_validation_time = {}

SECRET_KEY = settings.SECRET_KEY

for i in range(100000):
    start = timer()

    # RA must verify the signature
    verifier = PKCS1_v1_5.new(pubKey)
    verified = verifier.verify(digest, signed_message)

    # Decrypt the message and the token, to retrieve the team and patient info
    decryptor = PKCS1_OAEP.new(keyPair)
    decrypted = decryptor.decrypt(encrypted)
    decoded = jwt.decode(auth_token, SECRET_KEY, algorithm='HS256')

    team = get_object_or_404(Care_Team, pk=decoded['team_id'])
    repr(team)

    # Verifies breakglass allowed
    if team.care_team_breakglass:    
        ##################  DO PATIENT SEARCH PATIENT INFO ############################
        pass

    breakglass_validation_time[i] = round(timer() - start, 7)

with open('breakglass_1k.json', 'w') as f:
    json.dump(breakglass_validation_time, f)