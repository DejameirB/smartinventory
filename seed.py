from faker import Faker
from datetime import date, timedelta
import random
from database import SessionLocal, engine
from models import Product, Sale, Base


# Creates the tables in the database if they don't exist yet
Base.metadata.create_all(bind=engine)

fake = Faker()


def generate_data():
    session = SessionLocal()

    # --- PRODUCTS ---
    products = []
    categories = ["Dairy", "Meat", "Produce", "Bakery", "Beverages", "Frozen"]
    labels = ["Premium", "Organic", "Classic", "Fresh"]

    for i in range(50):
        product = Product(
            product_name=f"{random.choice(labels)} {fake.word().capitalize()}",
            category=random.choice(categories),
            base_sale_rate=random.randint(5, 40),
            day_of_week=fake.day_of_week(),
            weekend_multiplier=round(random.uniform(1.2, 2.5), 2)
        )
        session.add(product)
        products.append(product)

    # Flush sends the products to the DB so they get their IDs
    # before we reference them in the sales loop below
    session.flush()

    # --- SALES ---
    start_date = date(2024, 1, 1)

    for day_offset in range(90):
        current_date = start_date + timedelta(days=day_offset)
        day_name = current_date.strftime("%A")
        is_weekend = day_name in ["Saturday", "Sunday"]

        for product in products:

            # Base daily sales with random variation
            daily_sales = product.base_sale_rate * random.uniform(0.7, 1.3)

            # Apply weekend boost if Saturday or Sunday
            if is_weekend:
                daily_sales *= product.weekend_multiplier

            # Apply holiday boost if July or December
            if current_date.month in [7, 12]:
                daily_sales *= random.uniform(1.3, 1.8)

            sale = Sale(
                sale_date=current_date,
                day_of_week=day_name,
                product_id=product.id,
                product_name=product.product_name,
                category=product.category,
                units_sold=int(daily_sales),
                is_weekend=is_weekend
            )
            session.add(sale)

    session.commit()
    session.close()
    print("Data generated successfully.")


if __name__ == "__main__":
    generate_data()