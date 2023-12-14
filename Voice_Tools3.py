import os
import re
import constants as c
from MyAIIndex_Build import construct_index
import pygame
from gtts import gTTS
import time
#from langchain.chat_models import ChatOpenAI  # Updated import
import speech_recognition as sr
from openai import OpenAI
from langchain.chat_models import ChatOpenAI
import pgzero
from pgzero import music

# gets API Key from environment variable OPENAI_API_KEY
c.Get_API()
client = OpenAI()

preface_start = 'please keep your answer to '
preface_end = ' words and answer like a good buddy of mine would do.  Here is my question: '
preface = preface_start + '50' + preface_end

# Initialize the chat model with the new method
chat_model = ChatOpenAI(model_name="gpt-3.5-turbo")

def Init_Index():
    index = construct_index()

def Check_For_Wakeword():
    print("Listening for the wake word")
    # loop = 'yes'
    # while loop == 'yes':
    #     try:
    #         r = sr.Recognizer()
    #         with sr.Microphone() as source:
    #             audio = r.listen(source)
    #             prompt = r.recognize_google(audio)
    #             print("Prompt: " + prompt)
    #             if prompt is not None and "matrix" in prompt.lower():
    #                 Play_Prompt("How can I help?")
    #                 return 'Matrix'
    Play_Prompt("How can I help?")
    return 'Matrix'
    #     except:
    #         loop = 'yes'
    #     return

def Ask_Voice_Question():
    try:
        r = sr.Recognizer()
        print("Ask a question:")
        with sr.Microphone() as source:
            audio = r.listen(source)
        question = r.recognize_google(audio)
        longanswer = "comprehensive" in question.lower()
        if longanswer:
            preface = preface_start + '200' + preface_end
            question = preface + question
            return question
        elif "news" in question.lower():
            return question
        else:
            preface = preface_start + '50' + preface_end
            question = preface + question
            return question
    except sr.UnknownValueError:
        print("Could not understand audio")
        question = input("Type your question: ")
        return question

def Get_Answer(question, mp3file, instruct):
    response = ''
    if question is not None:
        if "comprehensive" in question.lower():
            preface = preface_start + '200' + preface_end
            full_question = preface + question
        elif "news" in question.lower():
            full_question = question
            print("News question: ", question)
        else:
            preface = preface_start + '50' + preface_end
            full_question = preface + question

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "user",
                    "content": full_question,
                },
            ],
        )

        text = response.choices[0].message.content
        print(text)
        cleaned_text = clean_text_for_tts(text)
        tts = gTTS(text=cleaned_text, lang='en', slow=False)
        savepath = "Z:/MyAI/tts/" + mp3file + ".mp3"
        tts.save(savepath)
        print('weather file saved', savepath)
    else:
        if instruct != 'silent':
            Play_Prompt("I am sorry, I did not understand that.")
    print(type(response))

def Play_Answer(mp3file, instruct):
    filepath = "Z:/MyAI/tts/" + mp3file + ".mp3"
    print(filepath)
    pygame.mixer.init()
    print("Initialized")
    pygame.mixer.music.set_volume(1.0)
    while not os.path.exists(filepath):
        time.sleep(1)
    pygame.mixer.music.load(filepath)
    print("Loaded")
    pygame.mixer.music.play()
    print("Playing")
    # while pygame.mixer.music.get_busy():
    #     pygame.time.Clock().tick(10)
    while pygame.mixer.music.get_busy() == True:
        continue
    print(" ")
    pygame.mixer.music.fadeout(1000)
    pygame.mixer.music.stop()
    pygame.quit()

    print("Play mp3 is done.")
    return

def Phrase_Exists(phrase, target):
    if phrase != None:
        phrase = phrase.lower()
        target = target.lower()
    else:
        phrase = "dummy phrase"
        target = "xxxxxx"

    if target in phrase:
        return True
    else:
        return False

def Play_Prompt(myPrompt, mp3file, instruct):
    print(myPrompt, mp3file, instruct)

    if instruct == 'silent':
        if os.path.exists(mp3file + ".mp3"):
            os.remove(mp3file + ".mp3")
        else:
            print(mp3file + ".mp3" + " does not exist")

        cleaned_text = clean_text_for_tts(myPrompt)

        if mp3file != 'spy':
            tts = gTTS(text=cleaned_text, lang='en', slow=False)
        else:
            tts = gTTS(text=cleaned_text, lang='en', slow=False)

        # Save to a file
        tts_filename = 'Z:\\MyAI\\tts\\' + mp3file + ".mp3"
        print(tts_filename)
        tts.save(tts_filename)
    # Now pass the filename to Play_Answer
    else:
        Play_Answer(mp3file, 'speak')
    return

def expand_contractions(text):
    contractions = {
        "can't": "cannot",
        "won't": "will not",
        # Add more contractions as needed
    }
    contractions_re = re.compile('(%s)' % '|'.join(contractions.keys()))

    def replace(match):
        return contractions[match.group(0)]
    return contractions_re.sub(replace, text)

import re

def clean_text_for_tts(content):
    content_str = str(content) + '%'
    text = content_str
    text = text.replace('.','.\n')
    text = expand_contractions(text)
    print(text)
    return text

# Example usage
if __name__ == "__main__":
    Init_Index()
    while True:
        wakeword = Check_For_Wakeword()
        if wakeword == 'Matrix':
            question = Ask_Voice_Question()
            Get_Answer(question)
