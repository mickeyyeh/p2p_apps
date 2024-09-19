# import pandas as pd
# # from zipfile import ZipFile
# # from io import BytesIO # for creating zip files
# import io
# import zipfile
# import streamlit as st

# # setting download button color
# m = st.markdown("""
# <style>
# div.stDownloadButton > button:first-child {
#     background-color: #3DED97;
#     color:#ffffff;
# }
# div.stDownloadButton > button:hover {
#     background-color: #3DED97;
#     color:#ffffff;
#     }
# </style>""", unsafe_allow_html=True)

# # setting sidebar width
# st.markdown(f'''
#     <style>
#         section[data-testid="stSidebar"] .css-ng1t4o {{width: 14rem;}}
#         section[data-testid="stSidebar"] .css-1d391kg {{width: 14rem;}}
#     </style>
# ''', unsafe_allow_html=True)


# def main():
#     ## -- setting titles --##
#     # Title/Heading
#     st.title("Excel Row to Files Splitter")
#     # Subheading
#     st.write("This website will help you split your Excel file equally into smaller files with the number of rows you want.")

#     ## -- Step1: To upload and see the file you uploaded --##
#     st.sidebar.header("Step 1: Upload your file")
#     df, upload_file_name = uploaded_file()  # calling function
#     # df = "" # to avoiderror -> NameError: name 'df' is not defined
#     st.write(df)

#     ## -- Steps after files are uploaded --##
#     if df is not None:  # so that it doesn't move on to step 2 if nothing is uploaded
#         ## -- Step2: To see the file that is uploaded --##
#         st.sidebar.header("Step 2: Set the number of rows to save in a file")

#         num_of_rows = int(st.sidebar.text_input(
#             "Number of rows you want in a file (press 'Enter' to apply):", '200'))
#         num_of_files = len(df)//num_of_rows + 1
#         st.sidebar.write("After splitting, you will have",
#                          num_of_files, "files in total.")
#         # call the row splitter function
#         row_splitter(num_of_rows)

#         ## -- Step3: Typing the name you want for the saved files --##
#         st.sidebar.header("Step 3: Set the name of the splitted files")
#         st.sidebar.write(
#             "This program will automatically add 'lines xxxx-xxxx' in the file name for you.")
#         # file_name = st.sidebar.text_input("Name of these files (press 'Enter' to apply):", "example: CompanyX AppleSales Fuji_A 01012023")
#         file_name = st.sidebar.text_input(
#             "Name of these files (press 'Enter' to apply):", upload_file_name)

#         ## -- Step4: Click Start Button To Start Downloading!! --##
#         # note: it is currently impossible to download multiple files at once through streamlit
#         # you can only pack the files you want to download into a zip folder and download the zip file
#         st.sidebar.header("Step 4: Start Downloading")
#         st.sidebar.write('Click Start Button To Start Compiling.')

#         # save all files into 1 ZIP file
#         # create a .zip file in-memory without storing it to disk with io.BytesIO()
#         zip_buffer = io.BytesIO()

#         # Adding multiple files to the zip
#         download_count = 0
#         # with zipfile.ZipFile(zip_buffer+"/test.zip", "w") as myzip: # TypeError: unsupported operand type(s) for +: '_io.BytesIO' and 'str'
#         with zipfile.ZipFile(zip_buffer, "w") as myzip:
#             for df_export_file in df_sliced:
#                 # setting name with appended values
#                 export_file_name = file_name + " lines " + \
#                     names_to_append[download_count] + ".xlsx"
#                 print(export_file_name)
#                 # print(df_export_file.info())
#                 # print(df_export_file)
#                 print(download_count)
#                 download_count += 1
#                 # export files
#                 with myzip.open(export_file_name, "w") as myfile:
#                     df_export_file.to_excel(myfile, index=False)

#         # download button to download zip file
#         st.sidebar.download_button(
#             "Download Excel Files",
#             file_name="splitted_data.zip",
#             mime="application/zip",
#             data=zip_buffer
#         )

#         ## -- Adding Additional White Spaces Under Download Button --##
#         st.sidebar.header("")


# ## -- Setup file upload accepting CSV and Excel --##
# def uploaded_file():
#     # use the global keyword, the variable belongs to the global scope
#     global df  # make the df global so other lines of code can read df
#     # valid = ["csv","xlsx"] # to raise error for wrong file upload formats

#     while True:
#         try:
#             uploaded_file = st.sidebar.file_uploader(label="Upload your Excel file here (one at a time)", type=[
#                                                      'xlsx'], accept_multiple_files=False, key='test')  # one file at a time!
#         except:
#             continue
#         else:
#             if uploaded_file is not None:
#                 # print(uploaded_file)
#                 # if type not in valid:
#                 #     raise ValueError("results: status must be one of %r." % valid)
#                 # elif type == "csv":
#                 #     df = pd.read_csv(uploaded_file, index_col=None, dtype=str)
#                 # else:
#                 try:
#                     upload_file_name = uploaded_file.name.split(
#                         ".")[0]  # to remove .xlsx
#                     df = pd.read_excel(
#                         uploaded_file, index_col=None, dtype=str, engine='openpyxl')
#                 except Exception as e:
#                     print(e)
#                     # st.write("File Error: Please upload an Excel file.")
#                     upload_file_name = uploaded_file.name.split(
#                         ".")[0]  # to remove .xlsx
#                     df = pd.read_excel(
#                         uploaded_file, index_col=None, dtype=str, engine='openpyxl')
#             else:
#                 df = None
#                 upload_file_name = None

#         return df, upload_file_name


