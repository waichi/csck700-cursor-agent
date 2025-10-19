# csck700-cursor-agent

Cursor Agent Mode enables intelligent automation and code generation, facilitating the rapid development of web applications. This repository demonstrates how to leverage Cursor Agent Mode for web app creation, including setup, configuration, and example workflows.

## Shopping Web Application

This project contains a fully functional shopping web application built with Flask, demonstrating the capabilities of AI-assisted development using Cursor Agent Mode.

### Features

- **Home Page**: Display shop information and navigation
- **Product List**: Browse 20 computer accessories with search functionality
- **Product Rating**: Rate products from 1-5 stars
- **Shopping Cart**: Add, update, and remove items with running totals
- **Enquiry Form**: Contact form with validation and confirmation
- **Responsive Design**: Modern, mobile-friendly UI

### Technology Stack

- **Python**: 3.11+
- **Flask**: 2.x (Lightweight web framework)
- **HTML/CSS**: Responsive design with modern UI
- **Session Management**: In-memory cart persistence

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/waichi/csck700-cursor-agent.git
   cd csck700-cursor-agent
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the Flask development server**:
   ```bash
   python app.py
   ```

2. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

### Project Structure

```
csck700-cursor-agent/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── templates/             # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── products.html
│   ├── cart.html
│   ├── enquiry.html
│   ├── enquiry_confirmation.html
│   └── checkout.html
└── static/                # Static files
    ├── css/
    │   └── style.css     # Responsive stylesheet
    └── images/           # Product images and logo
```

### Application Routes

- `/` - Home page with shop information
- `/products` - Product list with search
- `/rate_product/<id>` - Rate a product
- `/add_to_cart/<id>` - Add product to cart
- `/cart` - View shopping cart
- `/update_cart/<id>` - Update item quantity
- `/remove_from_cart/<id>` - Remove item from cart
- `/enquiry` - Contact form
- `/enquiry/confirmation` - Form submission confirmation
- `/checkout` - Checkout page (demo)

### Features Implemented

✅ Navigation menu on all pages  
✅ Home page with shop information (IKW Store)  
✅ Product list with 20 computer accessories  
✅ Case-insensitive product search  
✅ Product rating system (1-5 stars)  
✅ Shopping cart with add/update/remove  
✅ Running subtotal and total calculation  
✅ Enquiry form with validation  
✅ Email format validation  
✅ Input sanitization (injection attack prevention)  
✅ Confirmation page after form submission  
✅ Responsive, modern UI design  
✅ Session-based cart persistence  

### Development Notes

This application was developed as part of an observational case study on Developer-AI collaboration using Cursor Agent Mode. The application demonstrates rapid web development capabilities with AI assistance while maintaining code quality and following software engineering best practices.

### Future Enhancements

- Database integration for persistent data storage
- User authentication and accounts
- Payment gateway integration
- Product image upload functionality
- Order history and tracking
- Email notifications
- Product reviews and comments

### License

This project is created for educational and research purposes as part of the CSCK700 course.

