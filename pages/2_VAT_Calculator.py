import pandas as pd
import numpy as np
import openpyxl
import pycountry
import streamlit as st

from utils.vat_calculator.country_formatter import format_country


def getFile(uploaded_file, type="xlsx"):
    valid = ["csv", "xlsx"]

    if uploaded_file is not None:
        if type not in valid:
            raise ValueError("results: status must be one of %r." % valid)

        elif type == "csv":
            return pd.read_csv(uploaded_file)

        else:
            return pd.read_excel(uploaded_file)


def vatter(df):
    # load in vat table
    vat = pd.read_excel(
        "utils/vat_calculator/uk-eu vat rates.xlsx", engine="openpyxl")
    vat.rename(columns={"countrycode": "ISO_code"}, inplace=True)
    df = format_country(df, "Country")
    df = df.merge(vat, on="ISO_code")
    df['VAT value'] = df['Package Value'] * df["vat_rate"]
    df = df.loc[df['Package Value'] < 150]
    return df


# @st.cache_data
@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False)


def main():
    st.title("Vat Helper")
    st.subheader("Please add data below")
    uploaded_file = st.file_uploader("Choose a file")
    df = getFile(uploaded_file)

    if uploaded_file:

        df = vatter(df)

        st.subheader("User Inputs")
        st.write(df)

        fileName = st.text_input("What is the file name?")

        csv = convert_df(df)
        if fileName:
            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name=f'{fileName}.csv'
            )


if __name__ == '__main__':
    main()
