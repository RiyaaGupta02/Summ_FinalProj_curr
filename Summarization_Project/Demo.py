import streamlit as sl

from langchain.agents import create_react_agent, AgentExecutor
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain import hub
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder
from langchain.schema import SystemMessage
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_community.output_parsers.rail_parser import GuardrailsOutputParser

api_key = os.getenv('OPEN_API_KEY')

from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

with sl.sidebar:
    sl.markdown(""" Need a deeper dive? Stuck on a specific detail or curious about something in your summary? No problem! Our built-in research assistant is here to help. Just ask a question, and it'll scour the web for relevant info.
                It's like having a personal research assistant right at your fingertips!""")

sl.title(" Curious Assistant: ask anything")

"""
We're revolutionizing summarization by introducing a groundbreaking feature: Contextual Research. 
Our new in-app feature empowers you to refine summaries with real-time web searches, creating a more personalized and informative experience. 
Try more of these features for better efficiency. 
"""


if "messages" not in sl.session_state:
    sl.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a chatbot who can search the web. How can I help you?"}
    ]

for msg in sl.session_state.messages:
    sl.chat_message(msg["role"]).write(msg["content"])

prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="You are a helpful AI assistant that can search the internet for information."),
    MessagesPlaceholder(variable_name="chat_history"),
    MessagesPlaceholder(variable_name="human_input"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

if prompt := sl.chat_input(placeholder="Who won the Women's U.S. Open in 2018?"):
    sl.session_state.messages.append({"role": "user", "content": prompt})
    with sl.chat_message("user"):
        sl.markdown(prompt)

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", api_key = api_key, streaming=True)
    search_tool = DuckDuckGoSearchRun()
    tools = [search_tool]

    #create a system message & set up the memory
    system_msg = SystemMessage(content= "You are a helpful AI assistant that can search the internet and get answers.")
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # Create the React agent 
    react_agent = create_react_agent(
        llm= llm,
        tools=tools,
        prompt=prompt
    )

    agent_executor = AgentExecutor(
        agent=react_agent, 
        tools=tools,
        memory=memory,
        verbose=True
        )

    with sl.chat_message("assistant"):
        response = agent_executor.invoke(prompt)
        sl.markdown(response)

    sl.session_state.messages.append({"role": "assistant", "content": response})