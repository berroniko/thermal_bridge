import pandas as pd
import streamlit as st


#  from one level above root:
#  streamlit run /Users/niko/Python/PycharmProjects/thermal_bridge/__main__.py

def streamlit_app(df):
    st.set_page_config(layout="wide")
    st.title("Wärmebrückendaten")

    list_of_filters = ['Waermebruecke', 'Zusatzinfo Waermebruecke', 'staerke', 'material', 'dichte', 'dicke', 'wlg',
                       'VHAG']

    def reset_filter():
        return {col: "alle" for col in list_of_filters}

    # Initialize filter state
    if "filters" not in st.session_state:
        st.session_state.filters = reset_filter()

    # Reset button
    if st.button("🔄 Filter zurücksetzen"):
        st.session_state.filters = reset_filter()
        st.rerun()

    # --- Filter application logic ---
    def apply_filters(dataframe, filters):
        df_filtered = dataframe.copy()
        for col, val in filters.items():
            if val != "alle":
                df_filtered = df_filtered[df_filtered[col] == val]
        return df_filtered

    # --- Filter update logic ---
    # Create a copy to track updated filters
    updated_filters = st.session_state.filters.copy()

    # Loop over columns and create selectboxes with dynamic options
    for col in list_of_filters:
        # Apply filters excluding the current column
        temp_filters = {k: v for k, v in updated_filters.items() if k != col}
        temp_df = apply_filters(df, temp_filters)

        # Get available options for current column based on other filters
        available_options = sorted(temp_df[col].dropna().unique())
        dropdown_options = ["alle"] + available_options

        # Selectbox
        previous_value = updated_filters[col]
        selected_value = st.selectbox(f"{col.capitalize()}", dropdown_options, index=dropdown_options.index(
            previous_value) if previous_value in dropdown_options else 0)

        # If selection changed, update and rerun to refresh other filters
        if selected_value != previous_value:
            st.session_state.filters[col] = selected_value
            st.rerun()

    # Apply all filters and display
    final_filtered_df = apply_filters(df, st.session_state.filters)
    st.dataframe(final_filtered_df, use_container_width=True)

    # # User input field
    # search_query = st.text_input("Bezeichnung filtern:", placeholder="z.B.: aw44 035").strip()
    #
    # # Function to filter the table based on user input
    # def filter_data(query, dataframe):
    #     if not query:
    #         return dataframe  # Show all data if query is empty
    #
    #     keywords = query.lower().split()  # Split input into keywords
    #     return dataframe[
    #         dataframe["Bezeichnung"].str.lower().apply(
    #             lambda desc: all(keyword in desc for keyword in keywords)
    #         )
    #     ]
    #
    # # Apply filtering
    # filtered_df = filter_data(search_query, df_wmf)
    #
    # # Display the table
    # st.dataframe(filtered_df, use_container_width=False)


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
    df['dicke'] = pd.to_numeric(df['dicke'], errors='coerce').astype('Int64')
    streamlit_app(df=df)


if __name__ == '__main__':
    main()
