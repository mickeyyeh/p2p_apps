import streamlit as st
import pandas as pd
import io


def duplicate_rows(dataframe, duplicates, values):
    duplicated_rows = []  # Initialize an empty list to store duplicated rows
    for _, row in dataframe.iterrows():
        for i in range(len(values["Weight"])):
            new_row = row.copy()
            for column in values:
                if column in ["ItemDescription", "SKU", "HarmonizationCode"]:
                    new_row[column] = values[column][i]
                elif column == "LineItemQuantity":
                    new_row[column] = int(values[column][i])
                else:
                    new_row[column] = float(values[column][i])
            duplicated_rows.append(new_row)  # Append the new row to the list
    duplicated_dataframe = pd.concat(duplicated_rows, ignore_index=True)
    return duplicated_dataframe



def main():
    st.title("Duplicate Rows App")

    uploaded_file = st.file_uploader(
        "Upload CSV or Excel file", type=["csv", "xlsx"])

    if uploaded_file is not None:
        st.write("Original File:")
        if uploaded_file.name.endswith(".csv"):
            dataframe = pd.read_csv(uploaded_file)
        else:
            dataframe = pd.read_excel(uploaded_file)

        # Convert columns to appropriate data types
        dataframe["Weight"] = dataframe["Weight"].astype(float)
        dataframe["ItemDescription"] = dataframe["ItemDescription"].astype(str)
        dataframe["SKU"] = dataframe["SKU"].astype(str)
        dataframe["HarmonizationCode"] = dataframe["HarmonizationCode"].astype(str)
        dataframe["LineItemQuantity"] = dataframe["LineItemQuantity"].astype(int)
        dataframe["CustomsValue"] = dataframe["CustomsValue"].astype(float)

        st.write(dataframe)

        duplicates = st.number_input(
            "Number of Duplicates", min_value=1, value=1)

        values = {}
        for column in ["Weight", "ItemDescription", "SKU", "HarmonizationCode", "LineItemQuantity", "CustomsValue"]:
            value_str = st.text_input(
                f"Enter values for {column} (comma-separated):")
            values[column] = [val.strip() for val in value_str.split(",")]

        if st.button("Duplicate Rows"):
            duplicated_dataframe = duplicate_rows(
                dataframe, duplicates, values)

            st.write("Final Duplicated File:")
            st.write(duplicated_dataframe)

            # Offer download link for the duplicated file
            if uploaded_file.name.endswith(".csv"):
                csv = duplicated_dataframe.to_csv(index=False)
                st.download_button(
                    label="Download Duplicated CSV",
                    data=csv,
                    file_name="duplicated_data.csv",
                    mime="text/csv"
                )
            else:
                excel_bytes = io.BytesIO()
                duplicated_dataframe.to_excel(excel_bytes, index=False)
                excel_bytes.seek(0)
                st.download_button(
                    label="Download Duplicated Excel",
                    data=excel_bytes,
                    file_name="duplicated_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )


if __name__ == "__main__":
    main()
