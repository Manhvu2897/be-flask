import pytest, sys, os, json
import uuid
# Get the path to the application's root directory
app_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Add the path of the directory containing the index.py file to the system PATH
sys.path.insert(0, os.path.join(app_root))
from index import create_app
from api.config import supabase
from api.supabase_dashboard import SupabaseDashboard

URL_PREFIX = "/api/v1/"

PROJECT_ID = "15770834"

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    # remove token require
    app.before_request_funcs = {}
    # other setup can go here
    with app.app_context():
        yield app

@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def decode_data(data):
    new_data = json.loads(data.decode('utf-8'))
    return new_data

def test_host_name(client):
    response = client.get(URL_PREFIX)
    print('response host name::', response.json["response"])
    assert response.status_code == 200
    assert response.json["response"] == "TR System Api"

def test_check_auth(client):
    response = client.get(URL_PREFIX + 'check')
    assert response.status_code == 200
    assert response.json["success"] == True

@pytest.fixture()
def get_compile_id(client):
    data = {
        "projectId": PROJECT_ID
    }
    response = client.post(URL_PREFIX + 'compile', json=data)
    print('response....', response.json["response"])
    yield response.json["response"]

@pytest.fixture()
def create_backtest(get_compile_id, client):
    print('get_compile_id:::::', get_compile_id)
    data = {
        "projectId": PROJECT_ID,
        "compileId": get_compile_id["compileId"],
        "backtestName": "Unit test backtest"
    }
    response = client.post(URL_PREFIX + 'backtest/create', json=data)
    print('response create backtest::', response.json["response"])
    yield response.json["response"]

def test_read_backtest(create_backtest, client):
    data = {
        "projectId": PROJECT_ID,
        "backtestId": create_backtest["backtest"]["backtestId"]
    }
    response = client.post(URL_PREFIX + 'backtest/read', json=data)
    print('response read backtest statistics:::', response.json["response"])
    assert response.status_code == 200
    assert response.json["response"]["backtest"]["name"] == "Unit test backtest"
    assert response.json["response"]["backtest"]["backtestId"] == create_backtest["backtest"]["backtestId"]

def test_read_backtest_porfolio(client):
    data = {
        "projectId": PROJECT_ID,
        "backtestId": "46ce614043a06eb28c4b6c8ecf5e4a05"
    }
    response = client.post(URL_PREFIX + 'backtest/read/portfolio', json=data)
    print('response read backtest porfolio:::', response.json["response"])
    assert response.status_code == 200
    assert response.json["response"]["success"] == True

def test_read_backtest_orders(client):
    data = {
        "projectId": PROJECT_ID,
        "backtestId": "46ce614043a06eb28c4b6c8ecf5e4a05",
        "start": 0,
        "end": 100
    }
    response = client.post(URL_PREFIX + 'backtest/read/orders', json=data)
    print('response read backtest orders:::', response.json["response"])
    assert response.status_code == 200
    assert response.json["response"]["success"] == True

def test_insert_data_portfolio_into_supabase():
    sign_in = supabase.auth.sign_in_with_password({
        "email": "codaubo@gmail.com",
        "password": "cobau12a10ht"
    }).model_dump()
    user = supabase.auth.get_user(sign_in['session']['access_token']).model_dump()
    id_generate = str(uuid.uuid4())
    data_insert = {
        "id": id_generate,
        "user_id": user['user']['id'],
        "overall_return": 1000,
        "market_value": 100000,
        "portfolio_cost": 10000,
        "today_volumn": 30000,
        "overall_volumn": 50000
    }
    data_insert = SupabaseDashboard.insert('portfolio', data_insert)
    assert data_insert.data
    # delete the usage record for testing
    data_delete = SupabaseDashboard.delete('portfolio', 'id', id_generate)
    assert data_delete.data
    # break session
    supabase.auth.sign_out()

def test_insert_data_portfolio_trades_into_supabase():
    sign_in = supabase.auth.sign_in_with_password({
        "email": "codaubo@gmail.com",
        "password": "cobau12a10ht"
    }).model_dump()
    user = supabase.auth.get_user(sign_in['session']['access_token']).model_dump()
    id_generate = str(uuid.uuid4())
    data_insert = {
        "id": id_generate,
        "user_id": user['user']['id'],
        "symbol_id": "TSLA",
        "last_price": 200000,
        "last_price_change": 150000,
        "price": 180000,
        "shares": 500,
        "market_value": 300000,
        "gain": 2,
        "day_gain": 1,
        "return": 25600,
        "amount_today": 16700,
        "percent_today": 4,
        "total": 25000,
        "total_percent": 12,
        "current_value": -102204,
        "percent_account": 36,
        "quantity": 3600,
        "average_cost": 300,
        "total_cost": 30000,
        "amount_today_note": 15000,
        "percent_today_note": 18,
        "timestamp": 1672842960,
        "fees": 5.6,
        "side": None,
        "current_price": 113.58,
        "traded_fund": 20,
    }
    data_insert = SupabaseDashboard.insert('portfolio_trades', data_insert)
    assert data_insert.data
    # delete the usage record for testing
    data_delete = SupabaseDashboard.delete('portfolio_trades', 'id', id_generate)
    assert data_delete.data
    # break session
    supabase.auth.sign_out()