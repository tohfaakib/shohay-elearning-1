import random
import string


def random_string(stringLength=32):
    letters = ''.join([string.ascii_lowercase, string.ascii_uppercase, string.digits])
    return ''.join(random.choice(letters) for i in range(stringLength))
