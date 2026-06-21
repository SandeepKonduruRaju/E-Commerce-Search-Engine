"""
SQLAlchemy Database Models

Each class = one database table.
"""

from sqlalchemy import (
    Column, Integer, String, Float, Text, DateTime, 
    Boolean, ForeignKey, Table, Index, func
)
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class Category(Base):
    """Product Category model."""
    
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    slug = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    products = relationship("Product", back_populates="category")
    
    def __repr__(self):
        return f"<Category id={self.id} name={self.name}>"


class Product(Base):
    """Product model."""
    
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(
        Integer, 
        ForeignKey("categories.id"), 
        nullable=True, 
        index=True
    )
    
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False, index=True)
    original_price = Column(Float, nullable=True)
    
    rating = Column(Float, nullable=True, index=True)
    review_count = Column(Integer, default=0)
    
    stock_quantity = Column(Integer, default=0)
    in_stock = Column(Boolean, default=True, index=True)
    
    image_url = Column(String(500), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    category = relationship("Category", back_populates="products")
    
    __table_args__ = (
        Index('idx_product_price', 'price'),
        Index('idx_product_rating', 'rating'),
        Index('idx_product_category_id', 'category_id'),
        Index('idx_product_in_stock', 'in_stock'),
    )
    
    def __repr__(self):
        return f"<Product id={self.id} name={self.name} price=${self.price}>"


class ProductReview(Base):
    """Product Review model."""
    
    __tablename__ = "product_reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    user_id = Column(Integer, nullable=True)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Review product_id={self.product_id} rating={self.rating}>"