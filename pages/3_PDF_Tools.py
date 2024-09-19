# import streamlit as st
# import fitz  # PyMuPDF
# import io
# from PIL import Image


# def merge_pdfs(pdf_files):
#     merged_pdf_bytes = io.BytesIO()
#     merger = fitz.open()

#     try:
#         for pdf_file in pdf_files:
#             pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
#             merger.insert_pdf(pdf_document)

#         merger.save(merged_pdf_bytes)
#         merged_pdf_bytes.seek(0)
#         return merged_pdf_bytes.getvalue()

#     except Exception as e:
#         st.error(f"Error merging PDFs: {e}")
#         return None


# def split_pdf(pdf_content, pages_to_keep=None, exclude_pages=None):
#     pdf_document = fitz.open(stream=pdf_content, filetype="pdf")
#     num_pages = len(pdf_document)

#     writer = fitz.open()

#     if exclude_pages is not None:
#         for page_number in range(num_pages):
#             if (page_number + 1) not in exclude_pages:
#                 writer.insert_pdf(
#                     pdf_document, from_page=page_number, to_page=page_number)
#     elif pages_to_keep is not None:
#         for page_number in pages_to_keep:
#             writer.insert_pdf(
#                 pdf_document, from_page=page_number - 1, to_page=page_number - 1)

#     split_pdf_bytes = io.BytesIO()
#     writer.save(split_pdf_bytes)
#     split_pdf_bytes.seek(0)

#     return split_pdf_bytes.getvalue()


# def preview_pdf_pages(pdf_file, sort_order):
#     # Convert PDF to images for preview with higher DPI
#     pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
#     images = []
#     dpi = 600  # Increased DPI for sharper image quality

#     for page_number in range(len(pdf_document)):
#         page = pdf_document.load_page(page_number)
#         pix = page.get_pixmap(matrix=fitz.Matrix(
#             dpi / 72, dpi / 72))  # Set DPI
#         img = Image.open(io.BytesIO(pix.tobytes()))
#         images.append((page_number + 1, img))

#     # Sort pages based on user input
#     if sort_order == "Ascending":
#         images = sorted(images, key=lambda x: x[0])
#     elif sort_order == "Descending":
#         images = sorted(images, key=lambda x: x[0], reverse=True)
#     elif sort_order == "Alphabetical":
#         # Convert page number to string for alphabetical sorting
#         images = sorted(images, key=lambda x: str(x[0]))

#     return images


# def main():
#     st.title("PDF Tools")

#     option = st.selectbox(
#         "Select an action",
#         ("Merge PDFs", "Split PDF")
#     )

#     if option == "Merge PDFs":
#         uploaded_files = st.file_uploader(
#             "Upload PDF files to merge", accept_multiple_files=True, type="pdf"
#         )

#         if uploaded_files:
#             # Add sort order selection
#             sort_order = st.selectbox(
#                 "Sort Pages",
#                 ["Original Order", "Ascending", "Descending", "Alphabetical"]
#             )

#             all_images = []
#             for uploaded_file in uploaded_files:
#                 st.write(f"### Preview and Edit: {uploaded_file.name}")
#                 preview_images = preview_pdf_pages(uploaded_file, sort_order)
#                 all_images.extend(preview_images)

#             if all_images:
#                 st.write("### Final Preview")
#                 # Display images in a scrollable container
#                 for img in all_images:
#                     st.image(img, use_column_width=True)

#                 if st.button("Merge PDFs"):
#                     # Create temporary PDFs from the preview images
#                     temp_files = []
#                     for img in all_images:
#                         temp_pdf = io.BytesIO()
#                         img.save(temp_pdf, format='PDF')
#                         temp_pdf.seek(0)
#                         temp_files.append(temp_pdf)

#                     merged_pdf_bytes = merge_pdfs(temp_files)
#                     if merged_pdf_bytes:
#                         st.success("PDFs merged successfully!")
#                         st.download_button(
#                             label="Download Merged PDF",
#                             data=merged_pdf_bytes,
#                             file_name="merged_pdf.pdf",
#                             mime="application/pdf"
#                         )

