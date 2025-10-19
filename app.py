from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
import random
import re

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# Product data - 20 computer accessories
PRODUCTS = [
    {"id": 1, "name": "Wireless Mouse", "description": "Ergonomic wireless mouse with 2.4GHz connectivity", "price": 2500, "image": "mouse.svg"},
    {"id": 2, "name": "Mechanical Keyboard", "description": "RGB backlit mechanical gaming keyboard", "price": 8500, "image": "keyboard.svg"},
    {"id": 3, "name": "USB-C Hub", "description": "7-in-1 USB-C hub with HDMI and card readers", "price": 3200, "image": "hub.svg"},
    {"id": 4, "name": "Laptop Stand", "description": "Adjustable aluminum laptop stand for ergonomics", "price": 4500, "image": "stand.svg"},
    {"id": 5, "name": "Webcam HD", "description": "1080p HD webcam with built-in microphone", "price": 6800, "image": "webcam.svg"},
    {"id": 6, "name": "Wireless Headphones", "description": "Noise-cancelling over-ear headphones", "price": 12000, "image": "headphones.svg"},
    {"id": 7, "name": "USB Flash Drive 64GB", "description": "High-speed USB 3.0 flash drive", "price": 1800, "image": "usb.svg"},
    {"id": 8, "name": "Monitor Stand", "description": "Dual monitor mount with gas spring arms", "price": 9800, "image": "monitor-stand.svg"},
    {"id": 9, "name": "Cable Management Kit", "description": "Organizer clips and sleeves for cable management", "price": 1500, "image": "cables.svg"},
    {"id": 10, "name": "Laptop Cooling Pad", "description": "USB-powered cooling pad with 5 fans", "price": 3200, "image": "cooling.svg"},
    {"id": 11, "name": "Bluetooth Speaker", "description": "Portable waterproof Bluetooth speaker", "price": 5500, "image": "speaker.svg"},
    {"id": 12, "name": "External SSD 1TB", "description": "Portable NVMe external SSD", "price": 12500, "image": "ssd.svg"},
    {"id": 13, "name": "Gaming Mouse Pad", "description": "Large RGB gaming mouse pad", "price": 2800, "image": "mousepad.svg"},
    {"id": 14, "name": "USB-C Cable", "description": "Braided USB-C charging cable 2m", "price": 1200, "image": "cable.svg"},
    {"id": 15, "name": "Desk Lamp", "description": "LED desk lamp with adjustable brightness", "price": 3500, "image": "lamp.svg"},
    {"id": 16, "name": "Wrist Rest", "description": "Memory foam wrist rest for keyboard and mouse", "price": 1800, "image": "wristrest.svg"},
    {"id": 17, "name": "Portable Monitor", "description": "15.6 inch portable USB-C monitor", "price": 14800, "image": "portable-monitor.svg"},
    {"id": 18, "name": "USB Microphone", "description": "Professional USB condenser microphone", "price": 7200, "image": "mic.svg"},
    {"id": 19, "name": "Laptop Sleeve", "description": "Water-resistant neoprene laptop sleeve", "price": 2800, "image": "sleeve.svg"},
    {"id": 20, "name": "Docking Station", "description": "Thunderbolt 3 docking station with dual 4K support", "price": 13500, "image": "dock.svg"},
]

def get_cart():
    """Get current cart from session"""
    return session.get('cart', {})

def get_ratings():
    """Get current ratings from session"""
    return session.get('ratings', {})

def get_cart_total():
    """Calculate total price of items in cart"""
    cart = get_cart()
    total = 0
    for product_id, quantity in cart.items():
        product = next((p for p in PRODUCTS if p['id'] == int(product_id)), None)
        if product:
            total += product['price'] * quantity
    return total

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_input_security(text):
    """Validate input for potentially dangerous patterns - returns (is_valid, error_message)"""
    if not text:
        return True, None
    
    import re
    
    # Check for script tags
    if re.search(r'<script[^>]*>', text, re.IGNORECASE):
        return False, "Input contains script tags which are not allowed"
    
    # Check for javascript: protocol
    if re.search(r'javascript:', text, re.IGNORECASE):
        return False, "Javascript protocol is not allowed"
    
    # Check for on* event handlers (e.g., onclick, onerror, etc.)
    if re.search(r'on\w+\s*=', text, re.IGNORECASE):
        return False, "Event handlers are not allowed"
    
    # Check for data: protocol
    if re.search(r'data:\s*text/html', text, re.IGNORECASE):
        return False, "Data URIs are not allowed"
    
    # Check for common SQL injection patterns
    sql_patterns = [r'(\bOR\b|\bAND\b)\s+\d+\s*=\s*\d+', r';\s*DROP\s+TABLE', r'UNION\s+SELECT', r'/\*.*?\*/']
    for pattern in sql_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return False, "Potentially malicious SQL patterns detected"
    
    # Check for HTML tags (basic check)
    if re.search(r'<[^>]+>', text):
        return False, "HTML tags are not allowed"
    
    return True, None

