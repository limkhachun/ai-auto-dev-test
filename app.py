"""
Super Admin Dashboard — Flask Application Entry Point.
"""
from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from config import Config
from models import db

# Import blueprints
from routes.auth import auth_bp
from routes.shop import shop_bp
from routes.staff import staff_bp
from routes.admin import admin_bp


def create_app(config_class=Config):
    """Application factory."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Init database
    db.init_app(app)

    # Init CSRF protection — validates tokens for all POST/PUT/DELETE requests
    csrf = CSRFProtect(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(shop_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(admin_bp)

    # Root redirect
    @app.route('/')
    def index():
        from flask import redirect, url_for
        return redirect(url_for('auth.login'))

    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(500)
    def server_error(e):
        return render_template('errors/500.html'), 500

    # Create tables in dev mode
    with app.app_context():
        # Only create if they don't exist — safe for repeated runs
        import sqlalchemy
        inspector = sqlalchemy.inspect(db.engine)
        if not inspector.has_table('users'):
            db.create_all()
            print('[✓] Database tables created.')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
