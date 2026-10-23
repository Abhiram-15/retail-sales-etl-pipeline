from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "sales.csv"
OUTPUT_DIR = ROOT / "output"
DB_PATH = OUTPUT_DIR / "retail_sales.db"
CLEAN_PATH = OUTPUT_DIR / "cleaned_sales.csv"

REQUIRED_COLUMNS = [
    "order_id", "order_date", "customer_id", "product", "quantity",
    "unit_price", "region"
]

def extract(path: Path) -> pd.DataFrame:
    """Extract raw sales rows from a CSV file."""
    return pd.read_csv(path)

def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize fields, validate rows, and derive revenue."""
    missing_columns = sorted(set(REQUIRED_COLUMNS) - set(df.columns))
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    clean = df[REQUIRED_COLUMNS].copy()
    clean["order_id"] = clean["order_id"].astype("string").str.strip()
    clean["customer_id"] = clean["customer_id"].astype("string").str.strip()
    clean["product"] = clean["product"].astype("string").str.strip()
    clean["region"] = clean["region"].astype("string").str.strip().str.title()
    clean["order_date"] = pd.to_datetime(clean["order_date"], errors="coerce")
    clean["quantity"] = pd.to_numeric(clean["quantity"], errors="coerce")
    clean["unit_price"] = pd.to_numeric(clean["unit_price"], errors="coerce")

    before = len(clean)
    clean = clean.dropna(subset=REQUIRED_COLUMNS)
    clean = clean[
        (clean["order_id"] != "") &
        (clean["customer_id"] != "") &
        (clean["product"] != "") &
        (clean["quantity"] > 0) &
        (clean["unit_price"] >= 0)
    ]
    clean = clean.drop_duplicates(subset=["order_id"])
    clean["quantity"] = clean["quantity"].astype(int)
    clean["revenue"] = (clean["quantity"] * clean["unit_price"]).round(2)
    clean["order_date"] = clean["order_date"].dt.strftime("%Y-%m-%d")

    print(f"Rows read: {before}")
    print(f"Rows loaded: {len(clean)}")
    print(f"Rows removed during validation/deduplication: {before - len(clean)}")
    return clean

def load(df: pd.DataFrame, db_path: Path) -> None:
    """Load cleaned records into SQLite, replacing the table for repeatable runs."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        df.to_sql("sales", conn, if_exists="replace", index=False)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_sales_order_date ON sales(order_date)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_sales_region ON sales(region)")

def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    raw = extract(DATA_PATH)
    clean = transform(raw)
    clean.to_csv(CLEAN_PATH, index=False)
    load(clean, DB_PATH)
    print(f"\nDatabase created: {DB_PATH}")
    print(f"Clean CSV created: {CLEAN_PATH}")
    with sqlite3.connect(DB_PATH) as conn:
        result = pd.read_sql_query(
            "SELECT region, ROUND(SUM(revenue), 2) AS total_revenue "
            "FROM sales GROUP BY region ORDER BY total_revenue DESC",
            conn,
        )
    print("\nRevenue by region:")
    print(result.to_string(index=False))

if __name__ == "__main__":
    main()
