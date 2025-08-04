import streamlit as st
import pandas as pd

import io
import re
from typing import Union


# def color_columns(val: str, data_columns: list[str]) -> str:
#     color = 'yellow' if val in data_columns else ''
#     return f'background-color: {color}'


def find_tracking_column(columns: list[str]) -> Union[str, None]:
    tracking_keywords = ['tracking', 'track', 'awb', 'tracking number']
    for column in columns:
        if any(re.search(keyword, column, re.IGNORECASE) for keyword in tracking_keywords):
            return column
    return None


def main() -> None:
    st.title("Add SETA Columns")

    # File upload section
    st.header("Upload Files")
    invoice_file: st.runtime.uploaded_file_manager.UploadedFile | None = st.file_uploader(
        "Select Invoice File (`Excel-xlsx`/`.csv`)", type=['csv', 'xlsx'])
    data_file: st.runtime.uploaded_file_manager.UploadedFile | None = st.file_uploader(
        "Select Data File  (`Excel-xlsx`/`.csv`)", type=['csv', 'xlsx'])

    if invoice_file and data_file:
        # Read files
        if invoice_file.name.endswith('.csv'):
            invoice_df: pd.DataFrame = pd.read_csv(invoice_file, dtype='str')
        else:
            invoice_df = pd.read_excel(invoice_file, dtype='str')

        if data_file.name.endswith('.csv'):
            data_df: pd.DataFrame = pd.read_csv(data_file, dtype='str')
        else:
            data_df = pd.read_excel(data_file, dtype='str')

        # Column selection section
        st.header("Select Merge Columns")
        invoice_columns: list[str] = list(invoice_df.columns)
        data_columns: list[str] = list(data_df.columns)
        default_invoice_column = find_tracking_column(
            invoice_columns) or invoice_columns[0]
        default_data_column = find_tracking_column(
            data_columns) or data_columns[0]
        invoice_merge_column: str = st.selectbox(
            "Select Invoice Column", invoice_columns, index=invoice_columns.index(default_invoice_column))
        data_merge_column: str = st.selectbox(
            "Select Data Column", data_columns, index=data_columns.index(default_data_column))

        # Join type selection section
        st.header("Select Join Type")
        join_types: list[str] = ['Left Join',
                                 'Right Join', 'Inner Join', 'Outer Join']
        join_type: str = st.selectbox("Select Join Type", join_types, index=0)

        # Merge dataframes
        if join_type == 'Left Join':
            merged_df: pd.DataFrame = pd.merge(
                invoice_df, data_df, left_on=invoice_merge_column, right_on=data_merge_column, how='left')
        elif join_type == 'Right Join':
            merged_df = pd.merge(
                invoice_df, data_df, left_on=invoice_merge_column, right_on=data_merge_column, how='right')
        elif join_type == 'Inner Join':
            merged_df = pd.merge(
                invoice_df, data_df, left_on=invoice_merge_column, right_on=data_merge_column, how='inner')
        else:
            merged_df = pd.merge(
                invoice_df, data_df, left_on=invoice_merge_column, right_on=data_merge_column, how='outer')

        # Preview section
        st.header("Preview")

        # # Highlight columns to a different color -> Not Working
        # def highlight_columns(x):
        #     return color_columns(x, list(data_df.columns))
        # st.write(merged_df.style.map(highlight_columns))

        # Download section
        st.header("Download")
        if invoice_file.name.endswith('.csv'):
            default_filename: str = invoice_file.name.replace('.csv', '_customer_added')
        else:
            default_filename = invoice_file.name.replace('.xlsx', '_customer_added')
        filename: str = st.text_input("Enter filename", value=default_filename)
        output = io.BytesIO()
        merged_df.to_excel(output, index=False)
        output.seek(0)
        st.download_button(label="Download File", data=output.getvalue(), file_name=f'{filename}.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


if __name__ == "__main__":
    main()
