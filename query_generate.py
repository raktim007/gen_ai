import os
import streamlit as st
import openai
import pandas as pd
import pyodbc



# Configure OpenAI
openai.api_type = "azure"
openai.api_base = "https://generativetesing12.openai.azure.com/"
openai.api_version = "2022-12-01"
openai.api_key = "key"

# Streamlit app
st.title("SQL Query Generator")

generated_query = ""


try:
    con_string = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};' \
                r'DBQ=C:\Users\315604\Desktop\sql_generator\Test1.accdb;'
    conn = pyodbc.connect(con_string)

    cursor = conn.cursor()

    tables = [table.table_name for table in cursor.tables(tableType='TABLE')]

    # Display the list of tables
    st.write(f"Tables in the database: {', '.join(tables)}")

    # Get and display schema for each table
    # for table in tables:
    #     st.subheader(f"Features/Columns which are available for the table: {table}")
    #     cursor.execute(f"SELECT * FROM {table}")
    #     columns = [column[0] for column in cursor.description]
    #     st.write(columns)

    selected_table = st.selectbox("Select a table from the access database", tables)


    if selected_table:
        query = f'SELECT * FROM [{selected_table}]'
        df = pd.read_sql_query(query, conn)
        st.dataframe(df)


    user_input = st.text_input("Enter a natural language query:")

    # Text input
    sqlquery_prompt = f"Generate  an sql query to retrieve data:{user_input}"

    # Generate query
    if user_input and st.button("Generate SQL Query"):
        response = openai.Completion.create(
            engine="maltext",
            prompt=sqlquery_prompt,
            temperature=1,
            max_tokens=350,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            best_of=1,
            stop=None
        )
        
        # Extract generated email from response
        generated_query = response.choices[0].text.strip()
        
        # Display generated email
        st.write("Generated SQL Query:")
        st.code(generated_query)

        try:
            cursor.execute(generated_query)
            query_result = cursor.fetchall()

            #display the query result

            st.write("Generated SQL QUery")
            st.code(generated_query)
            st.write("Query Results:")
            st.code(query_result)

        except pyodbc.Error as e:
            st.error(f"Error executing SQL query: {str(e)}")

    conn.close()
except Exception as e:
    st.error(f"An error occurred: {str(e)}")


