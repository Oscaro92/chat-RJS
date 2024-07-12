import os, shutil
from decouple import config
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader


class AgentRJS():
    def __init__(self):
        temperature = 0.0
        model = "gpt-4-turbo"
        os.environ["OPENAI_API_KEY"] = config('OPENAI_API_KEY')

        self.llm = ChatOpenAI(model=model, temperature=temperature)
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    def loadDoc(self, url: str)->list:
        '''
        Charger les documents

        :param url: url of the document (PDF format)
        :return: list of fields PDF (Document)
        '''

        loader = PyPDFLoader(url)
        pages = loader.load_and_split()

        for page in pages:
            page.page_content = page.page_content.replace('\n', ' ')

        return pages

    def saveDoc(self, chunks: list):
        # Load the existing database.
        db = Chroma(persist_directory="chroma", embedding_function=self.embeddings)

        # Calculate Page IDs.
        chunks_with_ids = self.calculateChunkIds(chunks)

        # Add or Update the documents.
        existing_items = db.get(include=[])  # IDs are always included by default
        existing_ids = set(existing_items["ids"])
        print(f"Number of existing documents in DB: {len(existing_ids)}")

        # Only add documents that don't exist in the DB.
        new_chunks = []
        for chunk in chunks_with_ids:
            if chunk.metadata["id"] not in existing_ids:
                new_chunks.append(chunk)

        if len(new_chunks):
            print(f"👉 Adding new documents: {len(new_chunks)}")
            new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
            db.add_documents(new_chunks, ids=new_chunk_ids)
            db.persist()
        else:
            print("✅ No new documents to add")

    def calculateChunkIds(self, chunks):
        '''
        calculate chunk ids
        :param chunks: list of chunks
        :return: list of chunk with ids
        '''

        last_page_id = None
        current_chunk_index = 0

        for chunk in chunks:
            source = chunk.metadata.get("source")
            page = chunk.metadata.get("page")
            current_page_id = f"{source}:{page}"

            # If the page ID is the same as the last one, increment the index.
            if current_page_id == last_page_id:
                current_chunk_index += 1
            else:
                current_chunk_index = 0

            # Calculate the chunk ID.
            chunk_id = f"{current_page_id}:{current_chunk_index}"
            last_page_id = current_page_id

            # Add it to the page meta-data.
            chunk.metadata["id"] = chunk_id

        return chunks


    def similarity(self, query:str)->list:
        '''
        Return docs with scoring

        :param query: query to evaluate
        :return: list of document
        '''
        db = Chroma(persist_directory="chroma", embedding_function=self.embeddings)
        results = db.similarity_search_with_relevance_scores(query)

        return results


    def chat(self, docs: list, query: str)->str:
        '''
        get response of LLM

        :param docs: list of docs similary
        :param query: user request
        :return: LLM response
        '''

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Tu es un assistant de notice de jeu de société. A partir des données des notices fournis tu dois répondre aux questions posés.\n"
                    "Les notices fournis : {docs} \n"
                    "Si il y a aucune notice fournis répond : Désolé je n'ai pas la notice de ce jeu..."
                ),
                ("human", "{query}")
            ]
        )

        chain = prompt | self.llm
        response = chain.invoke(
            {
                "docs": docs,
                "query": query
            }
        )

        return response.content