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
#             return pd.read_csv(uploaded_file, dtype="str")

#         else:
#             return pd.read_excel(uploaded_file, dtype="str")


# def vatter(df):
#     # load in vat table
#     vat = pd.read_excel(
#         "utils/vat_calculator/uk-eu vat rates.xlsx", engine="openpyxl")
#     vat.rename(columns={"countrycode": "ISO_code"}, inplace=True)
#     df = format_country(df, "Country")
#     df = df.merge(vat, on="ISO_code")
#     # convert column typee from str to float
#     df['Package Value'] = df['Package Value'].astype(float)
#     df["vat_rate"] = df["vat_rate"].astype(float)
#     df['VAT value'] = df['Package Value'] * df["vat_rate"]
#     df = df.loc[df['Package Value'] < 150]
#     return df


# # @st.cache_data
# @st.cache
# def convert_df(df, file_name):
#     # IMPORTANT: Cache the conversion to prevent computation on every rerun
#     return df.to_excel(file_name, index=False)


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

#         csv_df = convert_df(df, fileName)
#         if fileName:
#             st.download_button(
#                 label="Download data as Excel (xlsx)",
#                 data=csv_df,
#                 file_name=f'{fileName}.xlsx'
#             )


# if __name__ == '__main__':
#     main()


import pandas as pd
import numpy as np
import openpyxl
import pycountry
import streamlit as st
from io import BytesIO

from utils.vat_calculator.country_formatter import format_country


def getFile(uploaded_file, type="xlsx"):
    valid = ["csv", "xlsx"]

    if uploaded_file is not None:
        if type not in valid:
            raise ValueError("results: status must be one of %r." % valid)

        elif type == "csv":
            return pd.read_csv(uploaded_file, dtype="str")

        else:
            return pd.read_excel(uploaded_file, dtype="str")


def vatter(df):
    # load in vat table
    vat = pd.read_excel(
        "utils/vat_calculator/uk-eu vat rates.xlsx", engine="openpyxl")
    vat.rename(columns={"countrycode": "ISO_code"}, inplace=True)
    df = format_country(df, "Country")
    df = df.merge(vat, on="ISO_code")
    # convert column typee from str to float
    df['Package Value'] = df['Package Value'].astype(float)
    df["vat_rate"] = df["vat_rate"].astype(float)
    df['VAT value'] = df['Package Value'] * df["vat_rate"]
    df = df.loc[df['Package Value'] < 150]
    return df


def convert_df(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data


def main():
    st.title("VAT Calculator")
    st.subheader("Please add data below")
    uploaded_file = st.file_uploader("Choose a file")
    df = getFile(uploaded_file)

    if uploaded_file:
        df = vatter(df)

        st.subheader("User Inputs")
        st.write(df)

        fileName = st.text_input("What is the file name?")

        if fileName:
            xlsx_data = convert_df(df)
            st.download_button(
                label="Download data as Excel (xlsx)",
                data=xlsx_data,
                file_name=f'{fileName}.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )


if __name__ == '__main__':
    main()

