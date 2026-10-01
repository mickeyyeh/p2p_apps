import streamlit as st
import pandas as pd
import numpy as np
import re
import io
from typing import Union


# Function to round up numbers
def round_up(n: float, decimals: int = 0) -> float:
    """Rounds up a number to the specified number of decimal places."""
    import math
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

# Function to parse multiplier input


def parse_multiplier(multiplier: str) -> float:
    """Parses the multiplier input and returns a float value."""
    if multiplier.endswith('%'):
        return 1 + float(multiplier.strip('%')) / 100
    else:
        return float(multiplier)

# Function to transform data


def transform_data(df: pd.DataFrame, multiplier: float = 1) -> Union[pd.DataFrame, None]:
    """Transforms the input data based on the specified rules."""

    # Check if file has 15.99 oz
    if (df['Weight'].astype(float) >= 0.996).any() and (df['Weight'].astype(float) <= 1).any():
        st.write('Note: File has 15.99 oz weight')
    else:
        st.write('Note: File does NOT have 15.99 oz weight')

    ## -- Weight Transformation Starts Here --##
    if 'Weight Min' in df.columns or 'Weight Max' in df.columns:
        # Melt the DataFrame to transform zone columns into rows
        zone_cols = df.columns[2:]
        transformed_df = pd.melt(df, id_vars=[
                                 'Weight Min', 'Weight Max'], value_vars=zone_cols, var_name='Zone', value_name='Rate')

        # Extract zone number from Zone column
        transformed_df['Zone'] = transformed_df['Zone'].apply(
            lambda x: x.split(' ')[1])

        # Add Country column
        transformed_df['Country'] = 'USA'

        # Reorder columns
        transformed_df = transformed_df[[
            'Country', 'Zone', 'Weight Min', 'Weight Max', 'Rate']]

        # Apply multiplier to Rate column
        transformed_df['Rate'] = transformed_df['Rate'].apply(
            lambda x: round_up(x * multiplier, 2))

        return transformed_df

    # For those less than 1lb: condition for rate sheets without a 15.99 oz rate (stopping at 15oz)
    elif 'Weight' in df.columns:
        # Calculate Weight Max column
        df['Weight Max'] = df['Weight'].astype(
            float).apply(lambda x: round_up(x, 3))

        # Calculate Weight Min column
        df['Weight Min'] = df['Weight Max'].shift(fill_value=0).astype(float)
        df.iloc[0, df.columns.get_loc('Weight Min')] = 0

        # Check if 'Weight' column contains any of the values [0.997, 0.9999375, 0.999938]
        special_weights = [0.997, 0.9999375, 0.999938]
        if df['Weight'].astype(float).isin(special_weights).any():
            mask_special = df['Weight Max'].isin(special_weights)
            mask_next = (df['Weight Max'] == 1) & df['Weight Max'].shift(
                1).isin(special_weights)

            df.loc[mask_special, 'Weight Min'] = 0.939
            df.loc[mask_special, 'Weight Max'] = df['Weight Max'] + 0.001
            df.loc[mask_next, 'Weight Min'] = 0.999
            df.loc[mask_next, 'Weight Max'] = 1

            # Calculate Weight Min for other weights
            mask_other = ~(mask_special | mask_next)
            for i in range(1, len(df)):
                if mask_other.iloc[i]:
                    df.iloc[i, df.columns.get_loc(
                        'Weight Min')] = df.iloc[i-1, df.columns.get_loc('Weight Max')] + 0.001
        else:
            # Vectorized operations to calculate Weight Min and Weight Max columns
            for i in range(1, len(df)):
                df.iloc[i, df.columns.get_loc(
                    'Weight Min')] = df.iloc[i-1, df.columns.get_loc('Weight Max')] + 0.001

        mask2 = (df['Weight Min'] == 0) & (df['Weight Max'] == 1)
        mask6 = df['Weight Max'] > 1

        df.loc[mask2, 'Weight Max'] = df.loc[mask2, 'Weight Max']
        df.loc[mask6, 'Weight Max'] = df.loc[mask6, 'Weight Max']

        # Melt the DataFrame to transform zone columns into rows
        zone_cols = df.columns[2:-2]
        transformed_df = pd.melt(df, id_vars=[
                                 'Weight Min', 'Weight Max'], value_vars=zone_cols, var_name='Zone', value_name='Rate')

        # Extract zone number from Zone column
        transformed_df['Zone'] = transformed_df['Zone'].apply(
            lambda x: x.split(' ')[1])

        # Add Country column and empty columns
        transformed_df['Country'] = 'USA'
        transformed_df['empty_col1'] = pd.NA
        transformed_df['empty_col2'] = pd.NA
        transformed_df['empty_col3'] = pd.NA

        # Reorder columns
        transformed_df = transformed_df[['Country', 'Zone', 'empty_col1',
                                        'Weight Min', 'Weight Max', 'empty_col2', 'empty_col3', 'Rate']]

        # Drop empty columns
        transformed_df = transformed_df[[
            'Country', 'Zone', 'Weight Min', 'Weight Max', 'Rate']]

        # Apply multiplier to Rate column
        transformed_df['Rate'] = transformed_df['Rate'].apply(
            lambda x: round_up(x * multiplier, 2))

        # Drop rows where Weight Min is 1.0009
        transformed_df = transformed_df[transformed_df['Weight Min'] != 1.0009]

        return transformed_df

    else:
        st.write(
            "Column names 'Weight' or 'Unit' not found. Please check the column names in your file.")
        return None

