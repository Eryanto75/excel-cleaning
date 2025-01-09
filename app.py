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
        df = pd.read_excel(uploaded_file)
        st.success("File uploaded successfully!")

        # Display entire data
        st.subheader("Preview of Uploaded Data")
        st.dataframe(df)  # Display all rows

        # Iterative cleansing loop
        continue_cleansing = "No"
        iteration = 0
        while continue_cleansing == "Yes" or iteration == 0:
            iteration += 1
            # Select columns and specify text patterns to delete
            columns = df.columns.tolist()
            column_contains_pairs = {}
            selected_columns = st.multiselect(f"Step {iteration}: Select columns to clean", options=columns, key=f"select_columns_{iteration}")
            for column in selected_columns:
                text_to_delete = st.text_input(f"Step {iteration}: Enter text to remove from '{column}' (case-insensitive)", key=f"text_to_delete_{iteration}_{column}")
                if text_to_delete:
                    column_contains_pairs[column] = text_to_delete

            if st.button(f"Cleanse Data (Step {iteration})", key=f"cleanse_button_{iteration}"):
                df = cleanse_data_by_contains(df, column_contains_pairs)
                st.subheader(f"Preview of Cleaned Data (After Step {iteration})")
                st.dataframe(df)  # Display all rows

                # Option to continue cleansing
                continue_cleansing = st.radio(f"Do you want to apply another cleansing step? (Step {iteration})", ("No", "Yes"), key=f"continue_{iteration}")

        # Allow user to download cleaned data
        st.download_button(
            label="Download Cleaned Excel",
            data=download_excel(df),
            file_name="cleaned_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        st.error(f"Error: {e}")
