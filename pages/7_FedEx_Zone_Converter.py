import streamlit as st
import pandas as pd

import os
import io

# Function to split zip code ranges into individual zip codes


def split_zip_codes(zip_code_range, zone):
    try:
        start, end = zip_code_range.split("-")
        start = int(start)
        end = int(end)
        return [(f"{i:05d}", zone) for i in range(start, end + 1)]
    except ValueError:
        # Handle cases where zip_code_range is not a range
        return [(zip_code_range.strip(), zone)]

# Function to process a single DataFrame


def process_dataframe(df):
    rows = []
    # Iterate through each row in the dataframe
    for index, row in df.iterrows():
        # Iterate through columns in pairs (assuming ZIP Code and Zone)
        for i in range(0, len(df.columns), 2):
            if i+1 >= len(df.columns):
                break  # Avoid IndexError if columns are odd
            # Strip out empty spaces
            zip_code_range = str(row[df.columns[i]]).strip()
            zone = row[df.columns[i+1]]
            if isinstance(zip_code_range, str) and "-" in zip_code_range:
                rows.extend(split_zip_codes(zip_code_range, zone))
            else:
                rows.append((zip_code_range, zone))

    # Create a new dataframe with the split zip codes
    new_df = pd.DataFrame(rows, columns=["Destination Zip", "Zone"])

    # Replace "NA" strings with pandas NA values and clean up
    new_df["Zone"] = new_df["Zone"].astype(str).str.strip()
    new_df = new_df.replace("NA", pd.NA)

    # Drop rows where Zone is empty or null
    new_df = new_df.dropna(subset=["Zone"])

    # Sort the "Destination Zip" column
    new_df = new_df.sort_values(by="Destination Zip").reset_index(drop=True)

    return new_df


# Streamlit App Layout
st.title("FedEx Zone File Converter")
st.write("""
    Upload one or multiple Excel (`.xlsx`) or CSV (`.csv`) FedEx zone files.
    The app will process each file and provide a transformed version for download.
""")
st.write("Official FedEx PARCEL Zone Chart Link: https://www.fedex.com/ratetools/RateToolsMain.do")
st.write("Official FedEx FREIGHT (FTL/LTL) Zone Chart Link: https://fxfzonelocator.van.fedex.com/")

# File uploader allows multiple files and accepts .xlsx and .csv
uploaded_files = st.file_uploader(
    "Choose Excel or CSV files",
    type=["xlsx", "csv"],
    accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_details = {"FileName": uploaded_file.name,
                        "FileType": uploaded_file.type}
        st.write(f"### Processing `{uploaded_file.name}`")

        # Read the uploaded file into a DataFrame
        try:
            if uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file, dtype=str, engine='openpyxl')
            elif uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file, dtype=str)
            else:
                st.error(f"Unsupported file type: {uploaded_file.name}")
                continue
        except Exception as e:
            st.error(f"Error reading `{uploaded_file.name}`: {e}")
            continue

        st.write(f"**Original Dataframe Shape:** {df.shape}")

        # Process the dataframe
        with st.spinner('Processing...'):
            transformed_df = process_dataframe(df)

        st.write(f"**Transformed Dataframe Shape:** {transformed_df.shape}")

        # Convert the transformed dataframe to Excel in memory
        towrite = io.BytesIO()
        try:
            with pd.ExcelWriter(towrite, engine='openpyxl') as writer:
                transformed_df.to_excel(writer, index=False, sheet_name='Transformed')
            towrite.seek(0)
        except Exception as e:
            st.error(f"Error converting transformed data to Excel for `{uploaded_file.name}`: {e}")
            continue

        # Create a download button
        transformed_filename = os.path.splitext(uploaded_file.name)[
            0] + "_transformed.xlsx"
        st.download_button(
            label="Download Transformed File",
            data=towrite,
            file_name=transformed_filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.success(f"**`{transformed_filename}` is ready for download!**")
        st.markdown("---")
else:
    st.info(
        "Please upload at least one Excel (`.xlsx`) or CSV (`.csv`) file to get started.")