#     elif option == "Split PDF":
#         uploaded_file = st.file_uploader(
#             "Upload PDF file to split", type="pdf"
#         )

#         if uploaded_file:
#             # Store the PDF content in memory for reuse
#             pdf_content = uploaded_file.getvalue()

#             num_pages = len(fitz.open(stream=pdf_content, filetype="pdf"))

#             # Let the user choose between excluding or selecting specific pages
#             split_option = st.radio(
#                 "How would you like to split the PDF?",
#                 ("Exclude pages", "Select specific pages to download")
#             )

#             if split_option == "Exclude pages":
#                 exclude_pages = st.multiselect(
#                     "Select pages to exclude from download",
#                     list(range(1, num_pages + 1)),
#                     format_func=lambda x: f"Page {x}"
#                 )

#                 if st.button("Split PDF") and exclude_pages:
#                     st.write(f"Excluding pages: {exclude_pages}")
#                     pdf_bytes = split_pdf(
#                         pdf_content, exclude_pages=exclude_pages)

#                     st.download_button(
#                         label="Download All Except Specified Pages",
#                         data=pdf_bytes,
#                         file_name="all_except_specified_pages.pdf",
#                         mime="application/pdf"
#                     )

#             elif split_option == "Select specific pages to download":
#                 pages_to_keep = st.multiselect(
#                     "Select pages to download",
#                     list(range(1, num_pages + 1)),
#                     format_func=lambda x: f"Page {x}"
#                 )

#                 if st.button("Download Selected Pages") and pages_to_keep:
#                     st.write(f"Downloading selected pages: {pages_to_keep}")
#                     pdf_bytes = split_pdf(
#                         pdf_content, pages_to_keep=pages_to_keep)

#                     st.download_button(
#                         label="Download Selected Pages PDF",
#                         data=pdf_bytes,
#                         file_name="selected_pages.pdf",
#                         mime="application/pdf"
#                     )


# if __name__ == "__main__":
#     main()


# import streamlit as st
# import fitz  # PyMuPDF
# import io
# from PIL import Image
# from typing import List, Optional, IO, Tuple


# def merge_pdfs(pdf_files: List[IO[bytes]]) -> Optional[bytes]:
#     merged_pdf_bytes = io.BytesIO()
#     merger = fitz.open()

#     try:
#         for pdf_file in pdf_files:
#             pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
#             merger.insert_pdf(pdf_document)

#         merger.save(merged_pdf_bytes)
#         merger.close()
#         merged_pdf_bytes.seek(0)
#         return merged_pdf_bytes.getvalue()

#     except Exception as e:
#         st.error(f"Error merging PDFs: {e}")
#         return None


# def split_pdf(
#     pdf_content: bytes,
#     pages_to_keep: Optional[List[int]] = None,
#     exclude_pages: Optional[List[int]] = None
# ) -> bytes:
#     pdf_document = fitz.open(stream=pdf_content, filetype="pdf")
#     num_pages = len(pdf_document)

#     writer = fitz.open()

#     if exclude_pages is not None:
#         for page_number in range(num_pages):
#             if (page_number + 1) not in exclude_pages:
#                 writer.insert_pdf(
#                     pdf_document, from_page=page_number, to_page=page_number)
#     elif pages_to_keep is not None:
#         for page_number in pages_to_keep:
#             writer.insert_pdf(
#                 pdf_document, from_page=page_number - 1, to_page=page_number - 1)

#     split_pdf_bytes = io.BytesIO()
#     writer.save(split_pdf_bytes)
#     writer.close()
#     split_pdf_bytes.seek(0)

#     return split_pdf_bytes.getvalue()


# def preview_pdf_pages(pdf_file: IO[bytes], sort_order: str) -> List[Tuple[int, Image.Image]]:
#     # Convert PDF to images for preview with higher DPI
#     pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
#     images: List[Tuple[int, Image.Image]] = []
#     dpi = 600  # Increased DPI for sharper image quality

