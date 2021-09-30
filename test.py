import requests


def google_get_access_token(code, redirect_uri):
    # Reference: https://developers.google.com/identity/protocols/oauth2/web-server#obtainingaccesstokens
    data = {
        'code': code,
        'client_id': '1040181526072-vglso30oqj92ubg63mttjqh5uhm0abg5.apps.googleusercontent.com',
        'client_secret': 'tuVVoUEQodSCl-9NLA2alW1V',
        'grant': 'code',
        'redirect_uri': '',
        'grant_type': 'authorization_code'
    }

    response = requests.post('https://www.googleapis.com/oauth2/v4/token', data=data)

    if not response.ok:
        print('Failed to obtain access token from Google.')

    # access_token = response.json()['access_token']
    print(response.status_code)
    access_token = response.text

    return access_token


# print(google_get_access_token('4/0AX4XfWgOMPxaDXbml3wxQGYFeh3EwQXGmsVMfVEE0FbcIM-L0_L5vz9AcL9lcchUFk7eCA', ''))


# client = Signet::OAuth2::Client.new(
#   authorization_uri: 'https://accounts.google.com/o/oauth2/v2/auth',
#   token_credential_uri:  'https://www.googleapis.com/oauth2/v4/token',
#   client_id: 'my client id',
#   client_secret: 'my client secret',
#   grant_type: 'authorization_code',
#   code: 'my code',
#   redirect_uri: 'my redirect uri'
# )
#
# client.fetch_access_token


from google.oauth2 import id_token
from google.auth.transport import requests

# (Receive token by HTTPS POST)
# ...

# try:
# Specify the CLIENT_ID of the app that accesses the backend:
idinfo = id_token.verify_oauth2_token("eyJhbGciOiJSUzI1NiIsImtpZCI6IjQ2Mjk0OTE3NGYxZWVkZjRmOWY5NDM0ODc3YmU0ODNiMzI0MTQwZjUiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIxMDQwMTgxNTI2MDcyLWs1bmttdnQxc2tmZDExcTNpdTBqZnB0aWtpOGlqYW90LmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiMTA0MDE4MTUyNjA3Mi12Z2xzbzMwb3FqOTJ1Ymc2M210dGpxaDV1aG0wYWJnNS5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsInN1YiI6IjExNjY0MDM3MTM0Njk2NTY0ODU2OCIsImVtYWlsIjoiYWJpcmhhc2Fuem9oYUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibmFtZSI6IkFCSVIgSEFTQU4gWk9IQSIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS0vQU9oMTRHakJ1c05Ja0w0ekF6SVI3WExKeUdaVnBkTUhoT1JvZmZhQ3BIaklaaUE9czk2LWMiLCJnaXZlbl9uYW1lIjoiQUJJUiBIQVNBTiIsImZhbWlseV9uYW1lIjoiWk9IQSIsImxvY2FsZSI6ImVuIiwiaWF0IjoxNjI4NzY2NTc3LCJleHAiOjE2Mjg3NzAxNzd9.uuusUAH_bQMUvGu7UjZjc-MSfGtTrSXA4YrmbOXJYSCcAEZN30XmEC7SibUpsGsRh3DWXNkX383oIygqM3E0IbXCMHV38mKNxVehBH5UWOguKIOM71zwJt7iYbm0aji413bbCp4u_Xvf6xMTIlDaqundbQs2Ijs-Obu3tSPGghb5wfYJN48jfpXRLtVBCEHyyDCTNAW6Y_Lm6qQv8mdcRsiJRMbBhafBxsIImlwUDvMawDRuj242jbITP7WZo0qUQ0Lg0ATB0e_A-Q4T_Gz3i2nW5GR42j6uJL9sh-Sg2KZUbKfcNwbq__VfsEt5rCawsuAozRueOB6w4zMhuME5pA", requests.Request(), '1040181526072-vglso30oqj92ubg63mttjqh5uhm0abg5.apps.googleusercontent.com')

# Or, if multiple clients access the backend server:
# idinfo = id_token.verify_oauth2_token(token, requests.Request())
# if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
#     raise ValueError('Could not verify audience.')

# If auth request is from a G Suite domain:
# if idinfo['hd'] != GSUITE_DOMAIN_NAME:
#     raise ValueError('Wrong hosted domain.')

# ID token is valid. Get the user's Google Account ID from the decoded token.
userid = idinfo['sub']
print(idinfo)
# except ValueError:
#     # Invalid token
#     pass