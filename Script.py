import re
import wave
import openai
import pyaudio
import pyttsx3
import whisper
import warnings

CHUNK = 1024; FORMAT = pyaudio.paInt16; CHANNELS = 1; RATE = 44100

p = pyaudio.PyAudio()

frames = []


stream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE, 
                input = True, frames_per_buffer = CHUNK)

print("AI Voice Assistant is listening\n")

while True:    
    try:
        data = stream.read(CHUNK)
        frames.append(data)
    except KeyboardInterrupt:
        break

print('User input receiving completed\n')
stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open("audio.wav",'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

warnings.filterwarnings('ignore')
model = whisper.load_model("base.en")
result = model.transcribe("audio.wav")
PROMPT = result["text"]
print('Q: ' + PROMPT)

openai.api_key = '' #Your OpenAI API KEY

response = openai.Completion.create(model = "text-davinci-003", prompt = PROMPT, temperature=0, max_tokens=60)

res = response["choices"][0]["text"].strip()

count = res.count('.')

text_to_speech = pyttsx3.init()

text_to_speech.setProperty('rate',165)

voices = text_to_speech.getProperty('voices')
text_to_speech.setProperty('voice', voices[0].id)

if count < 1:
    print('A: ' + res + '.')
    text_to_speech.say(res)
    text_to_speech.runAndWait()

elif count >= 1:
    
    multiple_res = re.search(r'\.(?!.*\.)', res)
    fin_res = res[0:multiple_res.start()]
    print('A: ' + res[0:multiple_res.start()] +'.')
    text_to_speech.say(fin_res)
    text_to_speech.runAndWait()