#     for page_number in range(len(pdf_document)):
#         page = pdf_document.load_page(page_number)
#         pix = page.get_pixmap(matrix=fitz.Matrix(
#             dpi / 72, dpi / 72))  # Set DPI
#         img = Image.open(io.BytesIO(pix.tobytes()))
#         images.append((page_number + 1, img))

#     # Sort pages based on user input
#     if sort_order == "Ascending":
#         images = sorted(images, key=lambda x: x[0])
#     elif sort_order == "Descending":
#         images = sorted(images, key=lambda x: x[0], reverse=True)
#     elif sort_order == "Alphabetical":
#         # Convert page number to string for alphabetical sorting
#         images = sorted(images, key=lambda x: str(x[0]))

#     return images


# def main() -> None:
#     st.title("PDF Tools")

#     option = st.selectbox(
#         "Select an action",
#         ("Merge PDFs", "Split PDF")
#     )

#     if option == "Merge PDFs":
#         uploaded_files = st.file_uploader(
#             "Upload PDF files to merge", accept_multiple_files=True, type="pdf"
#         )

#         if uploaded_files:
#             # Add sort order selection
#             sort_order = st.selectbox(
#                 "Sort Pages",
#                 ["Original Order", "Ascending", "Descending", "Alphabetical"]
#             )

#             all_images: List[Tuple[int, Image.Image]] = []
#             for uploaded_file in uploaded_files:
#                 st.write(f"### Preview and Edit: {uploaded_file.name}")
#                 preview_images = preview_pdf_pages(uploaded_file, sort_order)
#                 all_images.extend(preview_images)

#             if all_images:
#                 st.write("### Final Preview")
#                 # Display images in a scrollable container
#                 for page_num, img in all_images:
#                     st.image(img, caption=f"Page {
#                              page_num}", use_column_width=True)

#                 if st.button("Merge PDFs"):
#                     # Create temporary PDFs from the preview images
#                     temp_files: List[IO[bytes]] = []
#                     for page_num, img in all_images:
#                         temp_pdf = io.BytesIO()
#                         img.save(temp_pdf, format='PDF')
#                         temp_pdf.seek(0)
#                         temp_files.append(temp_pdf)

#                     merged_pdf_bytes = merge_pdfs(temp_files)
#                     if merged_pdf_bytes:
#                         st.success("PDFs merged successfully!")
#                         st.download_button(
#                             label="Download Merged PDF",
#                             data=merged_pdf_bytes,
#                             file_name="merged_pdf.pdf",
#                             mime="application/pdf"
#                         )

#     elif option == "Split PDF":
#         uploaded_file = st.file_uploader(
#             "Upload PDF file to split", type="pdf"
#         )

#         if uploaded_file:
#             # Store the PDF content in memory for reuse
#             pdf_content = uploaded_file.getvalue()

#             num_pages = len(fitz.open(stream=pdf_content, filetype="pdf"))

#             # Let the user choose between excluding or selecting specific pages
#             split_option = st.radio(
#                 "How would you like to split the PDF?",
#                 ("Exclude pages", "Select specific pages to download")
#             )

#             if split_option == "Exclude pages":
#                 exclude_pages = st.multiselect(
#                     "Select pages to exclude from download",
#                     list(range(1, num_pages + 1)),
#                     format_func=lambda x: f"Page {x}"
#                 )

#                 if st.button("Split PDF") and exclude_pages:
#                     st.write(f"Excluding pages: {exclude_pages}")
#                     pdf_bytes = split_pdf(
#                         pdf_content, exclude_pages=exclude_pages
#                     )

#                     st.download_button(
#                         label="Download All Except Specified Pages",
#                         data=pdf_bytes,
#                         file_name="all_except_specified_pages.pdf",
#                         mime="application/pdf"
#                     )

#             elif split_option == "Select specific pages to download":
#                 pages_to_keep = st.multiselect(
#                     "Select pages to download",
#                     list(range(1, num_pages + 1)),
#                     format_func=lambda x: f"Page {x}"
#                 )

#                 if st.button("Download Selected Pages") and pages_to_keep:
#                     st.write(f"Downloading selected pages: {pages_to_keep}")
#                     pdf_bytes = split_pdf(
#                         pdf_content, pages_to_keep=pages_to_keep
#                     )

