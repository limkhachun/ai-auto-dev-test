"""
Standalone admin utility module.
Provides helper functions for admin operations outside of Flask routes.
"""
from models import db, User, Product, Order, OrderItem, AuditLog
from datetime import datetime


def seed_superadmin(username='admin', email='admin@example.com', password='admin123'):
    """Create a default superadmin account if none exists."""
    existing = User.query.filter_by(role='superadmin').first()
    if existing:
        print(f'[i] Superadmin already exists: {existing.username}')
        return existing

    admin = User(
        username=username,
        email=email,
        role='superadmin',
        created_at=datetime.utcnow()
    )
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
    print(f'[✓] Superadmin created: {username} / {password}')
    return admin


def seed_sample_data():
    """Add sample products for demonstration."""
    if Product.query.count() > 0:
        print('[i] Products already exist, skipping seed.')
        return

    samples = [
        Product(name='Wireless Mouse', description='Ergonomic wireless mouse', price=29.99, stock=50),
        Product(name='Mechanical Keyboard', description='RGB mechanical keyboard', price=89.99, stock=30),
        Product(name='USB-C Hub', description='7-in-1 USB-C hub adapter', price=39.99, stock=100),
        Product(name='Monitor Stand', description='Adjustable monitor riser', price=49.99, stock=25),
        Product(name='Webcam HD', description='1080p HD webcam with microphone', price=59.99, stock=40),
    ]
    for p in samples:
        db.session.add(p)
    db.session.commit()
    print(f'[✓] Seeded {len(samples)} sample products.')


def list_all_users():
    """Print all users to stdout."""
    users = User.query.order_by(User.created_at.desc()).all()
    print(f'\n── Users ({len(users)}) ──')
    for u in users:
        print(f'  #{u.id} {u.username:20s} {u.email:30s} role={u.role}')


def list_all_products():
    """Print all products to stdout."""
    products = Product.query.order_by(Product.created_at.desc()).all()
    print(f'\n── Products ({len(products)}) ──')
    for p in products:
        print(f'  #{p.id} {p.name:30s} ${float(p.price):>8.2f} stock={p.stock}')


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_superadmin()
        seed_sample_data()
        list_all_users()
        list_all_products()
