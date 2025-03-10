import streamlit as st
import pandas as pd

# Sample data (replace this with your actual list of dictionaries)
data = [
    {"id": 1, "description": "ABC123 sample data"},
    {"id": 2, "description": "XYZ789 another entry"},
    {"id": 3, "description": "123ABC mixed example"},
    {"id": 4, "description": "DEF456 test data"},
]

# Convert list of dictionaries to DataFrame
df = pd.DataFrame(data)

# Streamlit UI
st.title("Live Search Table")

# User input field
search_query = st.text_input("Search:", placeholder="Type to filter (e.g., 'ABC 123')").strip()


# Function to filter the table based on user input
def filter_data(query, dataframe):
    if not query:
        return dataframe  # Show all data if query is empty

    keywords = query.lower().split()  # Split input into keywords
    return dataframe[
        dataframe["description"].str.lower().apply(
            lambda desc: all(keyword in desc for keyword in keywords)
        )
    ]


# Apply filtering
filtered_df = filter_data(search_query, df)

# Display the table
st.dataframe(filtered_df, use_container_width=True)
