from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).resolve().parents[1] / "output" / "retail_sales.db"

QUERIES = {
    "Top products by revenue": """
        SELECT product, ROUND(SUM(revenue), 2) AS revenue
        FROM sales GROUP BY product ORDER BY revenue DESC LIMIT 5;
    """,
    "Monthly revenue": """
        SELECT substr(order_date, 1, 7) AS month,
               ROUND(SUM(revenue), 2) AS revenue
        FROM sales GROUP BY month ORDER BY month;
    """,
    "Revenue by region": """
        SELECT region, ROUND(SUM(revenue), 2) AS revenue
        FROM sales GROUP BY region ORDER BY revenue DESC;
    """,
}

def main():
    if not DB_PATH.exists():
        raise SystemExit("Database not found. Run: python src/etl_pipeline.py")
    with sqlite3.connect(DB_PATH) as conn:
        for title, query in QUERIES.items():
            print(f"\n{title}\n" + "-" * len(title))
            rows = conn.execute(query).fetchall()
            for row in rows:
                print(row)

if __name__ == "__main__":
    main()
