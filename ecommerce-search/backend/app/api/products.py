# app/api/products.py
from fastapi import APIRouter, Query
from app.services.search import search_products_in_es

router = APIRouter()

@router.get("/search")
def search_products(
    q: str,
    category_id: int | None = Query(default=None),
    min_price: float | None = Query(default=None),
    max_price: float | None = Query(default=None)
):
    """
    Fuzzy full-text search endpoint powered by Elasticsearch.
    Targeting sub-60ms response windows.
    """
    if not q.strip():
        return []

    results = search_products_in_es(
        query=q,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price
    )
    return results