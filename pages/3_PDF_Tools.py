# # import streamlit as st
# # import fitz  # PyMuPDF
# # import io
# # from PIL import Image


# # def merge_pdfs(pdf_files):
# #     merged_pdf_bytes = io.BytesIO()
# #     merger = fitz.open()

# #     try:
# #         for pdf_file in pdf_files:
# #             pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
# #             merger.insert_pdf(pdf_document)

# #         merger.save(merged_pdf_bytes)
# #         merged_pdf_bytes.seek(0)
# #         return merged_pdf_bytes.getvalue()

# #     except Exception as e:
# #         st.error(f"Error merging PDFs: {e}")
# #         return None


# # def split_pdf(pdf_content, pages_to_keep=None, exclude_pages=None):
# #     pdf_document = fitz.open(stream=pdf_content, filetype="pdf")
# #     num_pages = len(pdf_document)

# #     writer = fitz.open()

# #     if exclude_pages is not None:
# #         for page_number in range(num_pages):
# #             if (page_number + 1) not in exclude_pages:
# #                 writer.insert_pdf(
# #                     pdf_document, from_page=page_number, to_page=page_number)
# #     elif pages_to_keep is not None:
# #         for page_number in pages_to_keep:
# #             writer.insert_pdf(
# #                 pdf_document, from_page=page_number - 1, to_page=page_number - 1)

# #     split_pdf_bytes = io.BytesIO()
# #     writer.save(split_pdf_bytes)
# #     split_pdf_bytes.seek(0)

# #     return split_pdf_bytes.getvalue()


# # def preview_pdf_pages(pdf_file, sort_order):
# #     # Convert PDF to images for preview with higher DPI
# #     pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
# #     images = []
# #     dpi = 600  # Increased DPI for sharper image quality

# #     for page_number in range(len(pdf_document)):
# #         page = pdf_document.load_page(page_number)
# #         pix = page.get_pixmap(matrix=fitz.Matrix(
# #             dpi / 72, dpi / 72))  # Set DPI
# #         img = Image.open(io.BytesIO(pix.tobytes()))
# #         images.append((page_number + 1, img))

# #     # Sort pages based on user input
# #     if sort_order == "Ascending":
# #         images = sorted(images, key=lambda x: x[0])
# #     elif sort_order == "Descending":
# #         images = sorted(images, key=lambda x: x[0], reverse=True)
# #     elif sort_order == "Alphabetical":
# #         # Convert page number to string for alphabetical sorting
# #         images = sorted(images, key=lambda x: str(x[0]))

# #     return images


# # def main():
# #     st.title("PDF Tools")

# #     option = st.selectbox(
# #         "Select an action",
# #         ("Merge PDFs", "Split PDF")
# #     )

# #     if option == "Merge PDFs":
# #         uploaded_files = st.file_uploader(
# #             "Upload PDF files to merge", accept_multiple_files=True, type="pdf"
# #         )

# #         if uploaded_files:
# #             # Add sort order selection
# #             sort_order = st.selectbox(
# #                 "Sort Pages",
# #                 ["Original Order", "Ascending", "Descending", "Alphabetical"]
# #             )

# #             all_images = []
# #             for uploaded_file in uploaded_files:
# #                 st.write(f"### Preview and Edit: {uploaded_file.name}")
# #                 preview_images = preview_pdf_pages(uploaded_file, sort_order)
# #                 all_images.extend(preview_images)

# #             if all_images:
# #                 st.write("### Final Preview")
# #                 # Display images in a scrollable container
# #                 for img in all_images:
# #                     st.image(img, use_column_width=True)

# #                 if st.button("Merge PDFs"):
# #                     # Create temporary PDFs from the preview images
# #                     temp_files = []
# #                     for img in all_images:
# #                         temp_pdf = io.BytesIO()
# #                         img.save(temp_pdf, format='PDF')
# #                         temp_pdf.seek(0)
# #                         temp_files.append(temp_pdf)

# #                     merged_pdf_bytes = merge_pdfs(temp_files)
# #                     if merged_pdf_bytes:
# #                         st.success("PDFs merged successfully!")
# #                         st.download_button(
# #                             label="Download Merged PDF",
# #                             data=merged_pdf_bytes,
# #                             file_name="merged_pdf.pdf",
# #                             mime="application/pdf"
# #                         )

# #     elif option == "Split PDF":
# #         uploaded_file = st.file_uploader(
# #             "Upload PDF file to split", type="pdf"
# #         )

# #         if uploaded_file:
# #             # Store the PDF content in memory for reuse
# #             pdf_content = uploaded_file.getvalue()

