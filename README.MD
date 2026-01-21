# 🛒 NexCart Backend

AI-powered e-commerce platform backend built with Django REST Framework.

## 🚀 Features

- **JWT Authentication** - Secure user authentication
- **Product Management** - Full CRUD operations for products
- **Smart Cart System** - Authentication-required shopping cart
- **AI Recommendations** - Machine learning-powered product recommendations
- **Payment Integration** - MeSomb mobile money payments (MTN, Orange)
- **OAuth2 Social Login** - Google, Discord, Microsoft
- **Order Management** - Complete order lifecycle
- **Wishlist** - Save favorite products
- **Reviews & Ratings** - Product review system
- **Admin Dashboard** - Django admin for management
- **Image Storage** - Cloudinary integration
- **Background Tasks** - Celery for async operations
- **Caching** - Redis for performance

## 🛠️ Tech Stack

- **Framework**: Django 5.2 + Django REST Framework
- **Database**: PostgreSQL (Neon)
- **Cache**: Redis (Upstash)
- **Storage**: Cloudinary
- **Task Queue**: Celery + Redis
- **Authentication**: JWT (Simple JWT)
- **ML**: Scikit-learn, Pandas, NumPy
- **Deployment**: Render

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL (Neon account)
- Redis (Upstash account)
- Cloudinary account

## 🔧 Local Development Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/nexcart-backend.git
cd nexcart-backend
```

### 2. Create virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Required variables:
- `SECRET_KEY` - Django secret key
- `DATABASE_URL` - Neon PostgreSQL URL
- `REDIS_URL` - Redis connection URL
- `CLOUDINARY_*` - Cloudinary credentials
- `GOOGLE_CLIENT_*` - OAuth credentials (optional)
- `MESOMB_*` - Payment gateway credentials (optional)

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create superuser

```bash
python manage.py createsuperuser
```

### 7. Run development server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`
Admin panel at `http://localhost:8000/admin/`

## 🚀 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions to Render.

Quick deploy:
1. Push code to GitHub
2. Connect repository to Render
3. Set environment variables
4. Deploy!

## 📡 API Endpoints

### Authentication
- `POST /api/users/auth/register/` - Register new user
- `POST /api/users/auth/login/` - Login
- `POST /api/users/auth/token/refresh/` - Refresh JWT token
- `GET /api/users/auth/profile/` - Get user profile
- `PATCH /api/users/auth/profile/` - Update profile

### Products
- `GET /api/products/` - List all products
- `GET /api/products/{id}/` - Get product details
- `GET /api/products/featured/` - Featured products
- `GET /api/recommendations/` - AI-powered recommendations

### Cart (Authentication Required)
- `GET /api/cart/` - Get user cart
- `POST /api/cart/add/` - Add item to cart
- `PATCH /api/cart/items/{id}/` - Update cart item
- `DELETE /api/cart/items/{id}/` - Remove from cart
- `DELETE /api/cart/clear/` - Clear cart

### Orders
- `GET /api/orders/` - List user orders
- `GET /api/orders/{id}/` - Order details
- `POST /api/orders/create/` - Create order from cart

### Payments
- `POST /api/payments/initiate/` - Initiate mobile payment
- `GET /api/payments/status/{transaction_id}/` - Check status

### Wishlist
- `GET /api/wishlist/` - Get wishlist
- `POST /api/wishlist/add/` - Add to wishlist
- `DELETE /api/wishlist/{id}/` - Remove from wishlist

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run with coverage
coverage run manage.py test
coverage report
```

## 📦 Project Structure

```
backend/
├── apps/
│   ├── users/          # User management & authentication
│   ├── products/       # Product catalog
│   ├── orders/         # Orders & cart
│   ├── payments/       # Payment processing
│   └── recommendations/# AI recommendations
├── core/
│   ├── config/         # Django settings
│   │   ├── settings/
│   │   │   ├── base.py
│   │   │   ├── dev.py
│   │   │   └── prod.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── common/         # Shared utilities
│   └── middleware/     # Custom middleware
├── ml_models/          # ML models for recommendations
├── staticfiles/        # Static files
├── media/              # User uploads (Cloudinary)
├── logs/               # Application logs
├── manage.py
├── requirements.txt
├── build.sh            # Deployment build script
├── render.yaml         # Render configuration
└── .env.example        # Environment variables template
```

## 🔐 Security Features

- JWT token authentication
- Password hashing with Django's PBKDF2
- CORS protection
- CSRF protection
- Rate limiting
- SQL injection protection (Django ORM)
- XSS protection
- HTTPS enforcement (production)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👥 Authors

- Your Name - [@yourhandle](https://github.com/yourhandle)

## 🙏 Acknowledgments

- Django REST Framework team
- Neon for serverless PostgreSQL
- Render for hosting
- Upstash for serverless Redis

## 📞 Support

For support, email support@nexcart.com or create an issue on GitHub.

---

**Built with ❤️ using Django REST Framework**
