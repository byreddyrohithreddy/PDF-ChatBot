from fastapi import FastAPI, File, UploadFile
import os
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import DocArrayInMemorySearch
from operator import itemgetter
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI,GoogleGenerativeAIEmbeddings
from pydantic import BaseModel

app = FastAPI()

llm = ""
gemini_embeddings = ""
parser = ""
chain = ""

# prompt template
template = ""
# prompt intiallization
prompt = " "

# loading pdf and splitting them
loader = ""
pages = ""

#vector store to store embeddings for easy retreival
vectorstore = ""

#Retriever which retrieves the values
retriever = ""

chain = ""

class Item(BaseModel):
    text:str

class Key(BaseModel):
    key:str

@app.post("/api/valid")
def key_validation(key:Key):
    global llm,gemini_embeddings,parser,chain,template,prompt
    print(key.key)
    os.environ["GOOGLE_API_KEY"]= key.key
    llm = ChatGoogleGenerativeAI(model="gemini-pro")
    gemini_embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    parser = StrOutputParser()
    chain = llm | parser

    template = """
    Answer the question based on the context below. If you can't 
    answer the question, reply "I don't know".

    Context: {context}

    Question: {question}
    """
    # prompt intiallization
    prompt = PromptTemplate.from_template(template)
    try:
        chain.invoke("tell me a joke")
        reply={"status":"true"}
    except Exception as e:
        print(e)
        reply={"status":"false"}
    return reply

@app.post("/api/python")
async def upload_pdf(file: UploadFile = File(...)):
    global loader,pages,vectorstore,retriever,chain
    contents = await file.read()

    with open(file.filename, "wb") as f:
        f.write(contents)

    loader = PyPDFLoader(file.filename)
    pages = loader.load_and_split()
    vectorstore = DocArrayInMemorySearch.from_documents(pages, embedding=gemini_embeddings)
    retriever = vectorstore.as_retriever()
    chain = (
    {
        "context": itemgetter("question") | retriever,
        "question": itemgetter("question"),
    }
    | prompt
    | llm
    | parser
    )
    os.remove(file.filename)
    return {"filename": file.filename}

@app.post("/api/chat")
async def chat(item:Item):
    out=chain.invoke({'question': item.text})
    print(out)
    return {"answer":out}
