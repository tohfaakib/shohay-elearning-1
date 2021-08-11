import random
import string


def random_string(stringLength=32):
    letters = ''.join([string.ascii_lowercase, string.ascii_uppercase, string.digits])
    return ''.join(random.choice(letters) for i in range(stringLength))


def bd_phone_validator(phone):
    phone = str(phone)
    phone = phone.replace(' ', '').replace('\n', '').replace('\t', '').replace('-', '')
    if len(phone) < 11 or len(phone) > 15:
        return False

    first_part = phone[:-9]
    if first_part == '01' or first_part == '+8801' or first_part == '8801' or first_part == '008801':
        return True

    return False

