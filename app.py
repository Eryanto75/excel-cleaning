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

        # Initialize session state for the original and cleaned data
        if "cleaned_df" not in st.session_state:
            st.session_state.cleaned_df = original_df.copy()

        # Display original data for reference
        st.subheader("Original Data Preview")
        st.dataframe(original_df)

        # Dictionary to store conditions for cleansing
        column_contains_pairs = {}

        # Condition 1
        st.markdown("### Condition 1: Remove values from column")
        column_1 = st.selectbox("Select column for Condition 1", original_df.columns, key="cond1_col")
        value_1 = st.text_input(f"Enter text to remove from '{column_1}'", key="cond1_val")
        if column_1 and value_1:
            column_contains_pairs[column_1] = value_1

        # Condition 2
        st.markdown("### Condition 2: Remove values from column")
        column_2 = st.selectbox("Select column for Condition 2", original_df.columns, key="cond2_col")
        value_2 = st.text_input(f"Enter text to remove from '{column_2}'", key="cond2_val")
        if column_2 and value_2:
            column_contains_pairs[column_2] = value_2

        # Condition 3
        st.markdown("### Condition 3: Remove values from column")
        column_3 = st.selectbox("Select column for Condition 3", original_df.columns, key="cond3_col")
        value_3 = st.text_input(f"Enter text to remove from '{column_3}'", key="cond3_val")
        if column_3 and value_3:
            column_contains_pairs[column_3] = value_3

        # Apply all conditions button
        if st.button("Apply All Conditions"):
            st.session_state.cleaned_df = cleanse_data_by_contains(st.session_state.cleaned_df, column_contains_pairs)
            st.success("All conditions have been applied!")

        # Display the cleaned data preview
        st.subheader("Cleaned Data Preview")
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