#                     st.download_button(
#                         label="Download Selected Pages PDF",
#                         data=pdf_bytes,
#                         file_name="selected_pages.pdf",
#                         mime="application/pdf"
#                     )


# if __name__ == "__main__":
#     main()


# import streamlit as st
# import fitz  # PyMuPDF
# import io
# from PIL import Image
# from typing import List, Optional, IO, Tuple


# def merge_pdfs(pdf_files: List[IO[bytes]]) -> Optional[bytes]:
#     merged_pdf_bytes = io.BytesIO()
#     merger = fitz.open()

#     try:
#         for pdf_file in pdf_files:
#             pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
#             merger.insert_pdf(pdf_document)

#         merger.save(merged_pdf_bytes)
#         merger.close()
#         merged_pdf_bytes.seek(0)
#         return merged_pdf_bytes.getvalue()

#     except Exception as e:
#         st.error(f"Error merging PDFs: {e}")
#         return None


# def split_pdf(
#     pdf_content: bytes,
#     pages_to_keep: Optional[List[int]] = None,
#     exclude_pages: Optional[List[int]] = None
# ) -> bytes:
#     pdf_document = fitz.open(stream=pdf_content, filetype="pdf")
#     num_pages = len(pdf_document)

#     writer = fitz.open()

#     if exclude_pages is not None:
#         for page_number in range(num_pages):
#             if (page_number + 1) not in exclude_pages:
#                 writer.insert_pdf(
#                     pdf_document, from_page=page_number, to_page=page_number)
#     elif pages_to_keep is not None:
#         for page_number in pages_to_keep:
#             writer.insert_pdf(
#                 pdf_document, from_page=page_number - 1, to_page=page_number - 1)
#     else:
#         # If no pages are specified, include all pages
#         writer.insert_pdf(pdf_document)

#     split_pdf_bytes = io.BytesIO()
#     writer.save(split_pdf_bytes)
#     writer.close()
#     split_pdf_bytes.seek(0)

#     return split_pdf_bytes.getvalue()


# def preview_pdf_pages(pdf_file: IO[bytes], sort_order: str) -> List[Tuple[int, Image.Image]]:
#     # Convert PDF to images for preview with specified DPI
#     pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
#     images: List[Tuple[int, Image.Image]] = []
#     dpi = 100  # Adjust DPI for faster rendering

#     for page_number in range(len(pdf_document)):
#         page = pdf_document.load_page(page_number)
#         pix = page.get_pixmap(matrix=fitz.Matrix(
#             dpi / 72, dpi / 72))  # Set DPI
#         img = Image.open(io.BytesIO(pix.tobytes()))
#         images.append((page_number + 1, img))

#     # Sort pages based on user input
#     if sort_order == "Ascending":
#         images = sorted(images, key=lambda x: x[0])
#     elif sort_order == "Descending":
#         images = sorted(images, key=lambda x: x[0], reverse=True)
#     elif sort_order == "Alphabetical":
#         # Convert page number to string for alphabetical sorting
#         images = sorted(images, key=lambda x: str(x[0]))

#     return images


# def preview_pdf_content(pdf_bytes: bytes) -> List[Tuple[int, Image.Image]]:
#     # Convert PDF bytes to images for preview
#     pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
#     images: List[Tuple[int, Image.Image]] = []
#     dpi = 100  # Adjust DPI as needed

#     for page_number in range(len(pdf_document)):
#         page = pdf_document.load_page(page_number)
#         pix = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))
#         img = Image.open(io.BytesIO(pix.tobytes()))
#         images.append((page_number + 1, img))

#     return images


# def main() -> None:
#     st.title("PDF Tools")

#     option = st.selectbox(
#         "Select an action",
#         ("Merge PDFs", "Split PDF")
#     )

#     if option == "Merge PDFs":
#         uploaded_files = st.file_uploader(
#             "Upload PDF files to merge", accept_multiple_files=True, type="pdf"
#         )

