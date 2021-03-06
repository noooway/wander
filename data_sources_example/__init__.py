import json
import sqlite3
import pandas as pd
from . import example_data


def init_data_sources(app):
    app.data_sources = {}
    register_dataframes(app)
    #import_csv(app)
    import_from_db(app)
    load_releases_info(app)


def register_dataframes(app):
    app.data_sources['revenue'] = example_data.revenue_df
    app.data_sources['installs'] = example_data.installs_df
    app.data_sources['regs'] = example_data.regs_df
    app.data_sources['online'] = example_data.online_df
    app.data_sources['first_sales'] = example_data.first_sales_df
    app.data_sources['sales'] = example_data.sales_df
    app.data_sources['virtual_currency_spent'] = \
        example_data.virtual_currency_spent_df
    app.data_sources['regs_to_first_sales'] = \
        example_data.regs_to_first_sales_df
    app.data_sources['first_sales_to_second_sales'] = \
        example_data.first_sales_to_second_sales_df


def import_csv(app):
    pass


def import_from_db(app):
    db_path = './data_sources_example/regs_pur.db'
    cohort_purchases_sql = """
    SELECT
        regs.reg_date AS reg_date,
        date(purchases.purchase_datetime) AS pur_date,
        SUM(purchase_amount) AS purchase_amount
    FROM purchases
    JOIN regs ON regs.id = purchases.reg_id
    GROUP BY regs.reg_date
    """
    db_conn = sqlite3.connect(
        db_path,
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    df = pd.read_sql_query(cohort_purchases_sql, db_conn)
    app.data_sources['regs_purchases'] = df
    db_conn.close()


def load_releases_info(app):
    releases_path = './data_sources_example/releases.json'
    with open(releases_path, 'r') as f:
        releases = json.load(f)
    app.data_sources['releases'] = releases['releases']
