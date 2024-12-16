import google.generativeai as genai
import config
import os

def call_llm(paper, field="academia", topic="research"):
    if "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"] = config.api_key

    genai.configure(api_key=config.api_key)

    model = genai.GenerativeModel("gemini-1.5-flash")
    sample_pdf = genai.upload_file(paper)
    response = model.generate_content(["I am a ", field, " researcher interested in ", topic, ". Give me a summary of this pdf file.", sample_pdf])
    return response.text