#         if uploaded_files:
#             # Add sort order selection
#             sort_order = st.selectbox(
#                 "Sort Pages",
#                 ["Original Order", "Ascending", "Descending", "Alphabetical"]
#             )

#             all_images: List[Tuple[int, Image.Image]] = []
#             for uploaded_file in uploaded_files:
#                 st.write(f"### Preview and Edit: {uploaded_file.name}")
#                 preview_images = preview_pdf_pages(uploaded_file, sort_order)
#                 all_images.extend(preview_images)

#             if all_images:
#                 st.write("### Final Preview Before Merging")
#                 # Display images in a scrollable container
#                 for page_num, img in all_images:
#                     st.image(img, caption=f"Page {
#                              page_num}", use_column_width=True)

#                 if st.button("Merge PDFs"):
#                     # Create temporary PDFs from the preview images
#                     temp_files: List[IO[bytes]] = []
#                     for page_num, img in all_images:
#                         temp_pdf = io.BytesIO()
#                         img.save(temp_pdf, format='PDF')
#                         temp_pdf.seek(0)
#                         temp_files.append(temp_pdf)

#                     merged_pdf_bytes = merge_pdfs(temp_files)
#                     if merged_pdf_bytes:
#                         st.success("PDFs merged successfully!")

#                         # Preview the merged PDF
#                         st.write("### Preview of Merged PDF")
#                         merged_preview_images = preview_pdf_content(
#                             merged_pdf_bytes)
#                         for page_num, img in merged_preview_images:
#                             st.image(
#                                 img, caption=f"Merged PDF - Page {page_num}", use_column_width=True)

#                         st.download_button(
#                             label="Download Merged PDF",
#                             data=merged_pdf_bytes,
#                             file_name="merged_pdf.pdf",
#                             mime="application/pdf"
#                         )

#     elif option == "Split PDF":
#         uploaded_file = st.file_uploader(
#             "Upload PDF file to split", type="pdf"
#         )

#         if uploaded_file:
#             # Store the PDF content in memory for reuse
#             pdf_content = uploaded_file.getvalue()

#             num_pages = len(fitz.open(stream=pdf_content, filetype="pdf"))

#             # Preview the uploaded PDF
#             st.write("### Preview of Uploaded PDF")
#             uploaded_preview_images = preview_pdf_content(pdf_content)
#             for page_num, img in uploaded_preview_images:
#                 st.image(img, caption=f"Page {
#                          page_num}", use_column_width=True)

#             # Let the user choose between excluding or selecting specific pages
#             split_option = st.radio(
#                 "How would you like to split the PDF?",
#                 ("Exclude pages", "Select specific pages to download")
#             )

#             if split_option == "Exclude pages":
#                 exclude_pages = st.multiselect(
#                     "Select pages to exclude from download",
#                     list(range(1, num_pages + 1)),
#                     format_func=lambda x: f"Page {x}"
#                 )

#                 if st.button("Split PDF"):
#                     st.write(f"Excluding pages: {exclude_pages}")
#                     pdf_bytes = split_pdf(
#                         pdf_content, exclude_pages=exclude_pages
#                     )

#                     # Preview the split PDF
#                     st.write("### Preview of Split PDF")
#                     split_preview_images = preview_pdf_content(pdf_bytes)
#                     for page_num, img in split_preview_images:
#                         st.image(
#                             img, caption=f"Split PDF - Page {page_num}", use_column_width=True)

#                     st.download_button(
#                         label="Download All Except Specified Pages",
#                         data=pdf_bytes,
#                         file_name="all_except_specified_pages.pdf",
#                         mime="application/pdf"
#                     )

#             elif split_option == "Select specific pages to download":
#                 pages_to_keep = st.multiselect(
#                     "Select pages to download",
#                     list(range(1, num_pages + 1)),
#                     format_func=lambda x: f"Page {x}"
#                 )

#                 if st.button("Split PDF"):
#                     st.write(f"Downloading selected pages: {pages_to_keep}")
#                     pdf_bytes = split_pdf(
#                         pdf_content, pages_to_keep=pages_to_keep
#                     )

