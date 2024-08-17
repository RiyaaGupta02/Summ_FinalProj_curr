from PyPDF2 import PdfReader
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain.chains.summarize import load_summarize_chain
from langchain_openai import OpenAI

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file"""
    try:
        with open(file_path, 'rb') as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def get_first_and_last_paragraphs(text: str) -> str:
    """Get the first and last paragraphs from the given text"""
    paragraphs = text.split("\n\n")
    if len(paragraphs) > 1:
        first_paragraph = paragraphs[0]
        last_paragraph = paragraphs[-1]
        return f"{first_paragraph}\n\n{last_paragraph}"
    else:
        return text

def summarize_pdf_text(file_path: str, token_limit: int = 1500, summarization_model: str = "gpt-3.5-turbo-instruct", temperature: float = 0.7) -> str:
    """
    Summarize a PDF file using LangChain and OpenAI.

    Args:
        file_path (str): The path to the PDF file.
        token_limit (int): The maximum number of tokens to consider for summarization.
        summarization_model (str): The OpenAI model to use for summarization.
        temperature (float): The temperature for the language model (between 0 and 1).

    Returns:
        str: The summarized text.
    """
    # Extract text from the PDF file
    text = extract_text_from_pdf(file_path)

    # Get the first and last paragraphs
    first_and_last_paragraphs = get_first_and_last_paragraphs(text)

    # Create a text splitter to chunk the text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=10)

    # Split the text into chunks
    chunks = text_splitter.split_text(first_and_last_paragraphs)
    
    # Prepare the prompt
    summarization_prompt = PromptTemplate(
        template= """
    Given the following pre-processed text chunks and their word frequencies, generate a concise summary that captures the 
    essence of the text while understanding its complexities. Aim for brevity, avoiding unnecessary information or repetition. 
    Highlight the most frequent words and mention any significant entities such as names of people or places. 
    The summary should be no longer than 5 lines:""",
    input_variables=["text"]      
    )

    # Load the OpenAI LLM
    llm = OpenAI(model_name=summarization_model, max_tokens=token_limit, temperature=temperature)

    # Create the summarization chain
    stuff_chain = load_summarize_chain(llm, chain_type="stuff", prompt=summarization_prompt)

    # Run the summarization chain and get the summary
    summary_pdf = stuff_chain.run(first_and_last_paragraphs)

    return summary_pdf