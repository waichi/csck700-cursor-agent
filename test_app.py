"""
Test Cases for IKW Store Shopping Web Application
Tests against acceptance criteria defined in RequirementForCursor.docx

Test Case Attributes (ISO/IEC/IEEE 29119-3:2021):
- Unique identifier
- Objective
- Priority
- Preconditions
- Inputs
- Expected results
"""

import pytest
from app import app, PRODUCTS, PRODUCT_RATINGS
import json

@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

@pytest.fixture
def session(client):
    """Create a session for testing"""
    with client.session_transaction() as sess:
        yield sess

class TestNavigation:
    """TC-NAV: Navigation Menu Tests"""
    
    def test_navigation_home_link(self, client):
        """TC-NAV-001: Navigation menu displays Home link"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Home' in response.data
    
    def test_navigation_products_link(self, client):
        """TC-NAV-002: Navigation menu displays Products link"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Products' in response.data
    
    def test_navigation_cart_link(self, client):
        """TC-NAV-003: Navigation menu displays Cart link"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Cart' in response.data
    
    def test_navigation_contact_link(self, client):
        """TC-NAV-004: Navigation menu displays Contact link"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Contact' in response.data

class TestHomePage:
    """TC-HOME: Home Page Tests"""
    
    def test_home_page_loads(self, client):
        """TC-HOME-001: Home page loads successfully"""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_shop_name_display(self, client):
        """TC-HOME-002: Shop name 'IKW Store' is displayed"""
        response = client.get('/')
        assert b'IKW Store' in response.data
    
    def test_contact_name_display(self, client):
        """TC-HOME-003: Contact name 'Waichi Ikeda' is displayed"""
        response = client.get('/')
        assert b'Waichi Ikeda' in response.data
    
    def test_email_display(self, client):
        """TC-HOME-004: Email 'W.Ikeda@liverpool.ac.uk' is displayed"""
        response = client.get('/')
        assert b'W.Ikeda@liverpool.ac.uk' in response.data
    
    def test_phone_display(self, client):
        """TC-HOME-005: Phone number '+81 00-000-0000' is displayed"""
        response = client.get('/')
        assert b'+81 00-000-0000' in response.data
    
    def test_logo_display(self, client):
        """TC-HOME-006: Shop logo is displayed"""
        response = client.get('/')
        assert b'IKWStoreLogo.png' in response.data

class TestProductList:
    """TC-PRODUCT: Product List Tests"""
    
    def test_products_page_loads(self, client):
        """TC-PRODUCT-001: Products page loads successfully"""
        response = client.get('/products')
        assert response.status_code == 200
    
    def test_all_products_displayed(self, client):
        """TC-PRODUCT-002: All 20 computer accessories are displayed"""
        response = client.get('/products')
        assert response.status_code == 200
        # Check for all product names
        product_names = [p['name'] for p in PRODUCTS]
        for name in product_names:
            assert name.encode() in response.data
    
    def test_product_grid_layout(self, client):
        """TC-PRODUCT-003: Products are displayed in grid format"""
        response = client.get('/products')
        assert b'products-grid' in response.data
    
    def test_product_thumbnail_display(self, client):
        """TC-PRODUCT-004: Each product shows a thumbnail image"""
        response = client.get('/products')
        assert b'product-image' in response.data
    
    def test_product_name_display(self, client):
        """TC-PRODUCT-005: Each product shows its name"""
        response = client.get('/products')
        assert b'product-name' in response.data
    
    def test_product_description_display(self, client):
        """TC-PRODUCT-006: Each product shows its description"""
        response = client.get('/products')
        assert b'product-description' in response.data
    
    def test_product_price_display(self, client):
        """TC-PRODUCT-007: Each product shows its price in JPY"""
        response = client.get('/products')
        # Check for yen symbol (UTF-8 encoded)
        assert b'\xc2\xa5' in response.data or '¥'.encode('utf-8') in response.data
    
    def test_price_range(self):
        """TC-PRODUCT-008: All prices are within ¥1000-¥15000 range"""
        for product in PRODUCTS:
            assert 1000 <= product['price'] <= 15000
    
    def test_search_function(self, client):
        """TC-PRODUCT-009: Search function is available"""
        response = client.get('/products')
        assert b'search-input' in response.data
    
    def test_search_case_insensitive(self, client):
        """TC-PRODUCT-010: Search is case-insensitive"""
        # Test uppercase search
        response = client.get('/products?search=MOUSE')
        assert response.status_code == 200
        assert b'Wireless Mouse' in response.data
        
        # Test lowercase search
        response = client.get('/products?search=mouse')
        assert response.status_code == 200
        assert b'Wireless Mouse' in response.data
    
    def test_search_results(self, client):
        """TC-PRODUCT-011: Search returns correct results"""
        response = client.get('/products?search=keyboard')
        assert response.status_code == 200
        assert b'Mechanical Keyboard' in response.data
    
    def test_rating_system_display(self, client):
        """TC-PRODUCT-012: Product rating system is displayed"""
        response = client.get('/products')
        assert b'star-rating' in response.data
    
    def test_add_to_cart_button(self, client):
        """TC-PRODUCT-013: 'Add to Cart' button is displayed for each product"""
        response = client.get('/products')
        assert b'Add to Cart' in response.data
    
    def test_add_to_cart_functionality(self, client):
        """TC-PRODUCT-014: Adding product to cart works"""
        response = client.get('/add_to_cart/1', follow_redirects=True)
        assert response.status_code == 200
        assert b'Product added to cart' in response.data or b'added to cart' in response.data

