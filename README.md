# AdminLTE + Flask Dashboard with Login System

A comprehensive dashboard system built with Flask and AdminLTE, featuring a secure login system and dynamic content management.

## Features

- **Authentication System**: Secure login/logout with Flask-Login
- **AdminLTE Integration**: Modern, responsive admin dashboard
- **Dynamic Sidebar**: Tree-structured navigation based on database content
- **Interactive Charts**: Chart.js integration for data visualization
- **MVC + DDD Architecture**: Clean, maintainable code structure
- **Multi-Database Support**: MariaDB and PostgreSQL ready

## Project Structure

```
dashboard_project/
├── app/
│   ├── config/           # Configuration files
│   ├── domain/           # Domain layer (models, services)
│   ├── infrastructure/   # Infrastructure layer (database, repositories)
│   ├── presentation/     # Presentation layer (controllers, forms)
│   └── static/           # Static files (CSS, JS)
├── templates/            # Jinja2 templates
├── requirements.txt      # Python dependencies
├── run.py               # Application entry point
├── database_setup.sql   # Database schema and sample data
└── .env.example         # Environment variables template
```

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Database Setup**
   ```bash
   # Create database and tables
   mysql -u root -p < database_setup.sql
   ```

3. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

4. **Run Application**
   ```bash
   python run.py
   ```

5. **Access Dashboard**
   - URL: http://localhost:5000
   - Username: admin
   - Password: admin123

## Login System

The authentication system includes:

- **User Model**: Flask-Login integration with bcrypt password hashing
- **Login Form**: WTForms validation with CSRF protection
- **Session Management**: Secure session handling with remember me option
- **Route Protection**: Login required decorators on protected endpoints

### Authentication Flow

1. User accesses protected route
2. Redirected to login page if not authenticated
3. Form validation and password verification
4. Session creation and user login
5. Redirect to originally requested page or dashboard

## Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `email`: User email
- `password_hash`: Bcrypt hashed password
- `is_active`: Account status
- `created_at`: Registration timestamp

### Business Tables
- `business_categories`: Navigation categories
- `business_contents`: Individual menu items

## API Endpoints

- `GET /`: Dashboard home (login required)
- `GET /auth/login`: Login page
- `POST /auth/login`: Login form submission
- `GET /auth/logout`: User logout
- `GET /api/categories`: Get navigation structure
- `GET /api/dashboard-data/<route>`: Get dashboard data

## Security Features

- CSRF protection on all forms
- Password hashing with bcrypt
- Session-based authentication
- SQL injection prevention
- Environment-based configuration

## Customization

### Adding New Dashboard Content

1. Add entries to `business_categories` and `business_contents` tables
2. Update `DashboardService.get_dashboard_data_by_route()` method
3. Sidebar will automatically reflect changes

### Styling

- Modify `app/static/css/custom.css` for custom styles
- AdminLTE themes can be changed in base template

## Development

The application follows DDD (Domain Driven Design) principles:

- **Domain Layer**: Business logic and models
- **Infrastructure Layer**: Database connections and external services  
- **Presentation Layer**: Controllers, forms, and templates

## Production Deployment

1. Set `FLASK_ENV=production` in environment
2. Use a production WSGI server (Gunicorn, uWSGI)
3. Configure reverse proxy (Nginx, Apache)
4. Set up SSL/TLS certificates
5. Use production database with connection pooling

## License

This project is open source and available under the MIT License.