import webbrowser
import random
from datetime import datetime
import sys
import threading
from gtts import gTTS
import pygame
import os
import time
import math
import psutil
import subprocess
import shutil
import wikipedia
import io

class Pragati:
    def __init__(self):
        self.notes = []
        self.reminders = []
        self.todos = []
        pygame.mixer.init()

    def speak(self, text, lang="en"):
        """Convert text to speech without saving a file"""
        def run_speech():
            try:
                tts = gTTS(text=text, lang=lang, tld='co.in')
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)

                pygame.mixer.music.load(fp, "mp3")
                pygame.mixer.music.play()

                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)

            except Exception as e:
                print("Error in speech:", e)

        threading.Thread(target=run_speech, daemon=True).start()

    def get_reply(self, message):
        """Return text reply instantly"""
        message = message.lower().strip()
        reply = None

        # GREETINGS:

        if "hello" in message or "hi" in message:
            reply = "Hello! How are you doing today?"

        elif "how are you" in message:
            reply = "I am doing great! How about you?"

        elif "your name" in message or "who are you" in message:
            reply = "I am Pragati, your personal AI assistant."

        elif "thank you" in message or "thanks" in message:
            reply = "You're welcome! Always here for you."

        elif "bye" in message or "exit" in message or "quit" in message:
            reply = "Goodbye! Have a nice day!"
            self.speak(reply)
            sys(exit)

        # DATE AND TIME:

        elif "time" in message:
            reply = "The current time is " + datetime.now().strftime("%I:%M %p")

        elif "date" in message:
            reply = "Today is " + datetime.now().strftime("%A, %B %d, %Y")

        elif "day" in message:
            reply = "It's " + datetime.now().strftime("%A")

        # WEBSITES:

        elif "open google" in message:
            webbrowser.open("https://www.google.com")
            reply = "Opening Google..."

        elif "open youtube" in message:
            webbrowser.open("https://www.youtube.com")
            reply = "Opening YouTube..."

        elif "open facebook" in message:
            webbrowser.open("https://www.facebook.com")
            reply = "Opening Facebook..."

        elif "open instagram" in message:
            webbrowser.open("https://www.instagram.com")
            reply = "Opening Instagram..."

        elif "open twitter" in message or "open x" in message:
            webbrowser.open("https://twitter.com")
            reply = "Opening Twitter..."

        elif "open gmail" in message:
            webbrowser.open("https://mail.google.com")
            reply = "Opening Gmail..."

        elif "open stackoverflow" in message:
            webbrowser.open("https://stackoverflow.com")
            reply = "Opening Stack Overflow..."

        elif "open netflix" in message:
            webbrowser.open("https://www.netflix.com")
            reply = "Opening Netflix..."

        elif "open github" in message:
            webbrowser.open("https://github.com")
            reply = "Opening GitHub..."

        elif "open wikipedia" in message:
            webbrowser.open("https://wikipedia.org")
            reply = "Opening Wikipedia..."

        elif "open amazon" in message:
            webbrowser.open("https://www.amazon.in")
            reply = "Opening Amazon..."

        elif "open linkedin" in message:
            webbrowser.open("https://www.linkedin.com")
            reply = "Opening LinkedIn..."

        elif "open whatsapp" in message:
            webbrowser.open("https://web.whatsapp.com")
            reply = "Opening WhatsApp Web..."

        # COMMAND PROMPT:

        elif "open cmd" in message or "cmd" in message:
            os.system("start cmd")
            reply = "Opening Command Prompt."

        # WIKIPEDIA SEARCH:

        elif "wikipedia" in message:
            try:
                topic = message.replace("wikipedia", "").strip()
                if topic:
                    summary = wikipedia.summary(topic, sentences=2)
                    reply = f"According to Wikipedia: {summary}"
                else:
                    reply = "Please tell me what to search on Wikipedia."
            except Exception:
                reply = "Sorry, I could not fetch data from Wikipedia."
        
        # SYSTEM FILES/FOLDERS/DRIVES:

        elif message.startswith("dir") or "list directory" in message or "list dir" in message:
            path = message.replace("dir", "").replace("list directory", "").replace("list dir", "").strip()
            if not path:
                path = "."
            try:
                output = subprocess.check_output(["cmd", "/c", "dir", path], stderr=subprocess.STDOUT, universal_newlines=True)
                reply = "Directory listing:\n" + (output[:2000] + "\n... (truncated)" if len(output) > 2000 else output)
            except Exception as e:
                reply = f"Error listing directory: {e}"

        elif message.startswith("open folder") or "open explorer" in message:
            path = message.replace("open folder", "").replace("open explorer", "").strip()
            if not path:
                path = os.path.expanduser("~")
            try:
                os.startfile(path)
                reply = f"Opened folder: {path}"
            except Exception as e:
                reply = f"Could not open folder: {e}"

        elif message.startswith("open file"):
            path = message.replace("open file", "").strip()
            if not path:
                reply = "Please tell me which file to open."
            else:
                try:
                    os.startfile(path)
                    reply = f"Opened file: {path}"
                except Exception as e:
                    reply = f"Could not open file: {e}"

        elif "list drives" in message or "show drives" in message:
            try:
                parts = psutil.disk_partitions(all=False)
                if not parts:
                    reply = "No drives found."
                else:
                    lines = []
                    for p in parts:
                        try:
                            usage = shutil.disk_usage(p.mountpoint)
                            lines.append(f"{p.device} -> {p.mountpoint} ({usage.total//(1024**3)} GB total, {(usage.used*100//usage.total)}% used)")
                        except Exception:
                            lines.append(f"{p.device} -> {p.mountpoint}")
                    reply = "Drives:\n" + "\n".join(lines)
            except Exception as e:
                reply = f"Error reading drives: {e}"

        elif message.startswith("disk usage "):
            path = message.replace("disk usage", "").strip()
            if not path:
                path = os.path.expanduser("~")
            try:
                usage = shutil.disk_usage(path)
                reply = (f"Disk usage for {path}: "
                         f"{usage.total//(1024**3)} GB total, "
                         f"{usage.used//(1024**3)} GB used, "
                         f"{usage.free//(1024**3)} GB free")
            except Exception as e:
                reply = f"Could not get disk usage: {e}"

        elif message.startswith("run command ") or message.startswith("cmd "):
            cmd_text = message.replace("run command", "").replace("cmd", "", 1).strip()
            if not cmd_text:
                reply = "Please tell me which command to run (e.g. 'run command dir C:\\')."
            else:
                try:
                    safe_cmd = ["cmd", "/c", cmd_text]
                    output = subprocess.check_output(safe_cmd, stderr=subprocess.STDOUT, universal_newlines=True, timeout=10)
                    reply = f"Command output:\n{output[:2000] + '\n... (truncated)' if len(output) > 2000 else output}"
                except subprocess.TimeoutExpired:
                    reply = "Command timed out."
                except Exception as e:
                    reply = f"Error running command: {e}"

        # FUN ACTIVITY:

        elif "joke" in message:
            jokes = [
                "Why did the computer go to the doctor? Because it caught a virus!",
                "Why don’t scientists trust atoms? Because they make up everything!",
                "Why do programmers hate nature? Because it has too many bugs!"
            ]
            reply = random.choice(jokes)

        elif "fact" in message:
            facts = [
                "Octopuses have three hearts.",
                "Bananas are berries, but strawberries are not.",
                "Sharks existed before trees.",
                "Honey never spoils."
            ]
            reply = random.choice(facts)

        elif "quote" in message:
            quotes = [
                "Push yourself, because no one else is going to do it for you.",
                "Success doesn’t come to you, you go to it.",
                "Believe you can and you're halfway there."
            ]
            reply = random.choice(quotes)

        elif "riddle" in message:
            riddles = {
                "What has to be broken before you can use it?": "An egg",
                "I’m tall when I’m young, and I’m short when I’m old. What am I?": "A candle",
                "What goes up but never comes down?": "Your age"
            }
            question, answer = random.choice(list(riddles.items()))
            reply = question + " (Answer: " + answer + ")"

        elif "motivate me" in message:
            quotes = [
                "Believe in yourself and all that you are!",
                "Push yourself, because no one else will do it for you.",
                "Don’t stop when you are tired, stop when you are done.",
                "Success doesn’t come to you, you go to it."
            ]
            reply = random.choice(quotes)

        elif "rock paper scissors" in message:
            options = ["rock", "paper", "scissors"]
            user = random.choice(options)
            bot = random.choice(options)
            if user == bot:
                result = "It's a tie!"
            elif (user == "rock" and bot == "scissors") or \
                 (user == "paper" and bot == "rock") or \
                 (user == "scissors" and bot == "paper"):
                result = "You win!"
            else:
                result = "I win!"
            reply = f"You chose {user}, I chose {bot}. {result}"

        elif "guess a number" in message:
            num = random.randint(1, 10)
            reply = f"My guess is {num}. Did I get it right?"

        elif "toss" in message or "coin" in message:
            reply = "It's " + random.choice(["Heads", "Tails"])

        elif "dice" in message:
            reply = "You rolled a " + str(random.randint(1, 6))

        # MATH HELP:

        elif "add" in message or "+" in message:
            nums = [int(s) for s in message.split() if s.isdigit()]
            reply = f"The sum is {sum(nums)}" if nums else "Please give me numbers to add."

        elif "subtract" in message or "minus" in message or "-" in message:
            nums = [int(s) for s in message.split() if s.isdigit()]
            reply = f"The result is {nums[0] - nums[1]}" if len(nums) >= 2 else "Give me two numbers."

        elif "multiply" in message or "x" in message:
            nums = [int(s) for s in message.split() if s.isdigit()]
            result = 1
            for n in nums: result *= n
            reply = f"The product is {result}" if nums else "Please give me numbers."

        elif "divide" in message or "/" in message:
            nums = [int(s) for s in message.split() if s.isdigit()]
            if len(nums) >= 2 and nums[1] != 0:
                reply = f"The result is {nums[0] / nums[1]:.2f}"
            else:
                reply = "Please give valid numbers to divide."

        elif "square" in message:
            nums = [int(s) for s in message.split() if s.isdigit()]
            reply = f"Square of {nums[0]} is {nums[0]**2}" if nums else "Give me a number."

        elif "cube" in message:
            nums = [int(s) for s in message.split() if s.isdigit()]
            reply = f"Cube of {nums[0]} is {nums[0]**3}" if nums else "Give me a number."

        elif "power" in message:
            nums = [int(s) for s in message.split() if s.isdigit()]
            reply = f"{nums[0]} to the power {nums[1]} is {nums[0]**nums[1]}" if len(nums) >= 2 else "Provide base and exponent."

        elif "square root" in message:
            nums = [int(s) for s in message.split() if s.isdigit()]
            reply = f"Square root of {nums[0]} is {math.sqrt(nums[0]):.2f}" if nums else "Give me a number."

        elif "factorial" in message:
            nums = [int(s) for s in message.split() if s.isdigit()]
            reply = f"The factorial of {nums[0]} is {math.factorial(nums[0])}" if nums else "Give me a number."

        elif "table" in message:
            nums = [int(s) for s in message.split() if s.isdigit()]
            if nums:
                table = [f"{nums[0]} x {i} = {nums[0]*i}" for i in range(1, 11)]
                reply = "\n".join(table)
            else:
                reply = "Please tell me which number's table you want."

        elif "prime" in message:
            nums = [int(s) for s in message.split() if s.isdigit()]
            if nums:
                n = nums[0]
                if n < 2:
                    reply = f"{n} is not prime."
                else:
                    reply = f"{n} is prime." if all(n % i != 0 for i in range(2, int(math.sqrt(n)) + 1)) else f"{n} is not prime."
            else:
                reply = "Give me a number."

        # UNIT CONVERSIONS:
        
        elif "cm to m" in message:
            nums = [int(s) for s in message.split() if s.isdigit()]
            reply = f"{nums[0]} cm = {nums[0]/100} meters" if nums else "Give me a number."

        elif "kg to g" in message:
            nums = [int(s) for s in message.split() if s.isdigit()]
            reply = f"{nums[0]} kg = {nums[0]*1000} grams" if nums else "Give me a number."

        elif "celsius to fahrenheit" in message:
            nums = [int(s) for s in message.split() if s.isdigit()]
            reply = f"{nums[0]}°C = {(nums[0]*9/5)+32}°F" if nums else "Give me a number."

        elif "fahrenheit to celsius" in message:
            nums = [int(s) for s in message.split() if s.isdigit()]
            reply = f"{nums[0]}°F = {(nums[0]-32)*5/9:.2f}°C" if nums else "Give me a number."

        # REMAINDER

        elif "set reminder" in message:
            note = message.replace("set reminder", "").strip()
            if note:
                self.reminders.append(note)
                reply = f"Reminder set: {note}"
            else:
                reply = "What reminder should I set?"

        elif "show reminders" in message:
            reply = "Your reminders: " + ", ".join(self.reminders) if self.reminders else "No reminders yet."

        elif "add note" in message:
            note = message.replace("add note", "").strip()
            if note:
                self.notes.append(note)
                reply = f"Note added: {note}"
            else:
                reply = "What should I note down?"

        elif "show notes" in message:
            reply = "Your notes: " + ", ".join(self.notes) if self.notes else "You have no notes yet."

        elif "add todo" in message:
            task = message.replace("add todo", "").strip()
            if task:
                self.todos.append(task)
                reply = f"Task added to your to-do list: {task}"
            else:
                reply = "What task should I add?"

        elif "show todo" in message:
            reply = "Your to-do list: " + ", ".join(self.todos) if self.todos else "Your to-do list is empty."

        elif "clear todo" in message:
            self.todos.clear()
            reply = "Your to-do list is cleared."

        elif "set alarm" in message:
            reply = "Sorry, I can't run background alarms yet, but I can remind you if you keep this open."

        # SYSTEM CONTROL:

        elif "system info" in message:
            reply = f"CPU usage: {psutil.cpu_percent()}%. Memory: {psutil.virtual_memory().percent}% used."

        elif "lock" in message:
            reply = "Locking system."
            os.system("rundll32.exe user32.dll,LockWorkStation")

        elif "battery" in message:
            battery = psutil.sensors_battery()
            if battery:
                reply = f"Your battery is at {battery.percent}%."
            else:
                reply = "Sorry, I can't read the battery on this system."

        elif "shutdown" in message:
            reply = "Shutting down your system."
            os.system("shutdown /s /t 1")

        elif "restart" in message:
            reply = "Restarting your system."
            os.system("shutdown /r /t 1")

        elif "log out" in message:
            reply = "Logging out."
            os.system("shutdown -l")

        # KNOWLEDGE:

        elif "what is ai" in message:
            reply = "Artificial Intelligence is the simulation of human intelligence by machines."

        elif "what is machine learning" in message:
            reply = "Machine learning is a branch of AI that allows computers to learn from data without explicit programming."

        elif "what is cloud" in message:
            reply = "Cloud computing delivers computing services like servers, storage, and databases over the internet."

        elif "what is database" in message:
            reply = "A database is an organized collection of data that can be easily accessed and managed."

        elif "what is operating system" in message:
            reply = "An operating system is system software that manages computer hardware and software resources."

        elif "what is python" in message:
            reply = "Python is a powerful and beginner-friendly programming language."

        elif "what is computer" in message:
            reply = "A computer is an electronic device used for storing and processing data."

        elif "what is internet" in message:
            reply = "The internet is a global system of interconnected computer networks."

        else:
            reply = "Hmm, I am not sure about that."

        self.speak(reply)
        return reply