def sanitize_input(text):
    """Sanitize user input to prevent injection attacks (fallback - should not be needed if validation works)"""
    if not text:
        return ""
    
    # Import html for proper escaping
    from html import escape
    
    # Escape HTML special characters to prevent XSS attacks
    text = escape(text, quote=True)
    
    return text

@app.route('/')
def home():
    """Home page with shop information"""
    return render_template('home.html')

@app.route('/products')
def products():
    """Product list page with search functionality"""
    search_query = request.args.get('search', '').lower()
    
    if search_query:
        filtered_products = [p for p in PRODUCTS if search_query in p['name'].lower()]
    else:
        filtered_products = PRODUCTS
    
    # Get ratings for all products
    ratings = get_ratings()
    
    return render_template('products.html', products=filtered_products, search_query=search_query, ratings=ratings)

@app.route('/rate_product/<int:product_id>', methods=['POST'])
def rate_product(product_id):
    """Handle product rating"""
    rating = request.form.get('rating')
    if rating and 1 <= int(rating) <= 5:
        ratings = get_ratings()
        ratings[str(product_id)] = int(rating)
        session['ratings'] = ratings
        product_name = next((p['name'] for p in PRODUCTS if p['id'] == product_id), 'this product')
        flash(f'Thank you for rating {product_name} {rating} stars!', 'success')
    return redirect(url_for('products'))

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    """Add product to shopping cart"""
    cart = get_cart()
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session['cart'] = cart
    flash('Product added to cart!', 'success')
    return redirect(url_for('products'))

@app.route('/cart')
def cart():
    """Shopping cart page"""
    cart = get_cart()
    cart_items = []
    for product_id, quantity in cart.items():
        product = next((p for p in PRODUCTS if p['id'] == int(product_id)), None)
        if product:
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': product['price'] * quantity
            })
    
    total = get_cart_total()
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/update_cart/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    """Update quantity of item in cart"""
    quantity = int(request.form.get('quantity', 1))
    cart = get_cart()
    
    if quantity <= 0:
        cart.pop(str(product_id), None)
        flash('Item removed from cart', 'info')
    else:
        cart[str(product_id)] = quantity
        flash('Cart updated!', 'success')
    
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    """Remove item from cart"""
    cart = get_cart()
    cart.pop(str(product_id), None)
    session['cart'] = cart
    flash('Item removed from cart', 'info')
    return redirect(url_for('cart'))

@app.route('/enquiry', methods=['GET', 'POST'])
def enquiry():
    """Enquiry form page"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        
        # Validation
        errors = []
        if not name:
            errors.append('Name is required')
        elif len(name) > 100:
            errors.append('Name must be less than 100 characters')
        else:
            # Security validation for name
            is_valid, error_msg = validate_input_security(name)
            if not is_valid:
                errors.append(f'Name: {error_msg}')
            
        if not email:
            errors.append('Email is required')
        elif len(email) > 255:
            errors.append('Email must be less than 255 characters')
        elif not validate_email(email):
            errors.append('Invalid email format')
        else:
            # Security validation for email
            is_valid, error_msg = validate_input_security(email)
            if not is_valid:
                errors.append(f'Email: {error_msg}')
            
        if not subject:
            errors.append('Subject is required')
        elif len(subject) > 200:
            errors.append('Subject must be less than 200 characters')
        else:
            # Security validation for subject
            is_valid, error_msg = validate_input_security(subject)
            if not is_valid:
                errors.append(f'Subject: {error_msg}')
            
        if not message:
            errors.append('Message is required')
        elif len(message) > 2000:
            errors.append('Message must be less than 2000 characters')
        else:
            # Security validation for message
            is_valid, error_msg = validate_input_security(message)
            if not is_valid:
                errors.append(f'Message: {error_msg}')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('enquiry.html')
        
        # Sanitize inputs (as a final safety measure)
        name = sanitize_input(name)
        email = sanitize_input(email)
        subject = sanitize_input(subject)
        message = sanitize_input(message)
        
        # Store in session for confirmation page
        session['enquiry_data'] = {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return redirect(url_for('enquiry_confirmation'))
    
    return render_template('enquiry.html')

@app.route('/enquiry/confirmation')
def enquiry_confirmation():
    """Confirmation page after enquiry submission"""
    enquiry_data = session.get('enquiry_data')
    if not enquiry_data:
        return redirect(url_for('enquiry'))
    
    return render_template('enquiry_confirmation.html', data=enquiry_data)

@app.route('/checkout')
def checkout():
    """Checkout page (demo only - no payment processing)"""
    cart = get_cart()
    if not cart:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('cart'))
    
    cart_items = []
    for product_id, quantity in cart.items():
        product = next((p for p in PRODUCTS if p['id'] == int(product_id)), None)
        if product:
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': product['price'] * quantity
            })
    
    total = get_cart_total()
    
    # Clear the cart after checkout
    session['cart'] = {}
    flash('Thank you for your order! Your cart has been cleared.', 'success')
    
    return render_template('checkout.html', cart_items=cart_items, total=total)

if __name__ == '__main__':
    app.run(debug=True, port=5001)

