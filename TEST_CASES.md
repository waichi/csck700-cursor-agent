# Test Case Specification

## Overview
This document contains test cases for the IKW Store shopping web application, designed to verify all functional requirements specified in `RequirementForCursor.docx`.

**Test Standard:** ISO/IEC/IEEE 29119-3:2021 (Test Documentation)

## Test Environment
- **Application:** IKW Store Shopping Web Application
- **Framework:** Flask 3.0.0
- **Testing Tool:** pytest 7.4.3
- **Python Version:** 3.11+

## Test Execution

### Running All Tests
```bash
pytest test_app.py -v
```

### Running Specific Test Classes
```bash
# Test Navigation
pytest test_app.py::TestNavigation -v

# Test Home Page
pytest test_app.py::TestHomePage -v

# Test Product List
pytest test_app.py::TestProductList -v

# Test Shopping Cart
pytest test_app.py::TestShoppingCart -v

# Test Enquiry Form
pytest test_app.py::TestEnquiryForm -v

# Test Product Rating
pytest test_app.py::TestProductRating -v

# Test Non-Functional Requirements
pytest test_app.py::TestNonFunctionalRequirements -v

# Test Performance
pytest test_app.py::TestPerformance -v
```

### Running with Coverage Report
```bash
pytest test_app.py --cov=app --cov-report=html
```

## Test Cases Summary

### TC-NAV: Navigation Tests (4 tests)
- TC-NAV-001: Navigation menu displays Home link
- TC-NAV-002: Navigation menu displays Products link
- TC-NAV-003: Navigation menu displays Cart link
- TC-NAV-004: Navigation menu displays Contact link

### TC-HOME: Home Page Tests (6 tests)
- TC-HOME-001: Home page loads successfully
- TC-HOME-002: Shop name 'IKW Store' is displayed
- TC-HOME-003: Contact name 'Waichi Ikeda' is displayed
- TC-HOME-004: Email 'W.Ikeda@liverpool.ac.uk' is displayed
- TC-HOME-005: Phone number '+81 00-000-0000' is displayed
- TC-HOME-006: Shop logo is displayed

### TC-PRODUCT: Product List Tests (14 tests)
- TC-PRODUCT-001: Products page loads successfully
- TC-PRODUCT-002: All 20 computer accessories are displayed
- TC-PRODUCT-003: Products are displayed in grid format
- TC-PRODUCT-004: Each product shows a thumbnail image
- TC-PRODUCT-005: Each product shows its name
- TC-PRODUCT-006: Each product shows its description
- TC-PRODUCT-007: Each product shows its price in JPY
- TC-PRODUCT-008: All prices are within ¥1000-¥15000 range
- TC-PRODUCT-009: Search function is available
- TC-PRODUCT-010: Search is case-insensitive
- TC-PRODUCT-011: Search returns correct results
- TC-PRODUCT-012: Product rating system is displayed
- TC-PRODUCT-013: 'Add to Cart' button is displayed for each product
- TC-PRODUCT-014: Adding product to cart works

### TC-CART: Shopping Cart Tests (11 tests)
- TC-CART-001: Shopping cart page loads
- TC-CART-002: Cart displays product contents
- TC-CART-003: Cart displays product quantities
- TC-CART-004: Cart displays running subtotal
- TC-CART-005: Cart displays overall total
- TC-CART-006: Cart allows updating product quantities
- TC-CART-007: Cart allows removing items
- TC-CART-008: Cart contents persist during session
- TC-CART-009: Cart displays 'Checkout' button
- TC-CART-010: Checkout page loads
- TC-CART-011: Cart is cleared after checkout

### TC-ENQUIRY: Enquiry Form Tests (11 tests)
- TC-ENQUIRY-001: Enquiry form page loads
- TC-ENQUIRY-002: Enquiry form has all required fields
- TC-ENQUIRY-003: All fields are marked as mandatory
- TC-ENQUIRY-004: Form validation prevents empty submission
- TC-ENQUIRY-005: Email format validation works
- TC-ENQUIRY-006: Valid email format is accepted
- TC-ENQUIRY-007: Confirmation page displays after submission
- TC-ENQUIRY-008: Form protects against XSS attacks
- TC-ENQUIRY-009: JavaScript protocol is blocked
- TC-ENQUIRY-010: HTML tags are blocked
- TC-ENQUIRY-011: Input length validation works

### TC-RATING: Product Rating Tests (5 tests)
- TC-RATING-001: Star rating system displays for each product
- TC-RATING-002: Rating submission works
- TC-RATING-003: Only ratings 1-5 are accepted
- TC-RATING-004: Average rating is calculated correctly
- TC-RATING-005: Rating count is displayed

### TC-NFR: Non-Functional Requirements Tests (3 tests)
- TC-NFR-001: Application has responsive design
- TC-NFR-002: User input is validated and cleaned
- TC-NFR-003: Session secret key is configured

### TC-PERF: Performance Tests (2 tests)
- TC-PERF-001: Home page loads within acceptable time
- TC-PERF-002: Products page loads within acceptable time

## Total Test Cases: 56

## Acceptance Criteria
All functional requirements defined in the requirements document are "must-have" criteria. Every test case specified in this document shall be executed and pass without error.

## Test Results
Run `pytest test_app.py -v` to see detailed test results.

## Notes
- Tests use pytest fixtures for client and session management
- Tests are isolated and can be run independently
- Some tests may modify global state (PRODUCT_RATINGS) - consider adding cleanup
- For production use, add database integration tests
- Consider adding end-to-end tests with Selenium/Playwright

