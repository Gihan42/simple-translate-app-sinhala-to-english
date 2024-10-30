import tkinter as tk
import speech_recognition as sr
from googletrans import Translator, LANGUAGES
import threading
from tkinter import messagebox

# Initialize variables for recognizer and translator
recognizer = sr.Recognizer()
translator = Translator()
listening = False

def recognize_callback(audio_data):
    try:
        # Set the language code for speech and translation
        speech_language_code = 'si'  # Sinhala language code
        translation_language_code = 'en'  # English language code

        # Recognize the speech
        spoken_text = recognizer.recognize_google(audio_data, language=speech_language_code)
        
        # Translate the spoken text
        translation = translator.translate(spoken_text, src=speech_language_code, dest=translation_language_code)
        translated_text = translation.text

        # Insert both spoken and translated text into the text box
        text_box.insert(tk.END, f"Spoken: {spoken_text}\nTranslated: {translated_text}\n\n")
        text_box.see(tk.END)  # Auto-scroll to the latest input
        root.update()

    except sr.UnknownValueError:
        text_box.insert(tk.END, "Sorry, I could not understand the audio.\n")
        text_box.see(tk.END)
        root.update()
    except sr.RequestError:
        messagebox.showerror("Error", "Could not connect to Google API")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def continuous_recognition():
    global listening
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        text_box.insert(tk.END, "Listening for speech...\n")
        root.update()

        while listening:
            audio_data = recognizer.listen(source)
            recognize_callback(audio_data)

def start_listening():
    global listening
    if not listening:  # Prevent multiple threads from starting
        listening = True
        recognize_thread = threading.Thread(target=continuous_recognition)
        recognize_thread.start()

def stop_listening():
    global listening
    listening = False
    text_box.insert(tk.END, "\nStopped listening.\n")
    root.update()

# Set up the GUI
root = tk.Tk()
root.title("Real-Time Speech Translator")
root.geometry("500x500")

# Text box for showing recognized and translated text
text_box = tk.Text(root, wrap=tk.WORD, height=20)
text_box.pack(pady=10, padx=10)

# Buttons to start and stop translation
start_button = tk.Button(root, text="Start Listening", command=start_listening)
start_button.pack(pady=5)

stop_button = tk.Button(root, text="Stop Listening", command=stop_listening)
stop_button.pack(pady=5)

root.mainloop()

