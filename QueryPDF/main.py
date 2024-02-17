#pip install cassio datasets openai tiktoken PyPDF2


from keys import ASTRA_DB_APPLICATION_TOKEN,ASTRA_DB_ID,OPENAI_API_KEY

from langchain_openai import ChatOpenAI
from langchain.vectorstores.cassandra import Cassandra 
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
import cassio
from PyPDF2 import PdfReader


def extract_text_with_pyPDF(PDF_File):
    from typing_extensions import Concatenate
    pdf_reader = PdfReader(PDF_File)
    raw_text = ''
    
    for i, page in enumerate(pdf_reader.pages):
        text = page.extract_text()
        if text:
            raw_text += text

    return raw_text
    
text_with_pyPDF = extract_text_with_pyPDF("SoftSkills.pdf")
print(text_with_pyPDF)

cassio.init(token=ASTRA_DB_APPLICATION_TOKEN,database_id=ASTRA_DB_ID)
llm=ChatOpenAI(openai_api_key="OPENAI_API_KEY", model="gpt-3.5-turbo",temperature=0.7)
embedding=OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

astra_vector_store=Cassandra(
    embedding=embedding,
    table_name="qa_mini_demo",
    session=None,
    keyspace=None
)
text_splitter=CharacterTextSplitter(
    seperator="\n",
    chunk_size=800,
    chunk_overlap=200,
    length_function=len
)
texts=text_splitter.split_text(text_with_pyPDF)

astra_vector_store.add_texts(texts)
astra_vector_index=VectorStoreIndexWrapper(vectorstore=astra_vector_store)
query_text=input("Enter text")
print( astra_vector_index.query(query_text, llm=llm))

