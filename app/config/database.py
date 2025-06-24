from app.config.settings import Config

class DatabaseConfig:
    @staticmethod
    def get_mariadb_config():
        return {
            'host': Config.MARIADB_HOST,
            'port': Config.MARIADB_PORT,
            'user': Config.MARIADB_USER,
            'password': Config.MARIADB_PASSWORD,
            'database': Config.MARIADB_DATABASE
        }
    
    @staticmethod
    def get_postgresql_config():
        return {
            'host': Config.POSTGRESQL_HOST,
            'port': Config.POSTGRESQL_PORT,
            'user': Config.POSTGRESQL_USER,
            'password': Config.POSTGRESQL_PASSWORD,
            'database': Config.POSTGRESQL_DATABASE
        }