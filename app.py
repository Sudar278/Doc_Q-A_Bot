import streamlit as st
from utils import get_pdf_size_and_page_count, parse_pdf, display_upload_section, display_parsed_info,create_vector_query

def main():
    st.title("Doc Q&A System")
    uploaded_file, parsing_instruction = display_upload_section()
    parsed_text = None  # Define parsed_text with a default value

    if uploaded_file is not None:
        pdf_contents = uploaded_file.read()
        pdf_size_mb, page_count = get_pdf_size_and_page_count(pdf_contents)
        if pdf_size_mb > 5:
            st.error("File size exceeds 5MB limit.")
            return
        if page_count > 18:
            st.error("Page count exceeds 18 pages limit.")
            return

        display_parsed_info(pdf_size_mb, page_count)

        if st.button("Parse"):
            with st.spinner("Parsing..."):
                try:
                    parsed_text, only_text = parse_pdf(pdf_contents, parsing_instruction)
                    # Store parsed text in a SessionState
                    session_state = st.session_state
                    session_state.parsed_text = parsed_text
                    session_state.only_text = only_text
                    # Set a flag to indicate that the content is initially hidden
                    session_state.content_visible = False
                except Exception as e:
                    st.error(f"Error parsing PDF: {e}")

    # Display parsed text only if "View Parsed Content" button is clicked
    if st.session_state.get("Parsed_text"):
        if st.button("View Parsed Content"):
            session_state = st.session_state
            # Toggle the visibility of the parsed content
            session_state.content_visible = not session_state.get("content_visible", False)
            if session_state.content_visible:
                st.write(session_state.only_text)
            else:
                st.write("")  # Empty placeholder to hide the content

    # Add Q&A section
    st.subheader("Chat with your Doc")
    qna_input = st.text_input("Ask your question:")
    if st.button("Ask"):
        if qna_input:
            if st.session_state.get("parsed_text"):  # Check if parsed_text has been assigned a value
                # Call the Q&A function here
                final_result = create_vector_query(st.session_state.parsed_text, qna_input)
                st.write("Answer:", final_result)
            else:
                st.warning("Please parse a PDF file first.")
        else:
            st.warning("Please input a question.")

if __name__ == "__main__":
    main()
