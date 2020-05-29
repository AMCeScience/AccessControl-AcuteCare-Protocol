from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.Cipher import PKCS1_OAEP
import binascii, json
from timeit import default_timer as timer
from datetime import datetime

keyPair = RSA.generate(4096)

pubKey = keyPair.publickey()

#print(f"Public key:  (n={hex(pubKey.n)}, e={hex(pubKey.e)})")
#print(f"Private key: (n={hex(pubKey.n)}, d={hex(keyPair.d)})")

t_end = str(datetime.now())
auth_token = b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTAyODIwMjksIm5iZiI6MTU5MDI4MTEyOSwidXNlcl9pZCI6MTAxNzh9.8V0JHxu-eLpGau0HMV3Hz28M5yVhOo3n7Qp2qsizau8'
team_id = 1000001
patient_id = 1000000

enc_and_sign_time = {}

for i in range(100000):
	start = timer()

	message = {
		'patient_id' : patient_id,
		'request' : "EndSession"
	}

	message = json.dumps(message).encode('utf-8')
	encryptor = PKCS1_OAEP.new(pubKey)
	encrypted = encryptor.encrypt(message)

	# Example sign message
	message_to_sign = {
		'auth_token' : auth_token.decode('utf-8'),
		'request' : "JoinTeam",
		'patient_id' : patient_id,

	}

	message = json.dumps(message_to_sign).encode('utf-8')
	digest = SHA256.new()
	digest.update(message)

	signer = PKCS1_v1_5.new(keyPair)
	sig = signer.sign(digest)

	enc_and_sign_time[i] = round(timer() - start, 7)

with open('m13_100k.json', 'w') as f:
    json.dump(enc_and_sign_time, f)