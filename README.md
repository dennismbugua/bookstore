# 📚 Modern Django Bookstore with PayPal Integration

A full-featured, modern e-commerce bookstore built with Django, featuring PayPal payments, beautiful UI/UX, and comprehensive order management.

## 🎯 Business Value & Use Cases

### Why This Matters for Business
- **E-commerce Ready**: Complete online bookstore with cart, checkout, and payment processing
- **Scalable Architecture**: Built on Django framework for enterprise-level scalability
- **Payment Integration**: Secure PayPal integration with sandbox testing capabilities
- **Modern UI/UX**: Professional design that converts visitors to customers
- **Order Management**: Complete order tracking and email notifications
- **Mobile Responsive**: Works perfectly on all devices and screen sizes

### Perfect For
- 📖 **Independent Bookstores** transitioning to online sales
- 🏢 **Publishers** selling directly to consumers
- 🎓 **Educational Institutions** selling course materials
- 👥 **Book Clubs** and literary communities
- 📱 **Digital Marketplaces** for books and publications

## ✨ Key Features

### 🛒 E-commerce Functionality
- **Product Catalog**: Browse books by categories, authors, and genres
- **Shopping Cart**: Add/remove items with real-time updates
- **Secure Checkout**: Multi-step checkout process with validation
- **Payment Processing**: PayPal integration with sandbox testing
- **Order Management**: Complete order tracking and history

### 🎨 Modern UI/UX
- **Responsive Design**: Mobile-first approach with Bootstrap integration
- **Animated Interactions**: Smooth animations with AOS (Animate On Scroll)
- **Professional Styling**: Glass-morphism effects and gradient designs
- **Enhanced Forms**: Beautiful form validation and user feedback
- **Interactive Elements**: Hover effects, loading states, and micro-interactions

### 🔧 Technical Features
- **Django 5.0.4**: Latest Django framework with modern features
- **PostgreSQL Ready**: Database configuration for production
- **HTTPS Support**: SSL/TLS encryption for secure transactions
- **Email Notifications**: Beautiful HTML emails for order confirmations
- **Environment Configuration**: Secure configuration with .env files
- **Country Selection**: Global country support with django-countries

## 🎬 Video Demo 📺