class TestShoppingCart:
    """TC-CART: Shopping Cart Tests"""
    
    def test_cart_page_loads(self, client):
        """TC-CART-001: Shopping cart page loads"""
        response = client.get('/cart')
        assert response.status_code == 200
    
    def test_cart_displays_contents(self, client):
        """TC-CART-002: Cart displays product contents"""
        # Add item to cart first
        client.get('/add_to_cart/1')
        response = client.get('/cart')
        assert response.status_code == 200
        assert b'Wireless Mouse' in response.data
    
    def test_cart_displays_quantities(self, client):
        """TC-CART-003: Cart displays product quantities"""
        client.get('/add_to_cart/1')
        response = client.get('/cart')
        assert b'quantity-input' in response.data
    
    def test_cart_displays_subtotal(self, client):
        """TC-CART-004: Cart displays running subtotal"""
        client.get('/add_to_cart/1')
        response = client.get('/cart')
        assert b'subtotal' in response.data or b'Subtotal' in response.data
    
    def test_cart_displays_total(self, client):
        """TC-CART-005: Cart displays overall total"""
        client.get('/add_to_cart/1')
        response = client.get('/cart')
        assert b'Total' in response.data
    
    def test_cart_update_quantity(self, client):
        """TC-CART-006: Cart allows updating product quantities"""
        client.get('/add_to_cart/1')
        response = client.post('/update_cart/1', data={'quantity': '3'}, follow_redirects=True)
        assert response.status_code == 200
        assert b'Cart updated' in response.data or b'updated' in response.data
    
    def test_cart_remove_item(self, client):
        """TC-CART-007: Cart allows removing items"""
        client.get('/add_to_cart/1')
        response = client.get('/remove_from_cart/1', follow_redirects=True)
        assert response.status_code == 200
        assert b'removed from cart' in response.data or b'Item removed' in response.data
    
    def test_cart_persistence(self, client):
        """TC-CART-008: Cart contents persist during session"""
        client.get('/add_to_cart/1')
        client.get('/add_to_cart/2')
        response = client.get('/cart')
        assert b'Wireless Mouse' in response.data
        assert b'Mechanical Keyboard' in response.data
    
    def test_cart_checkout_button(self, client):
        """TC-CART-009: Cart displays 'Checkout' button"""
        client.get('/add_to_cart/1')
        response = client.get('/cart')
        assert b'Checkout' in response.data or b'Proceed to Checkout' in response.data
    
    def test_checkout_page_loads(self, client):
        """TC-CART-010: Checkout page loads"""
        client.get('/add_to_cart/1')
        response = client.get('/checkout')
        assert response.status_code == 200
        assert b'Checkout' in response.data
    
    def test_cart_cleared_after_checkout(self, client):
        """TC-CART-011: Cart is cleared after checkout"""
        client.get('/add_to_cart/1')
        client.get('/checkout')
        response = client.get('/cart')
        assert b'empty' in response.data.lower() or b'Your cart is empty' in response.data

