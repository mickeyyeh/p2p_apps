import pandas as pd
import streamlit as st
import io
import re


def process_file(df):
    columns = ['UniqueParcelID', 'ConsigneeName', 'ConsigneeBusinessName', 'ConsigneeStreetAddress1', 'ConsigneeStreetAddress2',
               'ConsigneeStreetAddress3', 'ConsigneeCity', 'ConsigneeStateOrProvince', 'ConsigneePostalCode', 'ConsigneeCountry',
               'ConsigneeTelephone', 'WeightCode', 'Weight', 'SKU', 'HarmonizationCode',
               'CountryOfOrigin', 'CurrencyCode', 'ExpressRelease', 'ConsigneeEmail', 'TrackingRequired', 'CustOrderRefNumber',
               'TransactionID', 'ServiceRequired', 'CustomerUploadIdentifier', 'NumberOfPieces', 'DimsUnit', 'Dim1', 'Dim2', 'Dim3', 'ProductURL',
               'DutyPreferenceCode', 'DutyPreferenceRef']

    empty_df = pd.DataFrame(columns=columns)

    empty_df['ConsigneeName'] = df['NAME'].apply(lambda x: x.title())
    empty_df['ConsigneeBusinessName'] = df['COMPANY']
    empty_df['ConsigneeStreetAddress1'] = df['ADDRESS']
    empty_df['ConsigneeStreetAddress2'] = df['ADDRESS 2']
    empty_df['ConsigneeCity'] = df['CITY'].apply(lambda x: x.title())
    empty_df['ConsigneePostalCode'] = df['ZIP']
    empty_df['ConsigneeCountry'] = df['country'].apply(lambda x: x.title())
    empty_df['ConsigneeTelephone'] = df['PHONE']
    empty_df['WeightCode'] = ['L'] * len(df)
    empty_df['CountryOfOrigin'] = ['CN'] * len(df)
    empty_df['ExpressRelease'] = ['Y'] * len(df)
    empty_df['ConsigneeEmail'] = ['care@p2pg.com'] * len(df)
    empty_df['TrackingRequired'] = ['Y'] * len(df)
    empty_df['CustomerUploadIdentifier'] = ['NP_US'] * len(df)
    empty_df['NumberOfPieces'] = [1] * len(df)
    empty_df['DimsUnit'] = ['in'] * len(df)

    for i in range(len(df['BOX AND WEIGHT'])):
        string = df['BOX AND WEIGHT'][i]
        matches = re.findall(
            r'(\d+)\s*X\s*(\d+)\s*X\s*(\d+)\s*@ (\d+)\s*LBS', string)
        if matches:
            length, width, height, weight = matches[0]
            empty_df.at[i, 'Weight'] = weight
            empty_df.at[i, 'Dim1'] = length
            empty_df.at[i, 'Dim2'] = width
            empty_df.at[i, 'Dim3'] = height
        else:
            print("No matches found.")

    columns = ['ConsigneeName', 'ConsigneeCountry',
               'ItemDescription', 'CustomsValue', 'LineItemQuantity']
    items_df = pd.DataFrame(columns=columns)

    # original
    # for i in range(len(df['ITEM/COST'])):
    #     string = df['ITEM/COST'][i]
    #     name = df['NAME'][i].title()
    #     country = df['country'][i].title()
    #     lst = string.split(',')
    #     new_lst = [x.strip() for x in lst]

    #     for string in new_lst:
    #         string_list = string.split(" ")
    #         try:
    #             item_quantity = int(string_list[0])
    #             remaining_string_list = " ".join(string_list[1:]).split("-")
    #             item_description = remaining_string_list[0].title()
    #             cleaned_string = remaining_string_list[1].replace(
    #                 '/EA', '').lstrip('$').split()[0]
    #             price_per_unit = float(cleaned_string)
    #             items_df = pd.concat([items_df, pd.DataFrame([[name, country, item_description.strip(
    #             ), float(price_per_unit), item_quantity]], columns=columns)], ignore_index=True)
    #         except:
    #             item_quantity = 1
    #             remaining_string_list = " ".join(string_list).split("-")
    #             item_description = remaining_string_list[0].title()
    #             cleaned_string = remaining_string_list[1].replace(
    #                 '/EA', '').lstrip('$').split()[0]
    #             price_per_unit = float(cleaned_string)
    #             items_df = pd.concat([items_df, pd.DataFrame([[name, country, item_description.strip(
    #             ), float(price_per_unit), item_quantity]], columns=columns)], ignore_index=True)
    
    # new: for items without value
    for i in range(len(df['ITEM/COST'])):
        string = df['ITEM/COST'][i]
        name = df['NAME'][i].title()
        country = df['country'][i].title()
        lst = string.split(',')
        new_lst = [x.strip() for x in lst]
    
        for string in new_lst:
            string_list = re.split(r'\s(?=\d)', string)  # Split on space followed by a digit
            try:
                item_quantity = int(string_list[0])
                remaining_string_list = " ".join(string_list[1:]).split("-")
                print("Remaining String List:", remaining_string_list)  # Add this line to print remaining_string_list
                item_description = remaining_string_list[0].title()
                if len(remaining_string_list) == 2:
                    cleaned_string = remaining_string_list[1].replace(
                        '/EA', '').lstrip('$').split()[0]
                    price_per_unit = cleaned_string
                    items_df = pd.concat([items_df, pd.DataFrame([[name, country, item_description.strip(
                    ), price_per_unit, item_quantity]], columns=columns)], ignore_index=True)
                else:
                    cleaned_string = '$ Missing Item Value'
                    price_per_unit = cleaned_string
                    items_df = pd.concat([items_df, pd.DataFrame([[name, country, item_description.strip(
                    ), price_per_unit, item_quantity]], columns=columns)], ignore_index=True)
            except:
                item_quantity = 1
                remaining_string_list = " ".join(string_list).split("-")
                # print("Remaining String List:", remaining_string_list)  # Add this line to print remaining_string_list
                if len(remaining_string_list) == 2:
                    item_description = remaining_string_list[0].title()
                    cleaned_string = remaining_string_list[1].replace(
                        '/EA', '').lstrip('$').split()[0]
                    price_per_unit = cleaned_string
                    items_df = pd.concat([items_df, pd.DataFrame([[name, country, item_description.strip(
                    ), price_per_unit, item_quantity]], columns=columns)], ignore_index=True)
                else:
                    item_description = remaining_string_list[0].title()
                    cleaned_string = '$ Missing Item Value'
                    price_per_unit = cleaned_string
                    items_df = pd.concat([items_df, pd.DataFrame([[name, country, item_description.strip(
                    ), price_per_unit, item_quantity]], columns=columns)], ignore_index=True)



    new_df = pd.merge(empty_df, items_df, on=[
                      'ConsigneeName', 'ConsigneeCountry'], how='left')

    new_df = new_df[['UniqueParcelID', 'ConsigneeName', 'ConsigneeBusinessName', 'ConsigneeStreetAddress1', 'ConsigneeStreetAddress2',
                     'ConsigneeStreetAddress3', 'ConsigneeCity', 'ConsigneeStateOrProvince', 'ConsigneePostalCode', 'ConsigneeCountry',
                     'ConsigneeTelephone', 'WeightCode', 'Weight', 'ItemDescription', 'SKU', 'HarmonizationCode', 'LineItemQuantity',
                     'CountryOfOrigin', 'CustomsValue', 'CurrencyCode', 'ExpressRelease', 'ConsigneeEmail', 'TrackingRequired', 'CustOrderRefNumber',
                     'TransactionID', 'ServiceRequired', 'CustomerUploadIdentifier', 'NumberOfPieces', 'DimsUnit', 'Dim1', 'Dim2', 'Dim3', 'ProductURL',
                     'DutyPreferenceCode', 'DutyPreferenceRef']]

    return new_df


def main():
    st.title("Swag File Processor")
    # st.write("If system raised errors, make sure all items have a price. (example: T SHIRT-$14.99)")
        
    uploaded_file = st.file_uploader(
        "Upload your Excel file", type=["csv", "xlsx"])

    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        processed_df = process_file(df)
        st.subheader("Transformed Result")
        st.write(processed_df)

        # Allow user to specify the file name for download
        default_file_name = uploaded_file.name.split('.')[0] + '_transformed'

        file_name = st.text_input(
            "Enter file name for download:", default_file_name)

        # Offer download link for the processed file
        if uploaded_file.name.endswith(".xlsx"):
            excel_bytes = io.BytesIO()
            processed_df.to_excel(excel_bytes, index=False)
            excel_bytes.seek(0)
            st.download_button(
                label="Download Processed Excel",
                data=excel_bytes,
                file_name=f"{file_name}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        elif uploaded_file.name.endswith(".csv"):
            csv = processed_df.to_csv(index=False)
            st.download_button(
                label="Download Processed CSV",
                data=csv,
                file_name=f"{file_name}.csv",
                mime="text/csv"
            )


if __name__ == "__main__":
    main()
