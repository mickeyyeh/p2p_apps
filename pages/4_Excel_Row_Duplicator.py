import streamlit as st
import pandas as pd
import io


def duplicate_rows(dataframe, duplicates, values):
    duplicated_dataframe = pd.DataFrame(columns=dataframe.columns)
    for index, row in dataframe.iterrows():
        for i in range(len(values["Weight"])):
            new_row = row.copy()
            for column in values:
                if column in ["ItemDescription", "SKU", "HarmonizationCode"]:
                    new_row[column] = values[column][i]
                elif column == "LineItemQuantity":
                    new_row[column] = int(values[column][i])
                else:
                    new_row[column] = float(values[column][i])
            duplicated_dataframe = duplicated_dataframe.append(
                new_row, ignore_index=True)
    return duplicated_dataframe


def main():
    st.title("Excel Row Duplicator")

    uploaded_file = st.file_uploader(
        "Upload CSV or Excel file", type=["csv", "xlsx"])

    if uploaded_file is not None:
        st.write("Original File:")
        if uploaded_file.name.endswith(".csv"):
            dataframe = pd.read_csv(uploaded_file)
        else:
            dataframe = pd.read_excel(uploaded_file)

        st.write(dataframe)

        duplicates = st.number_input(
            "Number of Duplicates", min_value=1, value=1)

        values = {}
        for column in ["Weight", "ItemDescription", "HarmonizationCode", "LineItemQuantity", "CustomsValue"]:
            value_str = st.text_input(
                f"Enter values for {column} (comma-separated):")
            values[column] = [val.strip() for val in value_str.split(",")]

        file_name = st.text_input(
            "Enter file name (without extensions: .xlsx or .csv):", value="edited_data")

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
                    file_name=f"{file_name}.csv",
                    mime="text/csv"
                )
            else:
                excel_bytes = io.BytesIO()
                duplicated_dataframe.to_excel(excel_bytes, index=False)
                excel_bytes.seek(0)
                st.download_button(
                    label="Download Duplicated Excel",
                    data=excel_bytes,
                    file_name=f"{file_name}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )


if __name__ == "__main__":
    main()
