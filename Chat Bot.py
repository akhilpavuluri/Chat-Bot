import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import pyttsx3
import openai

# Set up your OpenAI API key
openai.api_key = 'provide you OpenAI API key here'

def chat_with_gpt(prompt):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",  # Using the gpt-3.5-turbo model
        prompt=prompt,
        temperature=0.7,
        max_tokens=150
    )
    return response.choices[0].text.strip()

def get_voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio)
        print(f"User: {query}")
        return query
    except Exception as e:
        print(e)
        return ""

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def send_message():
    user_input = entry.get()
    if user_input.lower() == 'exit':
        response_text.insert(tk.END, "Goodbye!\n")
        entry.delete(0, tk.END)
    else:
        response_text.insert(tk.END, "You: " + user_input + "\n")
        response = chat_with_gpt(user_input)
        response_text.insert(tk.END, "Bot: " + response + "\n\n")
        entry.delete(0, tk.END)
        speak(response)

def handle_voice_input():
    user_input = get_voice_input()
    entry.insert(tk.END, user_input)

def handle_voice_output():
    user_input = entry.get()
    response = chat_with_gpt(user_input)
    response_text.insert(tk.END, "You: " + user_input + "\n")
    response_text.insert(tk.END, "Bot: " + response + "\n\n")
    speak(response)

# Create the main window
root = tk.Tk()
root.title("Professional Chat Bot")

# Create widgets
entry = tk.Entry(root, width=50)
entry.pack(pady=10)

response_text = scrolledtext.ScrolledText(root, width=60, height=20)
response_text.pack(padx=10, pady=5)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(side=tk.LEFT, padx=5)

voice_input_button = tk.Button(root, text="Voice Input", command=handle_voice_input)
voice_input_button.pack(side=tk.LEFT, padx=5)

voice_output_button = tk.Button(root, text="Voice Output", command=handle_voice_output)
voice_output_button.pack(side=tk.LEFT, padx=5)

# Initial message
response_text.insert(tk.END, "Bot: Welcome to the Professional Chat Bot!\n")
response_text.insert(tk.END, "Bot: Type 'exit' to end the conversation.\n\n")

root.mainloop()
