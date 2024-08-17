from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
# from langchain.memory import ConversationBufferMemory
from TextClean import clean_text
import nltk
import collections
import tiktoken
# from nltk.tokenize import word_tokenize
# from nltk import pos_tag
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
# Access the API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')


def text_split_chunks(text):
    # text to split into chunks recursive way
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 250,
        chunk_overlap = 20,
        length_function = len,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = text_splitter.split_text(text)
    return chunks

def word_freq_analysis(text):
    word_freq = collections.defaultdict(int)
    words = text.split()
    for word in words:
        word_freq[word] += 1
    return word_freq
    """The word_frequency_analysis function takes a text input, splits it into words, and calculates the frequency
      of each word using the collections.Counter class."""
    
def extractor_agent(chunks):
    pre_proceeChunks = chunks
    word_freq = word_freq_analysis(' '.join(pre_proceeChunks))
    # hence the word_freq = method to find word freq applied on preprocesChunks i.e. actually text_chunks
    return pre_proceeChunks, word_freq
# hence extractor agent returns original chunks + word_freq 

# if req to count the no of tokens can do it using this to keep track of token usage
def num_tokens(text, encoding='cl100k_base'):
    """Get the number of tokens in a string."""
    encoding = tiktoken.get_encoding(encoding)
    return len(encoding.encode(text))


def generator_agent(pre_proceeChunks, word_freq):  
    #funct that generates the summary
# Initialize OpenAI model
    openai_model = OpenAI(temperature=0.5, model_name="gpt-3.5-turbo", openai_api_key = api_key)

    # Create prompt template
    prompt_template = PromptTemplate(
        template= """
    Given the following pre-processed text chunks and their word frequencies, generate a concise summary that captures the 
    essence of the text while understanding its complexities. Aim for brevity, avoiding unnecessary information or repetition. 
    Highlight the most frequent words and mention any significant entities such as names of people or places. 
    The summary should be no longer than 5 lines, with an optional extra line for a slightly more descriptive 
    touch if needed mentioned :
    Pre-processed chunks:
        {pre_proceeChunks}

        Word frequencies:
        {word_freq}
        """,
    input_variables=["pre_proceeChunks", "word_freq"]
    )
    formatted_chunks = "\n\n".join(pre_proceeChunks)
    # Create prompt
    prompt = prompt_template.format(pre_proceeChunks=formatted_chunks, word_freq=str(word_freq))
    
    # llm = OpenAI(temperature = 0.4, openai_api_key = api_key)
    llm = openai_model
    prompt = prompt_template
    # Create LLM chain
    llm_chain = prompt|llm

    # Run LLM chain and get summary
    summarized_text = llm_chain.invoke({"pre_proceeChunks": formatted_chunks, "word_freq": str(word_freq)})

    return summarized_text

#the main summarise chain
def summarize_text(text):
    text = clean_text(text)
    chunks = text_split_chunks(text)
    preprocessed_chunks, word_freq = extractor_agent(chunks)
    summary = generator_agent(preprocessed_chunks, word_freq)
    return summary


""" HENCE RESULTING INTO THIS FUNC HAVING 
- cleaned the text
- then chunks using text_split will be splitting and all
- pre-processing of chunk done and word_freq also brought
- finally summary generated as used 2 agents for it """
