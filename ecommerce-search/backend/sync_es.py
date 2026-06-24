# sync_es.py
from app.database import SessionLocal
from app.models import Product
from app.services.search import create_product_index, index_product

create_product_index()
db = SessionLocal()
products = db.query(Product).all()
for p in products:
    index_product(p)
print(f"Successfully synced {len(products)} products to Elasticsearch!")
db.close()