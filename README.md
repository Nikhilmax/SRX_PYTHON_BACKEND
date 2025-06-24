# SRX eCommerce Application BackEnd

This is a FastAPI-based eCommerce application designed to manage products, users, and orders efficiently. The application provides a RESTful API for various operations related to eCommerce functionalities.


## Project Structure

```
SRX_PY_BACKEND
├── app
│   ├── main.py                # Entry point of the FastAPI application
│   ├── api                    # API module containing endpoints
│   │   ├── __init__.py
│   │   ├── endpoints          # Contains individual endpoint files
│   │   │   ├── __init__.py
│   │   │   ├── products.py    # Product-related API endpoints
│   │   │   ├── users.py       # User management API endpoints
│   │   │   ├── orders.py      # Order processing API endpoints
│   │   │   └── auth.py        # Authentication API endpoints
│   ├── core                   # Core functionalities and configurations
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration settings
│   │   └── security.py        # Security functions
│   ├── crud                   # CRUD operations for database interactions
│   │   ├── __init__.py
│   │   ├── crud_product.py     # Product CRUD operations
│   │   ├── crud_user.py        # User CRUD operations
│   │   └── crud_order.py       # Order CRUD operations
│   ├── db                     # Database management
│   │   ├── __init__.py
│   │   ├── base.py            # Base model for SQLAlchemy
│   │   ├── models.py          # Database models
│   │   └── session.py         # Database session management
│   ├── schemas                # Pydantic schemas for data validation
│   │   ├── __init__.py
│   │   ├── product.py         # Product schemas
│   │   ├── user.py            # User schemas
│   │   └── order.py           # Order schemas
│   └── utils                  # Utility functions
│       ├── __init__.py
│       └── helpers.py         # Helper functions
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd SRX_PY_BACKEND
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   uvicorn app.main:app --reload
   ```

## Usage Guidelines

- **API Endpoints**
  - Products: `/api/products`
  - Users: `/api/users`
  - Orders: `/api/orders`
  - Authentication: `/api/auth`

Refer to the individual endpoint files for detailed information on available routes and their functionalities.
