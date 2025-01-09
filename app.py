import streamlit as st
import pandas as pd

st.title("Data Cleaning App")

# Upload file CSV
uploaded_file = st.file_uploader("Upload CSV file", type="csv")

if uploaded_file is not None:
    # Membaca file CSV ke dalam DataFrame
    df = pd.read_csv(uploaded_file)
    st.write("Original Data:")
    st.write(df)
    
    # Pembersihan data
    df_cleaned = df[~df['ItemName'].str.startswith(('in/', 'js/'))]
    df_cleaned = df_cleaned[df_cleaned['VEN'] != 'V']
    
    st.write("Cleaned Data:")
    st.write(df_cleaned)
    
    # Tombol untuk mendownload data yang telah dibersihkan
    csv = df_cleaned.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Cleaned CSV",
        data=csv,
        file_name='cleaned_data.csv',
        mime='text/csv'
    )
else:
    st.write("Please upload a CSV file to clean the data.")
