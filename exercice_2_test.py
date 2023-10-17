import chromadb
from datetime import date
from exercice_2 import create_doc_from_file, create_pdf_from_docx, update_doc, print_doc

chroma_client = chromadb.EphemeralClient()

#test in a separate collection the create_doc_from_file
id_test = "doc_p0"
test_collection = chroma_client.create_collection(name="unit_test")
create_doc_from_file(test_collection)

assert test_collection.count() == 3

doc0 = test_collection.get(ids=[id_test])
assert doc0["metadatas"][0]['page'] == 0
assert doc0["metadatas"][0]['date'] == date.today().strftime("%d/%m/%Y")
assert doc0["metadatas"][0]['source'] == 'test_technique_xerfi.pdf'

doc1 = test_collection.get(ids=["doc_p1"])
assert doc1["metadatas"][0]['page'] == 3
assert doc1["metadatas"][0]['date'] == date.today().strftime("%d/%m/%Y")

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