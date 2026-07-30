"""
Staff routes: inventory management, order processing, audit logging.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, Product, Order, OrderItem, AuditLog
from decorators import role_required
from datetime import datetime

staff_bp = Blueprint('staff', __name__, template_folder='../templates')


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


@staff_bp.route('/staff/dashboard')
@role_required('staff', 'superadmin')
def staff_dashboard():
    """Staff dashboard homepage."""
    products = Product.query.order_by(Product.created_at.desc()).all()
    pending_orders = Order.query.filter_by(status='paid').order_by(Order.created_at.desc()).all()
    return render_template('staff_dashboard.html', products=products, pending_orders=pending_orders)


@staff_bp.route('/staff/products/add', methods=['POST'])
@role_required('staff', 'superadmin')
def add_product():
    """Add a new product (with audit log)."""
    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()
    try:
        price = float(request.form.get('price', 0))
        stock = int(request.form.get('stock', 0))
    except ValueError:
        flash('Invalid price or stock format.', 'danger')
        return redirect(url_for('staff.staff_dashboard'))

    if not name:
        flash('Product name is required.', 'danger')
        return redirect(url_for('staff.staff_dashboard'))

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
    return redirect(url_for('staff.staff_dashboard'))


@staff_bp.route('/staff/products/edit/<int:product_id>', methods=['POST'])
@role_required('staff', 'superadmin')
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
        return redirect(url_for('staff.staff_dashboard'))

    log_audit(f'Edited product: ID {product_id}, Old name: {old_name}, New name: {product.name}', 'product')
    db.session.commit()

    flash(f'Product "{product.name}" updated successfully.', 'success')
    return redirect(url_for('staff.staff_dashboard'))


@staff_bp.route('/staff/products/delete/<int:product_id>', methods=['POST'])
@role_required('staff', 'superadmin')
def delete_product(product_id):
    """Delete a product (with audit log)."""
    product = Product.query.get_or_404(product_id)
    name = product.name

    log_audit(f'Deleted product: {name} (ID: {product_id})', 'product')
    db.session.delete(product)
    db.session.commit()

    flash(f'Product "{name}" deleted.', 'success')
    return redirect(url_for('staff.staff_dashboard'))


@staff_bp.route('/staff/orders')
@role_required('staff', 'superadmin')
def staff_orders():
    """View all orders."""
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('staff_orders.html', orders=orders)


@staff_bp.route('/staff/orders/ship/<int:order_id>', methods=['POST'])
@role_required('staff', 'superadmin')
def ship_order(order_id):
    """Mark order as shipped (with audit log)."""
    order = Order.query.get_or_404(order_id)
    if order.status != 'paid':
        flash('Only paid orders can be shipped.', 'warning')
        return redirect(url_for('staff.staff_orders'))

    order.status = 'shipped'

    log_audit(f'Shipped order: #{order_id}, User ID: {order.user_id}, Amount: ${order.total_amount}', 'order')
    db.session.commit()

    flash(f'Order #{order_id} has been marked as shipped.', 'success')
    return redirect(url_for('staff.staff_orders'))
