# # import pandas as pd
# # import numpy as np
# # import openpyxl
# # import pycountry
# # import streamlit as st

# # from utils.vat_calculator.country_formatter import format_country


# # def getFile(uploaded_file, type="xlsx"):
# #     valid = ["csv", "xlsx"]

# #     if uploaded_file is not None:
# #         if type not in valid:
# #             raise ValueError("results: status must be one of %r." % valid)

# #         elif type == "csv":
# #             return pd.read_csv(uploaded_file)

# #         else:
# #             return pd.read_excel(uploaded_file)


# # def vatter(df):
# #     # load in vat table
# #     vat = pd.read_excel(
# #         "utils/vat_calculator/uk-eu vat rates.xlsx", engine="openpyxl")
# #     vat.rename(columns={"countrycode": "ISO_code"}, inplace=True)
# #     df = format_country(df, "Country")
# #     df = df.merge(vat, on="ISO_code")
# #     df['VAT value'] = df['Package Value'] * df["vat_rate"]
# #     df = df.loc[df['Package Value'] < 150]
# #     return df


# # # @st.cache_data
# # @st.cache
# # def convert_df(df):
# #     # IMPORTANT: Cache the conversion to prevent computation on every rerun
# #     return df.to_csv(index=False)


# # def main():
# #     st.title("VAT Calculator")
# #     st.subheader("Please add data below")
# #     uploaded_file = st.file_uploader("Choose a file")
# #     df = getFile(uploaded_file)

# #     if uploaded_file:
# #         df = vatter(df)

# #         st.subheader("User Inputs")
# #         st.write(df)

# #         fileName = st.text_input("What is the file name?")

# #         csv = convert_df(df)
# #         if fileName:
# #             st.download_button(
# #                 label="Download data as CSV",
# #                 data=csv,
# #                 file_name=f'{fileName}.csv'
# #             )


# # if __name__ == '__main__':
# #     main()



# import pandas as pd
# import openpyxl
# import streamlit as st
# from io import BytesIO

# from utils.vat_calculator.country_formatter import format_country
# from typing import Optional


# def getFile(uploaded_file: Optional[st.runtime.uploaded_file_manager.UploadedFile], file_type: str = "xlsx") -> Optional[pd.DataFrame]:
#     valid = ["csv", "xlsx"]

#     if uploaded_file is not None:
#         if file_type not in valid:
#             raise ValueError(f"File type must be one of {valid}.")
#         elif file_type == "csv":
#             return pd.read_csv(uploaded_file, dtype=str)
#         else:
#             return pd.read_excel(uploaded_file, dtype=str)
#     else:
#         return None


# def vatter(df: pd.DataFrame) -> pd.DataFrame:
#     # Load in VAT table
#     vat = pd.read_excel(
#         "utils/vat_calculator/uk-eu vat rates.xlsx", engine="openpyxl"
#     )
#     vat.rename(columns={"countrycode": "ISO_code"}, inplace=True)
#     df = format_country(df, "Country")
#     df = df.merge(vat, on="ISO_code")
#     # convert column format
#     df['Package Value'] = df['Package Value'].astype(float)
#     df["vat_rate"] = df["vat_rate"].astype(float)
#     df['VAT value'] = df['Package Value'] * df["vat_rate"]
#     df = df.loc[df['Package Value'] < 150]
#     return df


# # @st.cache  # Consider using @st.cache_data if using Streamlit version >= 1.18
# # def convert_df(df: pd.DataFrame) -> str:
# #     # IMPORTANT: Cache the conversion to prevent computation on every rerun
# #     return df.to_csv(index=False)

# @st.cache  # Consider using @st.cache_data if using Streamlit version >= 1.18
# def convert_df_to_excel(df: pd.DataFrame) -> BytesIO:
#     # Cache the conversion to prevent computation on every rerun
#     output = BytesIO()
#     writer = pd.ExcelWriter(output, engine='openpyxl')
#     df.to_excel(writer, index=False, sheet_name='Sheet1')
#     writer.save()
#     output.seek(0)  # Set cursor back to the beginning of the file
#     return output


# # # Download as CSV
# # def main() -> None:
# #     st.title("VAT Calculator")
# #     st.subheader("Please add data below")
# #     uploaded_file = st.file_uploader("Choose a file")

