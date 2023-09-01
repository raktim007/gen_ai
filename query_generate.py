import os
import streamlit as st
import openai
import pandas as pd

# Configure OpenAI
openai.api_type = "azure"
openai.api_base = "https://generativetesing12.openai.azure.com/"
openai.api_version = "2022-12-01"
openai.api_key = "key"

# Streamlit app
st.title("SQL Query Generator")

generated_query = ""

#upload file
upload_file = st.file_uploader("Upload CSV file", type=["csv"])

# Text input
sqlquery_prompt = st.text_area("SQL Query Prompt:", value="Write a Mysql query.")

if upload_file:
    df = pd.read_csv(upload_file)
    st.dataframe(df)

# Generate query
if st.button("Generate SQL Query"):
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

