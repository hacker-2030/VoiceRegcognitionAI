import speech_recognition as sr
import pyttsx3
import openai
import tkinter as tk
from tkinter import scrolledtext
import webbrowser
import wikipedia

# OpenAI API Key (Replace with your key)
openai.api_key = "sk-proj--iTOs-oiUn3vgIshIW53Y4L6f8GT4K5J7gI-8BQQZiNULdmlTBxwI4B_aomVfKsXz5z1FgT1sGT3BlbkFJUKioPEMkd06RKl76CTvXduRmgzA8QxuuKgyMYq7hy6xi0T6ba6-eSf0xki-4r1mc4f434ADCs"

# Initialize Speech Engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        append_text("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        append_text(f"You: {command}")
        return command.lower()
    except sr.UnknownValueError:
        append_text("Sorry, I didn't understand.")
        return ""
    except sr.RequestError:
        append_text("Request error. Check your internet connection.")
        return ""

def ai_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error: {e}"

def process_command(command):
    if "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube")
        append_text("Opening YouTube...")
    elif "search wikipedia for" in command:
        topic = command.replace("search wikipedia for", "").strip()
        result = wikipedia.summary(topic, sentences=2)
        speak(result)
        append_text(f"Wikipedia: {result}")
    elif "search google for" in command:
        query = command.replace("search google for", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")
        speak(f"Searching Google for {query}")
        append_text(f"Google Search: {query}")
    else:
        response = ai_response(command)
        speak(response)
        append_text(f"AI: {response}")

def start_listening():
    command = listen()
    if command:
        process_command(command)

def append_text(text):
    text_area.config(state=tk.NORMAL)
    text_area.insert(tk.END, text + "\n")
    text_area.config(state=tk.DISABLED)
    text_area.yview(tk.END)

# GUI Setup
root = tk.Tk()
root.title("AI Voice Assistant")
root.geometry("500x400")

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, width=60, height=15)
text_area.pack(pady=10)

listen_button = tk.Button(root, text="🎤 Speak", command=start_listening, font=("Arial", 12), bg="blue", fg="white")
listen_button.pack()

root.mainloop()
