import streamlit as sl
import os
from dotenv import load_dotenv
from ai21 import AI21Client
from ai21.models.chat import ChatMessage

load_dotenv()

# Initialize AI21 client
client = AI21Client(api_key=os.environ.get("AI21_API_KEY"))

# Function to initialize session state
def init_session_state():
    return [{"role": "assistant", "content": "Hi, there I am your freindly AI assistant. How can I help you? "}]


# Streamlit UI setup
sl.title("Curious Assistant: ask anything")
sl.write("""
We're introducing an AI-powered assistant that can answer your questions and provide information on a wide range of topics. 
Our assistant uses advanced language models to generate informative and context-aware responses.
Try asking questions on various subjects to experience its capabilities!
""")

with sl.sidebar:
    sl.markdown("""
    This AI assistant helps in providing information and answer questions on a wide range of topics based on its training data. 
    While it doesn't perform real-time web searches, it has been trained on a vast amount of information up to its knowledge cutoff date.
    Feel free to ask questions about history, science, current events (up to its training data), and more!
    """)

    if sl.button("Refresh Chat", type= "primary"):
        sl.session_state.messages = init_session_state()
        sl.rerun()

# Initialize session state
if "messages" not in sl.session_state:
    sl.session_state.messages = [
        {"role": "assistant", "content": "Hi, there I am your freindly AI assistant. How can I help you? "}
    ]

# Display chat history
for msg in sl.session_state.messages:
    sl.chat_message(msg["role"]).write(msg["content"])

# Chat input and processing
if input_text := sl.chat_input(placeholder="Ask me anything! For example: What are the main causes of climate change?"):
    sl.session_state.messages.append({"role": "user", "content": input_text})
    sl.chat_message("user").write(input_text)

    with sl.chat_message("assistant"):
        # Prepare messages for AI21
        messages = [ChatMessage(role=msg["role"], content=msg["content"]) for msg in sl.session_state.messages]
        
        # Get response from AI21
        response = client.chat.completions.create(
            model= "jamba-instruct-preview",  # Using a more capable model
            messages=messages,
            max_tokens=500,
            temperature=0.7,
        )
        
        assistant_response = response.choices[0].message.content
        sl.session_state.messages.append({"role": "assistant", "content": assistant_response})
        sl.write(assistant_response)

        # Add a "Learn More" button
        if sl.button("Learn More"):
            with sl.expander("Additional Information"):
                # Get more detailed information from AI21
                detailed_response = client.chat.completions.create(
                    model="jamba-instruct-preview",
                    messages=messages + [ChatMessage(role="user", content="Please provide more detailed information on this topic.")],
                    max_tokens=1000,
                    temperature=0.6,
                )
                sl.write(detailed_response.choices[0].message.content)