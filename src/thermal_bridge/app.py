import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode, GridUpdateMode


#  from one level above root:
#  streamlit run /Users/niko/Python/PycharmProjects/thermal_bridge/__main__.py

def streamlit_app(df):
    st.set_page_config(layout="wide")
    st.title("Wärmebrückendaten")

    list_of_filters = {'Waermebruecke'           : 'Wärmebrücke',
                       'Zusatzinfo Waermebruecke': 'Zusatzinfo',
                       'staerke'                 : 'Stärke',
                       'material'                : 'Putz/Verblend',
                       'PPW'                     : 'PPW',
                       'dicke'                   : 'Dicke (mm)',
                       'WLG'                     : 'WLG',
                       'Psi-Wert'                : 'Psi-Wert',
                       'Bezeichnung'             : 'Bezeichnung'}

    def reset_filter():
        filter_settings = {col: "alle" for col in list_of_filters.keys()}
        filter_settings['Bezeichnung'] = ""
        return filter_settings

    # Initialize filter state
    if "filters" not in st.session_state:
        st.session_state.filters = reset_filter()

    # Reset button
    if st.button("🔄 Filter zurücksetzen"):
        st.session_state.filters = reset_filter()
        st.session_state.search_bezeichnung = ""
        st.rerun()

    # --- Filter application logic ---
    def apply_filters(dataframe, filters):
        df_filtered = dataframe.copy()
        for col, val in filters.items():
            if col == "Bezeichnung":
                continue
            if val != "alle":
                df_filtered = df_filtered[df_filtered[col] == val]
        if not filters.get('Bezeichnung', None):
            return df_filtered  # Show all data if query is empty

        keywords = filters.get('Bezeichnung').lower().split()  # Split input into keywords
        return df_filtered[
            df_filtered["Bezeichnung"].str.lower().apply(
                lambda desc: all(keyword in desc for keyword in keywords)
            )
        ]

    # --- Filter update logic ---
    # Create a copy to track updated filters
    updated_filters = st.session_state.filters.copy()

    left, right = st.columns([1, 1])

    # Loop over columns and create selectboxes with dynamic options
    num = 0
    for col in list_of_filters.keys():
        num += 1
        if col != 'Bezeichnung':
            # Apply filters excluding the current column
            temp_filters = {k: v for k, v in updated_filters.items() if k != col}
            temp_df = apply_filters(df, temp_filters)

            # Get available options for current column based on other filters
            available_options = sorted(temp_df[col].dropna().unique())
            dropdown_options = ["alle"] + available_options

            # Selectbox
            previous_value = updated_filters[col]
            if num % 2:
                selected_value = left.selectbox(f"{list_of_filters.get(col)}", dropdown_options,
                                                index=dropdown_options.index(
                                                    previous_value) if previous_value in dropdown_options else 0)
            else:
                selected_value = right.selectbox(f"{list_of_filters.get(col)}", dropdown_options,
                                                 index=dropdown_options.index(
                                                     previous_value) if previous_value in dropdown_options else 0)
        else:
            previous_value = updated_filters[col]
            selected_value = st.text_input("Bezeichnung filtern:", placeholder="z.B.: aw44 035",
                                           key="search_bezeichnung").strip()

        # If selection changed, update and rerun to refresh other filters
        if selected_value != previous_value:
            st.session_state.filters[col] = selected_value
            st.rerun()

    # Apply all filters
    final_filtered_df = apply_filters(df, st.session_state.filters)

    # JavaScript function for row styling
    row_style_code = JsCode("""
    function(params) {
        if (params.data.row_color) {
            return { backgroundColor: params.data.row_color };
        }
        return {};
    }
    """)

    # GridOptions with custom row styling
    gb = GridOptionsBuilder.from_dataframe(final_filtered_df)
    gb.configure_grid_options(enableCellTextSelection=True, ensureDomOrder=True, )

    gb.configure_column("row_color", hide=True)
    gb.configure_column("Farbe", hide=True)
    gb.configure_column("ebz", hide=True)
    gb.configure_column("W&P", hide=True)
    gb.configure_column("staerke", hide=True)
    gb.configure_column("material", hide=True)
    gb.configure_column("PPW", hide=True)
    gb.configure_column("dicke", hide=True)
    gb.configure_column("WLG", hide=True)
    gb.configure_column("Waermebruecke", width=400)
    gb.configure_column("Zusatzinfo Waermebruecke", width=400)
    gb.configure_column("Bezeichnung", width=1200)
    gb.configure_column("Psi-Wert", width=150)
    gb.configure_column("Ref", width=70, cellStyle={"textAlign": "center"})
    gb.configure_column("VHAG", width=100, cellStyle={"textAlign": "center"})
    gb.configure_column("Datum", width=180)
    gb.configure_column("Nr.", width=100, cellStyle={"textAlign": "right"})

    gb.configure_selection("single", use_checkbox=False)
    grid_options = gb.build()
    grid_options["getRowStyle"] = row_style_code

    # Display the grid with single row selection
    grid_response = AgGrid(
        final_filtered_df,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        enableBrowserClipboard=True,
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True  # Allow JsCode injection
    )


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
