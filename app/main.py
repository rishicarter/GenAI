import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Annotated


def generate_product_id(num):
    while True:
        yield num
        num += 1

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.products = []
    app.state.product_id = generate_product_id(0)
    yield
    print("Shutting Down Application!")

app = FastAPI(lifespan=lifespan)

class ProductDetails(BaseModel):
    name: str
    price: Annotated[float, Field(gt=0)]
    stock: Annotated[int, Field(ge=0)]
    sku: Annotated[str, "SKU must be unique"]

class Product(BaseModel):
    id: int
    name: str
    price: Annotated[float, Field(gt=0)]
    stock: Annotated[int, Field(ge=0)]
    sku: Annotated[str, "SKU must be unique"]

class Order(BaseModel):
    id: int
    product_id: int
    quantity: Annotated[int, Field(gt=0)]
    staus: Annotated[str, "Status must be one of: PENDING, SHIPPED, DELIVERED, CANCELLED"]

async def SKUValidate(dep: ProductDetails):
    tmp = dep.model_dump()
    for product in app.state.products:
        if tmp['sku'] == product['sku']:
            raise HTTPException(status_code=409, detail="SKU already present!")
    del tmp
    return dep

@app.post("/products/", status_code=status.HTTP_201_CREATED)
def add_products(product: Annotated[ProductDetails, Depends(SKUValidate)]):
    try:
        product_dict = {
            "id": next(app.state.product_id),
            **product.model_dump()
        }
        product = Product(**product_dict)
        app.state.products.append(product_dict)
        del product_dict
        return JSONResponse(content={"detail": "Data Inserted Successfully!"})
    except Exception as e:
        return JSONResponse(status_code=500,content={"detail": "Internal Server Error"})


@app.get("/products/", status_code=status.HTTP_200_OK)
async def get_products():
    return app.state.products

@app.get("/products/{id}")
async def get_product(id: int):
    try:
        return JSONResponse(status_code=200, content=app.state.products[id])
    except:
        raise HTTPException(status_code=404, detail=f"Product ID {id} not found!")

@app.put("/products/{id}")
async def update_product(id: int, product: ProductDetails):
    try:
        stored_data_dict = app.state.products[id]
        stored_data_model = Product(**stored_data_dict)
        update_data = product.model_dump(exclude_unset=True)
        updated_item = stored_data_model.model_copy(update=update_data)
        app.state.products[id-1] = updated_item.model_dump()
        return JSONResponse(status_code=200, content={"detail": f"Product ID {id} Udpated!"})
    except:
        raise HTTPException(status_code=404, detail=f"Product ID {id} not found!")

@app.delete("/products/{id}")
async def delete_product(id: int):
    try:
        app.state.products.pop(id)
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={"detail": "Delete Operation Successfull!"})
    except:
        raise HTTPException(status_code=404, detail=f"Product ID {id} not found!")



# @app.get("/")
# async def root():
#     return {"Hello": f"World"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)