#                     # Preview the split PDF
#                     st.write("### Preview of Selected Pages PDF")
#                     split_preview_images = preview_pdf_content(pdf_bytes)
#                     for page_num, img in split_preview_images:
#                         st.image(
#                             img, caption=f"Split PDF - Page {page_num}", use_column_width=True)

#                     st.download_button(
#                         label="Download Selected Pages PDF",
#                         data=pdf_bytes,
#                         file_name="selected_pages.pdf",
#                         mime="application/pdf"
#                     )


# if __name__ == "__main__":
#     main()

import streamlit as st
import fitz  # PyMuPDF
import io
import base64
from PIL import Image
from typing import List, Optional, IO, Tuple


def merge_pdfs(pdf_files: List[IO[bytes]]) -> Optional[bytes]:
    merged_pdf_bytes = io.BytesIO()
    merger = fitz.open()

    try:
        for pdf_file in pdf_files:
            pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
            merger.insert_pdf(pdf_document)

        merger.save(merged_pdf_bytes)
        merger.close()
        merged_pdf_bytes.seek(0)
        return merged_pdf_bytes.getvalue()

    except Exception as e:
        st.error(f"Error merging PDFs: {e}")
        return None


def split_pdf(
    pdf_content: bytes,
    pages_to_keep: Optional[List[int]] = None,
    exclude_pages: Optional[List[int]] = None
) -> bytes:
    pdf_document = fitz.open(stream=pdf_content, filetype="pdf")
    num_pages = len(pdf_document)

    writer = fitz.open()

    if exclude_pages is not None:
        for page_number in range(num_pages):
            if (page_number + 1) not in exclude_pages:
                writer.insert_pdf(pdf_document, from_page=page_number, to_page=page_number)
    elif pages_to_keep is not None:
        for page_number in pages_to_keep:
            writer.insert_pdf(pdf_document, from_page=page_number - 1, to_page=page_number - 1)
    else:
        # If no pages are specified, include all pages
        writer.insert_pdf(pdf_document)

    split_pdf_bytes = io.BytesIO()
    writer.save(split_pdf_bytes)
    writer.close()
    split_pdf_bytes.seek(0)

    return split_pdf_bytes.getvalue()


def preview_pdf_pages(pdf_file: IO[bytes], sort_order: str) -> List[Tuple[int, Image.Image]]:
    # Convert PDF to images for preview with specified DPI
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    images: List[Tuple[int, Image.Image]] = []
    dpi = 100  # Adjust DPI for faster rendering

    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        pix = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))  # Set DPI
        img = Image.open(io.BytesIO(pix.tobytes()))
        images.append((page_number + 1, img))

    # Sort pages based on user input
    if sort_order == "Ascending":
        images = sorted(images, key=lambda x: x[0])
    elif sort_order == "Descending":
        images = sorted(images, key=lambda x: x[0], reverse=True)
    elif sort_order == "Alphabetical":
        # Convert page number to string for alphabetical sorting
        images = sorted(images, key=lambda x: str(x[0]))

    return images


def preview_pdf_content(pdf_bytes: bytes) -> List[Tuple[int, Image.Image]]:
    # Convert PDF bytes to images for preview
    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
    images: List[Tuple[int, Image.Image]] = []
    dpi = 100  # Adjust DPI as needed

    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        pix = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))
        img = Image.open(io.BytesIO(pix.tobytes()))
        images.append((page_number + 1, img))

    return images


