import string
import requests        # helps in getting requests
from bs4 import BeautifulSoup
import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter
nltk.download('wordnet')
nltk.download('stopwords')


# Imports for another func that cleans Pdf --> clean_pdf function below
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
nltk.download('punkt')


def clean_text(text):
    # remove special char
    text = text.translate(str.maketrans("", "", string.punctuation))
    # above line text cleaning by removing punctuatuion marks
    text = text.lower()  # bringing to lower it

    # lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmas = [lemmatizer.lemmatize(word, pos='v') if lemmatizer.lemmatize(word, pos='v') != word else lemmatizer.lemmatize(word, pos='n') for word in text.split()]
    # remove stopwords
    stop_Wrd = set(stopwords.words('english'))
    filtered_lemmas = [lemma for lemma in lemmas if lemma not in stop_Wrd]

    #joining cleaned words
    cleaned_text = ' '.join(filtered_lemmas)  
 # so here to ensure white space is maintained simply cleaned_text = ' '.join() so we joined lemmatized word with giving space also 
    return cleaned_text


def clean_and_summarize_text(text, max_sentences=50, min_words=10, max_words=50):
    # Convert entire text to lowercase
    text = text.lower()
    
    # Sentence tokenization and length filtering
    sentences = sent_tokenize(text)
    filtered_sentences = [sentence for sentence in sentences 
                          if min_words <= len(sentence.split()) <= max_words]
    
    # Text cleaning
    def clean_pdf(text):
        text = text.translate(str.maketrans("", "", string.punctuation))
        
        lemmatizer = WordNetLemmatizer()
        stop_words = set(stopwords.words('english'))
        
        lemmas = [lemmatizer.lemmatize(word, pos='v') if lemmatizer.lemmatize(word, pos='v') != word 
                  else lemmatizer.lemmatize(word, pos='n') for word in text.split()]
        
        filtered_lemmas = [lemma for lemma in lemmas if lemma not in stop_words]
        return ' '.join(filtered_lemmas)
    
    # Clean the filtered sentences
    cleaned_sentences = [clean_pdf(sentence) for sentence in filtered_sentences]
    
    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(cleaned_sentences)
    
    # Calculate sentence scores
    sentence_scores = np.sum(tfidf_matrix.toarray(), axis=1)
    
    # Select top sentences
    top_sentence_count = min(max_sentences, len(filtered_sentences))
    top_sentence_indices = sentence_scores.argsort()[-top_sentence_count:][::-1]
    top_sentences = [filtered_sentences[i] for i in sorted(top_sentence_indices)]
    
    # Join the selected sentences
    processed_pdf = ' '.join(top_sentences)
    
    return processed_pdf
      
# Example usage:
# long_text = "Your very long text here..."
# summarized_text = clean_and_summarize_text(long_text)
# print(summarized_text)


# EXTRACTING TEXT FROM THE URL
def extract_and_process_url(url, max_sentences=30):
    # Step 1: Extracting text from URL using Beautiful Soup
    def extract_text_from_url(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Extract text from <p>, <h1>, <h2>, <h3>, <h4>, <h5>, <h6>, <ul>, <ol>, <li> tags
        tags = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul'])
        text = ' '.join(tag.get_text(separator=' ', strip=True) for tag in tags)
    
        # Break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
    
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    
        # Drop blank lines
        url_text = '\n'.join(chunk for chunk in chunks if chunk)

        return url_text

    # Step 2: Process and cleanse the extracted text
    def process_and_cleanse_text(text, max_sentences):
        # Convert to lowercase
        text = text.lower()

        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)

        # Tokenize into sentences
        sentences = sent_tokenize(text)

        # Remove repeated words in each sentence
        def remove_repeated_words(sentences, limit=15):
            word_count = Counter()
            for sentence in sentences:
                words = sentence.split()
                word_count.update(words)
            
            filtered_sentences = []
            for sentence in sentences:
                words = sentence.split()
                filtered_words = [word for word in words if word_count[word] <= limit]
                filtered_sentences.append(' '.join(filtered_words))
            return filtered_sentences
        
        sentences = remove_repeated_words(sentences)

        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        filtered_sentences = [
            ' '.join([word for word in sentence.split() if word not in stop_words])
            for sentence in sentences
        ]
        
        # Use TF-IDF to identify important sentences
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(filtered_sentences)
        
        # Calculate sentence scores
        sentence_scores = np.sum(tfidf_matrix.toarray(), axis=1)
        
        # Select top sentences
        top_sentence_indices = sentence_scores.argsort()[-max_sentences:][::-1]
        top_sentences = [sentences[i] for i in sorted(top_sentence_indices)]
        
        # Join the selected sentences
        processed_text = ' '.join(top_sentences)
        
        return processed_text

    # Extract text from URL
    extracted_text = extract_text_from_url(url)
    
    # Process and cleanse the extracted text
    processed_text = process_and_cleanse_text(extracted_text, max_sentences)
    
    return processed_text