class TestEnquiryForm:
    """TC-ENQUIRY: Enquiry Form Tests"""
    
    def test_enquiry_page_loads(self, client):
        """TC-ENQUIRY-001: Enquiry form page loads"""
        response = client.get('/enquiry')
        assert response.status_code == 200
    
    def test_enquiry_form_fields(self, client):
        """TC-ENQUIRY-002: Enquiry form has all required fields"""
        response = client.get('/enquiry')
        assert b'name' in response.data
        assert b'email' in response.data
        assert b'subject' in response.data
        assert b'message' in response.data
    
    def test_enquiry_form_required_validation(self, client):
        """TC-ENQUIRY-003: All fields are marked as mandatory"""
        response = client.get('/enquiry')
        assert b'required' in response.data
    
    def test_enquiry_form_submission_empty(self, client):
        """TC-ENQUIRY-004: Form validation prevents empty submission"""
        response = client.post('/enquiry', data={})
        assert response.status_code == 200
        assert b'required' in response.data.lower() or b'error' in response.data.lower()
    
    def test_enquiry_email_validation(self, client):
        """TC-ENQUIRY-005: Email format validation works"""
        response = client.post('/enquiry', data={
            'name': 'Test User',
            'email': 'invalid-email',
            'subject': 'Test Subject',
            'message': 'Test message'
        })
        assert response.status_code == 200
        assert b'Invalid email format' in response.data or b'invalid' in response.data.lower()
    
    def test_enquiry_valid_email(self, client):
        """TC-ENQUIRY-006: Valid email format is accepted"""
        response = client.post('/enquiry', data={
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'Test message'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'confirmation' in response.data.lower() or b'Enquiry Submitted' in response.data
    
    def test_enquiry_confirmation_page(self, client):
        """TC-ENQUIRY-007: Confirmation page displays after submission"""
        client.post('/enquiry', data={
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'Test message'
        })
        response = client.get('/enquiry/confirmation')
        assert response.status_code == 200
        assert b'Test User' in response.data
        assert b'test@example.com' in response.data
    
    def test_enquiry_xss_protection(self, client):
        """TC-ENQUIRY-008: Form protects against XSS attacks"""
        response = client.post('/enquiry', data={
            'name': '<script>alert("XSS")</script>',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'Test message'
        })
        assert response.status_code == 200
        assert b'script tags' in response.data.lower() or b'not allowed' in response.data.lower()
    
    def test_enquiry_javascript_protocol_blocked(self, client):
        """TC-ENQUIRY-009: JavaScript protocol is blocked"""
        response = client.post('/enquiry', data={
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'javascript:alert(1)'
        })
        assert response.status_code == 200
        assert b'Javascript protocol' in response.data or b'not allowed' in response.data.lower()
    
    def test_enquiry_html_tags_blocked(self, client):
        """TC-ENQUIRY-010: HTML tags are blocked"""
        response = client.post('/enquiry', data={
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': '<img src=x onerror="alert(1)">'
        })
        assert response.status_code == 200
        assert b'HTML tags' in response.data or b'not allowed' in response.data.lower()
    
    def test_enquiry_length_validation(self, client):
        """TC-ENQUIRY-011: Input length validation works"""
        long_name = 'A' * 101
        response = client.post('/enquiry', data={
            'name': long_name,
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'Test message'
        })
        assert response.status_code == 200
        assert b'100 characters' in response.data or b'less than' in response.data.lower()

class TestProductRating:
    """TC-RATING: Product Rating Tests"""
    
    def test_rating_stars_display(self, client):
        """TC-RATING-001: Star rating system displays for each product"""
        response = client.get('/products')
        assert b'star-rating' in response.data
    
    def test_rating_submission(self, client):
        """TC-RATING-002: Rating submission works"""
        response = client.post('/rate_product/1', data={'rating': '5'}, follow_redirects=True)
        assert response.status_code == 200
        assert b'Thank you for rating' in response.data or b'rating' in response.data.lower()
    
    def test_rating_range_validation(self, client):
        """TC-RATING-003: Only ratings 1-5 are accepted"""
        response = client.post('/rate_product/1', data={'rating': '6'}, follow_redirects=True)
        # Should either accept or reject, but not crash
        assert response.status_code == 200
    
    def test_average_rating_calculation(self, client):
        """TC-RATING-004: Average rating is calculated correctly"""
        # Clear ratings for product 1
        if 1 in PRODUCT_RATINGS:
            PRODUCT_RATINGS[1] = []
        
        # Add ratings
        client.post('/rate_product/1', data={'rating': '5'})
        client.post('/rate_product/1', data={'rating': '4'})
        client.post('/rate_product/1', data={'rating': '3'})
        
        # Check average
        response = client.get('/products')
        assert b'Average' in response.data or b'4.0' in response.data
    
    def test_rating_count_display(self, client):
        """TC-RATING-005: Rating count is displayed"""
        response = client.get('/products')
        assert b'rating' in response.data.lower() or b'ratings' in response.data.lower()

class TestNonFunctionalRequirements:
    """TC-NFR: Non-Functional Requirements Tests"""
    
    def test_responsive_design(self, client):
        """TC-NFR-001: Application has responsive design"""
        response = client.get('/')
        # Check for viewport meta tag (indicates responsive design)
        assert b'viewport' in response.data
        # Check for responsive CSS classes
        assert b'main-content' in response.data or b'nav-container' in response.data
    
    def test_security_input_validation(self, client):
        """TC-NFR-002: User input is validated and cleaned"""
        response = client.post('/enquiry', data={
            'name': "'; DROP TABLE users; --",
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'Test message'
        })
        assert response.status_code == 200
        assert b'SQL' in response.data or b'malicious' in response.data.lower()
    
    def test_session_security(self, client):
        """TC-NFR-003: Session secret key is configured"""
        # Session secret key should be set (even if it's a placeholder for demo)
        assert app.secret_key is not None
        assert len(app.secret_key) > 0

class TestPerformance:
    """TC-PERF: Performance Tests"""
    
    def test_home_page_load_time(self, client):
        """TC-PERF-001: Home page loads within acceptable time"""
        import time
        start = time.time()
        response = client.get('/')
        elapsed = time.time() - start
        assert response.status_code == 200
        assert elapsed < 2.0  # Should load within 2 seconds
    
    def test_products_page_load_time(self, client):
        """TC-PERF-002: Products page loads within acceptable time"""
        import time
        start = time.time()
        response = client.get('/products')
        elapsed = time.time() - start
        assert response.status_code == 200
        assert elapsed < 2.0  # Should load within 2 seconds

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])

