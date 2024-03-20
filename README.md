
# PDF Parser and Q&A Chat Bot

This project allows users to upload a PDF file, parse it using a GenAI-powered parsing tool, and then utilize a chat interface to ask questions related to the content of the PDF.


## Introduction
This application streamlines the process of extracting and querying information from PDF documents. By integrating a powerful parsing tool powered by GenAI, users can upload a PDF, have it parsed into structured data, and then interactively ask questions based on the content of the PDF.

## Installation

1. Clone this repository to your local machine.
2. Install the required dependencies by running:
    ```
    pip install -r requirements.txt
    ```
3. Set up the GenAI API credentials. Refer to the `.example.env` file for reference and create your own `.env` file with your API credentials.
4. This application is powered by the Mixtral-8x7b-32768 model getting inference from Groq LPU.
5. For embeddings, it is using the `jina-embeddings-v2-base-en` model.
6. The Llamaindex is the framework for building the application, and Streamlit is used for creating the interface.
    
## Usage

1. Open the application in your web browser. You can access the web application here
2. Upload a PDF file using the provided interface.
3. Click the "Parse" button to initiate the parsing process.
4. After successful parsing, click the "View Parsed Content" button to see the extracted data.
5. Enter your question in the chat interface.
6. Click the "Ask" button to submit your question.
7. Receive answers specific to the content of the uploaded PDF

