import requests, json
from flask import request, jsonify
from flask_restful import Resource, abort
from api.config import init_header, generate_token, BASE_URL_API
from api.auth_middleware import get_qc_secrets

class ReadNodeProject(Resource):
    def post(self):
        data_from_client = json.loads(request.data.decode())
        data = {
            "projectId": data_from_client["projectId"]
        }
        qc_secrets = get_qc_secrets(request.headers.get('Authorization'))
        if qc_secrets is None:
            abort(500, error_message='Cannot get QC secrets!')
        response = requests.post(BASE_URL_API + "/projects/nodes/read", auth=(qc_secrets['qc_api_user_id'], generate_token(qc_secrets['qc_api_token'])), data=data, headers = init_header())
        return jsonify({ "response": response.json() })