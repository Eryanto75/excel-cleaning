import streamlit as st
import pandas as pd
from io import BytesIO

# Fungsi untuk menghapus nilai tertentu dalam kolom
def cleanse_data_by_contains(df, column_contains_pairs):
    for column, text_to_delete in column_contains_pairs.items():
        if column in df.columns and text_to_delete:
            # Escape any special characters in the text_to_delete
            text_to_delete_escaped = text_to_delete.replace('/', '\/')
            df = df[~df[column].str.contains(text_to_delete_escaped, na=False, case=False)]
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
    try:
        # Load the entire file
        original_df = pd.read_excel(uploaded_file)
        st.success("File uploaded successfully!")

        # Initialize session state for the original and cleaned data
        if "cleaned_df" not in st.session_state:
            st.session_state.cleaned_df = original_df.copy()
        if "conditions" not in st.session_state:
            st.session_state.conditions = []

        # Display original data for reference
        st.subheader("Original Data Preview")
        st.dataframe(original_df)

        # Dynamic conditions input
        st.subheader("Cleansing Conditions")
        for i, condition in enumerate(st.session_state.conditions):
            col1, col2 = st.columns(2)
            with col1:
                selected_column = st.selectbox(f"Select column for Condition {i+1}", original_df.columns, key=f"col_{i}", index=original_df.columns.get_loc(condition["column"]) if condition["column"] in original_df.columns else 0)
            with col2:
                text_to_remove = st.text_input(f"Text to remove for Condition {i+1}", condition["text"], key=f"text_{i}")

            # Update condition in session state
            st.session_state.conditions[i] = {"column": selected_column, "text": text_to_remove}

        # Button to add new condition
        if st.button("Add New Condition"):
            st.session_state.conditions.append({"column": original_df.columns[0], "text": ""})

        # Apply all conditions button
        if st.button("Apply All Conditions"):
            column_contains_pairs = {condition["column"]: condition["text"] for condition in st.session_state.conditions if condition["text"]}
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
