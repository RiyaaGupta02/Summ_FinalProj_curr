from ai21 import AI21Client
from langchain.text_splitter import RecursiveCharacterTextSplitter
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
load_dotenv()

#Initialize AI21 client
client = AI21Client(api_key=os.getenv('AI21_API_KEY'))

def summarize_pdf_ai21(Pdf_cleantext, focus = None, chunk_size = 5000, chunk_overlap = 50):
     # Create a LangChain text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    # Split the text into chunks using LangChain
    chunks = text_splitter.split_text(Pdf_cleantext)

    # Summarize each chunk
    chunk_summaries = []       #created a list already for all the summaries of each chunk that'll come which later gets summarized into one main
    for chunk in chunks:
        summarize_params = {
            "source": chunk,
            "source_type": "TEXT"
        }

        if focus:
            summarize_params["focus"] = focus

        response = client.summarize.create(**summarize_params)
        chunk_summaries.append(response.summary)

    # Combine chunk summaries
    combined_summary = "\n\n".join(chunk_summaries)

    # Create final summary
    final_summarize_params = {
        "source": combined_summary,
        "source_type": "TEXT"
    }
    if focus:
        final_summarize_params["focus"] = focus

    final_response = client.summarize.create(**final_summarize_params)

    return final_response.summary



# for URL creating method same way

def summarize_url_Ai21(url, focus=None, max_tokens=1000):
    # Validate URL
    if not url.startswith(('http://', 'https://')):
        raise ValueError("Invalid URL. Please provide a URL starting with http:// or https://")

    # Fetch content from URL
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract text content
    text_content = ' '.join([p.text for p in soup.find_all('p')])

    # Truncate text to approximate token limit
    # Assuming average of 4 characters per token
    char_limit = max_tokens * 4
    truncated_text = text_content[:char_limit]

    # Prepare summarization parameters
    summarize_params = {
        "source": truncated_text,
        "source_type": "TEXT"
    }

    if focus:
        summarize_params["focus"] = focus

    # Generate summary
    response = client.summarize.create(**summarize_params)

    return response.summary



# creating here a summarizing function for the text 
def summarize_text_ai21(raw_text, focus = None, chunk_size = 60, chunk_overlap = 10):
     # Create a LangChain text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    # Split the text into chunks using LangChain
    chunks = text_splitter.split_text(raw_text)

    # Summarize each chunk
    chunk_summaries = []
    current_chunk = ""
    for chunk in chunks:
        current_chunk += chunk + " "
        if len(current_chunk.split()) >= 60:
            summarize_params = {
                "source": current_chunk.strip(),
                "source_type": "TEXT"
            }

            if focus:
                summarize_params["focus"] = focus

            try:
                response = client.summarize.create(**summarize_params)
                chunk_summaries.append(response.summary)
            except Exception as e:
                print(f"Error summarizing chunk: {e}")
            current_chunk = ""

    # Handle any remaining text
    if current_chunk:
        summarize_params = {
            "source": current_chunk.strip(),
            "source_type": "TEXT"
        }
        if focus:
            summarize_params["focus"] = focus
        try:
            response = client.summarize.create(**summarize_params)
            chunk_summaries.append(response.summary)
        except Exception as e:
            print(f"Error summarizing final chunk: {e}")

    # Combine chunk summaries
    combined_summary = "\n\n".join(chunk_summaries)

    # Create final summary
    if len(combined_summary.split()) >= 40:
        final_summarize_params = {
            "source": combined_summary,
            "source_type": "TEXT"
        }
        if focus:
            final_summarize_params["focus"] = focus

        final_text_response = client.summarize.create(**final_summarize_params)
        return final_text_response.summary
    else:
        return combined_summary 