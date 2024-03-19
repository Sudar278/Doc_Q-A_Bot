import os
import io
import tempfile
import PyPDF2
import streamlit as st
from llama_parse import LlamaParse
from llama_index.core import VectorStoreIndex
from llama_index.llms.groq import Groq
from llama_index.core import Settings
from llama_index.embeddings.jinaai import JinaEmbedding

jinaai_api_key = os.environ["JINAAI_API_KEY"]
groq_api_key = os.environ.get('GROQ_API_KEY')

Settings.embed_model = JinaEmbedding(
    api_key=jinaai_api_key,
    model="jina-embeddings-v2-base-en",
    embed_batch_size=16,
)

Settings.llms = Groq(model="mixtral-8x7b-32768", api_key=groq_api_key)
llm = Groq(model="mixtral-8x7b-32768", api_key=groq_api_key)

def get_pdf_size_and_page_count(pdf_contents):
    """
    Get the size and page count of a PDF file from its contents.
    """
    pdf_file = io.BytesIO(pdf_contents)
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    pdf_size_mb = len(pdf_contents) / (1024 * 1024)  # Calculate file size in MB
    page_count = len(pdf_reader.pages)  # Get number of pages
    return pdf_size_mb, page_count

def parse_pdf(pdf_contents, parsing_instruction=None):
    """
    Parse a PDF file and return parsed text.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf_file:
        temp_pdf_file.write(pdf_contents)
        temp_pdf_path = temp_pdf_file.name

    try:
        if parsing_instruction:
            parsed_text = LlamaParse(result_type="markdown", parsing_instruction=parsing_instruction).load_data(temp_pdf_path)
        else:
            parsed_text = LlamaParse(result_type="markdown").load_data(temp_pdf_path)
    finally:
        os.unlink(temp_pdf_path)

    only_text = [parsed_text[x].text for x in range(len(parsed_text))]
    
    return parsed_text , only_text

def display_upload_section():
    file_uploader_key = "file_uploader"
    text_input_key = "parsing_instruction"

    uploaded_file = st.file_uploader(label="Upload a PDF file", type="pdf", key=file_uploader_key)
    st.write("Maximum file size: 5MB. Maximum page count: 18.")

    parsing_instruction = st.text_input("Parsing Instruction (GenAI powered parsing tool)", key=text_input_key)
    return uploaded_file, parsing_instruction

def display_parsed_info(pdf_size_mb, page_count):
    st.write("PDF uploaded successfully!")
    st.write(f"File size: {pdf_size_mb:.2f} MB, Page count: {page_count}")
    
    
def create_vector_query(parsed_text,qna):
    
    vector_index = VectorStoreIndex.from_documents(documents=parsed_text)
    query_engine = vector_index.as_query_engine(llm=llm)
    result = query_engine.query(qna)
    final_result = result.response
    return final_result