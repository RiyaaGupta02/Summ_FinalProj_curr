import streamlit as st
import os
from ai21 import AI21Client
from langchain_community.document_loaders import TextLoader, PyPDFLoader
import numpy as np
from PIL import Image
import tempfile
import os
from dotenv import load_dotenv
load_dotenv()
api_key=os.getenv('AI21_API_KEY')
if not api_key:
    st.error("AI21 API key not found. Please set the AI21_API_KEY environment variable.")
    st.stop()
#Initialize AI21 client
client = AI21Client(api_key=api_key)

st.set_page_config(
    page_title="About_Us",
    page_icon=":memo:",
)

# Heading
st.markdown("""
<h1>
    <i class="fa-solid fa-pen-to-square"></i>
    <span style="color: #281862; opacity: 1;">About Us</span>
</h1>
""", unsafe_allow_html=True)

textbox_emoji = "A message from us :smile: :phone:"

aboutus_text = """Hi, we're a team of few developers, trying to breakthrough the world of LLM and AI as well as learning how to integrate Business with those LLM models.
Our current site is under development and running only for demo purpose so that we can develop it better. Kindly share your feedback with us."""
st.text_area(textbox_emoji, value=aboutus_text, height=130)

# Streamlit app
st.subheader("DOCUMENT CHATBOT")
st.markdown("""This is an upcoming feature where you can upload documents (PDF or TXT) and 
            ask questions related to them using our chatbot powered by AI21.""")

image = Image.open('Doc_chatbotPic.jpeg')
img_array = np.array(image)
st.text("Q&A with Document may look like this:")
st.image(img_array, width=600)

# File uploader for the document
uploaded_file = st.file_uploader("Select a PDF or TXT file", type=["pdf", "txt"])

# Initialize the Q&A functionality only if a file is uploaded
if uploaded_file is not None:
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    try:
        # Load the document
        if uploaded_file.type == "application/pdf":
            loader = PyPDFLoader(tmp_file_path)
        else:
            loader = TextLoader(tmp_file_path)
        
        documents = loader.load()

        # Combine all document content
        context = " ".join([doc.page_content for doc in documents])[:10000]

        user_emoji = "Ask a question about the document :crystal_ball: :technologist:"
        # Get user input
        user_input = st.text_input(user_emoji)

        if st.button("What's my answer"):
            if user_input:
                try:
            # Use AI21's Q&A functionality
                    response = client.library.answer.create(
                        question=user_input,
                        context=context
                        )
                    st.write("Full API Response:", response)  # Debug print
                    if hasattr(response, 'answer') and response.answer:
                        st.markdown(response.answer)
                    else:
                        st.write("The AI model couldn't generate an answer. This might be due to the context length or the nature of the question.")
                except Exception as e:
                    st.error(f"An error occurred while getting the answer: {str(e)}")
        else:
            st.write("Please enter a question.")

    except Exception as e:
        st.error(f"An error occurred while processing the file: {str(e)}")
    
    finally:
        # Clean up the temporary file
        os.unlink(tmp_file_path)

else:
    st.warning("Please upload a PDF or TXT file to start the Q&A.")

def feedback_message_box(message):
    st.markdown(f"""
        <style>
            .feedback-message {{
                position: fixed;
                bottom: 15px;
                left: 90%;
                transform: translateX(-50%);
                background-color: #f0f0f0;
                padding: 7px;
                border-radius: 15px;
                text-align: center;
                font-size: 12px;
                font-weight: normal;
                width: 65%;
                max-width: 250px;
            }}
        </style>
        <div class="feedback-message">{message}</div>
    """, unsafe_allow_html=True)

# Display the customized message box
feedback_message_box("Precious Feedbacks")