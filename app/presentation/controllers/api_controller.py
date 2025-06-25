from flask import Blueprint, jsonify, current_app, request
from flask_login import login_required
from app.infrastructure.database.sqlite_connection import SQLiteConnection
from app.domain.services.table_service import TableService

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

@api_bp.route('/table/<table_name>')
@login_required
def get_table_data(table_name):
    """테이블 데이터 조회 API (페이지네이션, 검색, 정렬 지원)"""
    try:
        # 쿼리 파라미터 추출
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        search_column = request.args.get('search_column')
        search_value = request.args.get('search_value')
        sort_column = request.args.get('sort_column')
        sort_direction = request.args.get('sort_direction', 'ASC').upper()
        
        # 고급 검색 필터 파라미터
        advanced_filters_json = request.args.get('advanced_filters')
        advanced_filters = None
        if advanced_filters_json:
            try:
                import json
                advanced_filters = json.loads(advanced_filters_json)
            except (json.JSONDecodeError, TypeError):
                advanced_filters = None
        
        # 페이지당 항목 수 제한 (성능 보호)
        per_page = min(per_page, 100)
        
        # 정렬 방향 검증
        if sort_direction not in ['ASC', 'DESC']:
            sort_direction = 'ASC'
        
        # 테이블 서비스 초기화
        db_connection = SQLiteConnection()
        table_service = TableService(db_connection)
        
        # 데이터 조회
        result = table_service.get_table_data(
            table_name=table_name,
            page=page,
            per_page=per_page,
            search_column=search_column,
            search_value=search_value,
            sort_column=sort_column,
            sort_direction=sort_direction,
            advanced_filters=advanced_filters
        )
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/table/<table_name>/filter-options/<column_name>')
@login_required
def get_filter_options(table_name, column_name):
    """특정 컬럼의 필터 옵션 조회"""
    try:
        db_connection = SQLiteConnection()
        table_service = TableService(db_connection)
        
        options = table_service.get_filter_options(table_name, column_name)
        
        return jsonify({
            'success': True,
            'options': options
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500