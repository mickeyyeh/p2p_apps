import streamlit as st
import pandas as pd
import io
from typing import Optional, List, Dict, Any


# ---------------------------------------------------------
# Function to parse the listItems column correctly
# ---------------------------------------------------------
def parse_items(cell: Any) -> List[Dict[str, Any]]:
    """
    Parse a cell from the 'listItems' column into a list of item dictionaries.

    Each item dictionary contains:
        - description (str)
        - qty (float)
        - price (float)

    Args:
        cell (Any): The cell value from the DataFrame (could be str or NaN).

    Returns:
        List[Dict[str, Any]]: A list of parsed items.
    """
    if pd.isna(cell):
        return []

    # Split at '---' which separates each item
    item_strings = str(cell).split('---')
    items: List[Dict[str, Any]] = []

    for item_str in item_strings:
        parts = item_str.split('|')

        # Basic validation: description is always at index 4
        if len(parts) < 11:
            continue

        desc = parts[4]

        # Qty and Price fields (must be numeric)
        try:
            qty = float(parts[8])
            price = float(parts[9])
        except ValueError:
            continue

        items.append({"description": desc, "qty": qty, "price": price})

    return items


# ---------------------------------------------------------
# Function to read uploaded file into a DataFrame
# ---------------------------------------------------------
def getFile(uploaded_file: Optional[
    st.runtime.uploaded_file_manager.UploadedFile],
            file_type: str = "xlsx") -> Optional[pd.DataFrame]:
    """
    Read an uploaded file (CSV or Excel) into a pandas DataFrame.

    Args:
        uploaded_file (UploadedFile): The file uploaded via Streamlit.
        file_type (str): The type of file ('csv' or 'xlsx').

    Returns:
        Optional[pd.DataFrame]: The DataFrame if successful, else None.
    """
    valid = ["csv", "xlsx"]

    if uploaded_file is not None:
        if file_type not in valid:
            raise ValueError(f"File type must be one of {valid}.")
        elif file_type == "csv":
            return pd.read_csv(uploaded_file, dtype=str)
        else:
            return pd.read_excel(uploaded_file, dtype=str)
    else:
        return None


# ---------------------------------------------------------
# Main Streamlit App
# ---------------------------------------------------------
def main() -> None:
    """
    Main function to run the Streamlit app.
    Allows user to upload a file, process 'listItems', and download Excel output.
    """
    st.title("CSV Processor: Parse listItems and Generate Excel Output")

    # File uploader widget
    uploaded_file = st.file_uploader("Choose a file")

    if uploaded_file:
        # Read the uploaded file into a DataFrame
        df = getFile(uploaded_file)
        if df is not None:
            # Lists to store processed data
            descriptions: List[str] = []
            quantities: List[str] = []
            prices: List[str] = []
            total_prices: List[float] = []

            # Process each row in 'listItems'
            for cell in df["listItems"]:
                items = parse_items(cell)
                descriptions.append(", ".join(item["description"]
                                              for item in items))
                quantities.append(", ".join(
                    str(item["qty"]) for item in items))
                prices.append(", ".join(str(item["price"]) for item in items))
                total_value = sum(item["qty"] * item["price"]
                                  for item in items)
                total_prices.append(total_value)

            # Add new columns to DataFrame
            df["Description"] = descriptions
            df["Qty"] = quantities
            df["Price"] = prices
            df["totalprice"] = total_prices

            # Show preview of processed data
            st.subheader("Processed Data Preview")
            st.dataframe(df.head())

            # Convert DataFrame to Excel for download
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='ProcessedData')
            output.seek(0)

            # Allow user to specify the file name for download
            default_file_name = uploaded_file.name.split(
                '.')[0] + '_transformed'
            file_name = st.text_input("Enter file name for download:",
                                      default_file_name)

            if file_name:
                st.download_button(
                    label="Download Processed Excel",
                    data=output,
                    file_name=f'{file_name}.xlsx',
                    mime=
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        else:
            st.error(
                "Failed to read the uploaded file. Please check the file format."
            )
    else:
        st.info("Please upload a CSV or Excel file to proceed.")


# ---------------------------------------------------------
# Entry point
# ---------------------------------------------------------
if __name__ == '__main__':
    main()
