# E-Commerce Cart REST API

A lightweight and clean RESTful backend service built with **FastAPI**, **SQLAlchemy ORM**, and **Pydantic**. The project provides a simple shopping cart system with user management, cart and item operations, and automatic calculation of cart totals using an SQLite database.

## Features

- **User Management**
  - Create users with unique email addresses.
  - Retrieve existing users.
  - Validate user input using Pydantic.

- **Relational Cart Workflow**
  - One-to-many relationship between users and shopping carts (`UserModel` ↔ `BasketModel`).
  - One-to-many relationship between shopping carts and items (`BasketModel` ↔ `ItemModel`).
  - Automatic orphan cleanup and cascade deletion for related items.

- **Cart & Item CRUD Operations**
  - Create dedicated shopping carts for users.
  - Add items to active carts.
  - Store item details such as name, brand, unit price, and quantity.
  - Update item quantities and other item details.
  - Remove items from a shopping cart.

- **Live Cart Total Calculation**
  - Dynamically calculate the total cart value.
  - The total is calculated by aggregating `price * quantity` across all items in the cart.

- **Strict Data Validation**
  - Type-safe request and response models using Pydantic.
  - Input constraints and structured validation errors.

- **Interactive API Documentation**
  - Automatically generated OpenAPI documentation.
  - Interactive Swagger UI provided by FastAPI.

## Tech Stack

| Technology | Purpose |
|---|---|
| **FastAPI** | REST API framework |
| **SQLAlchemy 2.0+** | ORM and database layer |
| **SQLite** | Relational database |
| **Pydantic v2** | Data validation and serialization |
| **Uvicorn** | ASGI server |

## Getting Started

### Prerequisites

Make sure you have the following installed:

- **Python 3.10+**
- **pip**
- **Git**

### Installation

#### 1. Clone the repository

```bash
git clone https://github.com/zent-iii/fastapi-cart-service.git
cd fastapi-cart-service
```

#### 2. Create and activate a virtual environment

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**

```powershell
python -m venv venv
venv\Scripts\activate
```

#### 3. Install dependencies

Install the required packages using `pip`:

```bash
pip install fastapi uvicorn sqlalchemy pydantic
```

#### 4. Run the application

Start the FastAPI development server with Uvicorn:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

Once the application is running, FastAPI automatically provides interactive API documentation.

### Swagger UI

Open:

```text
http://127.0.0.1:8000/docs
```

### ReDoc

Alternative API documentation is available at:

```text
http://127.0.0.1:8000/redoc
```

## Database

The application uses **SQLite** as its database.

SQLite is well suited for this project because it requires no separate database server and can be used immediately during development.

The database schema is built around three main entities:

```text
User
 └── Basket
      └── Item
```

The relationships are:

```text
UserModel
   │
   └── 1:N
        │
        ▼
BasketModel
   │
   └── 1:N
        │
        ▼
ItemModel
```

Items are associated with their parent basket, and orphaned items are automatically removed through the configured cascade relationship.

## Cart Total Calculation

The total value of a cart is calculated dynamically based on the unit price and quantity of each item:

```text
Total = Σ (unit_price × quantity)
```

For example:

```text
Product A: €10.00 × 2 = €20.00
Product B: €5.00  × 3 = €15.00
--------------------------------
Total:                  €35.00
```

This ensures that the cart total always reflects the current contents of the basket.

## Project Structure

A typical project structure looks like this:

```text
fastapi-cart-service/
├── main.py
├── models.py
├── schemas.py
├── database.py
├── crud.py
├── requirements.txt
├── README.md
└── venv/
```

> The exact structure may vary depending on how the application is organized.

## Development

To run the application in development mode with automatic reload:

```bash
uvicorn main:app --reload
```

The `--reload` option automatically restarts the server whenever source files are modified.

## License

This project is available for educational and development purposes.