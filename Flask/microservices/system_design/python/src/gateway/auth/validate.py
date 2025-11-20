import os
import requests

def token(request):
    # Safely get the Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return None, ("missing credentials", 401)

    try:
        response = requests.post(
            f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/validate",
            headers={"Authorization": auth_header},
        )
    except requests.RequestException as e:
        return None, (str(e), 500)

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)