# #             num_pages = len(fitz.open(stream=pdf_content, filetype="pdf"))

# #             # Let the user choose between excluding or selecting specific pages
# #             split_option = st.radio(
# #                 "How would you like to split the PDF?",
# #                 ("Exclude pages", "Select specific pages to download")
# #             )

# #             if split_option == "Exclude pages":
# #                 exclude_pages = st.multiselect(
# #                     "Select pages to exclude from download",
# #                     list(range(1, num_pages + 1)),
# #                     format_func=lambda x: f"Page {x}"
# #                 )

# #                 if st.button("Split PDF") and exclude_pages:
# #                     st.write(f"Excluding pages: {exclude_pages}")
# #                     pdf_bytes = split_pdf(
# #                         pdf_content, exclude_pages=exclude_pages)

# #                     st.download_button(
# #                         label="Download All Except Specified Pages",
# #                         data=pdf_bytes,
# #                         file_name="all_except_specified_pages.pdf",
# #                         mime="application/pdf"
# #                     )

# #             elif split_option == "Select specific pages to download":
# #                 pages_to_keep = st.multiselect(
# #                     "Select pages to download",
# #                     list(range(1, num_pages + 1)),
# #                     format_func=lambda x: f"Page {x}"
# #                 )

# #                 if st.button("Download Selected Pages") and pages_to_keep:
# #                     st.write(f"Downloading selected pages: {pages_to_keep}")
# #                     pdf_bytes = split_pdf(
# #                         pdf_content, pages_to_keep=pages_to_keep)

# #                     st.download_button(
# #                         label="Download Selected Pages PDF",
# #                         data=pdf_bytes,
# #                         file_name="selected_pages.pdf",
# #                         mime="application/pdf"
# #                     )


# # if __name__ == "__main__":
# #     main()


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
#     dpi = 100  # Lower DPI for faster rendering and smaller images

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
#     dpi = 72  # Lower DPI for faster rendering and smaller images

#     for page_number in range(len(pdf_document)):
#         page = pdf_document.load_page(page_number)
#         pix = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))
#         img = Image.open(io.BytesIO(pix.tobytes()))
#         images.append((page_number + 1, img))

#     return images


# def display_images_in_expander(images: List[Tuple[int, Image.Image]], caption_prefix: str):
#     with st.expander("Click to view preview"):
#         for page_num, img in images:
#             st.image(img, caption=f"{
#                      caption_prefix} - Page {page_num}", use_column_width=True)


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
#                 display_images_in_expander(all_images, "Page")

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
#                         display_images_in_expander(
#                             merged_preview_images, "Merged PDF")

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
#             display_images_in_expander(uploaded_preview_images, "Page")

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
#                     display_images_in_expander(
#                         split_preview_images, "Split PDF")

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
#                     display_images_in_expander(
#                         split_preview_images, "Split PDF")

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
from PIL import Image
from typing import List, Optional, IO, Tuple


def merge_pdfs_from_images(images: List[Tuple[str, int, Image.Image]]) -> Optional[bytes]:
    """
    Merge images into a single PDF.

    Parameters:
        images: List of tuples containing (source_file_name, page_number, image)

    Returns:
        Merged PDF as bytes, or None if an error occurs.
    """
    merged_pdf_bytes = io.BytesIO()
    merger = fitz.open()

    try:
        for source_file_name, page_num, img in images:
            temp_pdf = io.BytesIO()
            img.save(temp_pdf, format='PDF')
            temp_pdf.seek(0)
            temp_doc = fitz.open("pdf", temp_pdf.read())
            merger.insert_pdf(temp_doc)
            temp_doc.close()

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
                writer.insert_pdf(
                    pdf_document, from_page=page_number, to_page=page_number)
    elif pages_to_keep is not None:
        for page_number in pages_to_keep:
            writer.insert_pdf(
                pdf_document, from_page=page_number - 1, to_page=page_number - 1)
    else:
        # If no pages are specified, include all pages
        writer.insert_pdf(pdf_document)

    split_pdf_bytes = io.BytesIO()
    writer.save(split_pdf_bytes)
    writer.close()
    split_pdf_bytes.seek(0)

    return split_pdf_bytes.getvalue()
    

def preview_pdf_pages(pdf_file: IO[bytes], source_file_name: str) -> List[Tuple[str, int, Image.Image]]:
    """
    Convert PDF pages to images for preview.

    Parameters:
        pdf_file: Uploaded PDF file.
        source_file_name: Name of the source PDF file.

    Returns:
        List of tuples containing (source_file_name, page_number, image)
    """
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    images: List[Tuple[str, int, Image.Image]] = []
    dpi = 200  # Lower DPI for faster rendering and smaller images

    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        pix = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))
        img = Image.open(io.BytesIO(pix.tobytes()))
        images.append((source_file_name, page_number + 1, img))

    return images


