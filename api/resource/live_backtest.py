import requests, json
from flask import request, jsonify
from flask_restful import Resource, abort
from api.auth_middleware import get_qc_secrets
from api.config import init_header, generate_token, BASE_URL_API
from api.supabase_dashboard import SupabaseDashboard

# Read algo statistics by deployId
class ReadAlgoStatistics(Resource):
    def post(self):
        data_from_client = json.loads(request.data.decode())
        data = {
            "projectId": data_from_client["projectId"],
            "deployId": data_from_client["deployId"],
            "start": 0,
            "end": 1
        }
        qc_secrets = get_qc_secrets(request.headers.get('Authorization'))
        if qc_secrets is None:
            abort(500, error_message='Cannot get QC secrets!')
        response = requests.post(BASE_URL_API + "/live/read", auth=(qc_secrets['qc_api_user_id'], generate_token(qc_secrets['qc_api_token'])), json=data, headers = init_header())
        return jsonify({ "response": response.json() })

# Read live log by algorithmId
class ReadLog(Resource):
    def post(self):
        data_from_client = json.loads(request.data.decode())
        data = {
            "format": "json",
            "projectId": data_from_client["projectId"],
            "algorithmId": data_from_client["algorithmId"]
        }
        if data_from_client["start"]:
            data["start"] = data_from_client["start"]
        if data_from_client["end"]:
            data["end"] = data_from_client["end"]
        qc_secrets = get_qc_secrets(request.headers.get('Authorization'))
        if qc_secrets is None:
            abort(500, error_message='Cannot get QC secrets!')
        response = requests.post(BASE_URL_API + "/live/read/log", auth=(qc_secrets['qc_api_user_id'], generate_token(qc_secrets['qc_api_token'])), json=data, headers = init_header())
        return jsonify({ "response": response.json() })

# Read porfolio state
class ReadPorfolioState(Resource):
    def post(self):
        data_from_client = json.loads(request.data.decode())
        data = {
            "projectId": data_from_client["projectId"]
        }
        qc_secrets = get_qc_secrets(request.headers.get('Authorization'))
        if qc_secrets is None:
            abort(500, error_message='Cannot get QC secrets!')
        response = requests.post(BASE_URL_API + "/live/read/portfolio", auth=(qc_secrets['qc_api_user_id'], generate_token(qc_secrets['qc_api_token'])), json=data, headers = init_header())
        return jsonify({ "response": response.json() })

# Read orders
class ReadOrders(Resource):
    def post(self):
        data_from_client = json.loads(request.data.decode())
        data = {
            "projectId": data_from_client["projectId"],
            # Starting index of the orders to be fetched. Required if end > 100.
            "start": data_from_client["start"],
            # Last index of the orders to be fetched. Note that end - start must be less than 100.
            "end": data_from_client["end"],
        }
        qc_secrets = get_qc_secrets(request.headers.get('Authorization'))
        if qc_secrets is None:
            abort(500, error_message='Cannot get QC secrets!')
        response = requests.post(BASE_URL_API + "/live/read/orders", auth=(qc_secrets['qc_api_user_id'], generate_token(qc_secrets['qc_api_token'])), json=data, headers = init_header())
        return jsonify({ "response": response.json() })

# Read insights
class ReadInsights(Resource):
    def post(self):
        data_from_client = json.loads(request.data.decode())
        data = {
            "projectId": data_from_client["projectId"],
            # Starting index of the orders to be fetched. Required if end > 100.
            "start": data_from_client["start"],
            # Last index of the orders to be fetched. Note that end - start must be less than 100.
            "end": data_from_client["end"],
        }
        qc_secrets = get_qc_secrets(request.headers.get('Authorization'))
        if qc_secrets is None:
            abort(500, error_message='Cannot get QC secrets!')
        response = requests.post(BASE_URL_API + "/live/read/insights", auth=(qc_secrets['qc_api_user_id'], generate_token(qc_secrets['qc_api_token'])), json=data, headers = init_header())
        return jsonify({ "response": response.json() })

# List live algorthms by status
class ListLiveAlgorithms(Resource):
    def post(self):
        data_from_client = json.loads(request.data.decode())
        data = {
            "status": data_from_client["status"]
        }
        if data_from_client["start"]:
            data["start"] = data_from_client["start"]
        if data_from_client["end"]:
            data["end"] = data_from_client["end"]
        qc_secrets = get_qc_secrets(request.headers.get('Authorization'))
        if qc_secrets is None:
            abort(500, error_message='Cannot get QC secrets!')
        response = requests.post(BASE_URL_API + "/live/read", auth=(qc_secrets['qc_api_user_id'], generate_token(qc_secrets['qc_api_token'])), json=data, headers = init_header())
        return jsonify({ "response": response.json() })

