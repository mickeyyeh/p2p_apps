# import pandas as pd
# import numpy as np
# import openpyxl
# import pycountry
# import streamlit as st

# from utils.vat_calculator.country_formatter import format_country


# def getFile(uploaded_file, type="xlsx"):
#     valid = ["csv", "xlsx"]

#     if uploaded_file is not None:
#         if type not in valid:
#             raise ValueError("results: status must be one of %r." % valid)

#         elif type == "csv":
#             return pd.read_csv(uploaded_file)

#         else:
#             return pd.read_excel(uploaded_file)


# def vatter(df):
#     # load in vat table
#     vat = pd.read_excel(
#         "utils/vat_calculator/uk-eu vat rates.xlsx", engine="openpyxl")
#     vat.rename(columns={"countrycode": "ISO_code"}, inplace=True)
#     df = format_country(df, "Country")
#     df = df.merge(vat, on="ISO_code")
#     df['VAT value'] = df['Package Value'] * df["vat_rate"]
#     df = df.loc[df['Package Value'] < 150]
#     return df


# # @st.cache_data
# @st.cache
# def convert_df(df):
#     # IMPORTANT: Cache the conversion to prevent computation on every rerun
#     return df.to_csv(index=False)


# def main():
#     st.title("VAT Calculator")
#     st.subheader("Please add data below")
#     uploaded_file = st.file_uploader("Choose a file")
#     df = getFile(uploaded_file)

#     if uploaded_file:
#         df = vatter(df)

#         st.subheader("User Inputs")
#         st.write(df)

#         fileName = st.text_input("What is the file name?")

#         csv = convert_df(df)
#         if fileName:
#             st.download_button(
#                 label="Download data as CSV",
#                 data=csv,
#                 file_name=f'{fileName}.csv'
#             )


# if __name__ == '__main__':
#     main()


import pandas as pd
import numpy as np
import openpyxl
import pycountry
import streamlit as st

from utils.vat_calculator.country_formatter import format_country
from typing import Optional


def getFile(uploaded_file: Optional[st.runtime.uploaded_file_manager.UploadedFile], file_type: str = "xlsx") -> Optional[pd.DataFrame]:
    valid = ["csv", "xlsx"]

    if uploaded_file is not None:
        if file_type not in valid:
            raise ValueError(f"File type must be one of {valid}.")
        elif file_type == "csv":
            return pd.read_csv(uploaded_file)
        else:
            return pd.read_excel(uploaded_file)
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
    df['VAT value'] = df['Package Value'] * df["vat_rate"]
    df = df.loc[df['Package Value'] < 150]
    return df


@st.cache  # Consider using @st.cache_data if using Streamlit version >= 1.18
def convert_df(df: pd.DataFrame) -> str:
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False)


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

            file_name = st.text_input("What is the file name?")

            csv = convert_df(df)
            if file_name:
                st.download_button(
                    label="Download data as CSV",
                    data=csv,
                    file_name=f'{file_name}.csv'
                )
        else:
            st.error(
                "Failed to read the uploaded file. Please check the file format.")
    else:
        st.info("Please upload a CSV or Excel file to proceed.")


if __name__ == '__main__':
    main()
