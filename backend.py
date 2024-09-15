import fitz
from langchain_text_splitters import CharacterTextSplitter, TokenTextSplitter
from sentence_transformers import SentenceTransformer
import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOpenAI
import serial
import time

chroma_db_directory = "./chroma_db"
vectorstore = None
input_file_path = 'input/Commodore64UsersGuide.pdf'

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as pdf:
        for page_num in range(len(pdf)):
            page = pdf.load_page(page_num)
            text += page.get_text()
    return text

def embed_text(text):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    sentences = text.split('\n')
    embeddings = model.encode(sentences)
    return sentences, embeddings

def split_text(text):
    document = Document(page_content=text, metadata={"title": "Commodore 64 User's Guide"})
    
    text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    texts = text_splitter.split_documents([document])
    
    text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=10, encoding_name="cl100k_base")  # This is the encoding for text-embedding-ada-002
    texts = text_splitter.split_documents(texts)
    
    return texts

def retrieve_documents(query):
    return vectorstore.similarity_search(query, k=5)

def create_detailed_explanation(query):
    documents = retrieve_documents(query)
    
    # Create a detailed explanation using OpenAI model
    prompt_template = ChatPromptTemplate.from_template(
        "Based on the following information, provide a detailed step-by-step guide in 1-2 sentences on how to {task}:\n\n{documents}\n\nTask: {task}\n\nGuide:"
    )
    llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key="", temperature=0.1)
    chain = LLMChain(llm=llm, prompt=prompt_template, output_key="guide")
    
    # Combine document contents into a single string
    documents_content = "\n".join([doc.page_content for doc in documents])
    print("Documents content: ", documents_content)
    
    # Create the detailed explanation
    result = chain.run(documents=documents_content, task=query)
    
    return result

def replace_special_characters(text):
    replacements = {
        'Ö': 'O', 'Ü': 'U', 'É': 'E', 'Á': 'A',
        'ö': 'o', 'ü': 'u', 'é': 'e', 'á': 'a'
    }
    for key, value in replacements.items():
        text = text.replace(key, value)
    return text

if not os.path.exists(chroma_db_directory):
    text = extract_text_from_pdf(input_file_path)
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    doc1 = Document(page_content=text)
    
    text_splitter = CharacterTextSplitter(chunk_size=400, chunk_overlap=0)
    texts = text_splitter.split_documents([doc1])
    
    text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=10, encoding_name="cl100k_base")
    texts = text_splitter.split_documents(texts)
    
    vectorstore = Chroma.from_documents(documents=texts, embedding=embeddings, persist_directory=chroma_db_directory)
else:
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    vectorstore = Chroma(persist_directory=chroma_db_directory, embedding_function=embeddings)

ser = serial.Serial('/dev/ttys016', baudrate=300, timeout=2)

duration = 300  # Duration in seconds
interval = 3  # Interval in seconds

start_time = time.time()

while time.time() - start_time < duration:
    question = ser.readline().decode('ascii').rstrip()
    print(f"Received from VICE: {question}")
    time.sleep(interval)
    
    if question:
        answer = create_detailed_explanation(question)
        answer = replace_special_characters(answer)
        text = answer.upper().encode('ascii', 'ignore')
        
        # Send text to VICE
        ser.write(text)
        print(f"Sent to VICE: {answer}")

print("Exiting...")

ser.close()