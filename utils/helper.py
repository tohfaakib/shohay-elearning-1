import random
import string
import requests


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


# def get_access_token():
#     url = 'https://www.googleapis.com/oauth2/v4/token%20code=4/0AX4XfWirAf4Llj-nTWg9G5Qjt_L6MykUJKl5cEbqXl59tJF2XXcHE263HgrYE2vWN4iuFw&redirect_uri=https%3A%2F%2Fdevelopers.google.com%2Foauthplayground&client_id=1040181526072-vglso30oqj92ubg63mttjqh5uhm0abg5.apps.googleusercontent.com&client_secret=tuVVoUEQodSCl-9NLA2alW1V&scope=&grant_type=authorization_code'
#     data = {
#         'Content-length': '233',
#         'content-type': 'application/x-www-form-urlencoded',
#         'user-agent': 'google-oauth-playground',
#     }
#     res = requests.post(url, json=data)
#
#     print(res.text)
#     print(res.status_code)
#
# get_access_token()