from langchain.chat_models import AzureChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

llm = AzureChatOpenAI(
    deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("OPENAI_API_VERSION"),
    temperature=0.3
)

def generate_summary(text):
    prompt = f"Summarize the following document:\n{text[:4000]}"
    return llm.predict(prompt)