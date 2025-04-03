# Summarization & Documentation using LLM Models

## Overview
This application is designed to efficiently summarize Text, PDFs, and Urls providing concise and meaningful outputs. Initially focused on text summarization, the project expanded to then building up a Curious assistant feature & summarizing CSV files & providing visualizations for the data.
![image alt](https://github.com/RiyaaGupta02/Summ_FinalProj_curr/blob/affaafb5741065b56552ad5c84a4f4a0fb273d2c/WhatsApp%20Image%202025-03-18%20at%2002.20.45.jpeg)

## Features
- **Text Summarization:** Extracts key information from lengthy text inputs.
- **CSV files Summarization:** Processes and summarizes CSV files using Pandas, providing descriptive visualization.
- **PDF Summarization:** Extracts and summarizes text from PDFs, making document analysis more efficient.
- **URL Summarization:** Fetches and summarizes webpage content.
- **Curious Assistance:** A built-in site web search tool that allows users to look up doubts and information instantly without leaving the site, making it a one-stop solution for coursework and documentation needs.
- **Keyword-Focused Summarization:** Uses AI21’s model to generate summaries centered around a specific keyword, highlighting relevant insights and benefits.
 ![image alt](https://github.com/RiyaaGupta02/Summ_FinalProj_curr/blob/affaafb5741065b56552ad5c84a4f4a0fb273d2c/Text_Summarize_Proj.jpeg)
 ![image alt](https://github.com/RiyaaGupta02/Summ_FinalProj_curr/blob/affaafb5741065b56552ad5c84a4f4a0fb273d2c/WhatsApp%20Image%202025-03-18%20at%2002.23.52.jpeg)
  
## Tech Stack
- Python: Core programming language
- LangChain: Framework for working with LLMs
- Streamlit: Web application framework for UI
- OpenAI API as well as AI21: Language models used for understanding & testing on to know which to integrate as well as how to optimize leading to lower cost in production. 

## Description & an understanding on working of it

**Models Used**
The summarization functionality has been tested and implemented using:
- OpenAI API: Initially integrated via LangChain, but later faced API key expiration and compatibility issues.
- AI21 LLM: Demonstrated strong performance and for latter purposes used that model for summarization.

**NLP Techniques & Text Processing**
- To ensure effective summarization, several Natural Language Processing (NLP) techniques are utilized:
- Sentence Tokenization: Splitting text into meaningful sentence units.
- Text Chunking: Breaking large text into smaller, coherent segments while optimizing token usage.
- Named Entity Recognition (NER): Identifying and retaining important entities.
- TF-IDF & Embeddings: Ensuring relevant content is preserved based on contextual importance.
- Keyword Extraction: Extracting crucial terms to enhance summary relevance.

**Approach when worked along with Ai21 model briefly**
Divide-and-Conquer Strategy: Large text is split into smaller chunks using LangChain's RecursiveCharacterTextSplitter.Each chunk is summarized independently using AI21's summarization API. The individual summaries are further combined and summarized for a cohesive final result.

## Key Capabilities
- Processes text of any length using intelligent chunking.
- Optional focus parameter to guide summarization toward specific aspects.
- Customizable chunk size and overlap for fine-tuned control.
- Seamlessly handles text from various sources (raw text, PDFs, URLs).
- Robust error handling for smooth operation.

  ### additional features
   ![image alt](https://github.com/RiyaaGupta02/Summ_FinalProj_curr/blob/affaafb5741065b56552ad5c84a4f4a0fb273d2c/WhatsApp%20Image%202025-03-18%20at%2002.24.47.jpeg)
   ![image alt](https://github.com/RiyaaGupta02/Summ_FinalProj_curr/blob/affaafb5741065b56552ad5c84a4f4a0fb273d2c/WhatsApp%20Image%202025-03-18%20at%2002.26.13.jpeg)

 ## Conclusion
  This project evolved through a trial-and-error learning approach during an internship. While it is not a fully developed site, various features were tested to refine functionality. This aligns with my personal drive for continuous improvement and innovation, always striving to enhance and optimize solutions.

  ### About Me
  I am Riya Gupta a fresher recently graduated with a degree in B.E in Information Technology. I am actively looking out for good opportunities to reach me do visit my LinkedIn: https://www.linkedin.com/in/riyaa-gupta02/
  
