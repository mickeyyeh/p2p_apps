##-- Attempting To Add Key Word Scan in PDF Split --##
# import streamlit as st
# from PyPDF2 import PdfReader, PdfWriter

# import zipfile
# import io
# import re

# def natural_sort_key(s):
#     return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

# def merge_pdfs(pdf_files):
#     merged_pdf_bytes = io.BytesIO()
#     merger = PdfWriter()

#     try:
#         for pdf_file in pdf_files:
#             pdf_reader = PdfReader(pdf_file)
#             for page in pdf_reader.pages:
#                 merger.add_page(page)

#         merger.write(merged_pdf_bytes)
#         merged_pdf_bytes.seek(0)
#         return merged_pdf_bytes.getvalue()

#     except Exception as e:
#         st.error(f"Error merging PDFs: {e}")
#         return None

# def split_pdf(pdf_file, keywords):
#     pdf_reader = PdfReader(pdf_file)
#     num_pages = len(pdf_reader.pages)
#     zip_bytes = io.BytesIO()
#     pages_to_keep = []
#     split_files = []

#     try:
#         for page_number in range(num_pages):
#             page = pdf_reader.pages[page_number]
#             text = page.extract_text()
#             if not any(keyword.lower() in text.lower() for keyword in keywords):
#                 pages_to_keep.append(page_number)
#             writer = PdfWriter()
#             writer.add_page(page)
#             split_pdf_bytes = io.BytesIO()
#             writer.write(split_pdf_bytes)
#             split_pdf_bytes.seek(0)
#             split_files.append((f"page_{page_number + 1}.pdf", split_pdf_bytes.getvalue()))

#         # Sort split files naturally by their names
#         split_files = sorted(split_files, key=lambda x: natural_sort_key(x[0]))

#         # Create a ZipFile object and add sorted split files to the zip file
#         with zipfile.ZipFile(zip_bytes, 'w', zipfile.ZIP_DEFLATED) as zipf:
#             for file_name, file_data in split_files:
#                 zipf.writestr(file_name, file_data)

#     except Exception as e:
#         st.error(f"Error splitting PDF: {e}")

#     zip_bytes.seek(0)
#     st.download_button(
#         label="Download All Pages",
#         data=zip_bytes.getvalue(),
#         file_name="split_pdfs.zip",
#         mime="application/zip"
#     )

#     # Now display download buttons for each individual page
#     with zipfile.ZipFile(zip_bytes, 'r') as zipf:
#         for file_name, _ in split_files:
#             with zipf.open(file_name) as split_pdf_bytes:
#                 st.download_button(
#                     label=f"Download {file_name.split('.')[0].replace('_', ' ').capitalize()}",
#                     data=split_pdf_bytes.read(),
#                     file_name=file_name,
#                     mime="application/pdf"
#                 )

#     if keywords:
#         zip_bytes_keywords_removed = io.BytesIO()
#         with zipfile.ZipFile(zip_bytes_keywords_removed, 'w', zipfile.ZIP_DEFLATED) as zipf:
#             for page_number in pages_to_keep:
#                 page = pdf_reader.pages[page_number]
#                 writer = PdfWriter()
#                 writer.add_page(page)
#                 split_pdf_bytes = io.BytesIO()
#                 writer.write(split_pdf_bytes)
#                 split_pdf_bytes.seek(0)
#                 zipf.writestr(f"page_{page_number + 1}.pdf", split_pdf_bytes.getvalue())

#         zip_bytes_keywords_removed.seek(0)
#         st.download_button(
#             label="Download Pages Without Keywords",
#             data=zip_bytes_keywords_removed.getvalue(),
#             file_name="split_pdfs_keywords_removed.zip",
#             mime="application/zip"
#         )

# def main():
#     st.title("PDF Tools")
#     option = st.selectbox(
#         "Select an action",
#         ("Merge PDFs", "Split PDF")
#     )

#     if option == "Merge PDFs":
#         uploaded_files = st.file_uploader(
#             "Upload PDF files to merge", accept_multiple_files=True, type="pdf")

#         if uploaded_files:
#             sort_option = st.selectbox(
#                 "Sort files by",
#                 ("Original Order", "Ascending", "Descending", "Alphabetically"))

