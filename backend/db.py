import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    "dbname": "rent_detector",
    "user": "rent_user",
    "password": "password123",
    "host": "localhost",
    "port": 5432,
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)

def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS predictions (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    zip_code INT NOT NULL,
                    beds INT NOT NULL,
                    baths REAL NOT NULL,
                    sqft INT NOT NULL,
                    parking BOOLEAN NOT NULL,
                    in_unit_laundry BOOLEAN NOT NULL,
                    pet_friendly BOOLEAN NOT NULL,
                    utilities_included BOOLEAN NOT NULL,
                    asking_rent INT NOT NULL,
                    fair_rent INT NOT NULL,
                    range_low INT NOT NULL,
                    range_high INT NOT NULL,
                    delta INT NOT NULL,
                    verdict TEXT NOT NULL,
                    top_factors TEXT[] NOT NULL
                );
                """
            )

def save_prediction_to_db(prediction: dict):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO predictions (
                    zip_code,
                    beds,
                    baths,
                    sqft,
                    parking,
                    in_unit_laundry,
                    pet_friendly,
                    utilities_included,
                    asking_rent,
                    fair_rent,
                    range_low,
                    range_high,
                    delta,
                    verdict,
                    top_factors
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    prediction["zip_code"],
                    prediction["beds"],
                    prediction["baths"],
                    prediction["sqft"],
                    prediction["parking"],
                    prediction["in_unit_laundry"],
                    prediction["pet_friendly"],
                    prediction["utilities_included"],
                    prediction["asking_rent"],
                    prediction["fair_rent"],
                    prediction["range_low"],
                    prediction["range_high"],
                    prediction["delta"],
                    prediction["verdict"],
                    prediction["top_factors"],
                )
            )
