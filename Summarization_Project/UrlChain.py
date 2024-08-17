import re
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')

def summarize_url(uploaded_URL, token_limit=2000):
    loader = WebBaseLoader(uploaded_URL)
    docs = loader.load()

    # Split the content into smaller chunks (paragraphs)
    chunks = []
    for doc in docs:
        paragraphs = re.split(r'\n\s*\n', doc.page_content)
        chunks.extend([p.strip() for p in paragraphs if p.strip()])

    summaries = []
    for chunk in chunks:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=200)
        texts = text_splitter.split_text(chunk)

        for text in texts:
            openai_model = OpenAI(temperature=0.5, model_name="gpt-3.5-turbo-instruct", openai_api_key=api_key)

            # Create a prompt template
            prompt_template = PromptTemplate(
                template="Summarize the following text in 4 lines while staying within a token limit of {token_limit} tokens and focusing on keywords and bold lines. If exceeding token limit, focus on first and last lines and get summarization:\n\nToken limit: {token_limit}\n\nText:\n{text}",
                input_variables=["token_limit", "text"],
            )

            # Create the prompt with the template and values
            prompt = prompt_template.format(token_limit=token_limit, text=text)

            # Initialize the model
            chain = load_summarize_chain(llm=openai_model, chain_type="stuff", prompt=prompt_template)

            # Create a Document instance from the text
            input_document = Document(page_content=text)

            summary_of_url = chain.run(input_documents=[input_document], token_limit=token_limit)
            summaries.append(summary_of_url)

    return '\n\n'.join(summaries)