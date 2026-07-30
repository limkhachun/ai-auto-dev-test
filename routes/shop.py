"""
Shop routes: product browsing, shopping cart, checkout, order history for regular users.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, Product, Order, OrderItem
from decorators import login_required
from datetime import datetime
from decimal import Decimal

shop_bp = Blueprint('shop', __name__, template_folder='../templates')


@shop_bp.route('/shop')
@login_required
def index():
    """Product listing page."""
    products = Product.query.order_by(Product.created_at.desc()).all()
    cart = session.get('cart', {})
    return render_template('shop.html', products=products, cart=cart)


@shop_bp.route('/shop/add-to-cart', methods=['POST'])
@login_required
def add_to_cart():
    """Add item to cart (stored in session)."""
    product_id = str(request.form.get('product_id', ''))
    quantity = int(request.form.get('quantity', 1))

    product = Product.query.get(int(product_id))
    if not product:
        flash('Product not found.', 'danger')
        return redirect(url_for('shop.index'))

    if quantity < 1:
        quantity = 1

    cart = session.get('cart', {})
    if product_id in cart:
        cart[product_id]['quantity'] += quantity
    else:
        cart[product_id] = {
            'product_id': product.id,
            'name': product.name,
            'price': float(product.price),
            'quantity': quantity,
            'max_stock': product.stock,
        }
    session['cart'] = cart
    session.modified = True
    flash(f'Added {product.name} x{quantity} to cart.', 'success')
    return redirect(url_for('shop.index'))


@shop_bp.route('/shop/cart')
@login_required
def cart():
    """View shopping cart."""
    cart = session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return render_template('cart.html', cart=cart, total=total)


@shop_bp.route('/shop/update-cart', methods=['POST'])
@login_required
def update_cart():
    """Update cart item quantity."""
    product_id = str(request.form.get('product_id', ''))
    quantity = int(request.form.get('quantity', 1))
    cart = session.get('cart', {})

    if product_id in cart:
        if quantity <= 0:
            del cart[product_id]
        else:
            cart[product_id]['quantity'] = quantity
        session['cart'] = cart
        session.modified = True

    return redirect(url_for('shop.cart'))


@shop_bp.route('/shop/remove-from-cart', methods=['POST'])
@login_required
def remove_from_cart():
    """Remove item from cart."""
    product_id = str(request.form.get('product_id', ''))
    cart = session.get('cart', {})
    if product_id in cart:
        del cart[product_id]
        session['cart'] = cart
        session.modified = True
    return redirect(url_for('shop.cart'))


@shop_bp.route('/shop/checkout', methods=['POST'])
@login_required
def checkout():
    """
    Checkout (Mock Payment).
    1. Validate stock
    2. Deduct stock
    3. Create order (status = paid)
    4. Clear cart
    """
    cart = session.get('cart', {})
    if not cart:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('shop.cart'))

    user_id = session['user_id']
    order_items_data = []
    total_amount = Decimal('0.00')

    for pid_str, item in cart.items():
        product = Product.query.get(int(pid_str))
        if not product:
            flash(f'Product {item["name"]} no longer exists.', 'danger')
            return redirect(url_for('shop.cart'))
        if product.stock < item['quantity']:
            flash(f'Product {product.name} has insufficient stock (remaining {product.stock}).', 'danger')
            return redirect(url_for('shop.cart'))
        order_items_data.append({
            'product': product,
            'quantity': item['quantity'],
            'price': Decimal(str(item['price'])),
        })
        total_amount += Decimal(str(item['price'])) * item['quantity']

    order = Order(
        user_id=user_id,
        total_amount=total_amount,
        status='paid',
        created_at=datetime.utcnow()
    )
    db.session.add(order)
    db.session.flush()

    for data in order_items_data:
        product = data['product']
        qty = data['quantity']
        unit_price = data['price']

        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=qty,
            price=unit_price,
        )
        db.session.add(order_item)
        product.stock -= qty

    db.session.commit()

    session['cart'] = {}
    session.modified = True

    flash(f'Order #{order.id} placed successfully! Total: ${float(total_amount):.2f}', 'success')
    return redirect(url_for('shop.my_orders'))


@shop_bp.route('/shop/my-orders')
@login_required
def my_orders():
    """My order history."""
    user_id = session['user_id']
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    return render_template('my_orders.html', orders=orders)
