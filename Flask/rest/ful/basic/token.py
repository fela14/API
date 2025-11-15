# To create tk

import requests
import base64

client_id = "e94b1fd84d9a48b490ce9b1e0cf6784f"
client_secret = ""

# Encode credentials
auth = f"{client_id}:{client_secret}"
encoded_auth = base64.b64encode(auth.encode()).decode()

# Request token
response = requests.post(
    "https://accounts.spotify.com/api/token",
    headers={"Authorization": f"Basic {encoded_auth}"},
    data={"grant_type": "client_credentials"}
)

token = response.json()["access_token"]
print("Access Token:", token)
