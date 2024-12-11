import google.generativeai as genai
from IPython.display import Markdown
import config

# from langchain.document_loaders import PyPDFLoader
# from langchain import PromptTemplate
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.chains.summarize import load_summarize_chain
# from langchain.chat_models import ChatOpenAI

import os
from langchain.document_loaders import PyPDFLoader
from langchain import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain_google_vertexai import ChatVertexAI

model = ChatVertexAI(model="gemini-1.5-flash")