# ## -- Row Splitting Function: Allowing user to type the number of rows they want to split and save into --##
# def row_splitter(rows=200):
#     # use the global keyword, the variable belongs to the global scope
#     global df_sliced, names_to_append
#     df_sliced = []  # place holder for sliced datasets
#     names_to_append = []
#     total_splits = len(df)//rows
#     splits = 0
#     count = 0

#     while splits < total_splits:
#         ## -- splitting: for all files before the last remainding rows --##
#         df_new = df.iloc[count:(count+rows),]
#         df_sliced.append(df_new)
#         ## -- creating row count to append to file name --##
#         row_count = f"{count+1}-{count+rows}"  # python starts at 0
#         print(row_count)
#         names_to_append.append(row_count)

#         splits += 1
#         count += rows

#     else:
#         ## -- splitting: remainding rows for the last file --##
#         df_new = df.iloc[count:,]
#         df_sliced.append(df_new)
#         ## -- creating row count to append to file name --##
#         row_count = f"{count+1}-{len(df)}"  # python starts at 0
#         print(row_count)
#         names_to_append.append(row_count)


# if __name__ == '__main__':
#     main()


import pandas as pd
import io
import zipfile
import streamlit as st
from typing import Optional, List, Tuple

# Setting download button color
m = st.markdown("""
<style>
div.stDownloadButton > button:first-child {
    background-color: #3DED97;
    color:#ffffff;
}
div.stDownloadButton > button:hover {
    background-color: #3DED97;
    color:#ffffff;
    }
</style>""", unsafe_allow_html=True)

# Setting sidebar width
st.markdown('''
    <style>
        section[data-testid="stSidebar"] .css-ng1t4o {width: 14rem;}
        section[data-testid="stSidebar"] .css-1d391kg {width: 14rem;}
    </style>
''', unsafe_allow_html=True)


def main() -> None:
    """
    Main function to run the Streamlit app for splitting Excel files.
    """
    # Setting titles
    st.title("Excel Row to Files Splitter")
    st.write("This website will help you split your Excel file equally into smaller files with the number of rows you want.")

    # Step 1: Upload the file
    st.sidebar.header("Step 1: Upload your file")
    df, upload_file_name = uploaded_file()
    if df is not None:
        st.write(df)

        # Step 2: Set the number of rows per file
        st.sidebar.header("Step 2: Set the number of rows to save in a file")
        num_of_rows_str = st.sidebar.text_input(
            "Number of rows you want in a file (press 'Enter' to apply):", '200')
        try:
            num_of_rows = int(num_of_rows_str)
        except ValueError:
            st.sidebar.error(
                "Please enter a valid integer for the number of rows.")
            return

        num_of_files = len(df) // num_of_rows + \
            (1 if len(df) % num_of_rows != 0 else 0)
        st.sidebar.write(f"After splitting, you will have {num_of_files} files in total.")
        # Call the row splitter function
        row_splitter(num_of_rows, df)

        # Step 3: Set the name for the splitted files
        st.sidebar.header("Step 3: Set the name of the splitted files")
        st.sidebar.write(
            "This program will automatically add 'lines xxxx-xxxx' in the file name for you.")
        file_name = st.sidebar.text_input(
            "Name of these files (press 'Enter' to apply):", upload_file_name)

        # Step 4: Start Downloading
        st.sidebar.header("Step 4: Start Downloading")
        st.sidebar.write('Click Start Button To Start Compiling.')

        if st.sidebar.button("Start"):
            # Save all files into one ZIP file
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as myzip:
                for idx, df_export_file in enumerate(df_sliced):
                    # Setting name with appended values
                    export_file_name = f"{file_name} lines {names_to_append[idx]}.xlsx"
                    # Export files
                    excel_buffer = io.BytesIO()
                    df_export_file.to_excel(
                        excel_buffer, index=False, engine='openpyxl')
                    excel_buffer.seek(0)
                    myzip.writestr(export_file_name, excel_buffer.read())

            # Download button to download zip file
            st.sidebar.download_button(
                label="Download Excel Files",
                data=zip_buffer.getvalue(),
                file_name="splitted_data.zip",
                mime="application/zip"
            )

        # Adding additional white spaces under download button
        st.sidebar.header("")
    else:
        st.write("Please upload a file to proceed.")


def uploaded_file() -> Tuple[Optional[pd.DataFrame], Optional[str]]:
    """
    Function to handle file upload and read the Excel file.

    Returns:
        Tuple[Optional[pd.DataFrame], Optional[str]]: The DataFrame and the file name without extension.
    """
    uploaded_file = st.sidebar.file_uploader(
        label="Upload your Excel file here (one at a time)",
        type=['xlsx'],
        accept_multiple_files=False,
        key='file_uploader'
    )
    if uploaded_file is not None:
        try:
            upload_file_name = uploaded_file.name.rsplit(
                ".", 1)[0]  # Remove file extension
            df = pd.read_excel(uploaded_file, dtype=str, engine='openpyxl')
            return df, upload_file_name
        except Exception as e:
            st.error(f"File Error: {e}")
            return None, None
    else:
        return None, None


def row_splitter(rows: int, df: pd.DataFrame) -> None:
    """
    Function to split the DataFrame into smaller DataFrames based on the number of rows.

    Args:
        rows (int): Number of rows per split file.
        df (pd.DataFrame): The original DataFrame to split.
    """
    global df_sliced, names_to_append
    df_sliced: List[pd.DataFrame] = []
    names_to_append: List[str] = []
    total_rows = len(df)
    count = 0

    while count < total_rows:
        df_new = df.iloc[count:count + rows]
        df_sliced.append(df_new)
        # Creating row count to append to file name
        start_row = count + 1
        end_row = min(count + rows, total_rows)
        row_count = f"{start_row}-{end_row}"
        names_to_append.append(row_count)
        count += rows


if __name__ == '__main__':
    main()
