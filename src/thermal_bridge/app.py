import pandas as pd
import streamlit as st


#  from one level above root:
#  streamlit run /Users/niko/Python/PycharmProjects/thermal_bridge/__main__.py

def streamlit_app(df):
    # Streamlit UI
    st.title("Wärmebrückendaten")

    waermeb_filter = st.selectbox('Wärmebrückenfilter', ['alle'] + list(df['Waermebruecke'].unique()))
    if waermeb_filter != "alle":
        df_wbf = df.loc[df['Waermebruecke'] == waermeb_filter]
    else:
        df_wbf = df
    waermeb_zusatz_filter = st.selectbox('Zusatzinfofilter',
                                         ['alle'] + list(df_wbf['Zusatzinfo Waermebruecke'].unique()))
    if waermeb_zusatz_filter != "alle":
        df_wzf = f = df_wbf.loc[df_wbf['Zusatzinfo Waermebruecke'] == waermeb_zusatz_filter]
    else:
        df_wzf = df_wbf

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
    filtered_df = filter_data(search_query, df_wzf)

    # Display the table
    st.dataframe(filtered_df, use_container_width=False)


def main():
    from src.thermal_bridge.initialize import init_psi
    password = st.text_input("Enter password to continue:", type="password")

    if password != st.secrets.password:
        st.warning("Please enter the correct password to access the app.")
        st.stop()

    psi = init_psi()
    df = pd.DataFrame(psi.data)
    streamlit_app(df=df)


if __name__ == '__main__':
    main()
