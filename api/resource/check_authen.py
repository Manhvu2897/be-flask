from flask_restful import Resource, abort
from flask import jsonify, request
from api.config import init_header, generate_token, BASE_URL_API
from api.auth_middleware import get_qc_secrets
import requests

class CheckAuthenResource(Resource):
    def get(self):
        qc_secrets = get_qc_secrets(request.headers.get('Authorization'))
        if qc_secrets is None:
            abort(500, error_message='Cannot get QC secrets!')
        response = requests.get(BASE_URL_API + '/authenticate', auth=(qc_secrets['qc_api_user_id'], generate_token(qc_secrets['qc_api_token'])), headers = init_header())
        return response.json()