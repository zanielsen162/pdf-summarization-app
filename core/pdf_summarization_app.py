import google.generativeai as genai
import config
import os
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
import tempfile


token_max = 1000


def prepare_paper(paper, chunk_size=1000, chunk_overlap=50):
    return paper.temporary_file_path()

def call_llm(paper, field='academia', topic='research'):
    if "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"] = config.api_key
    
    genai.configure(api_key=config.api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prepared_paper = prepare_paper(paper)
    # response = model.generate_content("Explain how AI works")

    sample_pdf = genai.upload_file(prepared_paper)
    response = model.generate_content(["As a", field, "researcher interested in", topic, ", provide me a summary of this research paper broken into relevant sections.", sample_pdf])
    title = model.generate_content(["Here is a research paper.", sample_pdf, "Extract and return only the title of the document."])

    return(response.text, title.text)