#             if sort_option == "Ascending":
#                 uploaded_files = sorted(uploaded_files, key=lambda x: natural_sort_key(x.name))
#             elif sort_option == "Descending":
#                 uploaded_files = sorted(uploaded_files, key=lambda x: natural_sort_key(x.name), reverse=True)
#             elif sort_option == "Alphabetically":
#                 uploaded_files = sorted(uploaded_files, key=lambda x: x.name.lower())

#             if st.button("Merge PDFs"):
#                 merged_pdf_bytes = merge_pdfs(uploaded_files)
#                 if merged_pdf_bytes:
#                     st.success("PDFs merged successfully!")
#                     st.download_button(
#                         label="Download Merged PDF",
#                         data=merged_pdf_bytes,
#                         file_name="merged_pdf.pdf",
#                         mime="application/pdf"
#                     )

#     elif option == "Split PDF":
#         uploaded_file = st.file_uploader("Upload PDF file to split", type="pdf")
#         keywords = st.text_input("Enter keywords to remove pages (comma-separated)").split(',')

#         if uploaded_file:
#             if st.button("Split PDF"):
#                 split_pdf(uploaded_file, keywords)

# if __name__ == "__main__":
#     main()


import streamlit as st
from PyPDF2 import PdfReader, PdfWriter

import zipfile
import io
import re

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

def merge_pdfs(pdf_files):
    merged_pdf_bytes = io.BytesIO()
    merger = PdfWriter()

    try:
        for pdf_file in pdf_files:
            pdf_reader = PdfReader(pdf_file)
            for page in pdf_reader.pages:
                merger.add_page(page)

        merger.write(merged_pdf_bytes)
        merged_pdf_bytes.seek(0)
        return merged_pdf_bytes.getvalue()

    except Exception as e:
        st.error(f"Error merging PDFs: {e}")
        return None

def split_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)
    zip_bytes = io.BytesIO()

    with zipfile.ZipFile(zip_bytes, 'w', zipfile.ZIP_DEFLATED) as zipf:
        try:
            for page_number in range(num_pages):
                page = pdf_reader.pages[page_number]
                writer = PdfWriter()
                writer.add_page(page)
                split_pdf_bytes = io.BytesIO()
                writer.write(split_pdf_bytes)
                split_pdf_bytes.seek(0)
                zipf.writestr(f"page_{page_number + 1}.pdf", split_pdf_bytes.getvalue())

        except Exception as e:
            st.error(f"Error splitting PDF: {e}")

    zip_bytes.seek(0)
    st.download_button(
        label="Download All Pages",
        data=zip_bytes.getvalue(),
        file_name="split_pdfs.zip",
        mime="application/zip"
    )

    with zipfile.ZipFile(zip_bytes, 'r') as zipf:
        for page_number in range(num_pages):
            with zipf.open(f"page_{page_number + 1}.pdf") as split_pdf_bytes:
                st.download_button(
                    label=f"Download Page {page_number + 1}",
                    data=split_pdf_bytes.read(),
                    file_name=f"page_{page_number + 1}.pdf",
                    mime="application/pdf"
                )

def main():
    st.title("PDF Tools")
    option = st.selectbox(
        "Select an action",
        ("Merge PDFs", "Split PDF")
    )

    if option == "Merge PDFs":
        uploaded_files = st.file_uploader(
            "Upload PDF files to merge", accept_multiple_files=True, type="pdf")

        if uploaded_files:
            sort_option = st.selectbox(
                "Sort files by",
                ("Original Order", "Ascending", "Descending", "Alphabetically"))

            if sort_option == "Ascending":
                uploaded_files = sorted(uploaded_files, key=lambda x: natural_sort_key(x.name))
            elif sort_option == "Descending":
                uploaded_files = sorted(uploaded_files, key=lambda x: natural_sort_key(x.name), reverse=True)
            elif sort_option == "Alphabetically":
                uploaded_files = sorted(uploaded_files, key=lambda x: x.name.lower())

            if st.button("Merge PDFs"):
                merged_pdf_bytes = merge_pdfs(uploaded_files)
                if merged_pdf_bytes:
                    st.success("PDFs merged successfully!")
                    st.download_button(
                        label="Download Merged PDF",
                        data=merged_pdf_bytes,
                        file_name="merged_pdf.pdf",
                        mime="application/pdf"
                    )

    elif option == "Split PDF":
        uploaded_file = st.file_uploader("Upload PDF file to split", type="pdf")

        if uploaded_file:
            if st.button("Split PDF"):
                split_pdf(uploaded_file)

if __name__ == "__main__":
    main()

