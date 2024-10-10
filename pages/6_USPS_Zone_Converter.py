import streamlit as st
import pandas as pd
import os
import base64
import tempfile
import io

# Function to process Excel files


def process_excel_files(excel_files_list):
    updated_df_list = []
    for excelfile in excel_files_list:
        raw_excel = pd.read_excel(
            excelfile, index_col=None, dtype=str, engine='openpyxl')
        processed_data = pd.DataFrame(columns=['ZipCode', 'Zone'])
        for i in range(0, raw_excel.shape[1], 2):
            zip_column = raw_excel.iloc[:, i]
            zone_column = raw_excel.iloc[:, i + 1]
            for zip_code, zone in zip(zip_column, zone_column):
                if pd.isna(zip_code) or pd.isna(zone) or zip_code == "ZIP Code":
                    continue
                zone = str(zone).rstrip('*+')
                if '---' in str(zip_code):
                    start, end = zip_code.split('---')
                    for z in range(int(start), int(end) + 1):
                        processed_data = processed_data.append(
                            {'ZipCode': str(z).zfill(3), 'Zone': zone}, ignore_index=True)
                else:
                    processed_data = processed_data.append(
                        {'ZipCode': str(zip_code).zfill(3), 'Zone': zone}, ignore_index=True)
        updated_df_list.append(processed_data)
    return updated_df_list

# Main Streamlit app


def main():
    st.title("USPS Zone Converter")
    st.write("Link to USPS Official Zone Chart Database: https://postcalc.usps.com/DomesticZoneChart")

    # Upload Excel files
    uploaded_files = st.file_uploader(
        "Upload Excel files", type="xlsx", accept_multiple_files=True)

    if uploaded_files:
        # Process files
        updated_df_list = process_excel_files(uploaded_files)

        # Display processed data
        st.subheader("Processed Data:")
        for i, df in enumerate(updated_df_list):
            st.write(f"File {i + 1}:")
            st.write(df)

        # Download processed files
        st.subheader("Download Processed Files:")
        for i, df in enumerate(updated_df_list):
            excel_bytes = io.BytesIO()
            if uploaded_files[i].name.endswith(".xlsx"):
                df.to_excel(excel_bytes, index=False)
                st.download_button(
                    label=f"Download {uploaded_files[i].name.split('.')[0]}_Transformed.xlsx",
                    data=excel_bytes.getvalue(),
                    file_name=f"{uploaded_files[i].name.split('.')[0]}_Transformed.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            elif uploaded_files[i].name.endswith(".csv"):
                df.to_csv(excel_bytes, index=False)
                st.download_button(
                    label=f"Download {uploaded_files[i].name.split('.')[0]}_Transformed.csv",
                    data=excel_bytes.getvalue(),
                    file_name=f"{uploaded_files[i].name.split('.')[0]}_Transformed.csv",
                    mime="text/csv"
                )


if __name__ == "__main__":
    main()
