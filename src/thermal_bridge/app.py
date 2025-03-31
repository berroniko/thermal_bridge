import pandas as pd
import streamlit as st


def streamlit_app(df):
    # Streamlit UI
    st.title("Wärmebrückendaten")

    waermeb_filter = st.selectbox('Wärmebrückenfilter', ['alle']+ list(df['Waermebruecke'].unique()))
    waermeb_zusatz_filter = st.selectbox('Zusatzinfofilter', ['alle']+ list(df['Zusatzinfo Waermebruecke'].unique()))

    # User input field
    search_query = st.text_input("Bezeichnung filtern:", placeholder="z.B.: aw44 035").strip()

    # Function to filter the table based on user input
    def filter_data(query, dataframe):
        if not query:
            return dataframe  # Show all data if query is empty

        keywords = query.lower().split()  # Split input into keywords
        return dataframe[
            dataframe["Bezeichnung"].str.lower().apply(
                lambda desc: all(keyword in desc for keyword in keywords)
            )
        ]

    # Apply filtering
    filtered_df = filter_data(search_query, df)

    # Display the table
    st.dataframe(filtered_df, use_container_width=False)


def main():
    from src.thermal_bridge.initialize import init_psi
    psi = init_psi()
    df = pd.DataFrame(psi.data)
    streamlit_app(df=df)


if __name__ == '__main__':
    main()
