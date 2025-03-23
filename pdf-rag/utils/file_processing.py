import uuid
import pandas as pd
from PyPDF2 import PdfReader

def process_file(uploaded_file):
    file_id = str(uuid.uuid4())
    text = ""

    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif uploaded_file.type == "text/csv":
        df = pd.read_csv(uploaded_file)
        text = df.to_string(index=False)
    
    return file_id, text