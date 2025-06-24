from flask import Blueprint, jsonify, current_app
from flask_login import login_required

api_bp = Blueprint('api', __name__)

@api_bp.route('/categories')
@login_required
def get_categories():
    business_service = current_app.business_service
    categories = business_service.get_all_categories()
    return jsonify([{
        'id': cat.id,
        'name': cat.name,
        'description': cat.description,
        'contents': [{
            'id': content.id,
            'name': content.name,
            'route': content.route,
            'icon': content.icon
        } for content in cat.contents]
    } for cat in categories])

@api_bp.route('/dashboard-data/<content_route>')
@login_required
def get_dashboard_data(content_route):
    dashboard_service = current_app.dashboard_service
    data = dashboard_service.get_dashboard_data_by_route(content_route)
    return jsonify(data)