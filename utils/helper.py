import random
import string

import jwt


def random_string(stringLength=32):
    letters = ''.join([string.ascii_lowercase, string.ascii_uppercase, string.digits])
    return ''.join(random.choice(letters) for i in range(stringLength))


def get_user_uuid(token):
    with open('resources/public.pem') as reader:
        public_key = reader.read()
    try:
        decoded = jwt.decode(token, public_key, algorithms=["RS256"])
        # decoded = jwt.decode(token, public_key, algorithms=["RS256"], options={"verify_signature": False})
        return decoded['uuid']
    except:
        return ''