> **[ Click Here to Watch the Full Demo Video Here](https://www.youtube.com/watch?v=4RjOXi8lB0g)** 👇
>
> [![Book Store Demo](https://github.com/dennismbugua/bookstore/blob/main/files/YT/Book%20Store.PNG?raw=true)](https://www.youtube.com/watch?v=4RjOXi8lB0g)
> 
> - Product browsing and search functionality
> - Adding items to cart and checkout process
> - PayPal payment integration
> - Order confirmation and email notifications
> - Admin panel features
> - Responsive design on different devices

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git
- PostgreSQL (optional, uses SQLite by default)

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/django-bookstore.git
cd django-bookstore
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the project root:

```env
# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# PayPal Configuration
PAYPAL_TEST=True
PAYPAL_CLIENT_ID=your-paypal-client-id
PAYPAL_CLIENT_SECRET=your-paypal-client-secret
PAYPAL_BUSINESS_EMAIL=your-sandbox-business-email

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com

# Shipping Configuration
SHIPPING_COST=100

# SSL Configuration
SECURE_SSL_REDIRECT=False
SECURE_PROXY_SSL_HEADER_NAME=HTTP_X_FORWARDED_PROTO
SECURE_PROXY_SSL_HEADER_VALUE=https
```

### 5. Database Setup
```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 6. Load Sample Data (Optional)
```bash
# Load sample books and categories
python manage.py loaddata fixtures/sample_data.json
```

### 7. Run Development Server
```bash
# HTTP (development)
python manage.py runserver

# HTTPS (for PayPal testing)
python manage.py runsslserver
```

Visit `https://127.0.0.1:8000` to see your bookstore!

## 🔧 PayPal Sandbox Setup

### 1. Create PayPal Developer Account
1. Go to [PayPal Developer](https://developer.paypal.com/)
2. Sign in or create an account
3. Navigate to "My Apps & Credentials"

### 2. Create Sandbox Application
1. Click "Create App"
2. Choose "Sandbox" environment
3. Select "Merchant" account type
4. Note down your Client ID and Client Secret

### 3. Create Test Accounts
1. Go to "Sandbox" → "Accounts"
2. Create a **Business Account** (for receiving payments)
3. Create a **Personal Account** (for making test payments)
4. Fund the personal account with test money

### 4. Update Configuration
Add your credentials to the `.env` file:
```env
PAYPAL_CLIENT_ID=your-sandbox-client-id
PAYPAL_CLIENT_SECRET=your-sandbox-client-secret
PAYPAL_BUSINESS_EMAIL=your-sandbox-business-email
```

## 📁 Project Structure

```
django-bookstore/
├── bookstore/              # Main project directory
│   ├── settings.py         # Django settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI configuration
├── store/                 # Store app (products, categories)
│   ├── models.py          # Book, Category models
│   ├── views.py           # Store views
│   ├── templates/         # Store templates
│   └── static/            # CSS, JS, images
├── cart/                  # Shopping cart app
│   ├── cart.py            # Cart session management
│   ├── views.py           # Cart views
│   └── templates/         # Cart templates
├── order/                 # Order management app
│   ├── models.py          # Order, OrderItem models
│   ├── views.py           # Order and PayPal views
│   └── templates/         # Order templates
├── templates/             # Global templates
├── static/                # Global static files
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables example
└── manage.py             # Django management script
```

## 🎨 Customization Guide

### Adding New Payment Methods
1. Update `ORDER_PAYMENT_CHOICES` in `order/models.py`
2. Add payment fields in `order/templates/order/order.html`
3. Create payment processing views in `order/views.py`
4. Add corresponding URL patterns

### Customizing Email Templates
1. Edit templates in `order/templates/order/emails/`
2. Update email context in `order/views.py`
3. Customize CSS styles for better branding

### Adding New Book Fields
1. Update `Book` model in `store/models.py`
2. Create and run migrations
3. Update templates to display new fields
4. Add form fields if needed

## 🚀 Production Deployment

### Environment Variables for Production
```env
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
PAYPAL_TEST=False
SECURE_SSL_REDIRECT=True
```

### Recommended Hosting Platforms
- **Heroku**: Easy deployment with PostgreSQL addon
- **DigitalOcean**: App Platform or Droplets
- **AWS**: Elastic Beanstalk or EC2
- **Railway**: Modern platform with simple deployment

### Pre-deployment Checklist
- [ ] Update `ALLOWED_HOSTS` with your domain
- [ ] Set `DEBUG=False` in production
- [ ] Use PostgreSQL for production database
- [ ] Configure proper email backend (SendGrid, SES, etc.)
- [ ] Set up SSL certificate
- [ ] Configure static files serving (WhiteNoise, S3, etc.)
- [ ] Switch to live PayPal credentials

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🆘 Support & Troubleshooting

### Common Issues

**PayPal "Something doesn't look right" Error**
- Ensure you're using sandbox business email in settings
- Check that Client ID matches your sandbox app
- Verify you're logged in as a buyer (personal account) not seller

**CSRF Token Errors**
- Check `ALLOWED_HOSTS` configuration
- Ensure `.env` file is properly loaded
- Verify HTTPS is enabled for PayPal callbacks

**Email Not Sending**
- Check email configuration in `.env`
- Use app-specific passwords for Gmail
- Verify SMTP settings with your email provider

## 🌟 Acknowledgments

- Django community for the amazing framework
- PayPal for payment processing capabilities
- Bootstrap for responsive design components
- Font Awesome for beautiful icons
- AOS library for smooth animations

---

**⭐ If this project helped you, please give it a star on GitHub!**

*Built with ❤️ for the book-loving community*




