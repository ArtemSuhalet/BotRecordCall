import requests
import openai
from langchain.schema import Document

from config_data.config import *

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
ChatOpenAI.api_key = os.getenv('OPENAI_API_KEY')
embeddings = OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_API_KEY'))

def read_file_request():
    """
    Функция для чтения запроса из файла
    :return:
    """
    with open("transcribe1.txt", "r", encoding="utf-8") as file:
        file_request = file.read()
    print(type(file_request))
    transcript = [Document(page_content=file_request, metadata={"source": "local"})]
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
    docs = text_splitter.split_documents(transcript)
    db = FAISS.from_documents(docs, embeddings)
    return db


def process_gpt_request(db, user_request, k=4):
    """
    Функция для обработки запроса в GPT
    :param file_request:
    :param user_request:
    :return:
    """
    print("Processing user query:", user_request)  # Отладочное сообщение
    docs = db.similarity_search(user_request, k=k)
    docs_page_content = " ".join([d.page_content for d in docs])

    chat = ChatOpenAI(model_name="gpt-4", temperature=0.8, )

    # Template to use for the system message prompt
    template = """
            You are a helpful assistant that that can answer questions about youtube videos
            based on the video's transcript: {docs}

            Only use the factual information from the transcript to answer the question.

            If you feel like you don't have enough information to answer the question, say "I don't know".

            """

    system_message_prompt = SystemMessagePromptTemplate.from_template(template)

    # Human question prompt
    human_template = "Answer the following question: {question}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)

    response = chain.run(question=user_request, docs=docs_page_content)
    response = response.replace("\n", "")
    print('response', response)
    return response.strip()


def is_valid_google_meet_link(link):
    try:
        response = requests.head(link)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def request_chat(user_request):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": 'Your model response here.'},
            {"role": "user", "content": user_request},
        ],
    )

    if response and response.choices:
        response_text = response.choices[0].message['content']
        cleaned_response = response_text.strip()
        return cleaned_response