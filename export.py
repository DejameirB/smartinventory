import pandas as pd
from database import SessionLocal
from models import Sale


def export_sales_csv():
    session = SessionLocal()
    sales = session.query(Sale).all()

    # Convert the sales table into a list of dictionaries
    data = [
        {
            "sale_date": s.sale_date,
            "day_of_week": s.day_of_week,
            "product_id": s.product_id,
            "product_name": s.product_name,
            "category": s.category,
            "units_sold": s.units_sold,
            "is_weekend": s.is_weekend
        }
        for s in sales
    ]

    session.close()

    # Create a pandas dataframe and export to CSV
    df = pd.DataFrame(data)

    print("\n--- SALES DATAFRAME PREVIEW ---")
    print(df.head(10))
    print(f"\nTotal rows: {len(df)}")

    df.to_csv("sales_data.csv", index=False)
    print("\nExported successfully to sales_data.csv")


if __name__ == "__main__":
    export_sales_csv()