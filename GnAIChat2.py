# GnAIChatUI.py

import speech_recognition as sr
import pyttsx3
from openai import OpenAI
import os
import constants as c
#from MyAIIndex_Build import construct_index, load_index_from_storage
#from MyAIIndex_Build import chatbot
import time
import pygame
from gtts import gTTS
import Voice_Tools3 as v
import Skill_Launch as sl
import llama_index
myquestion = ''
from llama_index import StorageContext, load_index_from_storage


def get_index():
  index_store = llama_index.IndexStore('Z:/MyAI/Index_Data/index_store')
  vector_store = llama_index.VectorStore('Z:/MyAI/Index_Data/vector_store')
  graph_store = llama_index.GraphStore('Z:/MyAI/Index_Data/graph_store')

  storage_context = StorageContext(
    index_store=index_store,
    vector_stores=vector_store,
    graph_store=graph_store)

  # Load index
  from llama_index.indices.loading import load_index_from_storage

  index = load_index_from_storage(storage_context)
  return index

index = get_index()


# wait for wake word
while myquestion != 'exit':
  wakeword = v.Check_For_Wakeword()
  woken = v.Phrase_Exists(wakeword, "Matrix")
  if woken == True:
    wakeword = ''
    print('woken')
    quest = v.Ask_Voice_Question()
    if sl.Check_If_Skill(quest) == False:
      answer = chatbot(quest, index)
      print(answer)
      v.Play_Prompt(answer, 'response', 'speak')
    else:
      print(quest)
      sl.Run_Skill(quest)
  else:
    pass