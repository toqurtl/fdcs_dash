from flask import Flask
from flask_login import LoginManager
from app.config.settings import Config
from app.infrastructure.database.sqlite_connection import SQLiteConnection
from app.infrastructure.repositories.sql_business_repository import SqlBusinessRepository
from app.domain.services.business_service import BusinessService
from app.domain.services.dashboard_service import DashboardService
from app.domain.services.auth_service import AuthService
from app.presentation.controllers.main_controller import main_bp
from app.presentation.controllers.api_controller import api_bp
from app.presentation.controllers.auth_controller import auth_bp

def create_app():
    import os
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))
    
    app = Flask(__name__, 
                template_folder=template_dir,
                static_folder=static_dir)
    app.config.from_object(Config)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '로그인이 필요합니다.'
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.domain.models.user import User
        db_connection = SQLiteConnection()
        auth_service = AuthService(db_connection)
        return auth_service.get_user_by_id(int(user_id))
    
    db_connection = SQLiteConnection()
    business_repository = SqlBusinessRepository(db_connection)
    business_service = BusinessService(business_repository)
    dashboard_service = DashboardService(db_connection)
    
    app.business_service = business_service
    app.dashboard_service = dashboard_service
    
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    return app