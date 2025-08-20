import sys
import logging

import streamlit as st
import pandas as pd
import plotly.express as px

from backend import (
    get_server_connection,
    get_database_connection,
    get_databases,
    get_tables,
    get_table_info,
    get_row_count,
    execute_query,
)

from api_helpers import (
    generate_sql_from_nl, 
    format_result_to_nl,
    handle_nl_query
)

# --------------------------
# Logging setup
# --------------------------
logging.basicConfig(
    level=logging.DEBUG,  
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# --------------------------
# Page config
# --------------------------
st.set_page_config(
    page_title="Database Query Explorer",
    layout="wide"
)

st.title("🗄️ Database Query Explorer (MySQL)")

# --------------------------
# Login & connection
# --------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.subheader("Connect to your MySQL server")

    with st.form("login_form"):
        host = st.text_input("Host", "localhost")
        port = st.number_input("Port", value=3306, min_value=1, max_value=65535)
        username = st.text_input("Username", "root")
        password = st.text_input("Password", type="password")

        submitted = st.form_submit_button("🔐 Connect")

    if submitted:
        if not username or not password:
            st.error("Please provide username and password")
        else:
            server_engine = get_server_connection(host, port, username, password)
            if server_engine:
                st.session_state.logged_in = True
                st.session_state.server_engine = server_engine
                st.session_state.connection_params = {
                    "host": host,
                    "port": port,
                    "username": username,
                    "password": password,
                }
                st.success("✅ Connected to MySQL server!")
                st.rerun()
            else:
                st.error("❌ Connection failed. Check credentials or server status.")
    st.stop()

if st.sidebar.button("Log out"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.cache_data.clear()
    st.cache_resource.clear()
    st.rerun()

# --------------------------
# Main application
# --------------------------
if "server_engine" in st.session_state:
    server_engine = st.session_state.server_engine
    params = st.session_state.connection_params

    databases = get_databases(server_engine)

    if databases:
        st.sidebar.header("Database Selection")
        selected_database = st.sidebar.selectbox("Select database", databases)

        if st.sidebar.button("Connect to Database"):
            db_engine = get_database_connection(
                params["host"], params["port"], params["username"], params["password"], selected_database
            )
            if db_engine:
                st.session_state.db_engine = db_engine
                st.session_state.current_database = selected_database
                st.sidebar.success(f"✅ Connected to {selected_database}!")

        if "db_engine" in st.session_state:
            db_engine = st.session_state.db_engine
            current_db = st.session_state.current_database
            st.info(f"📊 Currently exploring: **{current_db}**")

            tables_df = get_tables(db_engine, current_db)

            if not tables_df.empty:
                tab1, tab2, tab3, tab4, tab5 = st.tabs([
                    "📊 Table Explorer", 
                    "🔍 Custom Query", 
                    "📈 Visualization", 
                    "ℹ️ Database Info",
                    "🧠 Ask in Natural Language"
                ])

                # --------------------------
                # Tab 1: Table Explorer
                # --------------------------
                with tab1:
                    st.subheader("Table Explorer")
                    table_options = tables_df["table_name"].tolist()
                    selected_table = st.selectbox("Select a table", table_options)

                    if selected_table:
                        col1, col2 = st.columns([1, 2])

                        with col1:
                            st.markdown(f"**Database:** {current_db}")
                            st.markdown(f"**Table:** {selected_table}")

                            columns_df = get_table_info(db_engine, current_db, selected_table)
                            st.dataframe(columns_df, use_container_width=True)

                            row_count = get_row_count(db_engine, current_db, selected_table)
                            st.metric("Total Rows", row_count)

                        with col2:
                            limit = st.number_input("Limit rows", min_value=10, max_value=1000, value=100)
                            query = f"SELECT * FROM `{selected_table}` LIMIT {limit}"
                            df = execute_query(db_engine, query)

                            if not df.empty:
                                st.dataframe(df, use_container_width=True)
                                csv = df.to_csv(index=False)
                                st.download_button("⬇️ Download CSV", csv, f"{selected_table}.csv", "text/csv")

                # --------------------------
                # Tab 2: Custom SQL Query
                # --------------------------
                with tab2:
                    st.subheader("Custom SQL Query")
                    query = st.text_area("Enter SQL query:", height=200, placeholder="SELECT * FROM your_table LIMIT 100")
                    limit = st.number_input("Result limit", min_value=10, max_value=10000, value=1000)

                    if st.button("Run Query"):
                        df = execute_query(db_engine, query, limit)
                        if not df.empty:
                            st.dataframe(df, use_container_width=True)

                # --------------------------
                # Tab 3: Visualization
                # --------------------------
                with tab3:
                    st.subheader("Quick Visualization")
                    viz_table = st.selectbox("Select a table", tables_df["table_name"].tolist(), key="viz_table")

                    if viz_table:
                        sample_query = f"SELECT * FROM `{viz_table}` LIMIT 1000"
                        viz_df = execute_query(db_engine, sample_query)

                        if not viz_df.empty:
                            x_col = st.selectbox("X-axis", viz_df.columns)
                            y_col = st.selectbox("Y-axis", viz_df.columns)

                            if st.button("Generate Chart"):
                                fig = px.scatter(viz_df, x=x_col, y=y_col)
                                st.plotly_chart(fig, use_container_width=True)

                # --------------------------
                # Tab 4: Database Info
                # --------------------------
                with tab4:
                    st.subheader("Database Info")
                    info = []
                    for _, row in tables_df.iterrows():
                        table_name = row["table_name"]
                        row_count = get_row_count(db_engine, current_db, table_name)
                        columns_df = get_table_info(db_engine, current_db, table_name)
                        info.append({
                            "Table": table_name,
                            "Columns": len(columns_df),
                            "Rows": row_count
                        })
                    st.dataframe(pd.DataFrame(info))

                # --------------------------
                # Tab 5: Natural Language Query
                # --------------------------
                with tab5:
                    st.subheader("Ask in Natural Language")
                    question = st.text_input("Enter your question")
                    if st.button("Ask"):
                        sql_query = handle_nl_query(question, "GROQ", "llm")
                        st.code(sql_query, language="sql")
                        results = execute_query(db_engine, sql_query)
                        st.dataframe(results)

    else:
        st.warning("No databases found on this server.")
