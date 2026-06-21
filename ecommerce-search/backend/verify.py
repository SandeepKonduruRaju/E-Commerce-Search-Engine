"""
Phase 5 Verification Script
Runs: connection check -> create tables -> seed data -> list data -> FastAPI smoke-test
"""

import sys
import logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# ── 1. Connection ──────────────────────────────────────────────────────────────
print("\n=== Step 1: Test PostgreSQL Connection ===")
from app.database import check_database_connection, init_db, seed_sample_data, SessionLocal
from app.models import Category, Product
import asyncio

if not check_database_connection():
    print("FAILED: Cannot connect to PostgreSQL. Check your .env / pg service.")
    sys.exit(1)
print("PASSED: PostgreSQL is reachable.\n")

# ── 2. Create Tables ───────────────────────────────────────────────────────────
print("=== Step 2: Create Tables ===")
asyncio.run(init_db())
print("PASSED: Tables created (or already exist).\n")

# ── 3. Seed Sample Data ────────────────────────────────────────────────────────
print("=== Step 3: Seed Sample Data ===")
seed_sample_data()
print("PASSED: Seed complete.\n")

# ── 4. Read Back Data ─────────────────────────────────────────────────────────
print("=== Step 4: Read Data from Database ===")
db = SessionLocal()
categories = db.query(Category).all()
products   = db.query(Product).all()
db.close()

print(f"  Categories ({len(categories)}):")
for c in categories:
    print(f"    - [{c.id}] {c.name}")

print(f"  Products ({len(products)}):")
for p in products:
    print(f"    - [{p.id}] {p.name}  ${p.price}")

assert len(categories) > 0, "No categories found!"
assert len(products)   > 0, "No products found!"
print("PASSED: Sample data is visible in the database.\n")

# ── 5. FastAPI smoke-test ──────────────────────────────────────────────────────
print("=== Step 5: FastAPI App Import Check ===")
from app.main import app
print(f"  App title : {app.title}")
print(f"  Routes    : {[getattr(r, 'path', '?') for r in app.routes]}")
print("PASSED: FastAPI app loads without errors.\n")

print("=" * 50)
print("ALL CHECKS PASSED - FastAPI <-> PostgreSQL is working!")
print("=" * 50)
