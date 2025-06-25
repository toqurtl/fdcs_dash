from flask import Blueprint, render_template, current_app
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def index():
    return render_template('dashboard/main.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    business_service = current_app.business_service
    categories = business_service.get_all_categories()
    return render_template('dashboard/main.html', categories=categories, user=current_user)

@main_bp.route('/dashboard/table-view')
@login_required
def table_view():
    business_service = current_app.business_service
    categories = business_service.get_all_categories()
    return render_template('dashboard/table_view.html', categories=categories, user=current_user)