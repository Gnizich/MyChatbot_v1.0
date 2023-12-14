import os
#from langchain import OpenAI
from langchain.llms import OpenAI
import openai
import sys
import constants as c
from langchain.chat_models import ChatOpenAI

c.Get_API()
client = OpenAI()

index = None

from llama_index import SimpleDirectoryReader, GPTListIndex, GPTVectorStoreIndex, LLMPredictor, PromptHelper, \
    load_index_from_storage

def construct_index():
    docs_dir = r'Z:/GnAIChat/MyAIChat_Docs'
    persist_dir = r'Z:/GnAIChat/MyAIChat_Index/Index'
    max_input_size = 4096
    num_outputs = 512
    max_chunk_overlap = 0.1
    chunk_size_limit = 600

    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

    llm = OpenAI(temperature=0.7, max_tokens=num_outputs)
    llm_predictor = LLMPredictor(llm=llm)

    documents = SimpleDirectoryReader(docs_dir).load_data()
    print("Documents loaded:")
    print(len(documents))
    index = GPTVectorStoreIndex(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)
    print("Index created.")
    index.storage_context.persist(persist_dir=persist_dir)
    return index


def chatbot(input_text):
    print("Received question:", input_text)
    query_engine = index.as_query_engine()
    response = query_engine.query(input_text)
    return response.response

# This block will only execute if the script is run directly (not when imported)
if __name__ == "__main__":
    c.Get_API()
    client = OpenAI()

    index = None

    from llama_index import SimpleDirectoryReader, GPTListIndex, GPTVectorStoreIndex, LLMPredictor, PromptHelper, \
        load_index_from_storage

    index = construct_index()
