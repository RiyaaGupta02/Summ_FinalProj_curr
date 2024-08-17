# here 1 in 1Summarization cos then placement of it be order wise so in pages folder Summ be at the top
import tempfile
import streamlit as sl
import numpy as np
from TextClean import clean_and_summarize_text
from TextClean import extract_and_process_url
from urllib.parse import urlparse
# from Raw_summ import text_split_chunks
from Raw_summ import summarize_text
from Raw_summ import num_tokens
from SummAi21 import summarize_pdf_ai21
from SummAi21 import summarize_url_Ai21
from SummAi21 import summarize_text_ai21
from CSV_summ import summarize_data
from CSV_summ import create_visualizations
# import pdfplumber
from langchain_community.document_loaders import WebBaseLoader
import requests
import time
import pandas as pd
import os
from langchain_openai import ChatOpenAI
from Chains import extract_text_from_pdf
from dotenv import load_dotenv
# for interacting with openAI model 
# Load environment variables from .env file
load_dotenv()
# Access the API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')
llm  = ChatOpenAI(temperature=0.5, model = "gpt-3.5-turbo-instruct")


sl.set_page_config(
    page_title= "Summarization",   # Then use the set_page_config() method of Streamlit to provide a page_title of that page
    page_icon= ":memo:", 
   )

with sl.sidebar:
    sl.markdown(""" Need a quick summary?  Just paste your text, upload a PDF, enter a URL or even upload your CSV for a quick visualization
                and we'll condense it for you. Want to know more about specific things go onto Curious Assistant and ask.""")

sl.markdown("""<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
""", unsafe_allow_html=True)
sl.markdown("""
<h1>
    <i class="fa-solid fa-pen-to-square"></i>
    <span style="color: #281862; opacity: 1;">Let's Summarize</span>
</h1>
""", unsafe_allow_html=True)


# lines left for the space btwn both markdown Summ heading & subheader
sl.subheader(" Input your text here in the prompt")
# selectbox made here for selecting the prompt what kind of prompt entering 
selectbox = sl.selectbox("Raw text or URL source or PDF", ("Raw text", "PDF", "URL", "CSV_file"))

# now here the conds for whatever the text be based upon them 
if selectbox == "Raw text":

    # Function to initialize session state
    def init_session_state():
        return [{"role": "assistant", "content": "Hi, there I am your freindly AI assistant. How can I help you? "}]
    

    sl.markdown(""" Helps in summarizing be it a normal text, conversations or your medical records 
                a story or a thesis; it helps fasten your learning. Do see your texts is more than 800 charachters. 
                Thank you for chosing us.""")
    raw_text = sl.text_area(label="Text", height=250, max_chars= 3000)   # this defines the textbox having text area
    if raw_text:
        model_choice = sl.radio("Choose summarization model:", ["OpenAI", "AI21"])

        if sl.button("Summarize"):
            if len(raw_text.split()) < 40:
                sl.error("Please enter at least 80 words or more than 800 charachters for summarization.")

            else:    
                if model_choice == "OpenAI":
                    SummaryNote = summarize_text(raw_text)
                else:
                    SummaryNote = summarize_text_ai21(raw_text)

            with sl.container():
                sl.write(" summarized text is:", ":sleuth_or_spy:")
                sl.text_area("Summary", value=SummaryNote, height=200, key="summary_box") 
                num_tokens_summary = num_tokens(SummaryNote)
                sl.write(f"The number of tokens used to summarize the text is: {num_tokens_summary}")

    if sl.button("Refresh Chat", type= "primary"):
                sl.session_state.messages = init_session_state()
                sl.rerun()



# here its an if else if kinda of a selectbox like choose one want to work on
# PLANNING -> so here hv this whole file upload making temp of it n then working on it extracting text of it n then hv whole 
# try - catch kind of for any error if facing then if text generate summary button implementing summary func
elif selectbox == "PDF":
    label_with_emoji = "Choose a PDF file :female-technologist: :crystal_ball:"        #now here cant put emoji n line together hence make a var that has both and placing that var then in later upload_file function.
    sl.markdown("""
    Side Note:
                Upload a Pdf to a max limit of 300pages. 
                If beyond that can split into multipls pdfs and then get a summary for each one of them.
                Thank you for choosing us. 
    """)
    uploaded_file = sl.file_uploader(label_with_emoji, type=["pdf"])
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name

        try:   
            text = extract_text_from_pdf(tmp_path)        # text got the text from pdf on this text will run later summarize func
            if text:
                sl.markdown("### Extracted text: ")
                sl.text_area("PDF Content", text, height=200)

                #here if the person adds the focus topic
                focus = sl.text_input("Enter a focus topic you want your summary to focus on(optional):")

                #adding a button here for summarizing the text we're getting if suppose we get the text or else simply the try n finally 
                # will run catching any issues present in the code can see it below else se
                if sl.button("Summarize the text "):
                    with sl.spinner("Summarizing..."):
                        Pdf_cleantext= clean_and_summarize_text(text)
                        summary = summarize_pdf_ai21(Pdf_cleantext)
                        sl.markdown("### Summary: ")
                        sl.text_area("summarized content", summary, height = 300)
                        # original sentence is below one
                        # sl.text_area("summarized content", summary, height = 300)
            else:
                sl.error("Failed to extract text from the PDF.")
        except Exception as e:
            sl.error(f"An error occurred: {str(e)}")
        finally:
            # Clean up the temporary file
            # above all things for by chance file runs in an error
            os.unlink(tmp_path)
    else:
        sl.info("Please upload a PDF file.")
