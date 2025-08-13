from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="My API with Pydantic")


# Crear la aplicación (lo más simple posible)
app = FastAPI(title="Mi Primera API")

# Endpoint 1: Hello World (OBLIGATORIO)
@app.get("/")
def hello_world():
    return {"message": "¡Mi primera API FastAPI!"}

# Endpoint 2: Info básica (OBLIGATORIO)
@app.get("/info")
def info():
    return {"api": "FastAPI", "week": 1, "status": "running"}

from fastapi import FastAPI

app = FastAPI(title="Mi Primera API")

@app.get("/")
def hello_world():
    return {"message": "¡Mi primera API FastAPI!"}

@app.get("/info")
def info():
    return {"api": "FastAPI", "week": 1, "status": "running"}

# NUEVO: Endpoint personalizado (solo si hay tiempo)
@app.get("/greeting/{name}")
def greet_user(name: str):
    return {"greeting": f"¡Hola {name}!"}

# Agregar al final de tu main.py existente

@app.get("/my-profile")
def my_profile():
    return {
        "name": "Paola Navas",           
        "bootcamp": "FastAPI",
        "week": 1,
        "date": "2025",
        "likes_fastapi": True              
    }

from fastapi import FastAPI

app = FastAPI(title="My First API")

# ANTES (Semana 1)
@app.get("/")
def hello_world():
    return {"message": "My first FastAPI!"}

# DESPUÉS (con type hints)
@app.get("/")
def hello_world() -> dict:
    return {"message": "My first FastAPI!"}

# Si tenías endpoint con parámetro
@app.get("/greeting/{name}")
def greet_user(name: str) -> dict:
    return {"greeting": f"Hello {name}!"}

# Endpoint con múltiples parámetros
@app.get("/calculate/{num1}/{num2}")
def calculate(num1: int, num2: int) -> dict:
    result = num1 + num2
    return {"result": result, "operation": "sum"}

from typing import List, Dict

# Lista de strings
@app.get("/fruits")
def get_fruits() -> List[str]:
    return ["apple", "banana", "orange"]

# Lista de números
@app.get("/numbers")
def get_numbers() -> List[int]:
    return [1, 2, 3, 4, 5]

# Diccionario con estructura conocida
@app.get("/user/{user_id}")
def get_user(user_id: int) -> Dict[str, str]:
    return {
        "id": str(user_id),
        "name": "Demo User",
        "email": "demo@example.com"
    }

from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    email: str

@app.post("/users")
def create_user(user: User):
    return {"user": user.dict()}

class Product(BaseModel):
    name: str
    price: int  # en centavos para evitar decimales
    available: bool = True  # valor por defecto

products = []
@app.get("/")
def hello_world() -> dict:
    return {"message": "API with Pydantic!"}

@app.post("/products")
def create_product(product: Product) -> dict:
    product_dict = product.dict()
    product_dict["id"] = len(products) + 1
    products.append(product_dict)
    return {"message": "Product created", "product": product_dict}

@app.get("/products")
def get_products() -> dict:
    return {"products": products, "total": len(products)}

from typing import Optional

class CompleteUser(BaseModel):
    name: str
    age: int
    email: str
    phone: Optional[str] = None  # campo opcional
    active: bool = True

@app.post("/users")
def create_user(user: CompleteUser) -> dict:
    return {"user": user.dict(), "valid": True}

@app.get("/products/{product_id}")
def get_product(product_id: int) -> dict:
    for product in products:
        if product["id"] == product_id:
            return {"product": product}
    return {"error": "Product not found"}

@app.get("/categories/{category}/products/{product_id}")
def product_by_category(category: str, product_id: int) -> dict:
    return {
        "category": category,
        "product_id": product_id,
        "message": f"Searching product {product_id} in {category}"
    }


from typing import Optional

@app.get("/search")
def search_products(
    name: Optional[str] = None,
    max_price: Optional[int] = None,
    available: Optional[bool] = None
) -> dict:
    results = products.copy()

    if name:
        results = [p for p in results if name.lower() in p["name"].lower()]
    if max_price:
        results = [p for p in results if p["price"] <= max_price]
    if available is not None:
        results = [p for p in results if p["available"] == available]

    return {"results": results, "total": len(results)}


from pydantic import BaseModel
from typing import List

class ProductResponse(BaseModel):
    id: int
    name: str
    price: int
    available: bool
    message: str = "Product retrieved successfully"

class ProductListResponse(BaseModel):
    products: List[dict]
    total: int
    message: str = "List retrieved successfully"

@app.get("/products", response_model=ProductListResponse)
def get_products() -> ProductListResponse:
    return ProductListResponse(
        products=products,
        total=len(products)
    )

@app.post("/products", response_model=ProductResponse)
def create_product(product: Product) -> ProductResponse:
    product_dict = product.dict()
    product_dict["id"] = len(products) + 1
    products.append(product_dict)
    return ProductResponse(**product_dict, message="Product created successfully")

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(title="My Enhanced API - Week 2")

class Product(BaseModel):
    name: str
    price: int
    available: bool = True

class ProductResponse(BaseModel):
    id: int
    name: str
    price: int
    available: bool
    message: str = "Successful operation"

class ProductListResponse(BaseModel):
    products: List[dict]
    total: int
    message: str = "List retrieved"

products = []

@app.get("/")
def hello_world() -> dict:
    return {"message": "Week 2 API with Pydantic and Type Hints!"}

@app.get("/products", response_model=ProductListResponse)
def get_products() -> ProductListResponse:
    return ProductListResponse(
        products=products,
        total=len(products)
    )

@app.post("/products", response_model=ProductResponse)
def create_product(product: Product) -> ProductResponse:
    product_dict = product.dict()
    product_dict["id"] = len(products) + 1
    products.append(product_dict)
    return ProductResponse(**product_dict, message="Product created")

@app.get("/products/{product_id}")
def get_product(product_id: int) -> dict:
    for product in products:
        if product["id"] == product_id:
            return {"product": product}
    raise HTTPException(status_code=404, detail="Product not found")

@app.get("/search")
def search_products(
    name: Optional[str] = None,
    max_price: Optional[int] = None,
    available: Optional[bool] = None
) -> dict:
    results = products.copy()
    if name:
        results = [p for p in results if name.lower() in p["name"].lower()]
    if max_price:
        results = [p for p in results if p["price"] <= max_price]
    if available is not None:
        results = [p for p in results if p["available"] == available]
    return {"results": results, "total": len(results)}


from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: int
    available: bool = True

class Item(BaseModel):
    name: str

@app.post("/items")
def create_item(item: Item) -> dict:
    return {"item": item.dict()}

class Item(BaseModel):
    name: str

@app.post("/items")
def create_item(item: Item) -> dict:
    return {"item": item.dict()}

@app.get("/")
def home() -> dict:
    return {"message": "it works"}