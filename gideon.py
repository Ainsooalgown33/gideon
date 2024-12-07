import os
import pyaudio
import vosk  # Import vosk for speech recognition
import json
import pyttsx3  # Text-to-speech library
import speech_recognition as sr  # For listening to commands after activation
import threading
import time
import tkinter as tk  # GUI library for displaying the robot emoji
import wikipedia  # Wikipedia library for fetching answers
from datetime import datetime

# Set the language and user agent for Wikipedia to comply with their policy
wikipedia.set_lang("en")
wikipedia.set_user_agent("GideonVoiceAssistant/1.0 (https://github.com/yourusername/yourrepo; contact@yourdomain.com)")

# Path to your Vosk model
model_path = "C:/vosk-model-small-en-us-0.15"  # Replace with the correct path
# Set up microphone for audio input
samplerate = 16000  # Correct sample rate for Vosk model
device_index = None  # Use default device

# Initialize pyaudio
p = pyaudio.PyAudio()

# Open stream to record audio from the microphone
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=samplerate,
                input=True,
                frames_per_buffer=1024)  # Reduced buffer size to avoid overflow

# Set up Vosk recognizer
model = vosk.Model(model_path)
rec = vosk.KaldiRecognizer(model, samplerate)

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def search_wikipedia(query):
    """Search Wikipedia and return a summary of the page."""
    try:
        summary = wikipedia.summary(query, sentences=2)  # Limit to first 2 sentences
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple results found: {e.options}"
    except wikipedia.exceptions.HTTPTimeoutError:
        return "Request timed out. Please try again."
    except wikipedia.exceptions.RequestError:
        return "There was a problem with the request."
    except wikipedia.exceptions.RedirectError:
        return "This page has been redirected."
    except wikipedia.exceptions.PageError:
        return "Sorry, I couldn't find anything on that topic."

# --- GUI Setup for Robot Emoji ---
root = tk.Tk()
root.title("Voice Assistant")
root.geometry("300x200")

# Robot emoji label (initially red)
robot_label = tk.Label(root, text="🤖", font=("Arial", 100), fg="red")
robot_label.pack(pady=30)

def change_robot_color(active=True):
    """Change the robot emoji's color based on activity state."""
    if active:
        robot_label.config(fg="green")  # Green when active
    else:
        robot_label.config(fg="red")  # Red when inactive

# --- Command Handling ---
def listen_for_question():
    """Listen for a question using the microphone and recognize speech."""
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Listening for a question...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        question = recognizer.recognize_google(audio).lower()
        print(f"Question received: {question}")
        return question
    except sr.UnknownValueError:
        print("Sorry, I did not understand the question.")
        speak("Sorry, I did not understand the question.")
        return None
    except sr.RequestError:
        print("Sorry, I couldn't process the request.")
        speak("Sorry, I couldn't process the request.")
        return None

def answer_question(question):
    """Answer the question based on predefined responses or Wikipedia."""
    # Predefined responses for common questions
    if "how are you" in question:
        return "I'm doing great, thank you for asking!"
    elif "who are you" in question or "what is your name" in question:
        return "I am Gideon, your voice assistant."
    elif "what is your function" in question or "what can you do" in question:
        return "I am here to assist you with various tasks like answering questions, telling the time, and much more."
    elif "what time is it" in question:
        current_time = datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}."
    elif "what is today's date" in question or "what date is it" in question:
        today_date = datetime.now().strftime("%B %d, %Y")
        return f"Today's date is {today_date}."
    elif "goodbye" in question or "exit" in question or "bye" in question:
        return "Goodbye! Shutting down."
    elif "who made you" in question:
        return "I was created by a developer using various tools and technologies like Vosk and Python."
    elif "are you alive" in question:
        return "I am not alive. I am just a program designed to assist you."
    elif "can you tell the time" in question:
        return "Yes, I can! Just ask me what time it is."
    else:
        # Use Wikipedia to answer the question
        return search_wikipedia(question)

def listen_for_wake_word():
    print("Ready to listen...")
    change_robot_color(active=False)  # Robot is inactive at first

    while True:
        data = stream.read(1024)  # Smaller buffer size for better real-time listening
        if rec.AcceptWaveform(data):
            result = rec.Result()
            print(result)

            # Process the result to get text
            result_json = json.loads(result)
            recognized_text = result_json.get("text", "").lower()

            # Check if the detected phrase is "Gideon"
            if "gideon" in recognized_text:
                print("Wake word 'Gideon' detected!")
                speak("Hello! How can I assist you?")
                change_robot_color(active=True)  # Change robot emoji to green
                
                # Start listening for questions after detecting the wake word
                listen_for_questions()

# New function to listen for questions continuously until "goodbye" is said
def listen_for_questions():
    """Keep listening for questions and answer until 'goodbye' is said."""
    while True:
        question = listen_for_question()

        if question:
            response = answer_question(question)
            print("Answering:", response)
            speak(response)

            # If "goodbye" is mentioned, stop listening
            if "goodbye" in question or "exit" in question or "bye" in question:
                change_robot_color(active=False)  # Change robot color to red
                break  # Exit the loop and stop the assistant

# Run the assistant in a separate thread so that the GUI stays active
def start_assistant():
    listen_for_wake_word()

# Start the assistant in a background thread
threading.Thread(target=start_assistant, daemon=True).start()

# Start the GUI loop
root.mainloop()

