from traitlets.config.application import T
from neuralintents import BasicAssistant
import speech_recognition
import pyttsx3 as tts
import sys

recognizer = speech_recognition.Recognizer()

speaker = tts.init()
speaker.setProperty('rate', 150)
todo_list = ['Play Game', 'Clean Room', 'Coding']

def create_note():
  global recognizer

  speaker.say("What do you want to write")
  speaker.runAndWait()

  done = False

  while not done:
    try:

      with speech_recognition.Microphone() as mic:

        recognizer.adjust_for_ambient_noise(mic, duration=0.2)
        audio = recognizer.listen(mic)

        note = recognizer.recognize_google(audio)
        note = note.lower()

        speaker.say("Choose a filename!")
        speaker.runAndWait()

        recognizer.adjust_for_ambient_noise(mic, duration=0.2)
        audio = recognizer.listen(mic)

        filename = recognizer.recognize_google(audio)
        filename = filename.lower()
      with open(filename, 'w') as f:
        f.write(note)
        done = True
        speaker.say("Created the note {filename}")
        speaker.runAndWait()
      
    except speech_recognition.UnknownValueError:
      recognizer = speech_recognition.Recognizer()
      speaker.say("Please try again!")
      speaker.runAndWait()


def add_todo():
  global recognizer

  speaker.say("What todo do you want to add")
  speaker.runAndWait()

  done = False

  while not done:
    try:
      with speech_recognition.Microphone() as mic:

        recognizer.adjust_for_ambient_noise(mic, duration=0.2)
        audio = recognizer.listen(mic)

        item = recognizer.recognize_google(audio)
        item = item.lower()

        todo_list.append(item)
        done = True

        speaker.say(f"added {item} to the list! ")
        speaker.runAndWait()
    except speech_recognition.UnknownValueError:
      recognizer = speech_recognition.Recognizer()
      speaker.say("Please try again!")
      speaker.runAndWait()

def show_todos():
  
  speaker.say("The item in to do list are")
  for item in todo_list:
    speaker.say(item)
  speaker.runAndWait()

def hello():

  speaker.say("Hello, what can I do for you")
  speaker.runAndWait()

def stop():
  speaker.say("Bye")
  speaker.runAndWait()
  sys.exit(0)

mappings = {
    "greeting": hello,
    "create_note": create_note,
    "add_todo": add_todo,
    "show_todos": show_todos ,
    "exit": stop
}

assistant = BasicAssistant('intents.json')
assistant.fit_model()

while True:
  try:
    with speech_recognition.Microphone() as mic:

      recognizer.adjust_for_ambient_noise(mic, duration=0.2)
      audio = recognizer.listen(mic)

      message = recognizer.recognize_google(audio)
      mesage = message.lower()

    assistant.request(message)
  except speech_recognition.UnknownValueError:
    recognizer = speech_recognition.Recognizer()
    speaker.say("Please try again!")
    speaker.runAndWait()