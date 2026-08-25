from sqlalchemy import Column, Integer, String, Float, Boolean, Date, ForeignKey
from database import Base, engine


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    base_sale_rate = Column(Integer, nullable=False)
    day_of_week = Column(String, nullable=False)
    weekend_multiplier = Column(Float, nullable=False)


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sale_date = Column(Date, nullable=False)
    day_of_week = Column(String, nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    product_name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    units_sold = Column(Integer, nullable=False)
    is_weekend = Column(Boolean, nullable=False)


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")