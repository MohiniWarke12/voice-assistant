
import speech_recognition as sr
import pyttsx3
import smtplib
import os
from email.mime.text import MIMEText

# Initialize
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Speak function
def speak(text):
    print("System:", text)
    engine.say(text)
    engine.runAndWait()

# Listen function
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            text = recognizer.recognize_google(audio)
            print("You:", text)
            return text.lower()

        except sr.UnknownValueError:
            speak("Sorry, I didn't understand.")
            return ""

        except sr.WaitTimeoutError:
            speak("No speech detected.")
            return ""

        except sr.RequestError:
            speak("Network error.")
            return ""

# Send email
def send_mail(receiver_email, message):

    sender_email = os.getenv("EMAIL_ADDRESS")
    sender_password = os.getenv("EMAIL_PASSWORD")

    if not sender_email or not sender_password:
        print("Email credentials are not configured.")
        return False

    msg = MIMEText(message)
    msg["Subject"] = "Voice Assistant Mail"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

        return True

    except Exception as e:
        print("Email Error:", e)
        return False

# Main conversation
def main():

    speak("Hi, welcome to Mohini.")

    speak("What is your name?")
    name = listen()

    if not name:
        name = "User"

    speak(f"Hello {name}, how can I help you?")

    command = listen()

    if "send message" in command or "send mail" in command:

        speak("Please tell me the receiver email address.")
        contact_email = listen().replace(" ", "")

        speak("Please tell me the content of the email.")
        mail_content = listen()

        print("\n===== MAIL CONTENT =====")
        print(mail_content)

        speak("Do you want to send this email?")
        confirmation = listen()

        if confirmation == "yes":

            if send_mail(contact_email, mail_content):
                speak("Email sent successfully!")
            else:
                speak("Failed to send email.")

        else:
            speak("Email cancelled.")

    else:
        speak("Sorry, I can only send emails for now.")

    speak("Goodbye!")

# Run assistant
if __name__ == "__main__":
    try:
        main()
    finally:
        engine.stop()