def display_images_in_scrollable_container(images: List[Tuple[int, Image.Image]], caption_prefix: str):
    image_html = ""
    for page_num, img in images:
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        image_html += f"""
            <div style='text-align:center; margin-bottom:10px;'>
                <img src='data:image/png;base64,{img_str}' style='max-width:100%; height:auto;'/>
                <p>{caption_prefix} - Page {page_num}</p>
            </div>
        """
    st.markdown(
        f"""
        <div style='height:500px; overflow-y: scroll; border:1px solid #ccc; padding:10px;'>
            {image_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    st.title("PDF Tools")

    option = st.selectbox(
        "Select an action",
        ("Merge PDFs", "Split PDF")
    )

    if option == "Merge PDFs":
        uploaded_files = st.file_uploader(
            "Upload PDF files to merge", accept_multiple_files=True, type="pdf"
        )

        if uploaded_files:
            # Add sort order selection
            sort_order = st.selectbox(
                "Sort Pages",
                ["Original Order", "Ascending", "Descending", "Alphabetical"]
            )

            all_images: List[Tuple[int, Image.Image]] = []
            for uploaded_file in uploaded_files:
                st.write(f"### Preview and Edit: {uploaded_file.name}")
                preview_images = preview_pdf_pages(uploaded_file, sort_order)
                all_images.extend(preview_images)

            if all_images:
                st.write("### Final Preview Before Merging")
                display_images_in_scrollable_container(all_images, "Page")

                if st.button("Merge PDFs"):
                    # Create temporary PDFs from the preview images
                    temp_files: List[IO[bytes]] = []
                    for page_num, img in all_images:
                        temp_pdf = io.BytesIO()
                        img.save(temp_pdf, format='PDF')
                        temp_pdf.seek(0)
                        temp_files.append(temp_pdf)

                    merged_pdf_bytes = merge_pdfs(temp_files)
                    if merged_pdf_bytes:
                        st.success("PDFs merged successfully!")

                        # Preview the merged PDF
                        st.write("### Preview of Merged PDF")
                        merged_preview_images = preview_pdf_content(merged_pdf_bytes)
                        display_images_in_scrollable_container(merged_preview_images, "Merged PDF")

                        st.download_button(
                            label="Download Merged PDF",
                            data=merged_pdf_bytes,
                            file_name="merged_pdf.pdf",
                            mime="application/pdf"
                        )

    elif option == "Split PDF":
        uploaded_file = st.file_uploader(
            "Upload PDF file to split", type="pdf"
        )

        if uploaded_file:
            # Store the PDF content in memory for reuse
            pdf_content = uploaded_file.getvalue()

            num_pages = len(fitz.open(stream=pdf_content, filetype="pdf"))

            # Preview the uploaded PDF
            st.write("### Preview of Uploaded PDF")
            uploaded_preview_images = preview_pdf_content(pdf_content)
            display_images_in_scrollable_container(uploaded_preview_images, "Page")

            # Let the user choose between excluding or selecting specific pages
            split_option = st.radio(
                "How would you like to split the PDF?",
                ("Exclude pages", "Select specific pages to download")
            )

            if split_option == "Exclude pages":
                exclude_pages = st.multiselect(
                    "Select pages to exclude from download",
                    list(range(1, num_pages + 1)),
                    format_func=lambda x: f"Page {x}"
                )

                if st.button("Split PDF"):
                    st.write(f"Excluding pages: {exclude_pages}")
                    pdf_bytes = split_pdf(
                        pdf_content, exclude_pages=exclude_pages
                    )

                    # Preview the split PDF
                    st.write("### Preview of Split PDF")
                    split_preview_images = preview_pdf_content(pdf_bytes)
                    display_images_in_scrollable_container(split_preview_images, "Split PDF")

                    st.download_button(
                        label="Download All Except Specified Pages",
                        data=pdf_bytes,
                        file_name="all_except_specified_pages.pdf",
                        mime="application/pdf"
                    )

            elif split_option == "Select specific pages to download":
                pages_to_keep = st.multiselect(
                    "Select pages to download",
                    list(range(1, num_pages + 1)),
                    format_func=lambda x: f"Page {x}"
                )

                if st.button("Split PDF"):
                    st.write(f"Downloading selected pages: {pages_to_keep}")
                    pdf_bytes = split_pdf(
                        pdf_content, pages_to_keep=pages_to_keep
                    )

                    # Preview the split PDF
                    st.write("### Preview of Selected Pages PDF")
                    split_preview_images = preview_pdf_content(pdf_bytes)
                    display_images_in_scrollable_container(split_preview_images, "Split PDF")

                    st.download_button(
                        label="Download Selected Pages PDF",
                        data=pdf_bytes,
                        file_name="selected_pages.pdf",
                        mime="application/pdf"
                    )


if __name__ == "__main__":
    main()