# #     if uploaded_file:
# #         df = getFile(uploaded_file)
# #         if df is not None:
# #             df = vatter(df)

# #             st.subheader("User Inputs")
# #             st.write(df)

# #             file_name = st.text_input("What is the file name?")

# #             csv = convert_df(df)
# #             if file_name:
# #                 st.download_button(
# #                     label="Download data as CSV",
# #                     data=csv,
# #                     file_name=f'{file_name}.csv'
# #                 )
# #         else:
# #             st.error(
# #                 "Failed to read the uploaded file. Please check the file format.")
# #     else:
# #         st.info("Please upload a CSV or Excel file to proceed.")


# # if __name__ == '__main__':
# #     main()

# # Download as Excel
# def main() -> None:
#     st.title("VAT Calculator")
#     st.subheader("Please add data below")
#     uploaded_file = st.file_uploader("Choose a file")

#     if uploaded_file:
#         df = getFile(uploaded_file)
#         if df is not None:
#             df = vatter(df)

#             st.subheader("User Inputs")
#             st.write(df)

#             if uploaded_file.name.endswith('.csv'):
#                 default_filename: str = uploaded_file.name.replace('.csv', '_VAT_ADDED')
#             else:
#                 default_filename = uploaded_file.name.replace('.xlsx', '_VAT_ADDED')
                
#             file_name: str = st.text_input("Enter filename", value=default_filename)

#             excel_data = convert_df_to_excel(df)
#             if file_name:
#                 st.download_button(
#                     label="Download data as Excel",
#                     data=excel_data,
#                     file_name=f'{file_name}.xlsx',
#                     mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
#                 )
#         else:
#             st.error(
#                 "Failed to read the uploaded file. Please check the file format.")
#     else:
#         st.info("Please upload a CSV or Excel file to proceed.")


# if __name__ == '__main__':
#     main()

import pandas as pd
import openpyxl
import streamlit as st
from io import BytesIO

from utils.vat_calculator.country_formatter import format_country
from typing import Optional


def getFile(uploaded_file: Optional[st.runtime.uploaded_file_manager.UploadedFile], file_type: str = "xlsx") -> Optional[pd.DataFrame]:
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


def vatter(df: pd.DataFrame) -> pd.DataFrame:
    # Load in VAT table
    vat = pd.read_excel(
        "utils/vat_calculator/uk-eu vat rates.xlsx", engine="openpyxl"
    )
    vat.rename(columns={"countrycode": "ISO_code"}, inplace=True)
    df = format_country(df, "Country")
    df = df.merge(vat, on="ISO_code")
    # convert column format
    df['Package Value'] = df['Package Value'].astype(float)
    df["vat_rate"] = df["vat_rate"].astype(float)
    df['VAT value'] = df['Package Value'] * df["vat_rate"]
    df = df.loc[df['Package Value'] < 150]
    return df


@st.cache_data  # Updated from @st.cache to avoid deprecation warning
def convert_df_to_excel(df: pd.DataFrame) -> BytesIO:
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    output.seek(0)  # Reset to beginning
    return output


# Download as Excel
def main() -> None:
    st.title("VAT Calculator")
    st.subheader("Please add data below")
    uploaded_file = st.file_uploader("Choose a file")

    if uploaded_file:
        df = getFile(uploaded_file)
        if df is not None:
            df = vatter(df)

            st.subheader("User Inputs")
            st.write(df)

            if uploaded_file.name.endswith('.csv'):
                default_filename: str = uploaded_file.name.replace('.csv', '_VAT_ADDED')
            else:
                default_filename = uploaded_file.name.replace('.xlsx', '_VAT_ADDED')
                
            file_name: str = st.text_input("Enter filename", value=default_filename)

            excel_data = convert_df_to_excel(df)
            if file_name:
                st.download_button(
                    label="Download data as Excel",
                    data=excel_data,
                    file_name=f'{file_name}.xlsx',
                    mime='application/vnd.openxmlformats-officerspreadsheetml.sheet'
                )
        else:
            st.error(
                "Failed to read the uploaded file. Please check the file format.")
    else:
        st.info("Please upload a CSV or Excel file to proceed.")


if __name__ == '__main__':
    main()