# Main function


def main() -> None:
    """The main function that runs the Streamlit app."""
    st.title("Data Transformation App")
    uploaded_files = st.file_uploader("Upload CSV or Excel files", type=[
                                      "csv", "xlsx"], accept_multiple_files=True)

    if uploaded_files:
        transformed_df_list = []
        original_df_list = []
        transformed_file_name = []
        for uploaded_file in uploaded_files:
            try:
                if uploaded_file.name.endswith(".csv"):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(
                        uploaded_file, index_col=None, engine="openpyxl")

                # Convert the 'unit' column to string type if it exists
                if 'unit' in df.columns:
                    df['unit'] = df['unit'].astype(str)

                original_df_list.append(df)
                transformed_file_name.append(uploaded_file.name)
            except Exception as e:
                st.write(f"Error: {e}")

        if original_df_list:
            st.write("Preview of original data:")
            for i, df in enumerate(original_df_list):
                st.write(f"File: {transformed_file_name[i]}")
                st.write(df)

            multiplier = st.text_input(
                "Enter Multiplier to Add Margins (e.g. 1.2 or 20%):", value="1")
            try:
                multiplier = parse_multiplier(multiplier)
            except ValueError:
                st.write(
                    "Invalid multiplier format. Please use a number or a percentage (e.g. 1.2 or 20%).")
                multiplier = 1  # Set default multiplier value

            transformed_df_list = []
            for df in original_df_list:
                transformed_df = transform_data(df, multiplier)
                if transformed_df is not None:
                    transformed_df_list.append(transformed_df)

            if transformed_df_list:
                st.write("Preview of transformed data:")
                preview_df = pd.concat(transformed_df_list, ignore_index=True)
                st.write(preview_df)

                @st.cache_data
                def convert_df_to_excel(df: pd.DataFrame) -> bytes:
                    """Converts a DataFrame to Excel format."""
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                        df.to_excel(writer, index=False)
                    return output.getvalue()

                excel_data = convert_df_to_excel(preview_df)

                # Get the original file name and add "_transformed" to it
                if len(transformed_file_name) == 1:
                    file_name = transformed_file_name[0].split(
                        '.')[0] + "_transformed.xlsx"
                else:
                    file_name = "transformed_data.xlsx"

                # Allow the user to edit the file name
                file_name = st.text_input("Enter file name:", value=file_name)

                # Ensure the file name ends with ".xlsx"
                if not file_name.endswith(".xlsx"):
                    file_name += ".xlsx"

                st.download_button(
                    label="Download transformed data as Excel",
                    data=excel_data,
                    file_name=file_name,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )


if __name__ == "__main__":
    main()
