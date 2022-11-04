from datetime import datetime
import logging

import configparser
import datetime as dt
import numpy as np
import pandas as pd
import psycopg2
import uuid

import psycopg2.extras as extras


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
)

log = logging.getLogger(__name__)


def merge_vendor():

    sql = """INSERT INTO vendors(vendor_name)
             VALUES(%s) RETURNING vendor_id;"""


def generate_grade_dataframe() -> pd.DataFrame:
    df = pd.DataFrame(columns=["id", "last_modified", "batch_uuid", "grade"])

    # grades
    grades = np.arange(60, 100)
    grades_results = np.random.choice(grades, 10)
    run_uuid = str(uuid.uuid4())

    df["id"] = np.arange(0, 10)
    df["last_modified"] = dt.datetime.now()
    df["batch_uuid"] = run_uuid
    df["grade"] = grades_results

    return df, run_uuid


def parse_config() -> dict:
    config = configparser.ConfigParser()
    config.read("/app/config.txt")
    return config


def create_connection(config: dict) -> psycopg2.extensions.connection:

    app_name = "generator"
    database = config["database"]["DB_DATABASE"]
    host = config["database"]["DB_HOST"]
    port = config["database"]["DB_PORT"]
    schema = config["database"]["DB_SCHEMA"]
    username = config["database"]["DB_USERNAME"]
    password = config["database"]["DB_PASSWORD"]
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=username,
        password=password,
        options=f"-c search_path={schema}",
        application_name=app_name,
    )

    return conn


def get_version(conn: psycopg2.extensions.connection) -> str:
    """
    Return the database version.
    """

    cur = conn.cursor()
    cur.execute("SELECT version()")
    db_version = cur.fetchone()
    cur.close()
    return db_version


def insert_values_do_nothing(
    conn: psycopg2.extensions.connection, df: pd.DataFrame, table: str
) -> int:
    """
    Using psycopg2.extras.execute_values() to insert the dataframe
    """
    # Create a list of tupples from the dataframe values
    tuples = [tuple(x) for x in df.to_numpy()]
    # Comma-separated dataframe columns
    cols = ",".join(list(df.columns))
    # SQL quert to execute
    query = "INSERT INTO %s(%s) VALUES %%s ON CONFLICT DO NOTHING;" % (table, cols)

    cursor = conn.cursor()
    try:
        psycopg2.extras.execute_values(cursor, query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1

    cursor.close()
    return 0


def insert_values_upsert(
    conn: psycopg2.extensions.connection, df: pd.DataFrame, table: str
):
    """
    Using psycopg2.extras.execute_values() to upsert the dataframe
    """
    # Create a list of tupples from the dataframe values
    tuples = [tuple(x) for x in df.to_numpy()]
    # Comma-separated dataframe columns
    cols = ",".join(list(df.columns))

    # SQL query for upserts
    query = """
        INSERT INTO %s(%s)
        VALUES %%s
        ON CONFLICT (id) 
        DO 
        UPDATE SET
            last_modified = excluded.last_modified,
            batch_uuid = excluded.batch_uuid,
            grade = excluded.grade
        ;
        
        """ % (
        table,
        cols,
    )
    cursor = conn.cursor()
    try:
        psycopg2.extras.execute_values(cursor, query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1

    cursor.close()
    return 0


def main():

    log.info('starting script.')

    # Parse Configuration.
    config = parse_config()

    # Connection
    conn = create_connection(config)
    # cur = conn.cursor()

    # Check version
    db_version = get_version(conn)
    log.info(f"PostgreSQL database version:  {db_version}")

    # Generate Data
    grade_df, uuid = generate_grade_dataframe()
    grade_df = grade_df.sample(5)

    # Upload to database
    dfs = {}
    dfs[f"grade"] = grade_df

    for table, df in dfs.items():
        result = insert_values_upsert(conn, df, table)

    log.info(f'completed run: {uuid}')


if __name__ == "__main__":
    main()
