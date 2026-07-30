"""
Super Admin routes: dashboard, product management, order shipping, staff management, audit logs.
Only accessible by users with role='superadmin'.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, User, Product, Order, OrderItem, AuditLog
from decorators import role_required
from datetime import datetime

admin_bp = Blueprint('admin', __name__, template_folder='../templates')


def log_audit(action_description, target_type=None):
    """Helper function to write audit log."""
    staff_id = session.get('user_id')
    if staff_id:
        log = AuditLog(
            staff_id=staff_id,
            action_description=action_description,
            target_type=target_type,
            created_at=datetime.utcnow()
        )
        db.session.add(log)


# ============================================================
# Dashboard
# ============================================================

@admin_bp.route('/admin/dashboard')
@role_required('superadmin')
def admin_dashboard():
    """Super Admin dashboard homepage.
    Renders overview with products, orders, staffs, audit_logs data.
    """
    products = Product.query.order_by(Product.created_at.desc()).all()
    orders = Order.query.order_by(Order.created_at.desc()).all()
    staffs = User.query.filter_by(role='staff').order_by(User.created_at.desc()).all()
    audit_logs = AuditLog.query.order_by(AuditLog.created_at.desc()).all()
    return render_template(
        'admin_dashboard.html',
        products=products,
        orders=orders,
        staffs=staffs,
        audit_logs=audit_logs
    )


# ============================================================
# Product Management
# ============================================================

@admin_bp.route('/admin/products/add', methods=['POST'])
@role_required('superadmin')
def add_product():
    """Add a new product (with audit log)."""
    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()
    try:
        price = float(request.form.get('price', 0))
        stock = int(request.form.get('stock', 0))
    except ValueError:
        flash('Invalid price or stock format.', 'danger')
        return redirect(url_for('admin.admin_dashboard'))

    if not name:
        flash('Product name is required.', 'danger')
        return redirect(url_for('admin.admin_dashboard'))

    product = Product(
        name=name,
        description=description,
        price=price,
        stock=stock,
        created_at=datetime.utcnow()
    )
    db.session.add(product)
    db.session.flush()

    log_audit(f'Added product: {name} (ID: {product.id}), Price: {price}, Stock: {stock}', 'product')
    db.session.commit()

    flash(f'Product "{name}" added successfully.', 'success')
    return redirect(url_for('admin.admin_dashboard', _anchor='tab-products'))


@admin_bp.route('/admin/products/edit/<int:product_id>', methods=['POST'])
@role_required('superadmin')
def edit_product(product_id):
    """Edit an existing product (with audit log)."""
    product = Product.query.get_or_404(product_id)
    old_name = product.name

    product.name = request.form.get('name', '').strip() or product.name
    product.description = request.form.get('description', '').strip() or product.description
    try:
        product.price = float(request.form.get('price', product.price))
        product.stock = int(request.form.get('stock', product.stock))
    except ValueError:
        flash('Invalid price or stock format.', 'danger')
        return redirect(url_for('admin.admin_dashboard'))

    log_audit(f'Edited product: ID {product_id}, Old name: {old_name}, New name: {product.name}', 'product')
    db.session.commit()

    flash(f'Product "{product.name}" updated successfully.', 'success')
    return redirect(url_for('admin.admin_dashboard', _anchor='tab-products'))


@admin_bp.route('/admin/products/delete/<int:product_id>', methods=['POST'])
@role_required('superadmin')
def delete_product(product_id):
    """Delete a product (with audit log)."""
    product = Product.query.get_or_404(product_id)
    name = product.name

    log_audit(f'Deleted product: {name} (ID: {product_id})', 'product')
    db.session.delete(product)
    db.session.commit()

    flash(f'Product "{name}" deleted.', 'success')
    return redirect(url_for('admin.admin_dashboard', _anchor='tab-products'))


# ============================================================
# Order Management
# ============================================================

@admin_bp.route('/admin/orders')
@role_required('superadmin')
def admin_orders():
    """View all orders."""
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin_orders.html', orders=orders)


@admin_bp.route('/admin/orders/ship/<int:order_id>', methods=['POST'])
@role_required('superadmin')
def ship_order(order_id):
    """Mark order as shipped (with audit log)."""
    order = Order.query.get_or_404(order_id)
    if order.status != 'paid':
        flash('Only paid orders can be shipped.', 'warning')
        return redirect(url_for('admin.admin_dashboard'))

    order.status = 'shipped'

    log_audit(f'Shipped order: #{order_id}, User ID: {order.user_id}, Amount: ${order.total_amount}', 'order')
    db.session.commit()

    flash(f'Order #{order_id} has been marked as shipped.', 'success')
    return redirect(url_for('admin.admin_dashboard', _anchor='tab-orders'))


# ============================================================
# Staff Management
# ============================================================

@admin_bp.route('/admin/staff/add', methods=['POST'])
@role_required('superadmin')
def add_staff():
    """Register a new staff account (with audit log)."""
    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')

    # Validation
    errors = []
    if not username or len(username) < 3:
        errors.append('Username must be at least 3 characters.')
    if not email or '@' not in email:
        errors.append('Please provide a valid email address.')
    if len(password) < 6:
        errors.append('Password must be at least 6 characters.')
    if User.query.filter_by(username=username).first():
        errors.append('Username is already taken.')
    if User.query.filter_by(email=email).first():
        errors.append('Email is already registered.')

    if errors:
        for err in errors:
            flash(err, 'danger')
        return redirect(url_for('admin.admin_dashboard'))

    staff = User(username=username, email=email, role='staff')
    staff.set_password(password)
    db.session.add(staff)
    db.session.flush()

    log_audit(f'Added staff account: {username} (ID: {staff.id}, Email: {email})', 'staff')
    db.session.commit()

    flash(f'Staff account "{username}" created successfully!', 'success')
    return redirect(url_for('admin.admin_dashboard', _anchor='tab-staff'))
