import pandas as pd
import streamlit as st


#  from one level above root:
#  streamlit run /Users/niko/Python/PycharmProjects/thermal_bridge/__main__.py

def streamlit_app(df):
    # Streamlit UI
    st.title("Wärmebrückendaten")

    waermeb_filter = st.selectbox('Wärmebrücken', ['alle'] + list(df['Waermebruecke'].unique()))
    if waermeb_filter != "alle":
        df_wbf = df.loc[df['Waermebruecke'] == waermeb_filter]
    else:
        df_wbf = df
    waermeb_zusatz_filter = st.selectbox('Zusatzinfo',
                                         ['alle'] + list(df_wbf['Zusatzinfo Waermebruecke'].unique()))
    if waermeb_zusatz_filter != "alle":
        df_wzf = df_wbf.loc[df_wbf['Zusatzinfo Waermebruecke'] == waermeb_zusatz_filter]
    else:
        df_wzf = df_wbf

    staerke_filter = st.selectbox('Stärke', ['alle'] + list(df_wzf['staerke'].unique()))
    if staerke_filter != "alle":
        df_wsf = df_wzf.loc[df_wzf['staerke'] == staerke_filter]
    else:
        df_wsf = df_wzf

    material_filter = st.selectbox('Material', ['alle'] + list(df_wsf['material'].unique()))
    if material_filter != "alle":
        df_wmf = df_wsf.loc[df_wsf['material'] == material_filter]
    else:
        df_wmf = df_wsf

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
    filtered_df = filter_data(search_query, df_wmf)

    # Display the table
    st.dataframe(filtered_df, use_container_width=False)


def authenticate():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.title("🔐 Wärmebrückendaten")

        password = st.text_input("Enter password to continue:", type="password")

        if st.button("Submit"):
            if password == st.secrets.password:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password")
        st.stop()


def main():
    from src.thermal_bridge.initialize import init_psi

    authenticate()

    psi = init_psi()
    df = pd.DataFrame(psi.data)
    streamlit_app(df=df)


if __name__ == '__main__':
    main()
