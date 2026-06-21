"""
Database Connection and Session Management

Handles:
- Creating database engine
- Creating session factory
- Creating database tables
"""

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool
import logging

from app.config import settings
from app.models import Base, Product, Category, ProductReview

logger = logging.getLogger(__name__)

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.SQLALCHEMY_ECHO,
    poolclass=NullPool,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    """
    Dependency for FastAPI endpoints.
    
    Usage:
        @app.get("/products")
        async def get_products(db: Session = Depends(get_db)):
            return db.query(Product).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def init_db():
    """Initialize database. Creates all tables."""
    logger.info("Creating database tables...")
    
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logger.info(f"Tables in database: {tables}")
        
    except Exception as e:
        logger.error(f"Failed to create database tables: {str(e)}")
        raise


def check_database_connection():
    """Check if database connection is working."""
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        logger.info("Database connection healthy")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        return False


def seed_sample_data():
    """Insert sample data for testing."""
    db = SessionLocal()
    
    try:
        existing = db.query(Category).first()
        if existing:
            logger.info("Sample data already exists, skipping seed")
            return
        
        categories = [
            Category(name="Electronics", slug="electronics", description="Electronic devices"),
            Category(name="Laptops", slug="laptops", description="Laptop computers"),
            Category(name="Phones", slug="phones", description="Mobile phones"),
            Category(name="Tablets", slug="tablets", description="Tablet computers"),
        ]
        db.add_all(categories)
        db.commit()
        logger.info(f"Created {len(categories)} categories")
        
        products = [
            Product(
                category_id=2,
                name="Dell XPS 13",
                description="13-inch FHD display, Intel i7, RTX 4050",
                price=1299.99,
                rating=4.8,
                review_count=245,
                stock_quantity=50,
                in_stock=True,
                image_url="https://example.com/dell-xps-13.jpg"
            ),
            Product(
                category_id=2,
                name="ASUS ROG Gaming",
                description="15-inch FHD display, Intel i9, RTX 4070",
                price=1599.99,
                rating=4.6,
                review_count=182,
                stock_quantity=30,
                in_stock=True,
                image_url="https://example.com/asus-rog.jpg"
            ),
            Product(
                category_id=2,
                name="HP Pavilion",
                description="14-inch FHD display, Intel i5, 8GB RAM",
                price=599.99,
                rating=4.2,
                review_count=95,
                stock_quantity=100,
                in_stock=True,
                image_url="https://example.com/hp-pavilion.jpg"
            ),
            Product(
                category_id=3,
                name="iPhone 15",
                description="6.1-inch display, A17 Pro, 128GB storage",
                price=799.99,
                rating=4.7,
                review_count=532,
                stock_quantity=75,
                in_stock=True,
                image_url="https://example.com/iphone-15.jpg"
            ),
            Product(
                category_id=3,
                name="Samsung Galaxy S24",
                description="6.2-inch display, Snapdragon 8 Gen 3, 256GB storage",
                price=999.99,
                rating=4.5,
                review_count=412,
                stock_quantity=60,
                in_stock=True,
                image_url="https://example.com/galaxy-s24.jpg"
            ),
        ]
        db.add_all(products)
        db.commit()
        logger.info(f"Created {len(products)} sample products")
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding data: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("Testing database connection...")
    if check_database_connection():
        print("Connection successful!")
    else:
        print("Connection failed!")