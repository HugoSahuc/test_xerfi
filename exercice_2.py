import chromadb
from chromadb.config import Settings
from langchain.document_loaders import PyPDFLoader
from datetime import date
import subprocess
import os

"""
We will need to change the docx to pdf to get the pages,
because .docx does not have the pages it's the software that print the pages, contrary to pdf.
Problem is that words is not avariable in linux
we can uses others alternatives like OpenOffice to convert doc with a process

https://stackoverflow.com/questions/62931764/convert-docx-to-pdf-in-python-in-linux
"""

def create_pdf_from_docx(path_pdf, path_docx):
    if not (os.path.isfile(path_docx)):
        print("Error: There is no .docx file")
        return False

    try:
        output = subprocess.check_output(['libreoffice', '--convert-to', 'pdf' ,path_docx])
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print("Error: you need to install LibreOffice")
        return False

    if not (os.path.isfile(path_pdf)):
        print("Error: the pdf file was not created")
        return False
    return True

def create_doc_from_file(collection):
    if not (create_pdf_from_docx("./test_technique_hugo.pdf", "./test_technique_hugo.docx")):
        return
    loader = PyPDFLoader("./test_technique_hugo.pdf")
    documents = loader.load_and_split()

    ids = []
    for doc in documents:
        id = f"doc_p{doc.metadata['page']}"
        collection.add(
            ids=[id],
            metadatas={"page": doc.metadata["page"] * 3,
                "date": date.today().strftime("%d/%m/%Y"),
                "source": "test_technique_xerfi.pdf"},
            documents=doc.page_content
        )
        ids.append(id)
    return ids

doc_id = "doc_p1"

def update_doc(text_to_add, doc_id, collection):
    text_doc =  text_to_add + collection.get(ids=[doc_id])["documents"][0]
    collection.update(
        ids=[doc_id],
        documents=[text_doc]
    )

def print_doc(collection, doc_id):
    doc = collection.get(
       ids=[doc_id], 
    )
    print(f"p:{doc['metadatas'][0]['page']}, {doc['metadatas'][0]['date']} {doc['documents'][0]}")

def main():
    chroma_client = chromadb.PersistentClient(path="test_db")
    collection = chroma_client.create_collection(name="test_xerfi")
    create_doc_from_file(collection)
    #print_doc(collection, "doc_p0")
    #update_doc("TEST", "doc_p0", collection)
    #print_doc(collection, "doc_p0")

if __name__ == "__main__":
    main()