import streamlit as st
import pandas as pd

st.title("Data Cleaning App")

# Fungsi untuk membaca file, baik itu CSV atau Excel
def load_data(file):
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    elif file.name.endswith(('.xls', '.xlsx')):
        return pd.read_excel(file)
    else:
        st.error("Unsupported file format. Please upload a CSV or Excel file.")
        return None

# Upload file CSV atau Excel
uploaded_file = st.file_uploader("Upload CSV or Excel file", type=['csv', 'xls', 'xlsx'])

if uploaded_file is not None:
    # Membaca file ke dalam DataFrame
    df = load_data(uploaded_file)
    
    if df is not None:
        st.write("Original Data:")
        st.write(df)

        # Pembersihan data
        df_cleaned = df[~df['ItemName'].str.startswith(('in/', 'js/'))]
        df_cleaned = df_cleaned[df_cleaned['VEN'] != 'V']

        st.write("Cleaned Data:")
        st.write(df_cleaned)

        # Tombol untuk mendownload data yang telah dibersihkan
        file_extension = 'csv' if uploaded_file.name.endswith('.csv') else 'xlsx'
        if file_extension == 'csv':
            cleaned_file = df_cleaned.to_csv(index=False).encode('utf-8')
            mime_type = 'text/csv'
        else:
            cleaned_file = df_cleaned.to_excel(index=False, engine='xlsxwriter')
            mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

        st.download_button(
            label="Download Cleaned File",
            data=cleaned_file,
            file_name=f'cleaned_data.{file_extension}',
            mime=mime_type
        )
else:
    st.write("Please upload a CSV or Excel file to clean the data.")
