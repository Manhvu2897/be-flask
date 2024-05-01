from flask import Blueprint, jsonify
from flask_restful import Api
from api.resource.resource import ReadBacktest, ReadOrdersBacktest, ReadPortfolioBacktest, CreateBacktest, UpdateBacktest, DeleteBacktest, CompileResource
from api.resource.check_authen import CheckAuthenResource
from api.resource.project import ReadNodeProject
from api.resource.live_backtest import ReadAlgoStatistics, CreateLiveAlgo, ReadLog, ReadPorfolioState, ReadOrders, ReadInsights, ListLiveAlgorithms, StartLiveAlgorithm, StopAlgorithm, LiquidateAlgorithm, StopLiveAlgorithm

bp = Blueprint("TR-System", __name__)
api = Api(bp)

# Check auth api
api.add_resource(CheckAuthenResource, "/check")
# Backtest APIs
api.add_resource(ReadBacktest, "/backtest/read")
api.add_resource(ReadOrdersBacktest, "/backtest/read/orders")
api.add_resource(ReadPortfolioBacktest, "/backtest/read/portfolio")
api.add_resource(CreateBacktest, "/backtest/create")
api.add_resource(UpdateBacktest, "/backtest/update")
api.add_resource(DeleteBacktest, "/backtest/delete")
api.add_resource(CompileResource, "/compile")
api.add_resource(ReadNodeProject, "/project/read")
# Live Managerment APIs
api.add_resource(ListLiveAlgorithms, "/live/list")
api.add_resource(ReadAlgoStatistics, "/live/read/statistics")
api.add_resource(ReadLog, "/live/read/log")
api.add_resource(ReadPorfolioState, "/live/read/portfolio")
api.add_resource(ReadOrders, "/live/read/orders")
api.add_resource(ReadInsights, "/live/read/insights")
api.add_resource(CreateLiveAlgo, "/live/create")
api.add_resource(LiquidateAlgorithm, "/live/update/liquidate")
api.add_resource(StopAlgorithm, "/live/update/stop")
api.add_resource(StartLiveAlgorithm, "/strategy/start")
api.add_resource(StopLiveAlgorithm, "/strategy/stop")


# Default page
@bp.route('/')
def home():
    return jsonify({'response': 'TR System Api'})