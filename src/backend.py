import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import urllib.parse

# MySQL CONNECTION FUNCTIONS

@st.cache_resource
def get_server_connection(host, port, username, password):
    """Connect to MySQL server (without specifying database)."""
    try:
        encoded_password = urllib.parse.quote_plus(password)
        connection_string = f"mysql+mysqlconnector://{username}:{encoded_password}@{host}:{port}"
        engine = create_engine(connection_string)

        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return engine
    except Exception as e:
        st.error(f"Server connection failed: {str(e)}")
        return None


@st.cache_resource
def get_database_connection(host, port, username, password, database_name):
    """Connect to a specific MySQL database."""
    try:
        encoded_password = urllib.parse.quote_plus(password)
        connection_string = f"mysql+mysqlconnector://{username}:{encoded_password}@{host}:{port}/{database_name}"
        engine = create_engine(connection_string)

        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return engine
    except Exception as e:
        st.error(f"Database connection failed: {str(e)}")
        return None


# METADATA FUNCTIONS

@st.cache_data
def get_databases(_engine):
    """List all databases on the MySQL server."""
    try:
        query = "SHOW DATABASES"
        df = pd.read_sql(query, _engine)
        return df.iloc[:, 0].tolist()
    except Exception as e:
        st.error(f"Error getting databases: {str(e)}")
        return []


@st.cache_data
def get_tables(_engine, database_name):
    """List all tables in a given database."""
    try:
        query = f"SHOW FULL TABLES FROM `{database_name}`"
        df = pd.read_sql(query, _engine)
        df.columns = ["table_name", "table_type"]
        return df
    except Exception as e:
        st.error(f"Error getting tables: {str(e)}")
        return pd.DataFrame()


@st.cache_data
def get_table_info(_engine, database_name, table_name):
    """Get column information for a table (safe, parameterized)."""
    try:
        query = text("""
            SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT, CHARACTER_MAXIMUM_LENGTH
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = :db AND TABLE_NAME = :tbl
            ORDER BY ORDINAL_POSITION
        """)
        return pd.read_sql(query, _engine, params={"db": database_name, "tbl": table_name})
    except Exception as e:
        st.error(f"Error getting table info: {str(e)}")
        return pd.DataFrame()


@st.cache_data
def get_row_count(_engine, database_name, table_name):
    """Count rows in a table (safe, parameterized)."""
    try:
        query = text("SELECT COUNT(*) as row_count FROM `{db}`.`{tbl}`".format(
            db=database_name.replace("`", ""),
            tbl=table_name.replace("`", "")
        ))
        result = pd.read_sql(query, _engine)
        return result['row_count'].iloc[0]
    except Exception as e:
        st.error(f"Error getting row count: {str(e)}")
        return "Error"


# QUERY EXECUTION

@st.cache_data
def execute_query(_engine, query, limit=1000):
    """Run a query and return a dataframe."""
    try:
        df = pd.read_sql(query, _engine)
        if len(df) > limit:
            st.warning(f"Results limited to {limit} rows. Total rows: {len(df)}")
            return df.head(limit)
        return df
    except Exception as e:
        st.error(f"Query error: {str(e)}")
        return pd.DataFrame()