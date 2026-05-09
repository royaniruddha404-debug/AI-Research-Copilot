from langchain_community.document_loaders import PyPDFLoader
import tempfile

def load_pdf(uploaded_file):

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as tmp_file:

        tmp_file.write(uploaded_file.read())

        temp_path = tmp_file.name

    loader = PyPDFLoader(temp_path)

    documents = loader.load()

    return documents