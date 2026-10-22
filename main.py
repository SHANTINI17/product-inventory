from fastapi import FastAPI
from model import Product
from database import session,engine
import database_models
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)
# @app.get("/")
# def sample():
#     return "FastAPI page"

database_models.Base.metadata.create_all(bind=engine)
products=[
    Product(id=1,name="phone",description="smartphone",price=69.99,quantity=2),
    Product(id=2,name="Laptop",description="acer",price=78.99,quantity=1),
    Product(id=3,name="computer",description="dell",price=45.99,quantity=2)
]

def init_db():
    db=session()
    for product in products:
        db.add(database_models.Product(**product.model_dump()))
    db.commit()

# init_db()

#get all products
@app.get("/products")
def get_all_prod():
    return products

#get product by id
@app.get("/products/{id}")
def get_prod_by_id(id:int):
    for product in products:
        if product.id==id:
            return product
    return "product not found"

#create a new product
@app.post("/products")
def create(product: Product):
    products.append(product)
    return "Product added successfully"

#update a product
@app.put("/products")
def update(id:int,product:Product):
    # for i in range(len(products)):
    for prod in products:
        if prod.id==id:
            prod=product
            return "Product updated successfully"
    return "Product not found"

#delete a product
@app.delete("/products")
def delete_prod(id:int):
    # for i in range(len(products)):
    for prod in products:
        if prod.id==id:
            # del products[i]
            products.remove(prod)
            return "product deleted successfully"
    return "Product not found"