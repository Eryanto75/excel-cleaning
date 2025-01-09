import streamlit as st
import pandas as pd
from io import BytesIO

# Fungsi untuk menghapus nilai tertentu dalam kolom
def cleanse_data_by_contains(df, column_contains_pairs):
    for column, text_to_delete in column_contains_pairs.items():
        if column in df.columns and text_to_delete:
            df = df[~df[column].str.contains(text_to_delete, na=False, case=False)]
    return df

# Fungsi untuk mengunduh file Excel
def download_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Cleaned Data')
    processed_data = output.getvalue()
    return processed_data

# Streamlit UI
st.title("Excel Data Cleansing Automation")

# File upload
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    # Load data
    try:
        # Load the entire file
        original_df = pd.read_excel(uploaded_file)
        st.success("File uploaded successfully!")

        # Initialize session state for iterative cleansing
        if "cleaned_df" not in st.session_state:
            st.session_state.cleaned_df = original_df.copy()

        # Iterative cleansing loop
        iteration = 1
        while True:
            st.markdown(f"### Step {iteration}: Cleanse Data")
            
            # Select columns and specify text patterns to delete
            columns = st.session_state.cleaned_df.columns.tolist()
            column_contains_pairs = {}
            selected_columns = st.multiselect(f"Step {iteration}: Select columns to clean", options=columns, key=f"select_columns_{iteration}")
            
            for column in selected_columns:
                text_to_delete = st.text_input(f"Step {iteration}: Enter text to remove from '{column}' (case-insensitive)", key=f"text_to_delete_{iteration}_{column}")
                if text_to_delete:
                    column_contains_pairs[column] = text_to_delete

            # Apply cleansing step
            if st.button(f"Cleanse Data (Step {iteration})", key=f"cleanse_button_{iteration}"):
                st.session_state.cleaned_df = cleanse_data_by_contains(st.session_state.cleaned_df, column_contains_pairs)
                st.success(f"Data cleansed at Step {iteration}.")
                st.experimental_rerun()

            # Option to break the loop
            continue_cleansing = st.radio(
                f"Do you want to apply another cleansing step? (Step {iteration})",
                ("No", "Yes"),
                key=f"continue_{iteration}",
                index=0  # Default to "No"
            )
            if continue_cleansing == "No":
                break

            iteration += 1

        # Display the cleaned data preview only after cleansing steps are completed
        st.subheader("Preview of Cleaned Data")
        st.dataframe(st.session_state.cleaned_df)

        # Allow user to download cleaned data
        st.download_button(
            label="Download Cleaned Excel",
            data=download_excel(st.session_state.cleaned_df),
            file_name="cleaned_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        st.error(f"Error: {e}")