def display_images_in_expander(images: List[Tuple[str, int, Image.Image]], selected_pages: List[str]) -> List[str]:
    """
    Display images in an expander and allow the user to select pages.

    Parameters:
        images: List of tuples containing (source_file_name, page_number, image)
        selected_pages: List of page identifiers that are selected.

    Returns:
        Updated list of selected page identifiers.
    """
    with st.expander("Click to view and select pages"):
        for idx, (source_file_name, page_num, img) in enumerate(images):
            page_id = f"{source_file_name} - Page {page_num}"
            cols = st.columns([1, 4])
            with cols[0]:
                is_selected = page_id in selected_pages
                selected = st.checkbox("Select", value=is_selected, key=f"select_{idx}")
                if selected and page_id not in selected_pages:
                    selected_pages.append(page_id)
                elif not selected and page_id in selected_pages:
                    selected_pages.remove(page_id)
            with cols[1]:
                st.image(img, caption=page_id, use_column_width=True)
    return selected_pages


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
            st.write("### Preview and Select Pages to Merge")

            # Initialize or retrieve selected pages from session state
            if 'selected_pages' not in st.session_state:
                st.session_state.selected_pages = []

            all_images: List[Tuple[str, int, Image.Image]] = []
            for uploaded_file in uploaded_files:
                source_file_name = uploaded_file.name
                preview_images = preview_pdf_pages(uploaded_file, source_file_name)
                all_images.extend(preview_images)

            # Sort options
            sort_order = st.selectbox(
                "Sort Pages",
                ["Original Order", "Ascending by Page Number", "Descending by Page Number", "Alphabetical by File Name"]
            )

            # Apply sort order
            if sort_order == "Original Order":
                pass  # Keep the original order
            elif sort_order == "Ascending by Page Number":
                all_images = sorted(all_images, key=lambda x: x[1])
            elif sort_order == "Descending by Page Number":
                all_images = sorted(all_images, key=lambda x: x[1], reverse=True)
            elif sort_order == "Alphabetical by File Name":
                all_images = sorted(all_images, key=lambda x: x[0])

            # Display images and allow selection
            st.session_state.selected_pages = display_images_in_expander(all_images, st.session_state.selected_pages)

            if st.button("Merge Selected Pages"):
                # Filter images based on selected pages
                selected_images = [
                    (source_file_name, page_num, img)
                    for source_file_name, page_num, img in all_images
                    if f"{source_file_name} - Page {page_num}" in st.session_state.selected_pages
                ]

                if not selected_images:
                    st.warning("No pages selected for merging.")
                    return

                merged_pdf_bytes = merge_pdfs_from_images(selected_images)
                if merged_pdf_bytes:
                    st.success("PDFs merged successfully!")

                    # Preview the merged PDF
                    st.write("### Preview of Merged PDF")
                    merged_preview_images = preview_pdf_content(merged_pdf_bytes)
                    with st.expander("Click to view merged PDF preview"):
                        for page_num, img in merged_preview_images:
                            st.image(img, caption=f"Merged PDF - Page {page_num}", use_column_width=True)

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
            with st.expander("Click to view PDF preview"):
                for page_num, img in uploaded_preview_images:
                    st.image(img, caption=f"Page {page_num}", use_column_width=True)

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
                    with st.expander("Click to view split PDF preview"):
                        for page_num, img in split_preview_images:
                            st.image(img, caption=f"Split PDF - Page {page_num}", use_column_width=True)

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
                    with st.expander("Click to view selected pages preview"):
                        for page_num, img in split_preview_images:
                            st.image(img, caption=f"Split PDF - Page {page_num}", use_column_width=True)

                    st.download_button(
                        label="Download Selected Pages PDF",
                        data=pdf_bytes,
                        file_name="selected_pages.pdf",
                        mime="application/pdf"
                    )


def preview_pdf_content(pdf_bytes: bytes) -> List[Tuple[int, Image.Image]]:
    # Convert PDF bytes to images for preview
    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
    images: List[Tuple[int, Image.Image]] = []
    dpi = 200  # Lower DPI as needed

    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        pix = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))
        img = Image.open(io.BytesIO(pix.tobytes()))
        images.append((page_number + 1, img))

    return images


if __name__ == "__main__":
    main()