# for PDF above will show extracted text in a small box n from it the Summarized pdf in box below it 


elif selectbox == "URL":

    if 'clear_inputs' not in sl.session_state:
        sl.session_state.clear_inputs = False

    label_emoji = "Add URL of your choice :female-technologist: :crystal_ball:"
    sl.markdown(""" 
                Since the site is in development phase and is working on lower optimal models 
                kindly refrain from adding higher complex websites as may not provide high accuracy result
                
                Until then will be working on making us better """)
    def is_valid_url(url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    uploaded_URL = sl.text_input(label_emoji, key="uploaded_URL")

    if uploaded_URL:
            if not is_valid_url(uploaded_URL):
                sl.warning("Please enter a valid URL.")
            else:
                try:
                    with sl.spinner("Extracting text from URL..."):
                        text = extract_and_process_url(uploaded_URL)
                    
                    if text:
                        sl.markdown("### Extracted text: ")
                        sl.text_area("URL content", text, height=200)

                        focus = sl.text_input("Enter a focus topic you want your summary to focus on (optional):")

                        if sl.button("Summarize the text"):
                            with sl.spinner("Summarizing..."):
                                # processed_content = clean_and_summarize_text(text)
                                url_summary = summarize_url_Ai21(uploaded_URL)
                                sl.markdown("### Summary: ")
                                sl.text_area("Summarized content", url_summary, height=300)

                                # Option to download the summarized text
                                sl.download_button(
                                    label="Download summary",
                                    data=url_summary,
                                    file_name="url_summary.txt",
                                    mime="text/plain"
                                )

                                #Adding here a Refresh Button 
                                if sl.button(" Start Over "):
                                    sl.session_state.clear_inputs = True
                                    sl.experimental_rerun()
                    else:
                        sl.warning("No text could be extracted from the given URL. Please try a different URL.")

                except Exception as e:
                    sl.error(f"An error occurred: {str(e)}")
                    sl.warning("Please try a different URL or check your internet connection.")

                    sl.session_state.clear_inputs = False
            
# This is a more specific exception type that belongs to the requests library (commonly used for making HTTP requests in Python).
# It only catches errors that occur during the process of making a request to a URL, like network issues, connection failures, or timeouts.

elif selectbox == "CSV_file":
    sl.markdown(" Please upload a CSV file that has minimum 20 rows. Also at present our model is only able to summarize files that have text in it for better understanding of numeric data kindly click on Visualization data & in it choose Descriptive statistics to get the visualization.")
    uploaded_csv = sl.file_uploader(" Upload a CSV file", type = "csv")
    if uploaded_csv is not None:
        df = pd.read_csv(uploaded_csv)
        sl.success("CSV file uploaded!")
        #also showcase the dataframe head 
        sl.dataframe(df.head(10))
        
        # Generate and display summary
        if sl.button("Summarize the text"):
            with sl.spinner("Summarizing..."):
                summary = summarize_data(df)
                sl.subheader("Data Summary")
                sl.write(summary)

        # Allow user to select data range
        sl.write("Select Data Range for Visualization")
        start_row = sl.number_input("Start Row:", min_value=0, max_value=len(df)-1, value=0, key="start")
        end_row = sl.number_input("End Row:", min_value=start_row, max_value=len(df)-1, value=min(len(df)-1, start_row+19), key="end")
            
            # Create visualizations for selected range
        create_visualizations(df, start_row, end_row)
        
else:
        sl.warning(" please upload a proper CSV file, to explore & learn more")






# text_pdf  = The text outlines a comprehensive roadmap for beginners aspiring to become AI Engineers. 
# It stresses the importance of coding and math skills as prerequisites and provides an eight-month study plan, 
# covering computer science fundamentals and Python basics. Additionally, it warns against educational scams and offers resources for effective research."""
        
