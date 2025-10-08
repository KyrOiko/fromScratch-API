from fastapi import FastAPI
from middlewares.postgres import PostgreSQLMiddleware
from routers import CustomerRouter, ProductRouter, PurchaseRouter

app = FastAPI()


app.add_middleware(PostgreSQLMiddleware)
app.include_router(PurchaseRouter().router)
app.include_router(CustomerRouter().router)
app.include_router(ProductRouter().router)
