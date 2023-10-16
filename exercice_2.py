import chromadb
from chromadb.config import Settings
from langchain.document_loaders import PyPDFLoader
from datetime import date
import subprocess
import os

chroma_client = chromadb.PersistentClient(path=".test_db")
collection = chroma_client.get_or_create_collection(name="test_xerfi")

"""
We will need to change the docx to pdf to get the pages,
because .docx does not have the pages it's the software that print the pages, contrary to pdf.
Problem is that I uses linux and words is not avariable, we can uses
others alternatives like OpenOffice to show the pages of the doc.

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


#print_doc(collection, doc_id)
id_test = "doc_p0"
test_collection = chroma_client.create_collection(name="unit_test")
create_doc_from_file(test_collection)

assert test_collection.count() == 3

doc0 = test_collection.get(ids=[id_test])
assert doc0["metadatas"][0]['page'] == 0
assert doc0["metadatas"][0]['source'] == 'test_technique_xerfi.pdf'

chroma_client.delete_collection(name="unit_test")

#test create_pdf
assert create_pdf_from_docx("./test_technique_hugo.pdf", "./test_technique_hugo.docx")

# test update_doc
phrase = " Il était une fois une histoire passionnante blablabla …"
to_add = "Bien le bonjour !"
result_phrase = "Bien le bonjour ! Il était une fois une histoire passionnante blablabla …"
id_test = 'test_1'

test_collection = chroma_client.create_collection(name="unit_test")
test_collection.add(
    ids=[id_test],
    metadatas={"page": 12, "date": "12/08"},
    documents=phrase
)

update_doc(to_add, id_test, test_collection)

result_test = test_collection.get(ids=[id_test])
assert result_test['documents'][0] == result_phrase
assert result_test['metadatas'][0]['page'] == 12

chroma_client.delete_collection(name="unit_test")