class CreateLiveAlgo(Resource):
    def post(self):
        data_from_client = json.loads(request.data.decode())
        data = {
            "versionId": "-1",
            "projectId": data_from_client["projectId"],
            "compileId": data_from_client["compileId"],
            "nodeId": data_from_client["nodeId"]
        }
        data["brokerage"] = {
            "id": "Default",
            "user": "",
            "password": "",
            "environment": "paper",
            "account": ""
        }
        qc_secrets = get_qc_secrets(request.headers.get('Authorization'))
        if qc_secrets is None:
            abort(500, error_message='Cannot get QC secrets!')
        response = requests.post(BASE_URL_API + "/live/create", auth=(qc_secrets['qc_api_user_id'], generate_token(qc_secrets['qc_api_token'])), json=data_from_client, headers = init_header())
        return jsonify({ "response": response.json() })
    
class StartLiveAlgorithm(Resource):
    def post(self):
        # TODO: send info strategy into QC, query by strategyId later
        data_from_client: dict = json.loads(request.data.decode())
        # get compile Id
        data_create_compileId = {
            "projectId": 15770834
        }
        qc_secrets = get_qc_secrets(request.headers.get('Authorization'))
        if qc_secrets is None:
            abort(500, error_message='Cannot get QC secrets!')
        response_compile = requests.post(BASE_URL_API + "/compile/create", json=data_create_compileId, auth=(qc_secrets['qc_api_user_id'], generate_token(qc_secrets['qc_api_token'])), headers = init_header())
        response_compile_json = response_compile.json()
        data = {
            "versionId": "-1",
            "projectId": 15770834,
            "compileId": response_compile_json["compileId"],
            "nodeId": "LN-a71c40b5bb6258ef6cc1d37369da2f33"
        }
        data["brokerage"] = {
            "id": "Default",
            "user": "",
            "password": "",
            "environment": "paper",
            "account": ""
        }
        response = requests.post(BASE_URL_API + "/live/create", auth=(qc_secrets['qc_api_user_id'], generate_token(qc_secrets['qc_api_token'])), json=data, headers = init_header())
        response_json: dict = response.json()
        if response.status_code == 200 and response_json['success'] == True:
            response_from_supabase = SupabaseDashboard.update('strategy_settings', {'is_started': True}, 'id', data_from_client.get('strategyId'))
            print('response_from_supabase', response_from_supabase)
            response_json["isStarted"] = True
        return jsonify({ "response": response_json })
    
# Liquidate algorithm
class LiquidateAlgorithm(Resource):
    def post(self):
        data_from_client = json.loads(request.data.decode())
        data = {
            "projectId": data_from_client["projectId"]
        }
        qc_secrets = get_qc_secrets(request.headers.get('Authorization'))
        if qc_secrets is None:
            abort(500, error_message='Cannot get QC secrets!')
        response = requests.post(BASE_URL_API + "/live/update/liquidate", auth=(qc_secrets['qc_api_user_id'], generate_token(qc_secrets['qc_api_token'])), json=data, headers = init_header())
        return jsonify({ "response": response.json() })
    
# Stop live algorithm
class StopAlgorithm(Resource):
    def post(self):
        data_from_client = json.loads(request.data.decode())
        data = {
            "projectId": data_from_client["projectId"]
        }
        qc_secrets = get_qc_secrets(request.headers.get('Authorization'))
        if qc_secrets is None:
            abort(500, error_message='Cannot get QC secrets!')
        response = requests.post(BASE_URL_API + "/live/update/stop", auth=(qc_secrets['qc_api_user_id'], generate_token(qc_secrets['qc_api_token'])), json=data, headers = init_header())
        return jsonify({ "response": response.json() })
    
class StopLiveAlgorithm(Resource):
    def post(self):
        data_from_client: dict = json.loads(request.data.decode())
        # TODO: query by strategyId later
        data = {
            "projectId": 15770834
        }
        qc_secrets = get_qc_secrets(request.headers.get('Authorization'))
        if qc_secrets is None:
            abort(500, error_message='Cannot get QC secrets!')
        response = requests.post(BASE_URL_API + "/live/update/stop", auth=(qc_secrets['qc_api_user_id'], generate_token(qc_secrets['qc_api_token'])), json=data, headers = init_header())
        response_json: dict = response.json()
        if response.status_code == 200 and response_json['success'] == True:
            response_from_supabase = SupabaseDashboard.update('strategy_settings', {'is_started': False}, 'id', data_from_client.get('strategyId'))
            print('response_from_supabase', response_from_supabase)
            response_json["isStarted"] = False
        return jsonify({ "response": response_json })