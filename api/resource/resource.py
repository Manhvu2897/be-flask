import requests, json
from flask import request, jsonify
from flask_restful import Resource, abort
from api.config import init_header, generate_token, BASE_URL_API
from api.auth_middleware import get_qc_secrets
from api.supabase_dashboard import SupabaseDashboard

class ReadBacktest(Resource):
    def post(self):
        data_from_client = json.loads(request.data.decode())
        data = {
            "projectId": data_from_client["projectId"]
        }
        if "backtestId" in data_from_client:
            data["backtestId"] = data_from_client["backtestId"]
        qc_secrets = get_qc_secrets(request.headers.get('Authorization'))
        if qc_secrets is None:
            abort(500, error_message='Cannot get QC secrets!')
        response = requests.post(BASE_URL_API + "/backtests/read", auth=(qc_secrets['qc_api_user_id'], generate_token(qc_secrets['qc_api_token'])), data=data, headers = init_header())
        return jsonify({ "response": response.json() })
class ReadPortfolioBacktest(Resource):
    def post(self):
        data_from_client = json.loads(request.data.decode())
        data = {
            "projectId": data_from_client["projectId"],
            "backtestId": data_from_client["backtestId"]
        }
        qc_secrets = get_qc_secrets(request.headers.get('Authorization'))
        if qc_secrets is None:
            abort(500, error_message='Cannot get QC secrets!')
        response = requests.post(BASE_URL_API + "/backtests/read/portfolio", auth=(qc_secrets['qc_api_user_id'], generate_token(qc_secrets['qc_api_token'])), data=data, headers = init_header()).json()
        if response and response["backtest"]:
            data_insert = {
                "overall_return": response["backtest"]["runtimeStatistics"]["Equity"].replace("$", "").replace(",", ""),
                "market_value": response["backtest"]["statistics"]["Estimated Strategy Capacity"].replace("$", "").replace(",", ""),
                "portfolio_cost": response["backtest"]["runtimeStatistics"]["Fees"].replace("$", "").replace(",", ""),
                "today_volumn": None, #value has not been determined
                "overall_volumn": response["backtest"]["runtimeStatistics"]["Volume"].replace("$", "").replace(",", "")
            }
            response_from_supabase = SupabaseDashboard.insert('portfolio', data_insert)
            print('response_from_supabase:::', response_from_supabase.data)
        return jsonify({ "response": response })
class ReadOrdersBacktest(Resource):
    def post(self):
        data_from_client = json.loads(request.data.decode())
        data = {
            "projectId": data_from_client["projectId"],
            "backtestId": data_from_client["backtestId"],
            "start": data_from_client["start"],
            "end": data_from_client["end"]
        }
        qc_secrets = get_qc_secrets(request.headers.get('Authorization'))
        if qc_secrets is None:
            abort(500, error_message='Cannot get QC secrets!')
        response = requests.post(BASE_URL_API + "/backtests/read/orders", auth=(qc_secrets['qc_api_user_id'], generate_token(qc_secrets['qc_api_token'])), data=data, headers = init_header()).json()
        if response and response["orders"]:
            orders_data = []
            for order in response["orders"]:
                orders_data.append({
                    "symbol_id": order["Symbol"]["ID"],
                    "last_price": order["OrderSubmissionData"]["BidPrice"],
                    "last_price_change": order["OrderSubmissionData"]["LastPrice"],
                    "price": order["Price"],
                    "shares": order["Symbol"]["Value"],
                    "market_value": order["OrderSubmissionData"]["LastPrice"],
                    "gain": None,
                    "day_gain": None,
                    "return": None,
                    "amount_today": None,
                    "percent_today": None,
                    "total": None,
                    "total_percent": None,
                    "current_value": order["Value"],
                    "percent_account": None,
                    "quantity": order["Quantity"],
                    "average_cost": None,
                    "total_cost": None,
                    "amount_today_note": None,
                    "percent_today_note": None,
                    "timestamp": order["Events"][0]["timestamp"],
                    "fees": order["Events"][1]["order-fee-amount"],
                    "side": None,
                    "current_price": order["OrderSubmissionData"]["AskPrice"],
                    "traded_fund": None,
                })
            response_from_supabase = SupabaseDashboard.insert('portfolio_trades', orders_data)
            print('response_from_supabase:::', response_from_supabase.data)
        return jsonify({ "response": response })
class CreateBacktest(Resource):
    def post(self):
        data_from_client = json.loads(request.data.decode())
        data = {
            "projectId": data_from_client["projectId"],
            "compileId": data_from_client["compileId"],
            "backtestName": data_from_client["backtestName"]
        }
        qc_secrets = get_qc_secrets(request.headers.get('Authorization'))
        if qc_secrets is None:
            abort(500, error_message='Cannot get QC secrets!')
        response = requests.post(BASE_URL_API + "/backtests/create", auth=(qc_secrets['qc_api_user_id'], generate_token(qc_secrets['qc_api_token'])), data=data, headers = init_header())
        return jsonify({ "response": response.json() })
class UpdateBacktest(Resource):
    def post(self):
        data_from_client = json.loads(request.data.decode())
        data = {
            "projectId": data_from_client["projectId"],
            "backtestId": data_from_client["backtestId"],
            "name": data_from_client["name"],
            "note": data_from_client["note"]
        }
        qc_secrets = get_qc_secrets(request.headers.get('Authorization'))
        if qc_secrets is None:
            abort(500, error_message='Cannot get QC secrets!')
        response = requests.post(BASE_URL_API + "/backtests/update", auth=(qc_secrets['qc_api_user_id'], generate_token(qc_secrets['qc_api_token'])), data=data, headers = init_header())
        return jsonify({ "response": response.json() })
class DeleteBacktest(Resource):
    def post(self):
        data_from_client = json.loads(request.data.decode())
        data = {
            "projectId": data_from_client["projectId"],
            "backtestId": data_from_client["backtestId"]
        }
        qc_secrets = get_qc_secrets(request.headers.get('Authorization'))
        if qc_secrets is None:
            abort(500, error_message='Cannot get QC secrets!')
        response = requests.post(BASE_URL_API + "/backtests/delete", auth=(qc_secrets['qc_api_user_id'], generate_token(qc_secrets['qc_api_token'])), data=data, headers = init_header())
        return jsonify({ "response": response.json() })
class CompileResource(Resource):
    def get(self):
        data_from_client = json.loads(request.data.decode("utf-8"))
        data = {
            "projectId": data_from_client["projectId"],
            "compileId": data_from_client["compileId"]
        }
        qc_secrets = get_qc_secrets(request.headers.get('Authorization'))
        if qc_secrets is None:
            abort(500, error_message='Cannot get QC secrets!')
        response = requests.post(BASE_URL_API + "/compile/read", data=data, auth=(qc_secrets['qc_api_user_id'], generate_token(qc_secrets['qc_api_token'])), headers = init_header())
        return jsonify({ "response": response.json() })

    def post(self):
        data_from_client = json.loads(request.data.decode("utf-8"))
        data = {
            "projectId": data_from_client["projectId"]
        }
        qc_secrets = get_qc_secrets(request.headers.get('Authorization'))
        if qc_secrets is None:
            abort(500, error_message='Cannot get QC secrets!')
        response = requests.post(BASE_URL_API + "/compile/create", data=data, auth=(qc_secrets['qc_api_user_id'], generate_token(qc_secrets['qc_api_token'])), headers = init_header())
        return jsonify({ "response": response.json() })