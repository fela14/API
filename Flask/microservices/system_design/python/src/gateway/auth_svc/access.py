import os
import requests

def login(request):
    """
    Calls the auth service /login endpoint.

    Returns:
        tuple: (response_text, None) if successful, else (None, (msg, status_code))
    """
    # Get Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return None, ("missing credentials", 401)

    # Call auth service
    try:
        response = requests.post(
            f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/login",
            headers={"Authorization": auth_header},
            json=request.get_json(silent=True)  # send JSON if present
        )
    except requests.RequestException as e:
        return None, (f"auth service error: {str(e)}", 500)

    # Check response
    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)
