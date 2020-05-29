from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.Cipher import PKCS1_OAEP
import binascii
import json
from timeit import default_timer as timer
from datetime import datetime

keyPair = RSA.generate(4096)

pubKey = keyPair.publickey()

#print(f"Public key:  (n={hex(pubKey.n)}, e={hex(pubKey.e)})")
#print(f"Private key: (n={hex(pubKey.n)}, d={hex(keyPair.d)})")

t_start = str(datetime.now())
auth_token = b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTAyODIwMjksIm5iZiI6MTU5MDI4MTEyOSwidXNlcl9pZCI6MTAxNzh9.8V0JHxu-eLpGau0HMV3Hz28M5yVhOo3n7Qp2qsizau8'
patient_id = 123456
team_id = 654321
user_id = 654123

enc_and_sign_time = {}

for i in range(100000):
	start = timer()

	# Example encrypt message
	message = {
		'request' : "Breakglass",
		'patient_id' : patient_id,
		'team_id' : team_id,
		'user_id' : user_id,
		't_start' : t_start
	}

	message = json.dumps(message).encode('utf-8')
	encryptor = PKCS1_OAEP.new(pubKey)
	encrypted = encryptor.encrypt(message)

	# Example sign message
	message_to_sign = {
		'request' : "Breakglass",
		'patient_id' : patient_id,
		'team_id' : team_id,
		'user_id' : user_id,
		't_start' : t_start

	}

	message = json.dumps(message_to_sign).encode('utf-8')
	digest = SHA256.new()
	digest.update(message)

	signer = PKCS1_v1_5.new(keyPair)
	sig = signer.sign(digest)

	enc_and_sign_time[i] = round(timer() - start, 7)

with open('m3_100k.json', 'w') as f:
    json.dump(enc_and_sign_time, f)