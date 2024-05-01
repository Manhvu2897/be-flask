from flask_restful import request
from api.config import supabase
def token_required():
    try:
        if request.method != 'OPTIONS':
            token = None
            token_user = supabase.auth.sign_in_with_password({"email": "duong.ngo@tradersrescue.com", "password": "cobau12a10ht"})
            print('token_______', token_user)
            if "Authorization" in request.headers:
                token = request.headers["Authorization"].split(" ")[1]
            if not token:
                return {
                    "message": "Authentication Token is missing!",
                    "error": "Unauthorized"
                }, 401
            user_by_token = supabase.auth.get_user(token).model_dump_json()
            if user_by_token is None:
                return {
                    "message": "Invalid Authentication token!",
                    "error": "Unauthorized"
                }, 401
    except Exception as e:
        return "401 Unauthorized\n{}\n\n".format(e), 401

def split_authorization_header(authorization_header):
    """Splits an Authorization header into the authorization scheme and credentials.

    Args:
    authorization_header: The Authorization header to split.

    Returns:
    A tuple of the authorization scheme and credentials.
    """

    parts = authorization_header.split()
    if len(parts) != 2:
        raise ValueError('Invalid Authorization header')

    return parts[0], parts[1]

def get_qc_secrets(authorization_header) -> dict:
    schema, credentials = split_authorization_header(authorization_header)
    qc_secrets = {
        'qc_api_token': '',
        'qc_api_user_id': ''
    }
    user = supabase.auth.get_user(credentials)
    data_user_json = user.model_dump()
    if data_user_json is not None:
        try:
            data = supabase.table('decrypted_qc_secrets').select('*').eq('user_id', "75eae08c-dc21-4118-8fd7-087396260fb9").execute()
            if data:
                qc_secrets['qc_api_token'] = data.data[0]['decrypted_qc_api_token']
                qc_secrets['qc_api_user_id'] = data.data[0]['decrypted_qc_api_user_id']
                return qc_secrets
        except Exception as e:
            return None
